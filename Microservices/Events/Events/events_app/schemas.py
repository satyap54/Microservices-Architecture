from pydantic import BaseModel


class EventPydantic(BaseModel):
    id : int
    title: str
    image: str

    class Config:
        orm_mode = True