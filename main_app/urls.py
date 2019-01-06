from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main_app'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
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
