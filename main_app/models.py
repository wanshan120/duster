from django.db import models
from auth_app.models import User

"""main_appのモデル定義.

Order:
    2: Tag
        1: MetaTag 固定タグ（管理者が管理）
        2: FreeTag 可変タグ（ユーザーが管理）
    3: Item
    4: Services
    5: ItemPrice
    6: Article
    7: Creater

Initial_data:
    command: ./manage.py loaddata main_app/fixtures/initial_data.yaml

"""


class TagElement(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class FreeTag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    elements = models.ForeignKey(TagElement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=40, unique=True)
    title_true = models.CharField(max_length=50)
    title_relate = models.ManyToManyField(
        'self', blank=True, related_name='title_relate')
    tag = models.ManyToManyField(FreeTag, blank=True)
    movie = models.URLField(blank=True)
    thumnail = models.ImageField(upload_to='images/', blank=True)
    synopsis = models.TextField(blank=True, max_length=400)
    up_status = models.DateField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    name = models.ForeignKey(Item, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class ItemPrice(models.Model):
    name = models.ForeignKey(Item, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Creater(models.Model):
    name = models.CharField(max_length=50)
    name_true = models.CharField(max_length=50)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    official = models.URLField(blank=True)
    other_site = models.URLField(blank=True)
    thumnail = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Follow(models.Model):
    follow_from_user = models.ForeignKey(
        User, related_name="follow_from_user",
        on_delete=models.CASCADE, null=True)
    follow = models.ManyToManyField(User, related_name="follow")
    follower = models.ManyToManyField(User, related_name="followwe")

    def __str__(self):
        return self.from_user


class Score(models.Model):
    SCORE = (
        (0, '0'),
        (0.5, '0.5'),
        (1.0, '1.0'),
        (1.5, '1.5'),
        (2.0, '2.0'),
        (2.5, '2.5'),
        (3.0, '3.0'),
        (3.5, '3.5'),
        (4.0, '4.0'),
        (4.5, '4.5'),
        (5.0, '5.0'),
    )
    score = models.IntegerField(choices=SCORE)
    score_from_user = models.ForeignKey(
        User, related_name="score_from_user", on_delete=models.CASCADE,
        null=True)
    title = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.score


class WatchStatus(models.Model):
    STATUS = (
        (0, '未視聴'),
        (2, '視聴済み'),
    )
    STOCK = (
        (0, '後で見るへ'),
        (2, '後で見る 解除'),
    )
    watch_from_user = models.ForeignKey(
        User, related_name="watch_from_user", on_delete=models.CASCADE)
    title = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=STATUS, null=True)
    stock = models.IntegerField(choices=STOCK, null=True)


class Review(models.Model):
    review_from_user = models.ForeignKey(
        User, related_name="review_from_user", on_delete=models.CASCADE,
        null=True)
    head = models.CharField(max_length=40)
    title = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(FreeTag, blank=True)
    movie = models.URLField(blank=True)
    thumnail = models.ImageField(upload_to='images/', blank=True)
    synopsis = models.TextField(blank=True, max_length=400)
    upadate_at = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(
        User, related_name="review_liked_user", blank=True)
    disliked = models.ManyToManyField(
        User, related_name="review_disliked_user", blank=True)

    def __str__(self):
        return self.head
