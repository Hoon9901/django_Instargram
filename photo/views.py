from typing import List
from django.http.response import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import View
from urllib.parse import urlparse
from .models import Photo

# Create your views here.


class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'  # 북마크 모델


class PhotoCreate(CreateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url = '/'   # 성공하면 메인 페이지로 연결

    # 폼 유효성 검사
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})


class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_update'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        photo = self.get_object()
        if photo.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        photo = self.get_object()
        if photo.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)


class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'


class PhotoLike(View):
    # get 요청
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated :  #로그인 체크
            return HttpResponseForbidden() 
        else :
            if 'photo_id' in kwargs : 
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():    # 좋아요 취소
                    photo.like.remove(user)
                else :                          # 좋아요
                    photo.like.add(user)
            # 좋아요 누른 경로에 따라 머무르기
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

class Photofavorite(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated :  #로그인 체크
            return HttpResponseForbidden()
        else :
            if 'photo_id' in kwargs : 
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.favorite.all():
                    photo.favorite.remove(user)
                else :
                    photo.favorite.add(user)
            return HttpResponseRedirect('/')

class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 내가 좋아요한 글을 보여주
        user = self.request.user
        queryset = user.like_post.all()
        return queryset

class PhotoFavoriteList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:   # 로그인 확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoFavoriteList, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        # 내가 담은 글 보여주기
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset

class PhotoMyList(ListView) :
    model = Photo
    template_name = 'photo/photo_mylist.html'

    def dispatch(self , request, *args, **kwargs) :
        if not request.user.is_authenticated:   # 로그인 확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoMyList, self).dispatch(request, *args, **kwargs)
        