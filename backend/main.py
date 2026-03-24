from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import reg,login,loan,verify

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
)

# include routers
app.include_router(reg.router)
app.include_router(verify.router)
app.include_router(login.router)
app.include_router(loan.router)



@app.get("/")
def root():
    return {"message": "API running"}