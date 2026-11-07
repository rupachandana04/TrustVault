from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', auth_views.LoginView.as_view(
        template_name='documents/login.html'
    ), name='login'),

    path('upload/', views.upload_document, name='upload_document'),
    path(
    'download/<int:document_id>/',
    views.download_document,
    name='download_document'
),
    path('my-documents/', views.document_list, name='document_list'),
    path(
    'share/<int:document_id>/',
    views.share_document,
    name='share_document'
),
]