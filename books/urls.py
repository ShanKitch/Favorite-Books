from django.urls import path 
from . import views
urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login', views.login),
    path ('logout', views.logout),
    path('success',views.success), 
    path('add_book', views.add_book),
    path('view_book/<int:id>', views.view_book),
    path('update/<int:id>',views.update),
    path('delete/<int:id>',views.delete),
    path('favorite/<int:id>', views.favorite),
    path('unfavorite/<int:id>',views.unfavorite)

]
