import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("users", self.channel_name)
        await self.channel_layer.group_add("employees", self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("users", self.channel_name)
        await self.channel_layer.group_discard("employees", self.channel_name)

    async def send_dashboard_stats(self, event):
        await self.send(
            text_data=json.dumps({"type": event["event_type"], "data": event["data"]})
        )
