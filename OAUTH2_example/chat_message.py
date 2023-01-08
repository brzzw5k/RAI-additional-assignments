import uuid
from datetime import datetime


class ChatMessageDB:

    messages = {}

    @classmethod
    def add(cls, message):
        cls.messages.update({message.id: message})
        return message

    @classmethod
    def get_all(cls):
        return cls.messages.values()


class ChatMessage:

    def __init__(self, message, sender):
        self.id = uuid.uuid4()
        self.dt = datetime.now()
        self.message = message
        self.sender = sender

    @classmethod
    def create(cls, message, sender):
        return ChatMessageDB.add(ChatMessage(message, sender))

    @classmethod
    def get_all(cls):
        return [{'user': ChatMessage.handle_null_sender(m), 'message': m.message} for m in ChatMessageDB.get_all()]

    @staticmethod
    def handle_null_sender(message):
        return message.sender \
            if message is not None and message.sender is not None \
            else 'System'
