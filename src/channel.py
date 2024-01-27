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
    
    def __show_id_playlists(self):
        id_playlist = [[item['snippet']['description'], item['id']] for item in self.__build_response_playlist()["items"]]
        return id_playlist

    def __build_response_playlistvideos(self, list_id):
        playlist_videos = self.youtube.playlistItems().list(playlistId=list_id, part="contentDetails", maxResults=50).execute()
        return playlist_videos
    
    def __show_id_videos(self, list_id):
        id_videos = [video['contentDetails']['videoId'] for video in self.__build_response_playlistvideos(list_id)]
        return id_videos

    def __build_response_timevideo(self):
        time_video = self.youtube.videos().list()
    
    def print_info(self, value="channel", id_playlist=None) -> None:   
        """Выводит в консоль информацию о канале."""
        
        match value:
            case "channel":
                print(json.dumps(self.__build_response_channel(), indent=2, ensure_ascii=False))
            case "playlists":
                for playlist in self.__build_response_playlist()['items']:
                    print(json.dumps(playlist, indent=2, ensure_ascii=False))
            case "id_playlists":
                for id_p in self.__show_id_playlists():
                    print(id_p)
            case "playlist_videos":
                print(json.dumps(self.__build_response_playlistvideos(id_playlist), indent=2, ensure_ascii=False))
            case "id_videos":
                print(self.__show_id_videos(id_playlist))
            case _:
                raise ValueError("Ожидалось значени value='channel', 'playlists', 'playlist_videos', 'id_videos'")
                
        
        