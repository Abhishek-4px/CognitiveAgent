from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import AnyUrl
class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    PINECONE_API_KEY: str
    DATABASE_URL:str
    REDIS_URL: str                   #AnyUrl: strictly for https,mysql,postgres links
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()                #type: ignore

