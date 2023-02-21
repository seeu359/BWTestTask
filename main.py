from fastapi import FastAPI
from api.routes import router
import uvicorn


app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
