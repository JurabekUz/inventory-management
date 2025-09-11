from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class MeSerializer(serializers.ModelSerializer):
    org__name = serializers.CharField(source='org.name', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'org__name']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        del data["refresh"]
        data["access"] = str(refresh.access_token)
        data["full_name"] = self.user.get_full_name()

        # remove update last login feature
        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)

        return data


class CheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']