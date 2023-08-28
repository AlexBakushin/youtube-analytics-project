# Импор всех необходимых библиотек
import json
from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""
    # Пустой список для информации о каналах
    info = []
    # Пустой список для инициализаторов класса
    youtube_object = []

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        channel_id = id канала
        __name = название канала
        __video_count = количество видео
        __sub_count = количество просмотров
        """
        self.channel_id = channel_id
        Channel.youtube_object.append(self)
        self.__name = self.print_info().get('items')[0].get('snippet').get('title')
        self.__video_count = self.print_info().get('items')[0].get('statistics').get('videoCount')
        self.__sub_count = int(self.print_info().get('items')[0].get('statistics').get('subscriberCount'))

    def __str__(self):
        """
        :return: 'название канала'('ссылка на канал')
        """
        return f"{self.__name} ({Channel.url(self)})"

    def __add__(self, other):
        """
        Суммирование подпищиков каналов
        :param other: количество подпищиков другого канала
        :return: общее количество подпищиков или ошибка
        """
        if type(other) == Channel:
            return self.__sub_count + other.__sub_count
        else:
            raise TypeError

    def __sub__(self, other):
        """
        Вычитание подпищиков каналов
        :param other: количество подпищиков другого канала
        :return: разница количества подпищиков или ошибка
        """
        if type(other) == Channel:
            return self.__sub_count - other.__sub_count
        else:
            raise TypeError

    def __lt__(self, other):
        """
        Если количество подпищиков первого канала меньше количества подпищиков второго
        :param other: количество подпищиков другого канала
        :return: True или False или ошибка
        """
        if type(other) == Channel:
            return self.__sub_count < other.__sub_count
        else:
            raise TypeError

    def __le__(self, other):
        """
        Если количество подпищиков первого канала меньше или равно количеству подпищиков второго
        :param other: количество подпищиков другого канала
        :return: True или False или ошибка
        """
        if type(other) == Channel:
            return self.__sub_count <= other.__sub_count
        else:
            raise TypeError

    def __gt__(self, other):
        """
        Если количество подпищиков первого канала больше количества подпищиков второго
        :param other: количество подпищиков другого канала
        :return: True или False или ошибка
        """
        if type(other) == Channel:
            return self.__sub_count > other.__sub_count
        else:
            raise TypeError

    def __ge__(self, other):
        """
        Если количество подпищиков первого канала больше или равно количеству подпищиков второго
        :param other: количество подпищиков другого канала
        :return: True или False или ошибка
        """
        if type(other) == Channel:
            return self.__sub_count >= other.__sub_count
        else:
            raise TypeError

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
