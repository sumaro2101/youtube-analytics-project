from src.channel import Channel
import datetime
import json
import isodate

class PlayList(Channel):
    
    def __init__(self, id_playlist: int) -> None:
        super()._validate_id(id_playlist)
        self.__id_playlist = id_playlist
        self.__playlist = self._build_response_timevideo(self.__id_playlist)['items']
        self.__title = self.__build_response_playlist()['items'][0]['snippet']['title']
        self.__url = 'https://www.youtube.com/playlist?list=' + self.__id_playlist
        self.__total_duration = self.__total_duration()
       
        
    @property
    def title(self):
        return self.__title
    
    @property
    def url(self):
        return self.__url
    
    @property
    def total_duration(self):
        return self.__total_duration
    
    
    def __build_response_playlist(self):
        playlist = self.youtube.playlists().list(id=self.__id_playlist, part='snippet').execute()
        return playlist

    
    def __list_duration(self):
        time_videos = [isodate.parse_duration(duration['contentDetails']['duration'])
                       for duration
                       in self.__playlist]
        
        return time_videos
    
    
    def __total_duration(self):
        result = datetime.timedelta()
        
        for delta in self.__list_duration():
            result += delta
        
        return result
    
    
    def show_best_video(self):
        video_likes = 0
        best_video = None
        
        for item in self.__playlist:
            if video_likes < int(item['statistics']['likeCount']):
                best_video = item['id']
                video_likes = int(item['statistics']['likeCount'])
                
        return f'https://youtu.be/{best_video}'
