"""
    Workflow: client submits request to ws(s)://server.domain/ws/notifications
    the "Payload": {'model': 'app.model_name', 'id': 'pk or a secure version of pk'}
    all sockets are accepted at first

    if user is authenticated and has permissions for the specific onject 
    then they are assigned a group to receive updates via socket. if not then 
    they are presented with errors such as need to login, or register, renew tokens, etc

    consumer handles all incoming requests and assigns sockets to different groups

    consumer/function will act as emitter to broadcast all changes to the 
    specific subscribers. it will format the message/payload to have model_name
    in similar form as the original request: {'update_to_model': 'new_model_data_in_JSON'}

    consumer will handle change-requests from user. these will be assigned 
    to helper functions that will manipulated data and then save it to db which 
    triggers the emitter to broadcast

"""

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # always accept. can be closed later if needed
        await self.accept()

    async def notify(self, event):
        # emitter that relays other group_send msgs
        # incoming is {type: notify, content: json_msg}
        await self.send_json(event['content'])

    async def receive_json(self, content, **kwargs):
        # validate data then permissions
        serializer = self.get_serializer(data=content)
        if not serializer.is_valid():
            return
        group_name = serializer.get_group_name()
        self.groups.append(group_name)

    def get_serializer(self, data):
        # based on fields in data, find correct serializer and then serialize it and return the serializer
        pass