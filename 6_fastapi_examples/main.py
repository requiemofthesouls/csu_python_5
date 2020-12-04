from fastapi import FastAPI
import uvicorn


def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def better_fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/fib/{n}")
async def compute_fib(n: int):
    return {"result": fib(n)}


@app.get("/better_fib/{n}")
async def compute_better_fib(n: int):
    return {"result": better_fib(n)}


uvicorn.run(app)
