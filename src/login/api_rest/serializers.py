from django.contrib.auth.models import User
from rest_framework import serializers


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password")

    def create(self, validated_data):
        return self.update(User(username=validated_data.get('username')), validated_data)


    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        instance.save()

        return  instance