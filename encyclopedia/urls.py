from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("createpage", views.createpage, name="createpage"),
    path("random-page", views.random_page, name="random page"),
    path("edit-page/<str:entry>", views.edit_page, name="edit page"),
    path("search", views.search, name="search"),
    path("save-page", views.save_page, name="save page"),
    path("save-page/<str:entry>", views.save_page, name="save edited page")
    

]
