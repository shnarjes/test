from rest_framework import serializers
from user.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name','email')


'''
class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def create(self, validated_data):
            user = User.objects.create_user(
                validated_data['username'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            return user
'''
