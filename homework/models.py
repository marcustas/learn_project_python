from pydantic import BaseModel, validator


class PublicationModel(BaseModel):
    name: str
    author: str
    year_of_publish: int


class BookModel(PublicationModel):
    pass


class MagazineModel(PublicationModel):
    month: int
