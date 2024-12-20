from fastapi import FastAPI
from views.v1.users import router as users_router
from config import configs

app = FastAPI()

config = configs[os.getenv("ENV", "default")]

app.include_router(users_router, prefix="/v1/users")
