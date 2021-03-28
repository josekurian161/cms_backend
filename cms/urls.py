from django.urls import path
from cms import views

app_name = "cms_api"

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Registration.as_view(), name='register'),
    path('list_content', views.ListContent.as_view(), name='list_content'),
    path('add_content', views.AddContent.as_view(), name="add_content"),
    path('update_content', views.UpdateContent.as_view(), name="update_content"),
    path('delete_content', views.DeleteContent.as_view(), name="delete_content"),
]
