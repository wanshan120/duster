from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.shortcuts import (
     redirect, resolve_url, get_object_or_404, reverse, render
)
from django.template.loader import get_template
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, ItemCreateForm
)
from .models import (Item, FreeTag, TagElement, Follow)
from django.contrib import messages
from django.db.models import Avg
import json
from django.http import HttpResponse

User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'main_app/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'main_app/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'main_app/top.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'main_app/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template(
            'main_app/mail_templates/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template(
            'main_app/mail_templates/create/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('main_app:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'main_app/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'main_app/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'main_app/user_detail.html'


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'main_app/user_form.html'

    def get_success_url(self):
        return resolve_url('main_app:user_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('main_app:password_change_done')
    template_name = 'main_app/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'main_app/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'main_app/mail_templates/password_reset/subject.txt'
    email_template_name = 'main_app/mail_templates/password_reset/message.txt'
    template_name = 'main_app/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('main_app:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'main_app/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('main_app:password_reset_complete')
    template_name = 'main_app/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'main_app/password_reset_complete.html'


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
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context['view_count'] = Item.objects.count()
        return context


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