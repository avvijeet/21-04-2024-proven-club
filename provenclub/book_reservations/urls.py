from book_reservations.views import BooksViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r"books", BooksViewSet, basename="book")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
