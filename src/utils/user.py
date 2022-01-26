# from socket import socket
# from .channel import Channel
# from .message import Message
#
# class User:
#     def __init__(self, conn: socket):
#         self.channel = Channel(conn)
#
#     def push_text(self, message: Message, data: str):
#         message = message.clone()
#         message.action = "normal"
#         message.text = data
#         self.channel.send(message)
#
#     def push_warning(self, )
#
#
#
