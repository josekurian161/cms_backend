# Generated by Django 3.1.7 on 2021-03-27 16:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CmsUsersMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_type', models.CharField(choices=[('admin', 'admin'), ('user', 'user')], default='user', max_length=100)),
                ('email_id', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='please enter valid email_id', regex='^\\+?1?\\d{9,15}$')])),
                ('password', models.CharField(max_length=500)),
                ('full_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=60, null=True)),
                ('state', models.CharField(max_length=60, null=True)),
                ('country', models.CharField(max_length=60, null=True)),
                ('pincode', models.CharField(max_length=60)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'cms_users_master',
            },
        ),
        migrations.CreateModel(
            name='UsersContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('body', models.CharField(max_length=300)),
                ('summary', models.CharField(max_length=60)),
                ('pdf_document_path', models.CharField(max_length=100)),
                ('categories', models.CharField(choices=[('blog_writer', 'blog writer'), ('brand_journalist', 'brand journalist'), ('technical_writer', 'technical writer')], max_length=60)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.cmsusersmaster')),
            ],
            options={
                'db_table': 'cms_users_content',
            },
        ),
    ]
