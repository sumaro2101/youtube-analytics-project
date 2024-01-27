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
        playlist = self.youtube.playlists().list(channelId=self.channel_id, part='contentDetails,snippet', maxResults=10).execute()
        return playlist

    def __build_response_playlistvideos(self, list_id):
        playlist_videos = self.youtube.playlistItems().list(playlistId=list_id, part="contentDetails", maxResults=50).execute()
        return playlist_videos

    def __build_response_timevideo(self):
        time_video = self.youtube.videos().list()
    
    def print_info(self, value="channel", id_playlist=None) -> None:   
        """Выводит в консоль информацию о канале."""
        
        match value:
            case "channel":
                print(json.dumps(self.__build_response_channel(), indent=2, ensure_ascii=False))
            case "playlist":
                for playlist in self.__build_response_playlist()['items']:
                    print(json.dumps(playlist, indent=2, ensure_ascii=False))
            case "playlist_items":
                print(json.dumps(self.__build_response_playlistvideos(id_playlist), indent=2, ensure_ascii=False))
            case _:
                raise ValueError("Ожидалось значени value='channel', 'playlist', 'playlist_items'")
                
        
        