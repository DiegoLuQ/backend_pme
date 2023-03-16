from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.api.base import router as router_base
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(router_base)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422, content={"detail":"the data sent is not valid"}
    )

@app.get('/')
def Home():
    return {"pme":"2023"}