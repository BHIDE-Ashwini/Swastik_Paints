from django.urls import path

from .views import (
    DeliveryChallanDetailView,
    DeliveryChallanListCreateView,
)

urlpatterns = [
    path(
        "delivery-challans/",
        DeliveryChallanListCreateView.as_view(),
        name="delivery-challan-list",
    ),
    path(
        "delivery-challans/<int:pk>/",
        DeliveryChallanDetailView.as_view(),
        name="delivery-challan-detail",
    ),
] 