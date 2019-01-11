from django import forms
from .models import Item, FreeTag, WatchStatus, Score
from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory
from django.forms import BaseFormSet


class ModelFormWithFormSetMixin():

    def __init__(self, *args, **kwargs):
        super(ModelFormWithFormSetMixin, self).__init__(*args, **kwargs)
        if self.is_bound:
            self.formset = self.formset_class(
                instance=self.instance,
                data=self.data
                )
        else:
            self.formset = self.formset_class()

    def is_valid(self):
        return super(ModelFormWithFormSetMixin, self).is_valid() and self.formset.is_valid()

    def save(self, commit=True):
        saved_instance = super(ModelFormWithFormSetMixin, self).save(commit)
        self.formset.save(commit)
        return saved_instance


class BaseItemTagFormSet(BaseInlineFormSet):
    """form_set_factoryのオーバーライド.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = FreeTag.objects.filter(elements__name='ジャンル')


TagInlineFormSet = inlineformset_factory(
    Item,
    Item.tag.through,
    fields='__all__',
    can_delete=False,
    extra=10,
    )


class ItemCreateForm(ModelFormWithFormSetMixin, forms.ModelForm):
    formset_class = TagInlineFormSet

    class Meta:
        model = Item
        fields = ('title',
                  'title_true',
                  'title_relate',
                  'movie',
                  'thumnail',
                  'synopsis',
                  'up_status'
                  )


class WatchStatusForm(forms.ModelForm):
    class Meta:
        model = WatchStatus
        fields = ('status', 'stock',)


class WatchScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('score',)

