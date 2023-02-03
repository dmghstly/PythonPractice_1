"""
Описание схем объектов (DTO).
"""

from typing import Optional

from pydantic import BaseModel, Field


class BookModel(BaseModel):
    """
    Модель книги:

    .. code-block::

        BookModel(
            authors="Иванов И.М., Петров С.Н.",
            title="Наука как искусство",
            edition="3-е",
            city="СПб.",
            publishing_house="Просвещение",
            year=2020,
            pages=999,
        )
    """

    authors: str
    title: str
    edition: Optional[str]
    city: str
    publishing_house: str
    year: int = Field(..., gt=0)
    pages: int = Field(..., gt=0)


class InternetResourceModel(BaseModel):
    """
    Модель интернет ресурса:

    .. code-block::

        InternetResourceModel(
            article="Наука как искусство",
            website="Ведомости",
            link="https://www.vedomosti.ru/",
            access_date="01.01.2021",
        )
    """

    article: str
    website: str
    link: str
    access_date: str


class ArticlesCollectionModel(BaseModel):

    """
    Модель сборника статей:

    .. code-block::

        ArticlesCollectionModel(
            authors="Иванов И.М., Петров С.Н.",
            article_title="Наука как искусство",
            collection_title="Сборник научных трудов",
            city="СПб.",
            publishing_house="АСТ",
            year=2020,
            pages="25-30",
        )
    """

    authors: str
    article_title: str
    collection_title: str
    city: str
    publishing_house: str
    year: int = Field(..., gt=0)
    pages: str


class MagazineArticleModel(BaseModel):

    """
    Модель статьи из журнала:

    .. code-block::

        MagazineArticleModel(
            authors="Иванов И.М., Петров С.Н.",
            article_name="Наука как искусство",
            magazine_name="Образование и наука",
            pub_year="2020",
            magazine_num="10",
            pages="25-30",
        )
    """

    authors: str
    article_name: str
    magazine_name: str
    pub_year: int = Field(..., gt=0)
    magazine_num: int = Field(..., gt=0)
    pages: str


class NewsArticleModel(BaseModel):

    """
    Модель статьи из газеты:

    .. code-block::

        MagazineArticleModel(
            authors="Иванов И.М., Петров С.Н.",
            article_name="Наука как искусство",
            news_name="Южный Урал",
            edition_year="1980",
            news_pub_date="01.10",
            article_num="5",
        )
    """

    authors: str
    article_name: str
    news_name: str
    edition_year: int = Field(..., gt=0)
    news_pub_date: str
    article_num: int = Field(..., gt=0)
