# Generated by Django 2.0.3 on 2019-01-03 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_auto_20190103_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.CharField(choices=[(0, '未評価'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], max_length=2),
        ),
        migrations.AlterField(
            model_name='watchstatus',
            name='status',
            field=models.IntegerField(choices=[(0, '未視聴'), (1, '後で見る'), (2, '視聴済み')], max_length=1, null=True),
        ),
    ]
