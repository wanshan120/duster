from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager

"""Dusterのモデル定義.

Order:
    1: User
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


class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email


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
    from_user = models.ForeignKey(
        User, related_name="from_user", on_delete=models.CASCADE)
    follow = models.ManyToManyField(User, related_name="follow")
    follower = models.ManyToManyField(User, related_name="followwe")

    def __str__(self):
        return self.from_user


class Review(models.Model):
    SCORE = (
        (0, '未評価'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    head = models.CharField(max_length=40)
    title = models.ForeignKey(
        Item, related_name="title", on_delete=models.SET_NULL, null=True)
    score = models.CharField(max_length=2, choices=SCORE)
    tag = models.ManyToManyField(FreeTag, blank=True)
    movie = models.URLField(blank=True)
    thumnail = models.ImageField(upload_to='images/', blank=True)
    synopsis = models.TextField(blank=True, max_length=400)
    upadate_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.head
