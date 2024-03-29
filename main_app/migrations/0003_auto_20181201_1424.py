# Generated by Django 2.0.3 on 2018-12-01 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20181123_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('name_true', models.CharField(max_length=50)),
                ('twitter', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
                ('instagram', models.URLField(blank=True)),
                ('official', models.URLField(blank=True)),
                ('other_site', models.URLField(blank=True)),
                ('thumnail', models.ImageField(blank=True, upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FreeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, unique=True)),
                ('title_true', models.CharField(max_length=50)),
                ('movie', models.URLField(blank=True)),
                ('thumnail', models.ImageField(blank=True, upload_to='images/')),
                ('synopsis', models.TextField(blank=True, max_length=400)),
                ('up_status', models.DateField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tag', models.ManyToManyField(blank=True, to='main_app.FreeTag')),
                ('title_relate', models.ManyToManyField(blank=True, related_name='_item_title_relate_+', to='main_app.Item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServicePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Item')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Service')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TagElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='itemprice',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Store'),
        ),
        migrations.AddField(
            model_name='freetag',
            name='elements',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.TagElement'),
        ),
        migrations.AddField(
            model_name='creater',
            name='title',
            field=models.ManyToManyField(to='main_app.Item'),
        ),
    ]
