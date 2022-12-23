# Generated by Django 3.2 on 2022-12-23 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('linkedin_token', models.TextField(blank=True, default='')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=60, null=True)),
                ('last_name', models.CharField(max_length=60, null=True)),
                ('bio', models.TextField(blank=True, max_length=2000, null=True)),
                ('date_of_birth', models.DateTimeField(null=True, verbose_name='date of birth')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='image')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('endpoint_name', models.CharField(max_length=150, null=True)),
                ('private', models.BooleanField(default=False)),
                ('file_name', models.TextField(max_length=4096, null=True)),
                ('file_content', models.TextField()),
                ('file_type', models.CharField(max_length=21)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
