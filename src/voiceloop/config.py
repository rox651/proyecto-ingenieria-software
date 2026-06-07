from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    voiceloop_host: str = "127.0.0.1"
    voiceloop_port: int = 8000
    sample_rate: int = 16000
    channels: int = 1
    whisper_model: str = "tiny"
    tts_voice: str = "es-MX-DaliaNeural"
    vad_energy_threshold: float = 50.0
    vad_silence_ms: int = 700
    chunk_duration_ms: int = 100


settings = Settings()
