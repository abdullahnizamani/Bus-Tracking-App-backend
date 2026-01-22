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
from rest_framework import status
from users.models import User
from django.db.models import Q
from users.serializers import UserSerializer
from users.models import Student, Driver
from transport.serializers import BusSerializer
from transport.models import Bus

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



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request._auth.delete()
    return Response({"success": True})



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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_bus_view(request):
    """
    Returns the bus assigned to the logged-in student.
    """
    try:
        student = Student.objects.get(user=request.user)
        bus = student.bus_id  # Assuming Student model has a ForeignKey to Bus
        if not bus:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        serializer = BusSerializer(bus)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response(None, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def driver_bus_view(request):
    """
    Returns the bus assigned to the logged-in driver.
    """
    try:
        # Step 1: get driver profile
        driver = Driver.objects.get(user=request.user)

        # Step 2: get bus assigned to this driver
        bus = Bus.objects.get(driver_id=driver)

        serializer = BusSerializer(bus)
        return Response(serializer.data)

    except Driver.DoesNotExist:
        return Response(
            {"detail": "Driver profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Bus.DoesNotExist:
        return Response(
            {"detail": "No bus assigned to this driver"},
            status=status.HTTP_404_NOT_FOUND
        )
    

    
@api_view(['GET', 'PATCH'])
def bus_info(request, id):
        try:
            bus = Bus.objects.get(id=id)

        except Bus.DoesNotExist:
            return Response(
                {"detail": "No bus exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.method == "GET":
                serializer = BusSerializer(bus)
                return Response(serializer.data)
        elif request.method == 'PATCH':
            # Expect status in request.data
            new_status = request.data.get('status')
            if new_status is None:
                return Response(
                    {"detail": "Status not provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Make sure it's a boolean
            if not isinstance(new_status, bool):
                return Response(
                    {"detail": "Status must be a boolean"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            bus.is_active = new_status
            bus.save()
            return Response({'status': 'success'})
        

@api_view(['GET'])
def bus_list(request):
    bus = Bus.objects.all()
    serializer = BusSerializer(bus, many=True)
    return Response(serializer.data)