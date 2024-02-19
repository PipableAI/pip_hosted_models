from fastapi import FastAPI, Form, HTTPException
import torch

from transformers import pipeline

# Instantiate the pipeline with CUDA support
a_pipeline = pipeline(
    "text-generation",
    model="Nexusflow/NexusRaven-V2-13B",
    torch_dtype="auto",
    device_map="auto",
)

app = FastAPI()


@app.post("/raven")
async def register_user(prompt: str = Form(...)):
    try:
        print("Raven processing ....")
        res = raven_prompt(prompt)
        torch.cuda.empty_cache()
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def raven_prompt(prompt: str):
    global a_pipeline

    # Custom stopping criterion
    stop_tokens = ["\nThought:"]

    generated_text = ""
    while True:
        # Generate text in chunks
        chunk = (
            a_pipeline(
                prompt,
                max_new_tokens=50,  # Generate text in chunks
                do_sample=False,
                temperature=0.001,
                return_full_text=False,
            )[0]["generated_text"]
            .replace("Call:", "")
            .strip()
        )
        generated_text += chunk

        # Check if any stop token is present in the generated text
        if any(stop_token in generated_text for stop_token in stop_tokens):
            break

    torch.cuda.synchronize()
    generated_text = generated_text.split(" \nThought:")[0]
    print(generated_text)
    return generated_text
