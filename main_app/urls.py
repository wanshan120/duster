from django.urls import path
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
    path('item/my_watch_list/',
         views.MyWatchList.as_view(), name='my_watch_list'),
    path('item/my_stock_list/',
         views.MyStockList.as_view(), name='my_stock_list'),
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
    # ステータス
    path('item/detail/<int:pk>/status/', views.update_status, name='ajax_status'),
    # スコア
    path('item/detail/<int:pk>/score/', views.update_score, name='ajax_score'),
    # ストック
    path('item/detail/<int:pk>/stock/', views.update_stock, name='ajax_stock'),
    # ステータス
    path('item/my_stock_list/<int:pk>/status/', views.update_status_list, name='ajax_status_list'),
    # スコア
    path('item/my_stock_list/<int:pk>/score/', views.update_score, name='ajax_score_list'),
    # ストック
    path('item/my_stock_list/<int:pk>/stock/', views.update_stock_list, name='ajax_stock_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
