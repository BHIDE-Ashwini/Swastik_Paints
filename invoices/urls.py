from django.urls import path

from .views import (
    DeliveryChallanDetailView,
    DeliveryChallanListCreateView,
    InvoiceDetailView,
    InvoiceListCreateView,
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
    path(
        "",
        InvoiceListCreateView.as_view(),
        name="invoice-list",
    ),
    path(
        "<int:pk>/",
        InvoiceDetailView.as_view(),
        name="invoice-detail",
    ),
]