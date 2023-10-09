from pydantic import BaseModel


class PublicationModel(BaseModel):
    title: str
    author: str
    year: int


class BookModel(PublicationModel):
    pass


class MagazineModel(BookModel):
    month: int
