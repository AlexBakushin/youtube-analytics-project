# Импорт всех необходимых библиотек
import isodate
import datetime
from googleapiclient.discovery import build
import os


class PlayList:
    """
    Класс для плэй-листа
    """
    def __init__(self, playlist_id):
        """
        Инициализация экземпляра по id плэй-листа
        :param playlist_id: id плэй-листа
        url = ссылка на плэй-лист
        video_response = массив информации о плэй-листе
        """
        self.playlist_id = playlist_id
        youtube = self.get_service()
        playlist = youtube.playlists().list(id=playlist_id, part='contentDetails,snippet').execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id
        self.video_response = self.print_info()

    def __str__(self):
        """
        :return: Название видео "Никак не смог найти вариант, как можно получить название плэй-листа по его id"
        """
        return self.title

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращает объект для работы с YouTube API
        """
        api_key = os.environ.get('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def print_info(self):
        """
        Выводит всю информацию о плэй-листе в json-формате
        :return: массив информации о плэй-листе
            """
        youtube = self.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                       maxResults=50, ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_resp = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()
        return video_resp

    @property
    def total_duration(self):
        """
        Выводит суммапрную длительность плэй-листа в формате iso date
        :return: продолжительность плэй-листа
        """
        duration_list = []
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_list.append(duration)
            duration_summ = datetime.timedelta(seconds=0)
            for duration_part in duration_list:
                duration_summ += duration_part
        return duration_summ

    def show_best_video(self):
        """
        Выводит ссылку на самое популярное видео в плэй-листе
        :return: ссылку
        """
        like_count = 0
        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > like_count:
                like_count = int(video['statistics']['likeCount'])
        return 'https://youtu.be/' + video['id']
