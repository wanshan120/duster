# Generated by Django 2.0.3 on 2018-12-31 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_follow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=40)),
                ('movie', models.URLField(blank=True)),
                ('thumnail', models.ImageField(blank=True, upload_to='images/')),
                ('synopsis', models.TextField(blank=True, max_length=400)),
                ('upadate_at', models.DateTimeField(auto_now_add=True)),
                ('tag', models.ManyToManyField(blank=True, to='main_app.FreeTag')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(choices=[(0, '未評価'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], max_length=2)),
                ('score_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score_user', to=settings.AUTH_USER_MODEL)),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Item')),
            ],
        ),
    ]
