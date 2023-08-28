# Импорт необходимых библиотек
from googleapiclient.discovery import build
import os


class Video:
    """
    Класс для видео
    """
    def __init__(self, video_id):
        """
        Инициализация экземпляра по id видео
        :param video_id: id видео
        video_title = название видео
        url = ссылка на видео
        view_count = количество просмотров
        like_count = количество лайков
        """
        self.__video_id = video_id
        self.__video_title: str = self.print_info()['items'][0]['snippet']['title']
        self.__url: str = 'https://www.youtube.com/channel/' + self.__video_id
        self.__view_count: int = self.print_info()['items'][0]['statistics']['viewCount']
        self.__like_count: int = self.print_info()['items'][0]['statistics']['likeCount']

    def __str__(self):
        """
        :return: Название видео
        """
        return self.__video_title

    def print_info(self):
        """
        Выводит всю информацию о видео в json-формате
        :return: массив информации о видео
        """
        api_key = os.environ.get('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.__video_id).execute()
        return video_response

    def video_title(self):
        """
        :return: название видео
        """
        return self.__video_title

    def url(self):
        """
        :return: ссылка на видео
        """
        return self.__url

    def view_count(self):
        """
        :return: количество просмотров
        """
        return self.__view_count

    def like_count(self):
        """
        :return: количество лайков
        """
        return self.__like_count


class PLVideo:
    """
    Класс для видео по плэй-листу
    """
    def __init__(self, video_id, playlist_id):
        """
        Инициализация экземпляра класса видео
        :param video_id: id видео
        :param playlist_id: id плэй-листа
        __video_title = название видео
        __url = ссылка на канал
        __view_count = количество просмотров
        __like_count = количество лайков
        """
        self.__video_id = video_id
        self.__playlist_id = playlist_id
        self.__video_title: str = self.print_info_video()['items'][0]['snippet']['title']
        self.__url: str = 'https://www.youtube.com/channel/' + self.__video_id
        self.__view_count: int = self.print_info_video()['items'][0]['statistics']['viewCount']
        self.__like_count: int = self.print_info_video()['items'][0]['statistics']['likeCount']

    def __str__(self):
        """
        :return: Название видео
        """
        return self.__video_title

    def print_info_playlist(self):
        """
        Выводит всю информацию о плэй-листе в json-формате
        :return: массив информации о плэй-листе
        """
        api_key = os.environ.get('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=self.__playlist_id, part='contentDetails',
                                                       maxResults=50, ).execute()
        return playlist_videos

    def print_info_video(self):
        """
        Выводит всю информацию о видео в json-формате
        :return: массив информации о видео
        """
        api_key = os.environ.get('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.__video_id).execute()
        return video_response
