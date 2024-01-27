import os
from googleapiclient.discovery import build
import json

class Channel:
    """Класс для ютуб-канала"""

    API_YOUTUBE = os.getenv("API_YOUTUBE")

    youtube = build('youtube', 'v3', developerKey=API_YOUTUBE)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__validate_id(channel_id)
        self.channel_id = channel_id

    @classmethod
    def __validate_id(cls, id):
        if not isinstance(id, str):
            raise TypeError(f"Получен {type(id)}, ожидалась строка")

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, id):
        self.__channel_id = id
    
    def __build_response_channel(self):
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel
    
    def __build_response_playlist(self):
        playlist = self.youtube.playlists().list(id=self.channel_id, part='contentDetails,snippet', maxResults=50).execute()
        return playlist

    def print_info(self, value="channel") -> None:
        """Выводит в консоль информацию о канале."""
        if value == "channel":
            print(json.dumps(self.__build_response_channel(), indent=2, ensure_ascii=False))
        
        if value == "playlist":
            print(json.dumps(self.__build_response_playlist(), indent=2, ensure_ascii=False))
        