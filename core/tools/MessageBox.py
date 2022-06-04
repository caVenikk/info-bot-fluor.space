from contextlib import suppress

from aiogram.types import Message
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from loader import bot


class MessageBox:
    _storage: dict[int: dict[int: [Message]]] = dict()
    _messages: dict[int: dict[int: {int}]] = dict()
    _default_chat_id: int = None

    @classmethod
    def _validate_chat_id(cls, chat_id: int) -> int:
        if not chat_id and cls._default_chat_id:
            chat_id = cls._default_chat_id
        elif not chat_id:
            raise ValueError("Default chat ID must be integer.")
        return chat_id

    @classmethod
    def set_chat_id(cls, chat_id: int):
        cls._default_chat_id = chat_id

    @classmethod
    def put(cls, message: Message, user_id: int, chat_id: int = None):
        chat_id = cls._validate_chat_id(chat_id)
        if chat_id not in cls._messages:
            cls._messages[chat_id] = dict()
        if user_id not in cls._messages[chat_id]:
            cls._messages[chat_id][user_id] = set()

        if message.message_id not in cls._messages[chat_id][user_id]:
            cls._messages[chat_id][user_id].add(message.message_id)
            if chat_id not in cls._storage:
                cls._storage[chat_id] = dict()
            if user_id not in cls._storage[chat_id]:
                cls._storage[chat_id][user_id] = []
            cls._storage[chat_id][user_id].append(message)

    @classmethod
    def get(cls, user_id: int, chat_id: int = None) -> Message | None:
        chat_id = cls._validate_chat_id(chat_id)
        if chat_id in cls._storage and user_id in cls._storage[chat_id] and cls._storage[chat_id][user_id]:
            return cls._storage[chat_id][user_id].pop()
        else:
            return None

    @classmethod
    async def delete_last(cls, user_id: int, chat_id: int = None):
        chat_id = cls._validate_chat_id(chat_id)
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            _message = cls.get(user_id=user_id, chat_id=chat_id)
            if _message is not None:
                if chat_id in cls._messages and user_id in cls._messages[chat_id]:
                    cls._messages[chat_id][user_id].discard(_message.message_id)
                await bot.delete_message(chat_id=chat_id, message_id=_message.message_id)

    @classmethod
    async def replace_last(cls, message: Message, user_id: int, chat_id: int = None):
        """
        Deleting last message at the user's stack and put
        on new message.
        """
        chat_id = cls._validate_chat_id(chat_id)
        await cls.delete_last(user_id=user_id, chat_id=chat_id)
        cls.put(message=message, user_id=user_id, chat_id=chat_id)
