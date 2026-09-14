from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import DeliveryChallan
from .serializers import DeliveryChallanSerializer


class DeliveryChallanListCreateView(generics.ListCreateAPIView):
    queryset = (
        DeliveryChallan.objects
        .select_related("client")
        .prefetch_related("items__paint")
        .order_by("-challan_date", "-id")
    )
    serializer_class = DeliveryChallanSerializer


class DeliveryChallanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        DeliveryChallan.objects
        .select_related("client")
        .prefetch_related("items__paint")
    )
    serializer_class = DeliveryChallanSerializer