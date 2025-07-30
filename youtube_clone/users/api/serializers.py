from rest_framework import serializers

from youtube_clone.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "name",
            "email",
            "id",
            "is_active",
            "last_name",
            "last_login",
        )


class UserMeReadSerializer(UserCustomSerializer):
    modules = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            *UserCustomSerializer.Meta.fields,
            "modules",
        )

    @staticmethod
    def get_modules(obj: User):
        return list(
            set([module for group in obj.groups.all() for module in group.modules])
        )
