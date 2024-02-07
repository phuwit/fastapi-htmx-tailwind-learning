import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import Settings
from app.routes import router

settings = Settings()


def get_app() -> FastAPI:
    """Create a FastAPI app with the specified settings."""

    app = FastAPI(**settings.fastapi_kwargs)

    app.include_router(router)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for FastAPI app. It will run all code before `yield`
    on app startup, and will run code after `yeld` on app shutdown.
    """

    try:
        subprocess.run([
            "tailwindcss",
            "-i",
            settings.STATIC_DIR + '/src/tailwind.css',
            "-o",
            settings.STATIC_DIR + '/css/main.css',
            "--minify"
        ])
    except Exception as e:
        print(f"Error running tailwindcss: {e}")

    yield

app = FastAPI(lifespan=get_app())

app.mount('/static', StaticFiles(directory=settings.STATIC_DIR))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)