from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()

_pipline = None


@app.post("/raven")
async def register_user(prompt: str = Form(...)):
    try:
        print("Raven processing ....")
        return raven_prompt(prompt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def raven_prompt(prompt: str):
    global _pipeline
    if _pipeline is None:

        from transformers import pipeline

        _pipeline = pipeline(
            "text-generation",
            model="Nexusflow/NexusRaven-V2-13B",
            torch_dtype="auto",
            device_map="auto",
        )
    result = (
        _pipeline(
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
