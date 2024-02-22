from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("add_page", views.add_page, name="add_page"),
    path("randomPage", views.randomPage, name='randomPage'),
    path("edit_page", views.edit_page, name="edit_page"),
]
