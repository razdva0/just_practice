from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Main(BaseModel):
    secret_key: str


class DataBase(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str


class JWT(BaseModel):
    algorithm: str
    access_ttl: int


class Settings(BaseSettings):
    main: Main
    db: DataBase
    jwt: JWT

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        case_sensitive = True


CONFIG = Settings()
