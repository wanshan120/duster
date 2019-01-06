from models import (TagElement)


if __name__ == "__main__":
    default_tag1, _ = TagElement.objects.get_or_create(
        name='ジャンル')
    default_tag2, _ = TagElement.objects.get_or_create(
        name='タイプ')
    default_tag3, _ = TagElement.objects.get_or_create(
        name='年代')
    default_tag4, _ = TagElement.objects.get_or_create(
        name='制作国')
    default_tag5, _ = TagElement.objects.get_or_create(
        name='言語')
    default_tag6, _ = TagElement.objects.get_or_create(
        name='日本語対応')
    default_tag7, _ = TagElement.objects.get_or_create(
        name='年齢制限')
    default_tag8, _ = TagElement.objects.get_or_create(
        name='再生時間')
    default_tag9, _ = TagElement.objects.get_or_create(
        name='制作会社')
    default_tag10, _ = TagElement.objects.get_or_create(
        name='受賞')
    default_tag11, _ = TagElement.objects.get_or_create(
        name='感情')
    default_tag12, _ = TagElement.objects.get_or_create(
        name='世界観')
    default_tag13, _ = TagElement.objects.get_or_create(
        name='職業')
    default_tag13, _ = TagElement.objects.get_or_create(
        name='スポーツ')
