from .channel import Channel
import json

class Video(Channel):
    
    def __init__(self, id_video: str) -> None:
        super()._validate_id(id_video)
        self.__id_video = id_video
        self.__video_responce = super()._build_response_statistics_video(self.__id_video)
        self.__name_video = self.__video_responce['items'][0]['snippet']['title']
        self.__view_count = self.__video_responce['items'][0]['statistics']['viewCount']
        self.__like_count = self.__video_responce['items'][0]['statistics']['likeCount']
     
    def __str__(self) -> str:
        return self.__name_video
    
    def __repr__(self) -> str:
        return f'''{[(item, value)
    for item, value
    in self.__dict__.items()
    if not isinstance(value, (list, dict))]}
{self.__class__.__name__}
{self.__id_video}
{self.__name_video}
{self.__view_count}
{self.__like_count}
{json.dumps(self.__video_responce, ensure_ascii=False, indent=2)}'''
        
        
class PLVideo(Video):
    
    def __init__(self, id_video: str, id_playlist) -> None:
        super().__init__(id_video)
        super()._validate_id(id_playlist)
        self.__id_playlist = id_playlist
        self.__playlist_info = super()._show_id_videos(self.__id_playlist)
        
    @property
    def playlist_info(self):
        return self.__playlist_info
    
    def __repr__(self) -> str:
        return f'''{super().__repr__()}
{self.__playlist_info}'''
