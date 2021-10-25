from rest_framework import serializers
from apps.user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'identity', 'first_name', 'last_name', 'mobile_phone', 'direction', 'city',
                  'postal_code')
        read_only_fields = ('id',)
