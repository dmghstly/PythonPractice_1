"""
Стиль цитирования по ГОСТ Р 7.0.5-2008.
"""
from string import Template

from pydantic import BaseModel

from formatters.models import (
    BookModel,
    InternetResourceModel,
    ArticlesCollectionModel,
    MagazineArticleModel,
    NewsArticleModel,
)
from formatters.styles.base import BaseCitationStyle
from logger import get_logger


logger = get_logger(__name__)


class GOSTBook(BaseCitationStyle):
    """
    Форматирование для книг в формате ГОСТ.
    """

    data: BookModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $title. – $edition$city: $publishing_house, $year. – $pages с."
        )

    def substitute(self) -> str:

        logger.info('Форматирование книги "%s" ...', self.data.title)

        return self.template.substitute(
            authors=self.data.authors,
            title=self.data.title,
            edition=self.get_edition(),
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )

    def get_edition(self) -> str:
        """
        Получение отформатированной информации об издательстве.

        :return: Информация об издательстве.
        """

        return f"{self.data.edition} изд. – " if self.data.edition else ""


class GOSTInternetResource(BaseCitationStyle):
    """
    Форматирование для интернет-ресурсов в формате ГОСТ.
    """

    data: InternetResourceModel

    @property
    def template(self) -> Template:
        return Template(
            "$article // $website URL: $link (дата обращения: $access_date)."
        )

    def substitute(self) -> str:

        logger.info('Форматирование интернет-ресурса "%s" ...', self.data.article)

        return self.template.substitute(
            article=self.data.article,
            website=self.data.website,
            link=self.data.link,
            access_date=self.data.access_date,
        )


class GOSTCollectionArticle(BaseCitationStyle):
    """
    Форматирование для статьи из сборника в формате ГОСТ.
    """

    data: ArticlesCollectionModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title // $collection_title. – $city: $publishing_house, $year. – С. $pages."
        )

    def substitute(self) -> str:

        logger.info('Форматирование сборника статей "%s" ...', self.data.article_title)

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            collection_title=self.data.collection_title,
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )


class GOSTMagazineArticle(BaseCitationStyle):
    """
    Форматирование для статьи из журнала в формате ГОСТ.
    """

    data: MagazineArticleModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_name // $magazine_name. – $pub_year. – № $magazine_num. – С. $pages."
        )

    def substitute(self) -> str:

        logger.info('Форматирование статьи из журнала "%s" ...', self.data.article_name)

        return self.template.substitute(
            authors=self.data.authors,
            article_name=self.data.article_name,
            magazine_name=self.data.magazine_name,
            pub_year=self.data.pub_year,
            magazine_num=self.data.magazine_num,
            pages=self.data.pages,
        )


class GOSTNewsArticle(BaseCitationStyle):
    """
    Форматирование для статьи из газеты в формате ГОСТ.
    """

    data: NewsArticleModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_name // $news_name. – $edition_year. – № $article_num. – $news_pub_date."
        )

    def substitute(self) -> str:

        logger.info('Форматирование статьи из газеты "%s" ...', self.data.article_name)

        return self.template.substitute(
            authors=self.data.authors,
            article_name=self.data.article_name,
            news_name=self.data.news_name,
            edition_year=self.data.edition_year,
            news_pub_date=self.data.news_pub_date,
            article_num=self.data.article_num,
        )


class GOSTCitationFormatter:
    """
    Базовый класс для итогового форматирования списка источников в формате ГОСТ.
    """

    formatters_map = {
        BookModel.__name__: GOSTBook,
        InternetResourceModel.__name__: GOSTInternetResource,
        ArticlesCollectionModel.__name__: GOSTCollectionArticle,
        MagazineArticleModel.__name__: GOSTMagazineArticle,
        NewsArticleModel.__name__: GOSTNewsArticle,
    }

    def __init__(self, models: list[BaseModel]) -> None:
        """
        Конструктор.

        :param models: Список объектов для форматирования
        """

        formatted_items = []
        for model in models:
            formatted_items.append(self.formatters_map.get(type(model).__name__)(model))  # type: ignore

        self.formatted_items = formatted_items

    def format(self) -> list[BaseCitationStyle]:
        """
        Форматирование списка источников.

        :return:
        """

        return sorted(self.formatted_items, key=lambda item: item.formatted)
