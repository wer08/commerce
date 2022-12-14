from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newListing", views.newListing, name="newListing"),
    path("categories", views.categories, name="categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("addComment", views.addComment, name="addComment"),
    path("search",views.search, name="search"),
    path("won",views.won, name="won"),
    path("closeAuction/<int:listing>", views.closeAuction, name="closeAuction"),
    path("addWatchlist/<int:listing>", views.addWatchlist, name="addWatchlist"),
    path("category/<str:category_listing>", views.category_listing, name="category_listing"),
    path("edit/<int:listing>", views.edit, name="edit"),
    path("<int:listing>", views.listing, name="listing")
]
