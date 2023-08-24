import json

from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""
    info = []
    youtube_object = []

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        Channel.youtube_object.append(self)
        self.__name = self.print_info().get('items')[0].get('snippet').get('title')
        self.__video_count = self.print_info().get('items')[0].get('statistics').get('videoCount')
        self.__sub_count = int(self.print_info().get('items')[0].get('statistics').get('subscriberCount'))

    def __str__(self):
        return f"{self.__name} ({Channel.url(self)})"

    def __add__(self, other):
        return self.__sub_count + other.__sub_count

    def __sub__(self, other):
        return self.__sub_count - other.__sub_count

    def __lt__(self, other):
        return self.__sub_count < other.__sub_count

    def __le__(self, other):
        return self.__sub_count <= other.__sub_count

    def __gt__(self, other):
        return self.__sub_count > other.__sub_count

    def __ge__(self, other):
        return self.__sub_count >= other.__sub_count

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        api_key = os.environ.get('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.info.append(channel)
        return channel

    def title(self):
        """
        Возвращает название
        """
        return self.__name

    def video_count(self):
        """
        Возвращает количество видео на канале
        """
        return self.__video_count

    def url(self):
        """
        Возвращает полную ссылку на канал
        """
        return 'https://www.youtube.com/channel/' + self.channel_id

    @classmethod
    def get_service(cls):
        """
        - класс-метод `get_service()`, возвращающий объект для работы с YouTube API
        """
        return cls.youtube_object[0]

    def to_json(self, file_name):
        """
        - метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра `Channel`
        """
        with open(file_name, 'w') as outfile:
            return json.dump(self.print_info(), outfile)
