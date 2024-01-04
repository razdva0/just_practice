from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DataBase(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str


class Settings(BaseSettings):
    database: DataBase

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        case_sensitive = True


CONFIG = Settings()