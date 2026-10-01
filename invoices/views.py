from rest_framework import generics

from .models import DeliveryChallan, Invoice
from .serializers import (
    DeliveryChallanSerializer,
    InvoiceSerializer,
)


class DeliveryChallanListCreateView(generics.ListCreateAPIView):
    queryset = (
        DeliveryChallan.objects
        .select_related("client", "created_by")
        .prefetch_related("items__paint")
        .order_by("-challan_date", "-id")
    )
    serializer_class = DeliveryChallanSerializer


class DeliveryChallanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        DeliveryChallan.objects
        .select_related("client", "created_by")
        .prefetch_related("items__paint")
    )
    serializer_class = DeliveryChallanSerializer


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = (
        Invoice.objects
        .select_related("client", "created_by")
        .prefetch_related("items__paint", "delivery_challans")
        .order_by("-invoice_date", "-id")
    )
    serializer_class = InvoiceSerializer


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        Invoice.objects
        .select_related("client", "created_by")
        .prefetch_related("items__paint", "delivery_challans")
    )
    serializer_class = InvoiceSerializer