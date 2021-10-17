import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import AsyncToSync

count = 0
class Chat(WebsocketConsumer):
    def connect(self):
       self.room_name = self.scope['url_route']['kwargs']['room_name']
       self.room_group_name = 'chat_'+self.room_name
       AsyncToSync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
       self.accept()

    def disconnect(self,code):
       AsyncToSync(self.channel_layer.group_discard)(self.room_group_name,self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        AsyncToSync(self.channel_layer.group_send)(self.room_group_name,{'type':'chat_message','message':message,'sender':sender,'receiver':receiver})
    
    def chat_message(self,event):
        message = event['message']
        sender =event['sender']
        receiver =event['receiver']
        self.send(text_data=json.dumps({'command':'message','message':message,'sender':sender,'receiver':receiver}))
    
class Status(WebsocketConsumer):
    def connect(self):
        self.room_name = 'status'
        self.room_group_name = 'status_'+self.room_name
        AsyncToSync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
        self.accept()
        global count
        count += 1
        self.send(json.dumps({'count':count}))
    
    def disconnect(self,code):
        AsyncToSync(self.channel_layer.group_discard)(self.room_group_name,self.channel_name)
        global count
        count -= 1
        self.send(json.dumps({'count':count}))

    def receive(self, text_data=None, bytes_data=None):
        pass

class Typing(WebsocketConsumer):
    def connect(self):
        self.room_name = 'typing'
        self.room_group_name = 'typing_'+self.room_name
        AsyncToSync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
        self.accept()

    def disconnect(self,code):
        AsyncToSync(self.channel_layer.group_discard)(self.room_group_name,self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        typer = text_data_json['typer']
        receiver = text_data_json['receiver']
        status = text_data_json['status']
        AsyncToSync(self.channel_layer.group_send)(self.room_group_name,{'type':'typingstatus','typer':typer,'status':status,'receiver':receiver})

    def typingstatus(self,event):
        typer = event['typer']
        receiver = event['receiver']
        status = event['status']
        self.send(text_data=json.dumps({'command':'message','typer':typer,'status':status,'receiver':receiver}))
