# from django.shortcuts import render
# from django.http import HttpResponse
# from rest_framework import routers, serializers, viewsets
# # Create your views here.

# def index(request):
#     return HttpResponse('hi')

from django.contrib.auth import login
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from rest_framework.response import Response
from users.models import User
from django.db.models import Q
from users.serializers import UserSerializer
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data['user']
    login(request, user)

    token = AuthToken.objects.create(user)[1]

    return Response({
        "token": token
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request._auth.delete()
    return Response({"success": True})




@permission_classes([IsAuthenticated])
@api_view(['GET'])
def users(request, role):
    search = request.GET.get("search")

    qs = User.objects.all()
    qs = qs.filter(role=role)

    if search:
        qs = qs.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    # data = qs.values("id", "first_name", "last_name", "email", "role")
    serializer = UserSerializer(qs, many=True)
    return Response(serializer.data)
