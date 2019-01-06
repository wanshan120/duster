from django.urls import reverse_lazy
from django.shortcuts import (reverse, render)
from django.views import generic
from .forms import (ItemCreateForm, WatchStatusForm)
from .models import (Item, FreeTag, TagElement, Follow, WatchStatus)
from django.contrib import messages
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic.edit import ModelFormMixin


class Top(generic.TemplateView):
    template_name = 'main_app/top.html'


class ItemCreate(generic.CreateView):
    model = Item
    form_class = ItemCreateForm
    template_name = 'main_app/item_create.html'

    def get_success_url(self):
        return reverse('main_app:item_detail', args=(self.object.id,))

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.warning(self.request, "保存できませんでした")
        return super().form_invalid(form)


class ItemDetail(ModelFormMixin, generic.DetailView):
    model = Item
    form_class = WatchStatusForm
    template_name = 'main_app/item_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context['view_count'] = Item.objects.count()
        try:
            # 履歴があるか検索
            value = WatchStatus.objects.get(
                watch_from_user=self.request.user,
                title=self.kwargs['pk'])
            # 履歴があったらHTMLへテンプレート出力
            context['watchstatus'] = value.get_status_display()
            context['watchstock'] = value.get_stock_display()
            context['statuscode'] = value.status
            context['stockcode'] = value.stock
            return context
        except Exception:
            # 履歴が無い場合
            context['watchstatus'] = '未視聴'
            context['statuscode'] = 0
            context['watchstock'] = '後で見るへ'
            context['stockcode'] = 0
            return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # バリデーション
            post_pk = self.kwargs['pk']
            item = form.save(commit=False)
            """item.watch_from_user = request.user
            item.title = Item.objects.get(id=post_pk)
            item.status = request.POST.get('status')"""
            item, created = WatchStatus.objects.update_or_create(
                watch_from_user=request.user,
                title=Item.objects.get(id=post_pk),
                defaults={
                    'status': request.POST.get('status'),
                    'stock': request.POST.get('stock')}
            )
            item.save()
            return self.form_valid(form, item)
        else:
            self.object = self.get_object()
            return self.form_invalid(form)

    def form_valid(self, form, item):
        # バリデーションが通ったら実行
        data = {
            'status': item.status,
            'stock': item.stock,
        }
        return JsonResponse(data)


class ItemUpdate(generic.UpdateView):
    model = Item
    form_class = ItemCreateForm
    template_name = 'main_app/item_update.html'

    def get_success_url(self):
        return reverse('main_app:item_detail', args=(self.object.id,))

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.warning(self.request, "保存できませんでした")
        return super().form_invalid(form)


class ItemDelete(generic.DeleteView):
    model = Item
    form_class = ItemCreateForm
    success_url = reverse_lazy('main_app:top')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result


class TagElementCreate(generic.CreateView):
    """タグエレメントの作成"""
    model = TagElement
    fields = '__all__'
    success_url = reverse_lazy('main_app:top')


class TagCreate(generic.CreateView):
    """タグの作成"""
    model = FreeTag
    fields = '__all__'
    success_url = reverse_lazy('main_app:top')


class TagUpdate(generic.UpdateView):
    """タグの更新"""
    model = FreeTag
    fields = '__all__'
    success_url = reverse_lazy('main_app:top')


class TagDelete(generic.DeleteView):
    """タグの削除"""
    model = FreeTag
    fields = '__all__'
    success_url = reverse_lazy('main_app:top')


class PopupTagCreate(TagCreate):
    """ポップアップでのタグ作成"""

    def form_valid(self, form):
        tag = form.save()
        context = {
            'object_name': str(tag),
            'object_pk': tag.pk,
            'function_name': 'add_tag'
        }
        return render(self.request, 'main_app/close.html', context)


class FollowCreate(generic.CreateView):
    """フォローする"""
    model = Follow
    fields = '__all__'
    success_url = reverse_lazy('main_app:top')


class FollowDelete(generic.DeleteView):
    """フォローしない"""
    model = Follow
    fields = '__all__'
    success_url = reverse_lazy('main_app:top')


def ajax_title_search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        title_list = Item.objects.filter(title__icontains=q)[: 6]
        results = []
        for item in title_list:
            if item.thumnail:
                title_json = {
                    'value': item.title,
                    'label': item.title,
                    'desc':  item.pk,
                    'icon':  item.thumnail.url,
                }
                results.append(title_json)
            else:
                title_json = {
                    'value': item.title,
                    'label': item.title,
                    'desc':  item.pk,
                    'icon':  "",
                }
                results.append(title_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

