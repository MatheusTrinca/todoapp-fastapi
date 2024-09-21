from fastapi import FastAPI
import models
from database import engine
from router import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'Status': 'Healthy'}


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(todos.router)
