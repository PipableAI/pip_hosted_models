from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import PlainTextResponse
import torch

from transformers import pipeline

# Instantiate the pipeline with CUDA support
a_pipeline = pipeline(
    "text-generation",
    model="Nexusflow/NexusRaven-V2-13B",
    torch_dtype=torch.float16,  # Set the dtype to float16 for CUDA support
    device=0 if torch.cuda.is_available() else -1,  # Use CUDA if available
)

app = FastAPI()


@app.post("/raven")
async def register_user(prompt: str = Form(...)):
    try:
        print("Raven processing ....")
        res = await raven_prompt(prompt)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def raven_prompt(prompt: str):
    with torch.cuda.amp.autocast():  # Automatic mixed precision
        result = (
            a_pipeline(
                prompt,
                max_new_tokens=2000,
                do_sample=False,
                temperature=0.001,
                return_full_text=False,
            )[0]["generated_text"]
            .replace("Call:", "")
            .strip()
        )
    print(result)
    return result
