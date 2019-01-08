from django.urls import reverse_lazy
from django.shortcuts import (reverse, render)
from django.views import generic
from .forms import (ItemCreateForm, WatchStatusForm)
from .models import (Item, FreeTag, TagElement, Follow, WatchStatus, Score)
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


class ItemDetail(generic.DetailView):
    model = Item
    template_name = 'main_app/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

        except Exception:
            # 履歴が無い場合
            context['watchstatus'] = '未視聴'
            context['statuscode'] = 0
            context['watchstock'] = '後で見るへ'
            context['stockcode'] = 0
        return context


def update_status(request, pk):
    """アイテムの視聴状況を更新する.
    処理の流れ:
        ItemDetailで初期値のＨＭＴＬを作成
        フォーム送信時にformのactionでupdate_statusを呼び出す
        データ保存したらJSON形式で返却（AJAX）
    """
    if request.method == "POST":
        item, created = WatchStatus.objects.update_or_create(
            watch_from_user=request.user,
            title=Item.objects.get(id=pk),
            # 検索値
            defaults={
                'status': request.POST.get('status'),
                'stock': request.POST.get('stock'),
                }
            # 設定値
        )
        data = {
            'status': item.status,
            'stock': item.stock,
        }
        return JsonResponse(data)
    else:
        data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


update_stock = update_status
""" update_statusをupdate_stock用にコピー."""


def update_score(request, pk):
    if request.method == "POST":
        item, created = Score.objects.update_or_create(
            watch_from_user=request.user,
            title=Item.objects.get(id=pk),
            defaults={
                'score': request.POST.get('score'),
                }
        )
        data = {
            'score': item.score,
        }
        return JsonResponse(data)
    else:
        data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


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


""" マイスコア.
class ScoreCreate(generic.CreateView):
    model = Score
    fields = '__all__'
    success_url = reverse_lazy('main_app:top')


class PopupScoreCreate(ScoreCreate):

    def form_valid(self, form):
        f = form.save()
        context = {
            'object_name': str(f),
            'object_pk': f.pk,
            'function_name': 'my_score'
        }
        return render(self.request, 'main_app/close.html', context)


class ScoreUpdate(generic.UpdateView):
    model = Score
    fields = '__all__'
    success_url = reverse_lazy('main_app:top')
"""
