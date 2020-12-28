
import jwt
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from Cave_Farmers.settings import SECRET_KEY


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    # from client: {'token': xyz, 'game_id': 123}
    # to consumer to client: {'type': 'notify', 'content': msg_as_dict}
    # to client: {'type/message/payload': msg_as_dict}
    groups = []
    un_authenticated = True
    user_id = 0

    async def authenticate_self(self, content):
        token = content.get('token', 0)
        if token == 0:
            return
        try:
            decrypted = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
            decrypted = {'id': '0'}
        self.user_id = int(decrypted['id'])
        self.un_authenticated = self.user_id == 0

    async def connect(self):
        await self.accept()

    async def notify(self, event):
        await self.send_json(event['content'])

    async def receive_json(self, content, **kwargs):
        if self.un_authenticated:
            await self.authenticate_self(content)
            if self.un_authenticated:
                await self.close()
        game_id = content.get('game_id', 0)
        game = f"Game_{game_id}"
        player = f"player_{self.user_id}"
        self.groups.extend([game, player])
        await self.channel_layer.group_add(game, self.channel_name)
        await self.channel_layer.group_add(player, self.channel_name)



