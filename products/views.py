from rest_framework import generics

from .models import Category, Paint
from .serializers import CategorySerializer, PaintSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PaintListCreateView(generics.ListCreateAPIView):
    queryset = (
        Paint.objects
        .select_related("category")
        .prefetch_related("images")
    )
    serializer_class = PaintSerializer


class PaintDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        Paint.objects
        .select_related("category")
        .prefetch_related("images")
    )
    serializer_class = PaintSerializer