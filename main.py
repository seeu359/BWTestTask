import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from api.routes.operations import operations_router
from api.routes.users import users_router

app = FastAPI()


@app.exception_handler(ValidationError)
async def value_error_exception_handler(
        request: Request,
        exc: ValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=exc.errors(),
    )

app.include_router(users_router)
app.include_router(operations_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
