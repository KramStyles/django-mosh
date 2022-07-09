from djoser.serializers import UserCreateSerializer as BaseCreateSerializer


class UserCreateSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
