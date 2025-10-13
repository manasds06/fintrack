from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root_point():
  return {"message": "Start of API"}