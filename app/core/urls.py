from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
router=SimpleRouter()
router.register('movies',views.MoviesViewSet)
router.register('directors',views.DirectorViewSet)
router.register('user-profiles',views.UserProfileViewSet)
router.register('friends-profiles',views.FriendsProfilesViewSet)
router.register('main_page',views.MainPageViewSet)
router.register('comments',views.CommentsViewSet)
urlpatterns= [
    path('',include(router.urls))
]