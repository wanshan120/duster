from django import forms
from .models import Item, FreeTag, WatchStatus, Score


class ItemCreateForm(forms.ModelForm):
    """作品作成フォーム"""
    tag_genre = forms.ModelChoiceField(
        label='ジャンル１',
        queryset=FreeTag.objects.filter(elements__name='ジャンル')
        )
    tag_genre2 = forms.ModelChoiceField(
        label='ジャンル2',
        queryset=FreeTag.objects.filter(elements__name='ジャンル'),
        )
    tag_age = forms.ModelChoiceField(
        label='年代',
        queryset=FreeTag.objects.filter(elements__name='年代'),
        )
    tag_country = forms.ModelChoiceField(
        label='制作国',
        queryset=FreeTag.objects.filter(elements__name='制作国'),
        )
    tag_language = forms.ModelChoiceField(
        label='言語',
        queryset=FreeTag.objects.filter(elements__name='言語'),
        )
    tag_japanease = forms.ModelChoiceField(
        label='日本語対応',
        queryset=FreeTag.objects.filter(elements__name='日本語対応'),
        )
    tag_rating_system = forms.ModelChoiceField(
        label='年齢制限',
        queryset=FreeTag.objects.filter(elements__name='年齢制限'),
        )
    tag_runtime = forms.ModelChoiceField(
        label='視聴時間',
        queryset=FreeTag.objects.filter(elements__name='視聴時間'),
        )
    tag_status = forms.ModelChoiceField(
        label='公開状況',
        queryset=FreeTag.objects.filter(elements__name='公開状況'),
        )
    tag_timelimit = forms.ModelChoiceField(
        label='終了予定',
        queryset=FreeTag.objects.filter(elements__name='終了予定'),
        )
    tag_volume = forms.ModelChoiceField(
        label='巻数、話数',
        queryset=FreeTag.objects.filter(elements__name='巻数、話数'),
        )
    tag_creater = forms.ModelChoiceField(
        label='制作者',
        queryset=FreeTag.objects.filter(elements__name='制作者'),
        )
    tag_company = forms.ModelChoiceField(
        label='制作会社',
        queryset=FreeTag.objects.filter(elements__name='制作会社'),
        )
    tag_cast = forms.ModelChoiceField(
        label='キャスト',
        queryset=FreeTag.objects.filter(elements__name='キャスト'),
        )
    tag_original_author = forms.ModelChoiceField(
        label='原作者',
        queryset=FreeTag.objects.filter(elements__name='原作者'),
        )
    tag_award = forms.ModelChoiceField(
        label='受賞',
        queryset=FreeTag.objects.filter(elements__name='受賞'),
        )

    class Meta:
        model = Item
        fields = ('title',
                  'title_true',
                  'title_relate',
                  'movie',
                  'thumnail',
                  'synopsis',
                  'up_status')


class WatchStatusForm(forms.ModelForm):
    class Meta:
        model = WatchStatus
        fields = ('status', 'stock',)


class WatchScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('score',)
