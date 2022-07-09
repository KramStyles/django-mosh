from djoser.serializers import UserCreateSerializer as BaseCreateSerializer, UserSerializer as BaseSerializer


class UserCreateSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']


class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        fields = ['id', 'email', 'username', 'first_name', 'last_name']