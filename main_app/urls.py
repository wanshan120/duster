from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main_app'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(),
         name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(),
         name='user_create_complete'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(),
         name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(),
         name='user_update'),
    path('password_change/', views.PasswordChange.as_view(),
         name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(),
         name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(),
         name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(),
         name='password_reset_complete'),
    path('item/create/',
         views.ItemCreate.as_view(), name='item_create'),
    path('item/detail/<int:pk>',
         views.ItemDetail.as_view(), name='item_detail'),
    path('item/update/<int:pk>',
         views.ItemUpdate.as_view(), name='item_update'),
    path('item/delete/<int:pk>',
         views.ItemDelete.as_view(), name='item_delete'),
    path('tag/create/',
         views.PopupTagCreate.as_view(), name='popup_tag_create'),
    path('tag/update/<int:pk>',
         views.TagUpdate.as_view(), name='tag_update'),
    path('tag/delete/<int:pk>',
         views.TagDelete.as_view(), name='tag_delete'),
    path('follow/create/<int:pk>',
         views.FollowCreate.as_view(), name='follow_create'),
    path('follow/delete/<int:pk>',
         views.FollowDelete.as_view(), name='follow_delete'),
    path('ajax_title_search',
         views.ajax_title_search, name='ajax_title_search'),
    path('ajax_watch_status',
         views.ajax_title_search, name='ajax_title_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
