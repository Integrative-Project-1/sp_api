from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserCapacity


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User - vista pública."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado del usuario (información personal)."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class LoginSerializer(serializers.Serializer):
    """Serializer para login - acepta username y password."""
    username = serializers.CharField(
        max_length=150,
        write_only=True,
        help_text='Username del usuario'
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Contraseña del usuario'
    )

    def validate(self, data):
        """Validar credenciales."""
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                'Debe proporcionar tanto usuario como contraseña.'
            )

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError(
                'Credenciales inválidas.'
            )

        data['user'] = user
        return data


class UserCapacitySerializer(serializers.ModelSerializer):
    """Serializer para configuración de capacidad del usuario."""

    class Meta:
        model = UserCapacity
        fields = ['daily_limit']

    def validate_daily_limit(self, value):
        """Validar que el límite esté en el rango válido."""
        if value < 1 or value > 16:
            raise serializers.ValidationError(
                'Asegúrese de que este valor sea mayor o igual a 1.'
            )
        return value
