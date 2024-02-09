import os
from googleapiclient.discovery import build
import json
import isodate


class Channel:
    """Класс для ютуб-канала"""

    API_YOUTUBE = os.getenv("API_YOUTUBE")
    youtube = build('youtube', 'v3', developerKey=API_YOUTUBE)
    
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        
        self._validate_id(channel_id)
        self.__channel_id = channel_id
        self.__channel = self.__build_response_channel()
        self.__title = self.__channel["items"][0]["snippet"]["title"]
        self.__description = self.__channel["items"][0]["snippet"]["description"]
        self.__url = "https://www.youtube.com/channel/" + self.__channel["items"][0]["id"]
        self.__subscriber_count = int(self.__channel["items"][0]["statistics"]["subscriberCount"])
        self.__video_count = int(self.__channel["items"][0]["statistics"]["videoCount"])
        self.__view_count = int(self.__channel["items"][0]["statistics"]["viewCount"])
        
            
    @classmethod
    def __verify_data(cls, data) -> None:
        """Проверка операнда на совместимость
        """        
        if not isinstance(data, int|Channel):
            raise TypeError("Ожидался класс 'Channel' или число")
        
        
    @classmethod
    def _validate_id(cls, id: str) -> None:
        """Валидация входного значения ID канала
        """   
             
        if not isinstance(id, str):
            raise TypeError(f"Получен {type(id)}, ожидалась строка")
        
        
    def __add__(self, other: int) -> int:
        self.__verify_data(other)
        return self.__subscriber_count + other.__subscriber_count
    
    def __sub__(self, other: int) -> int:
        self.__verify_data(other)
        return self.__subscriber_count - other.__subscriber_count
    
    def __mul__(self, other: int) -> int:
        self.__verify_data(other)
        return self.__subscriber_count * other.__subscriber_count
    
    def __truediv__(self, other: int) -> float:
        self.__verify_data(other)
        return self.__subscriber_count / other.__subscriber_count
    
    def __floordiv__(self, other: int) -> int:
        self.__verify_data(other)
        return self.__subscriber_count // other.__subscriber_count
    
    def __mod__(self, other: int) -> int:
        self.__verify_data(other)
        return self.__subscriber_count % other.__subscriber_count
    
    def __eq__(self, other: int) -> bool:
        self.__verify_data(other)
        return self.__subscriber_count == other.__subscriber_count
    
    def __lt__(self, other: int) -> bool:
        self.__verify_data(other)
        return self.__subscriber_count < other.__subscriber_count
    
    def __le__(self, other: int) -> bool:
        self.__verify_data(other)
        return self.__subscriber_count <= other.__subscriber_count
    
    def __gt__(self, other: int) -> bool:
        self.__verify_data(other)
        return self.__subscriber_count > other.__subscriber_count
    
    def __ge__(self, other: int) -> bool:
        self.__verify_data(other)
        return self.__subscriber_count >= other.__subscriber_count

    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def video_count(self) -> str:
        return self.__video_count
    
    @property
    def url(self) -> str:
        return self.__url

    @classmethod
    def get_service(cls): 
        return cls.youtube
    
    
    def __build_response_channel(self) -> dict:
        """Построение запроса на получение данных о канале

        Returns:
            dict: Возвращает готовый ответ данных о канале
        """   
             
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel
    
    
    def __build_response_playlist(self) -> dict:
        """Построение запроса на получение данных о плейлистах канала

        Returns:
            dict: Возвращает полученный данные о плейлистах
        """ 
             
        playlist = self.youtube.playlists().list(channelId=self.__channel_id, part='contentDetails,snippet', maxResults=10).execute()
        return playlist
    
    
    def __show_id_playlists(self) -> list:
        """ID плейлистов канала

        Returns:
            list: Возвращает полученный данные ID плейлистов
        """  
             
        id_playlist = [[item['snippet']['description'], item['id']] for item in self.__build_response_playlist()["items"]]
        return id_playlist
    

    def __build_response_playlistvideos(self, list_id: str) -> dict:
        """Построение запроса на получения данных о видео в указанном плейлисте 

        Args:
            list_id (str): ID плейлиста

        Returns:
            dict: Возвращает полученные данные видео в плейлисте
        """
                
        playlist_videos = self.youtube.playlistItems().list(playlistId=list_id, part="contentDetails", maxResults=50).execute()
        return playlist_videos
    
    
    def _show_id_videos(self, list_id: str) -> list:
        """Получает ID видео

        Args:
            list_id (str): _description_

        Returns:
            list: Возращает ID видео
        """   
             
        id_videos = [video['contentDetails']['videoId'] for video in self.__build_response_playlistvideos(list_id)['items']]
        return id_videos


    def __build_response_timevideo(self, list_id: str) -> dict:
        """Построение запроса на получение данных видео для вывода времени видео

        Args:
            list_id (str): ID плейлиста

        Returns:
            dict: Возращает данные видео
        """    
            
        time_video = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(self.__show_id_videos(list_id))).execute()
        return time_video
    
    
    def _build_response_statistics_video(self, id_video: str) -> dict:
        """Построение запроса на получения статистики видео

        Args:
            id_video (str): ID видео

        Returns:
            dict: Возращает данные статистики видео
        """   
             
        video_response = self.youtube.videos().list(part="snippet,statistics,contentDetails,topicDetails", id=id_video).execute()
        return video_response
    
    
    def print_info(self, value: str="channel", id_playlist: str|None=None, id_video: str| None=None) -> None:   
        """Вывод информации тех данных которые будут указаны

        Args:
            value (str, optional): Значение для получения желаемых данных. Defaults to "channel".
            id_playlist (srt|None, optional): ID плейлиста. Defaults to None.
            id_video (str|None, optional): ID видео. Defaults to None.
        """        
        
        match value:
            #Возвращает готовый ответ данных о канале
            case "channel":
                print(json.dumps(self.__build_response_channel(), indent=2, ensure_ascii=False))
            #Возвращает полученный данные о плейлистах
            case "playlists":
                for playlist in self.__build_response_playlist()['items']:
                    print(json.dumps(playlist, indent=2, ensure_ascii=False))
            #Возвращает полученный данные ID плейлистов     
            case "id_playlists":
                for id_p in self.__show_id_playlists():
                    print(id_p)
            #Возвращает полученные данные видео в плейлисте   
            case "playlist_videos":
                print(json.dumps(self.__build_response_playlistvideos(id_playlist), indent=2, ensure_ascii=False))
            #Возращает ID видео
            case "id_videos":
                print(self.__show_id_videos(id_playlist))
            #Возращает данные видео (время) 
            case "time_videos":
                for video in self.__build_response_timevideo(id_playlist)['items']:
                    # YouTube video duration is in ISO 8601 format
                    iso_8601_duration = video['contentDetails']['duration']
                    duration = isodate.parse_duration(iso_8601_duration)
                    print(duration)
            #Возращает данные статистики видео
            case "video_info":
                print(f'''Description: {self.__build_response_statistics_video(id_video)['items'][0]['snippet']['title']}
ViewCount: {self.__build_response_statistics_video(id_video)['items'][0]['statistics']['viewCount']}
LikeCount: {self.__build_response_statistics_video(id_video)['items'][0]['statistics']['likeCount']}
CommentCount: {self.__build_response_statistics_video(id_video)['items'][0]['statistics']['commentCount']}''')
            #Если не одно название не совпадает - исключение
            case _:
                raise ValueError("Ожидалось значени value='channel', 'playlists','id_playlist', 'playlist_videos', 'id_videos', 'time_videos', 'video_info'")
       
            
    def __dict_to_json(self):
        """Функция заполняющая словарь
        """   
             
        result = {}
        
        for key, value in self.__dict__.items():
            if not isinstance(value, list|dict):
                result[key] = value
                
        return result
        
                
    def to_json(self, name_file):
        """

        Args:
            name_file (src): путь к по которому будет создан json файл
        """   
             
        with open(name_file, 'w', encoding='utf-8') as f:
            json.dump([self.__dict_to_json()], f, ensure_ascii=False, indent=2)
            
    def __str__(self) -> str:
        return f'{self.__title} ({self.__url})'
            