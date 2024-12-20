import os
from datetime import timezone, datetime

class BaseConfig:
    DEBUG        = False
    DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/mydatabase")

class DevConfig(BaseConfig):
    DEBUG        = True
    DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/mydatabase")

class ProdConfig(BaseConfig):
    DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/mydatabase")

configs = {
    "prod"   : ProdConfig,
    "dev"    : DevConfig,
    "default": DevConfig
}

# timestamping
def current_unix_ts:
    return int(datetime.now(tz=timezone.utc).timestamp())
