from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token['user_id'], is_active=True)

        return user
    except get_user_model().DoesNotExist:
        return AnonymousUser()
