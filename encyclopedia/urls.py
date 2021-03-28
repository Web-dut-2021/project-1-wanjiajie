from django.urls import path

from . import views
app_name='encyclopedia'
urlpatterns = [
    path("index/", views.index, name="index"),
    path("wiki/<str:title>/",views.renderSubPage, name="subPage"),
    path("search/",views.search,name="result"),
    path("add/",views.create,name="create"),
    path("edit/<str:title>/",views.edit,name="edit"),
    path("random/",views.randomEntry,name="random")
]
