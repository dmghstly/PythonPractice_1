"""
Тестирование функций чтения данных из источника.
"""
from typing import Any

import pytest

from formatters.models import (
    BookModel,
    InternetResourceModel,
    ArticlesCollectionModel,
    MagazineArticleModel,
    NewsArticleModel,
)
from readers.reader import (
    BookReader,
    GOSTSourcesReader,
    InternetResourceReader,
    ArticlesCollectionReader,
    MagazineArticleReader,
    NewsArticleReader,
    APASourcesReader,
)
from settings import TEMPLATE_FILE_PATH


class TestReaders:
    """
    Тестирование функций чтения данных из источника.
    """

    @pytest.fixture
    def gost_workbook(self) -> Any:
        """
         Получение объекта тестовой рабочей книги.
        :return:
        """

        return GOSTSourcesReader(TEMPLATE_FILE_PATH).workbook

    @pytest.fixture
    def apa_workbook(self) -> Any:
        """
         Получение объекта тестовой рабочей книги.
        :return:
        """

        return APASourcesReader(TEMPLATE_FILE_PATH).workbook

    def test_gost_book(self, gost_workbook: Any) -> None:
        """
        Тестирование чтения книги.

        :param workbook: Объект тестовой рабочей книги.
        """

        models = BookReader(gost_workbook).read()

        assert len(models) == 4
        model = models[0]

        model_type = BookModel

        assert isinstance(model, model_type)
        assert model.authors == "Иванов И.М., Петров С.Н."
        assert model.title == "Наука как искусство"
        assert model.edition == "3-е"
        assert model.city == "СПб."
        assert model.publishing_house == "Просвещение"
        assert model.year == 2020
        assert model.pages == 999

        # проверка общего количества атрибутов
        assert len(model_type.schema().get("properties", {}).keys()) == 7

    def test_gost_internet_resource(self, gost_workbook: Any) -> None:
        """
        Тестирование чтения интернет-ресурса.

        :param workbook: Объект тестовой рабочей книги.
        """

        models = InternetResourceReader(gost_workbook).read()

        assert len(models) == 3
        model = models[0]

        model_type = InternetResourceModel

        assert isinstance(model, model_type)
        assert model.article == "Наука как искусство"
        assert model.website == "Ведомости"
        assert model.link == "https://www.vedomosti.ru"
        assert model.access_date == "01.01.2021"

        # проверка общего количества атрибутов
        assert len(model_type.schema().get("properties", {}).keys()) == 4

    def test_gost_articles_collection(self, gost_workbook: Any) -> None:
        """
        Тестирование чтения сборника статей.

        :param workbook: Объект тестовой рабочей книги.
        """

        models = ArticlesCollectionReader(gost_workbook).read()

        assert len(models) == 1
        model = models[0]

        model_type = ArticlesCollectionModel

        assert isinstance(model, model_type)
        assert model.authors == "Иванов И.М., Петров С.Н."
        assert model.article_title == "Наука как искусство"
        assert model.collection_title == "Сборник научных трудов"
        assert model.city == "СПб."
        assert model.publishing_house == "АСТ"
        assert model.year == 2020
        assert model.pages == "25-30"

        # проверка общего количества атрибутов
        assert len(model_type.schema().get("properties", {}).keys()) == 7

    def test_gost_magazine_article(self, gost_workbook: Any) -> None:
        """
        Тестирование чтения статей из журналов.

        :param workbook: Объект тестовой рабочей книги.
        """

        models = MagazineArticleReader(gost_workbook).read()

        assert len(models) == 1
        model = models[0]

        model_type = MagazineArticleModel

        assert isinstance(model, model_type)
        assert model.authors == "Иванов И.М., Петров С.Н."
        assert model.article_name == "Наука как искусство"
        assert model.magazine_name == "Образование и наука"
        assert model.magazine_num == 10
        assert model.pub_year == 2020
        assert model.pages == "25-30"

        # проверка общего количества атрибутов
        assert len(model_type.schema().get("properties", {}).keys()) == 6

    def test_gost_news_article(self, gost_workbook: Any) -> None:
        """
        Тестирование чтения статей из газет.

        :param workbook: Объект тестовой рабочей книги.
        """

        models = NewsArticleReader(gost_workbook).read()

        assert len(models) == 1
        model = models[0]

        model_type = NewsArticleModel

        assert isinstance(model, model_type)
        assert model.authors == "Иванов И.М., Петров С.Н."
        assert model.article_name == "Наука как искусство"
        assert model.news_name == "Южный Урал"
        assert model.article_num == 5
        assert model.edition_year == 1980
        assert model.news_pub_date == "01.10"

        # проверка общего количества атрибутов
        assert len(model_type.schema().get("properties", {}).keys()) == 6

    def test_gost_sources_reader(self) -> None:
        """
        Тестирование функции чтения всех моделей из источника.
        """

        models = GOSTSourcesReader(TEMPLATE_FILE_PATH).read()
        # проверка общего считанного количества моделей
        assert len(models) == 10

        # проверка наличия всех ожидаемых типов моделей среди типов считанных моделей
        model_types = {model.__class__.__name__ for model in models}
        assert model_types == {
            BookModel.__name__,
            InternetResourceModel.__name__,
            ArticlesCollectionModel.__name__,
            MagazineArticleModel.__name__,
            NewsArticleModel.__name__,
        }

    def test_apa_book(self, apa_workbook: Any) -> None:
        """
        Тестирование чтения книги.

        :param workbook: Объект тестовой рабочей книги.
        """

        models = BookReader(apa_workbook).read()

        assert len(models) == 4
        model = models[0]

        model_type = BookModel

        assert isinstance(model, model_type)
        assert model.authors == "Иванов И.М., Петров С.Н."
        assert model.title == "Наука как искусство"
        assert model.edition == "3-е"
        assert model.city == "СПб."
        assert model.publishing_house == "Просвещение"
        assert model.year == 2020
        assert model.pages == 999

        # проверка общего количества атрибутов
        assert len(model_type.schema().get("properties", {}).keys()) == 7

    def test_apa_internet_resource(self, apa_workbook: Any) -> None:
        """
        Тестирование чтения интернет-ресурса.

        :param workbook: Объект тестовой рабочей книги.
        """

        models = InternetResourceReader(apa_workbook).read()

        assert len(models) == 3
        model = models[0]

        model_type = InternetResourceModel

        assert isinstance(model, model_type)
        assert model.article == "Наука как искусство"
        assert model.website == "Ведомости"
        assert model.link == "https://www.vedomosti.ru"
        assert model.access_date == "01.01.2021"

        # проверка общего количества атрибутов
        assert len(model_type.schema().get("properties", {}).keys()) == 4

    def test_apa_sources_reader(self) -> None:
        """
        Тестирование функции чтения всех моделей из источника.
        """

        models = APASourcesReader(TEMPLATE_FILE_PATH).read()
        # проверка общего считанного количества моделей
        assert len(models) == 7

        # проверка наличия всех ожидаемых типов моделей среди типов считанных моделей
        model_types = {model.__class__.__name__ for model in models}
        assert model_types == {
            BookModel.__name__,
            InternetResourceModel.__name__,
        }
