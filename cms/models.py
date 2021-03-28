from django.db import models
from cms import shared,constants


# Create your models here.


class CmsUsersMaster(models.Model):
    role_type = models.CharField(choices=constants.ROLES, max_length=100, default=constants.USER)
    email_id = models.CharField(max_length=100, validators=[constants.email_id_regex],unique=True)
    password = models.CharField(max_length=500)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=60, null=True)
    state = models.CharField(max_length=60, null=True)
    country = models.CharField(max_length=60, null=True)
    pincode = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'cms_users_master'


class UsersContent(models.Model):
    user = models.ForeignKey(CmsUsersMaster, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    summary = models.CharField(max_length=60)
    pdf_document_path = models.CharField(max_length=100)
    categories = models.CharField(max_length=60, choices=constants.CATEGORIES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'cms_users_content'
