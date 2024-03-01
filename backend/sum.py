from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import matplotlib.pyplot as plt
import io
import base64
import cmath
import numpy as np

app = FastAPI()

origins = [
    "http://localhost:3000"
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
    return {"message": "Welcome to the Fourier transform lab."}

@app.post("/plot")
async def generate_plot(inp: graph_input):
    fig, (ax, bx) = plt.subplots(1, 2)

    arrow_properties = dict(
        facecolor='black', edgecolor='black', linewidth=0.005, width=0.05, head_width=0.2, head_length=0.2
    )
    l = dict(facecolor='black', edgecolor='black', linewidth=0.005, width=0.05, head_width=0, head_length=0)

    t = {}
    signals = [[1, 2, 0]]
    m = signals[0][1]
    for i in signals:
        a = i[0]
        w = i[1]
        phi = i[2]
        if w not in t:
            t[w] = 0
            t[-1 * w] = 0
        t[w] += a * np.exp(1j * phi) / (2j)
        t[-1 * w] += a * np.exp(-1j * phi) / (-2j)

    for i in t:
        ax.arrow(i, 0, 0, np.abs(t[i]), **arrow_properties)
        bx.arrow(i, 0, 0, cmath.phase(t[i]), **l)

    ax.set_title("Magnitude")
    bx.set_title("Phase")

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    bx.set_ylim(-1 * np.pi, np.pi)
    bx.set_xlim(-5, 5)

    ax.axhline(0, color='grey', linewidth=0.8)
    ax.axvline(0, color='grey', linewidth=0.8)
    bx.axhline(0, color='grey', linewidth=0.8)
    bx.axvline(0, color='grey', linewidth=0.8)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_base64 = base64.b64encode(img.getvalue()).decode()

    plt.close()

    return {"plot_base64": plot_base64}
