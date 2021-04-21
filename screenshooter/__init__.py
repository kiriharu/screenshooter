import uvicorn

from screenshooter.app import app


if __name__ == "__main__":
    uvicorn.run(app)
