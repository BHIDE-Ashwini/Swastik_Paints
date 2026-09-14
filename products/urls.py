from django.urls import path

from .views import (
    CategoryDetailView,
    CategoryListCreateView,
    PaintDetailView,
    PaintListCreateView,
)

urlpatterns = [
    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list",
    ),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "paints/",
        PaintListCreateView.as_view(),
        name="paint-list",
    ),
    path(
        "paints/<int:pk>/",
        PaintDetailView.as_view(),
        name="paint-detail",
    ),
]