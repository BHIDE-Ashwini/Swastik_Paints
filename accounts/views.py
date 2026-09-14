from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminProfile


class MeView(APIView):
    permission_classes = [IsAdminProfile]

    def get(self, request):
        admin = request.user.admin_profile

        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "full_name": admin.full_name,
            "phone_number": admin.phone_number,
            "role": admin.role,
            "is_active": admin.is_active,
        })