from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./travel_planner.db"

    class Config:
        env_file = ".env"