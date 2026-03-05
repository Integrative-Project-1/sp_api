from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserCapacity
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    LoginSerializer,
    UserCapacitySerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    POST /api/auth/login/
    
    Login con username y password. Retorna user data y JWT token.
    
    Request:
        {
            "username": "demo",
            "password": "demo123"
        }
    
    Response 200:
        {
            "user": {"id": 1, "username": "demo", "email": "demo@example.com"},
            "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
        }
    
    Response 401:
        {"detail": "Credenciales inválidas."}
    """
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'user': UserDetailSerializer(user).data,
                'token': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {'detail': serializer.errors.get('non_field_errors', ['Credenciales inválidas.'])[0]},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    POST /api/auth/logout/
    
    Logout (simplemente invalida el token en el frontend).
    
    Response 200: {}
    """
    # En JWT stateless, el logout se maneja en el cliente borrando el token
    # Aquí simplemente confirmamos la respuesta
    return Response({}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    GET /api/auth/me/
    
    Retorna información del usuario autenticado.
    
    Response 200:
        {"id": 1, "username": "demo", "email": "demo@example.com", ...}
    
    Response 401:
        {"detail": "No autenticado."}
    """
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def capacity_view(request):
    """
    GET /api/capacity/ - Obtener capacidad del usuario
    PATCH /api/capacity/ - Actualizar capacidad del usuario
    
    GET Response 200:
        {"daily_limit": 6}
    
    PATCH Request:
        {"daily_limit": 8}
    
    PATCH Response 200:
        {"daily_limit": 8}
    
    PATCH Response 400:
        {"daily_limit": ["Asegúrese de que este valor sea mayor o igual a 1."]}
    """
    if request.method == 'GET':
        capacity, created = UserCapacity.objects.get_or_create(
            user=request.user,
            defaults={'daily_limit': 6}
        )
        serializer = UserCapacitySerializer(capacity)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        capacity, created = UserCapacity.objects.get_or_create(
            user=request.user,
            defaults={'daily_limit': 6}
        )

        serializer = UserCapacitySerializer(capacity, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


