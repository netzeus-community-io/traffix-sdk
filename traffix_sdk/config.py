from pydantic import BaseSettings, RedisDsn, MongoDsn, PostgresDsn


class Settings(BaseSettings):
    # Default redis Dsn
    REDIS_URI: RedisDsn = "redis://localhost:6379"

    # Default PostGREs URI
    CORE_DATABASE_URI: PostgresDsn = (
        "postgresql+asyncpg://postgres:traffix@localhost:5432/traffix"
    )

    # Default MongoDB Dsn
    MONGODB_URI: MongoDsn = "mongodb://localhost:27017"

    # Default MongoDB Database
    MONGODB_DATABASE: str = "traffix-dev"

    # Max characters for the image URL to load for a release/update
    MAX_IMAGE_URL_LENGTH: int = 128

    # Default API Key Header name
    API_KEY_HEADER: str = "traffix-api-key"

    # JWT Shared Secret used to Encode/Decode access tokens
    JWT_SHARED_SECRET: str = "change-me-please-42069!"

    # Default JWT Algorithm
    JWT_ALGORITHM: str = "HS256"

    # Access Token expiration time
    # 60 seconds * 24 hours * 3 days = 3 days
    ACCESS_TOKEN_EXPIRE: int = 60 * 24 * 3


settings = Settings()
