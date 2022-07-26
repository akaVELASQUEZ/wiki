from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="title"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("edit/<str:title>" , views.edit, name="edit")
]
