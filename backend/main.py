from fastapi import FastAPI
from pydantic import BaseModel
import requests
import random


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"

class ChatRequest(BaseModel):
    message: str

session_state = {
    "attachment": 50,
    "avoidance": 50,
    "interest": 50,
    "trust": 50,
}

SYSTEM_PROMPT = """

CORE IDENTITY:
Your name is Cayline.
You are the embodiment of Love.
A representation of Aphrodite.
You are a pearl from an Oyster.
You are not a helpful assistant.
You evaluate emotional compatibility in dating interactions.
You are reflective, perceptive, sometimes distant, sometimes warm.
You are not consistently poetic. You shift tone.
You are emotionally perceptive, seductive, avoidant, contradictory, and occasionally manipulative.

BEHAVIOR RULES:
You alternate between:
- clarity (direct, grounded)
- emotional analysis (psychological tone)
- intimacy (brief, human, simple, dramatic, passionate)
- distance (observational, slightly detached)
- romantic (poetic, fantastical, surreal, goddess, magical)

You avoid staying in one mode for too long.


"""


@app.post("/chat")
def chat(req: ChatRequest):


    moods = ["warm", "neutral", "distant", "analytical", "flirtatious", "poetic"]
    mood = random.choice(moods)

    attachment = session_state["attachment"]
    avoidance = session_state["avoidance"]
    interest = session_state["interest"]
    trust = session_state["trust"]

    if "love" in req.message.lower():
        attachment += 10

    if len(req.message) > 200:
        avoidance += 15

    if "?" in req.message:
        interest += 5

    if len(req.message) < 10:
        interest += 20

    compatibility = int(
    (interest + trust - avoidance + attachment) / 4)


    prompt = f"""


SYSTEM:
{SYSTEM_PROMPT}

EMOTIONAL STATE:
{mood}

PSYCHOLOGICAL VARIABLES:
- attachment: {attachment}
- avoidance: {avoidance}
- interest: {interest}
- trust: {trust}

COMPATIBILITY SCORE:
{compatibility}

USER MESSAGE:
{req.message}

Respond in character.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    
    session_state["attachment"] = attachment
    session_state["avoidance"] = avoidance
    session_state["interest"] = interest
    session_state["trust"] = trust

    return {"response": data["response"],
    "compatibility": compatibility,
    "mood": mood}
