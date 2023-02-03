"""
Стиль цитирования по стандарту APA (7-е издание)
"""
from string import Template

from pydantic import BaseModel

from formatters.models import BookModel, InternetResourceModel
from formatters.styles.base import BaseCitationStyle
from logger import get_logger


logger = get_logger(__name__)


class APABook(BaseCitationStyle):
    """
    Форматирование для книг в формате APA.
    """

    data: BookModel

    # стоит отметить, что в стандарте APA некоторые данные из таблицы просто не нужны (город и кол-во страниц)
    @property
    def template(self) -> Template:
        return Template(
            "$authors ($year). $title. " + "$edition" + "$publishing_house."
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

        return f"({self.data.edition} ed.). " if self.data.edition else ""


class APAInternetResource(BaseCitationStyle):
    """
    Форматирование для интернет-ресурсов в формате APA.
    """

    data: InternetResourceModel

    # во входных данных нет даты, поэтому стоит n. d.
    @property
    def template(self) -> Template:
        return Template("$article. (n. d.). $website. $link")

    def substitute(self) -> str:

        logger.info('Форматирование интернет-ресурса "%s" ...', self.data.article)

        return self.template.substitute(
            article=self.data.article,
            website=self.data.website,
            link=self.data.link,
            access_date=self.data.access_date,
        )


class APACitationFormatter:
    """
    Базовый класс для итогового форматирования списка источников в формате APA.
    """

    formatters_map = {
        BookModel.__name__: APABook,
        InternetResourceModel.__name__: APAInternetResource,
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
