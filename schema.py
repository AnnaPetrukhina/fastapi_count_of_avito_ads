from pydantic import BaseModel
from pydantic import Field


class Params(BaseModel):
    region: str = Field(..., title="Region", description="Search region", max_length=50,
                        regex=r"\b[а-яА-ЯёЁ]+[-\s]?[а-яА-ЯёЁ]*[-\s]?[а-яА-ЯёЁ]*\b")
    query: str = Field(..., title="Query", description="Query text", max_length=50)

    class Config:
        orm_mode = True


class Counter(BaseModel):
    timestamp: str = Field(..., title="Timestamp", description="Counter timestamp", max_length=50)
    count: int = Field(..., title="Counts", description="Count of ads")

    class Config:
        orm_mode = True
