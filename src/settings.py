'''Global settings module'''
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    '''Global settings class'''
    POSTGRES_DRIVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    @property
    def database_url(self) -> str:
        '''Create url for database connection'''
        return (
            f'{self.POSTGRES_DRIVER}://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}/{self.POSTGRES_DB}'
        )

    model_config = ConfigDict(env_file='.env', extra='ignore')


settings = Settings()
