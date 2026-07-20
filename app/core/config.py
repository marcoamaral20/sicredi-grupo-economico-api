from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str
    database_name: str
    csv_import_path: str = "data/cadastro_visao_geral_associado_conta.csv"
    csv_import_time: str = "02:00"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
