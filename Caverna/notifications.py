from channels.layers import get_channel_layer
from .serializers import UserSerializerDRF

async def update_user(user_object):
    serializer = UserSerializerDRF(user_object)
    #need to write custom method in serializer
    group_name = serializer.get_group_name()
    channel_layer = get_channel_layer()
    content = {
        # type used on front-end
        'type': 'UPDATE_User',
        'payload': serializer.data,
    }
    await channel_layer.group_send(group_name, {
        'type': 'notify',
        'content': content
    })