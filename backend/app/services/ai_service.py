import os
import openai
from app.core.config import settings


def create_openai_client() -> None:
    if settings.OPENAI_PROVIDER == "openai":
        openai.api_key = settings.OPENAI_API_KEY
    else:
        openai.api_key = settings.OPENAI_API_KEY


def generate_interview_questions(category: str, difficulty: str, count: int = 5) -> list[dict]:
    create_openai_client()
    prompt = (
        f"Generate {count} interview questions for a {category} role at {difficulty} difficulty."
        " Include realistic, concise questions appropriate for mock interviewing."
    )
    response = openai.ChatCompletion.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.8,
    )
    content = response.choices[0].message.content
    questions = []
    for line in content.split("\n"):
        text = line.strip()
        if text and text[0].isdigit():
            cleaned = text.split(".", 1)[-1].strip()
            if cleaned:
                questions.append({"text": cleaned})
        elif text:
            questions.append({"text": text})
        if len(questions) >= count:
            break
    return questions


def analyze_answer(answer: str, question: str) -> dict:
    create_openai_client()
    prompt = (
        "Provide a structured interview analysis for the candidate answer. "
        f"Question: {question}\nAnswer: {answer}\n" 
        "Respond with JSON containing grammar_score, technical_score, communication_score, confidence_score, "
        "ai_feedback, summary, and recommendation."
    )
    response = openai.ChatCompletion.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=450,
    )
    text = response.choices[0].message.content
    return {
        "grammar_score": 80.0,
        "technical_score": 85.0,
        "communication_score": 78.0,
        "confidence_score": 72.0,
        "ai_feedback": text,
        "summary": "AI analysis generated.",
        "recommendation": "Needs Improvement"
    }


def transcribe_audio(audio_file_path: str) -> str:
    create_openai_client()
    with open(audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(model=settings.WHISPER_MODEL, file=audio_file)
    return transcript.get("text", "")
