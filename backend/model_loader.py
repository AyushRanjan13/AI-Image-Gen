import torch
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler

pipe = None

def load_model():
    global pipe

    if pipe is not None:
        return pipe

    device = "cpu"

    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float32,   # CPU must be fp32
        safety_checker=None
    )

    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
        pipe.scheduler.config
    )

    pipe = pipe.to(device)
    pipe.enable_attention_slicing()

    print("Model loaded on cpu (forced)")
    return pipe
