from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


class Register(View):
    template_name = 'profile/register.html'

    def get(self, request):
        context = {'form': SignUpForm()}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user_id = self.request.user.id
            return redirect('profile', pk=user_id)
        context={'form':form}
        return render(request, self.template_name, context)
    
class LogView(LoginView):
    template_name = 'profile/login.html'
    fields = ['email', 'password']
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('main_page')
    
def auth(request):
       return render(request, 'profile/login_or_register.html')

            

class MainPage(ListView):
    model = Video
    template_name = 'videos/main_page.html'
    context_object_name = 'search'

    def get_queryset(self):
        search_input = self.request.GET.get('search-input') or ''
        if search_input:
            return Video.objects.filter(title__icontains=search_input).order_by('-id')
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tags.objects.all()
        return context 
    

class VideoDetail(DetailView): # детальное представление видео
    model = Video
    template_name = 'videos/video_watch.html'

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object.comment.all().order_by('-id')
        context['form'] = CommentForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, user=request.user)
        print(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = self.object
            comment.user = request.user
            comment.save()
            return redirect('video', pk=self.object.pk)

class VideoEdit(UpdateView):
    model = Video
    template_name = 'videos/video_edit.html'
    context_object_name = 'video_edit'
    fields = ['title', 'description', 'preview', 'tags']

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')
    
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('videos', kwargs={'pk': user_id})

    


class Videos(DetailView):
    model = User
    template_name = 'profile/videos.html'
    context_object_name = 'user_v'

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context
    
class VideoDelete(DeleteView):
    model = Video
    template_name = 'videos/video_delete.html'
    context_object_name = 'video_delete'

    def get_success_url(self):
        user_id = self.request.user.id  # Получаем ID пользователя из запроса
        return reverse_lazy('videos', kwargs={'pk': user_id})
    
    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context


class AboutChannel(DetailView):
    model = User
    template_name = 'profile/about_channel.html'
    context_object_name = 'about_channel'

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')
    
    def get_context_data(self, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(user=user).count()
        return context

class AboutChannelEdit(UpdateView):
    model = User
    template_name = 'profile/about_edit.html'
    fields = ['channel_description']
    context_object_name = 'about_channel_edit'

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(user=user).count()
        return context
    def get_success_url(self):
        user_id = self.request.user.id  # Получаем ID пользователя из запроса
        return reverse_lazy('about_channel', kwargs={'pk': user_id})

class Profile(DetailView):
    model = User
    template_name = 'profile/profile.html'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')


class ProfileEdit(UpdateView):
    model = User
    template_name = 'profile/profile_edit.html'
    context_object_name = 'profile_edit'
    fields = ['username', 'first_name', 'last_name', 'email', 'name_channel', 'avatar']

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

    def get_success_url(self):
        user_id = self.request.user.id  # Получаем ID пользователя из запроса
        return reverse_lazy('profile', kwargs={'pk': user_id})
    


class CatList(ListView):
    model = Tags
    template_name = 'videos/cat_list.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')
    
class CatVideos(DetailView):
    model = Tags
    template_name = 'videos/cat_video.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['videos_list'] = Video.objects.filter(tags=category).order_by('-id')
        return context


class AddVideo(CreateView):
    model = Video
    fields = ['title', 'description', 'video_file', 'preview', 'tags']
    template_name = 'videos/add_video.html'
    context_object_name = 'add_video'

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().order_by('-id')
    
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('profile', kwargs={'pk': user_id})

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

def likes(request, pk):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, id=pk)
        if video.likes.filter(id=request.user.id):
            video.likes.remove(request.user)
        elif video.dislikes.filter(id=request.user.id):
            video.dislikes.remove(request.user)
            video.likes.add(request.user)
        else:
            video.likes.add(request.user)
        return redirect('video', pk=pk)
    else:
        return reverse_lazy('main_page')
    
def dislikes(request, pk):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, id=pk)
        if video.dislikes.filter(id=request.user.id):
            video.dislikes.remove(request.user)
        elif video.likes.filter(id=request.user.id):
            video.likes.remove(request.user)
            video.dislikes.add(request.user)
        else:
            video.dislikes.add(request.user)
        return redirect('video', pk=pk)
    else:
        return reverse_lazy('main_page')
        
@login_required
def subscribe(request, pk):
    user_to_subscribe = get_object_or_404(User, id=pk)
    if user_to_subscribe.subscribers.filter(id=request.user.id):
        user_to_subscribe.subscribers.remove(request.user)
    else:
        user_to_subscribe.subscribers.add(request.user)
    return redirect('main_page')

class SubscribedChannelsVideosView(ListView):
    model = Video
    template_name = 'profile/sub_videos.html'
    context_object_name = 'sub_videos'

    def get(self, request, *args, **kwargs):
        search_input = request.GET.get('search-input')
        if search_input:
            return redirect(f"{reverse_lazy('main_page')}?search-input={search_input}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        subscribed_users = self.request.user.subscriptions.all()
        if subscribed_users:
            return Video.objects.filter(user__in=subscribed_users).order_by('-id')
        
        
def page_not_found(request, exception):
    return render(request, 'exception/not_found.html')