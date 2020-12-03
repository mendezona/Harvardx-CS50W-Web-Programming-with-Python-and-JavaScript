from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("newpage.html", views.newPage, name="newPage"),
    path("editwiki.html", views.editWiki, name="editWiki"),
    path("randompage", views.randomPage, name="randomPage"),
    path("<str:entryName>", views.entryName, name="entryName")
]
