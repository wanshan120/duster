# Generated by Django 2.0.3 on 2019-01-05 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_auto_20190105_2356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]