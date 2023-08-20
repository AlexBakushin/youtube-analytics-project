import json

from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""
    info = []
    youtube_object = None

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        Channel.info.append(self)

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        api_key = os.environ.get('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        Channel.info.append(channel)
        return channel

    def title(self):
        """
        Возвращает название
        """
        return Channel.info[1].get('items')[0].get('snippet').get('title')

    def video_count(self):
        """
        Возвращает количество видео на канале
        """
        return Channel.info[1].get('items')[0].get('statistics').get('videoCount')

    def url(self):
        """
        Возвращает полную ссылку на канал
        """
        return 'https://www.youtube.com/channel/' + Channel.info[1].get('items')[0].get('id')

    @classmethod
    def get_service(cls):
        """
        - класс-метод `get_service()`, возвращающий объект для работы с YouTube API
        """
        return cls.info[0]

    def to_json(self, file_name):
        """
        - метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра `Channel`
        """
        with open(file_name, 'w') as outfile:
            return json.dump(Channel.info[1], outfile)
