from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import numpy as np
from pydantic import BaseModel
import matplotlib.pyplot as plt
import io
import base64


app = FastAPI()

origins = [
    "http://localhost:5173"
]
class graph_input(BaseModel):
    text: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to the fouier transform lab."}

@app.post("/plot")
async def generate_plot(inp:graph_input):
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]

    plt.plot(x, y)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sample Plot')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plt.close()

    return StreamingResponse(io.BytesIO(img.getvalue()), media_type="image/png")