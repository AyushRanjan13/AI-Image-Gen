from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.model_loader import load_model
from fastapi.responses import Response
from io import BytesIO
import numpy as np
import torch

app = FastAPI()

pipe = None

class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: str | None = None


@app.on_event("startup")
def startup_event():
    global pipe
    pipe = load_model()


@app.post("/generate")
def generate_image(req: GenerateRequest):
    global pipe

    if pipe is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # CPU-safe generator
    generator = torch.Generator().manual_seed(42)

    print("Starting image generation...")

    image = pipe(
        prompt=req.prompt,
        negative_prompt=req.negative_prompt,
        num_inference_steps=15,
        guidance_scale=7.5,
        height=512,
        width=512,
        generator=generator
    ).images[0]

    print("Image generation finished")

    img_np = np.array(image)

    if np.isnan(img_np).any():
        raise HTTPException(
            status_code=500,
            detail="Generated image contained NaN values"
        )

    if img_np.mean() < 1:
        raise HTTPException(
            status_code=500,
            detail="Generated image is invalid (nearly black)"
        )

    buf = BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    return Response(content=buf.read(), media_type="image/png")
