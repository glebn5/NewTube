from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
		path('', MainPage.as_view(), name='main_page'),
        path('video/<int:pk>/', VideoDetail.as_view(), name='video'),
        path('video/<int:pk>/edit', VideoEdit.as_view(), name='video_edit'),
        path('video/<int:pk>/delete', VideoDelete.as_view(), name='video_delete'),
        path('video/<int:pk>/like/', likes, name='video_like'),
        path('video/<int:pk>/dislike/', dislikes, name='video_dislike'),

        path('category/<int:pk>/', CatVideos.as_view(), name='category'),
        path('category_list/', CatList.as_view(), name='cat_list'),


        path('user/<int:pk>/videos/', Videos.as_view(), name='videos'),
        path('user/<int:pk>/follow/', subscribe, name='follow'),
        path('sub_videos', SubscribedChannelsVideosView.as_view(), name='sub_videos'),

        path('user/<int:pk>/about_channel/', AboutChannel.as_view(), name='about_channel'),
        path('user/<int:pk>/about_channel_eidt/', AboutChannelEdit.as_view(), name='about_channel_edit'),
        path('user/<int:pk>/profile/', Profile.as_view(), name='profile'),
        path('user/<int:pk>/edit/', ProfileEdit.as_view(), name='profile_edit'),
        path('add_video/', AddVideo.as_view(), name='add_video'),
		
        path('register/', Register.as_view(), name='register'),
        path('login/', LogView.as_view(), name='login'),
        path('logout/', LogoutView.as_view(next_page='main_page'), name='logout'),
        path('authorization/', auth, name='auth'),
]