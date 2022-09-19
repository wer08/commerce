from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newListing", views.newListing, name="newListing"),
    path("categories", views.categories, name="categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("/category/<str:category_listing>", views.category_listing, name="category_listing"),
    path("<str:listing>", views.listing, name="listing")
]