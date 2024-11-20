from django.urls import path
from . import views
urlpatterns = [
    path('ver_produto/', views.ver_produto, name="ver_produto")
]