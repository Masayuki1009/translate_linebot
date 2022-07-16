from fastapi import FastAPI, APIRouter


app = FastAPI(id="first fastAPI server", openapi_url="/openapi.json")
api_router = APIRouter()

@api_router.get(path="/")
def hello():
          print("hello")
          return "hello"

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=5555, log_level="debug")
