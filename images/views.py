from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from actions.utils import create_action
from common.decorators import ajax_required
from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            # show action in activity stream
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html',
                  {'section': 'images',
                   'image': image})


@ajax_required
@login_required
# Returns an HttpResponseNotAllowed object (status code 405)
# if the HTTP request is not done via GET.
# This way allowed only GET response for this view.
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                # show action in activity stream
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


# when user initially loads loads the image list page, 1st page will be displayed.
# when he scroll to the bottom of the page, following page of images will be loaded via AJAX
@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 10)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # if ajax and page is out of range return an empty page
            return HttpResponse('')
        # if page is out of range - deliver last page
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html',
                      {'section': 'images',
                       'images': images})
    return render(request, 'images/image/list.html',
                  {'section': 'images',
                   'images': images})