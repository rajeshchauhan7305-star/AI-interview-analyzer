import json
import openai
from app.core.config import settings


def create_openai_client() -> None:
    openai.api_key = settings.OPENAI_API_KEY


def generate_interview_questions(category: str, difficulty: str, count: int = 5) -> list[dict]:
    create_openai_client()
    prompt = (
        f"Generate {count} interview questions for a {category} role at {difficulty} difficulty. "
        "Return only a numbered list of questions, no additional text."
    )
    response = openai.ChatCompletion.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.8,
    )
    content = response.choices[0].message.content
    questions = []
    for line in content.splitlines():
        text = line.strip()
        if not text:
            continue
        if text[0].isdigit():
            cleaned = text.split(".", 1)[-1].strip()
        else:
            cleaned = text
        if cleaned:
            questions.append({"text": cleaned})
        if len(questions) >= count:
            break
    return questions


def analyze_answer(answer: str, question: str) -> dict:
    create_openai_client()
    prompt = (
        "Provide a JSON interview review for the answer below. "
        f"Question: {question}\nAnswer: {answer}\n"
        "Return a JSON object only with keys grammar_score, technical_score, communication_score, confidence_score, "
        "ai_feedback, summary, and recommendation. Scores should be numbers between 0 and 100."
    )
    response = openai.ChatCompletion.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.35,
        max_tokens=450,
    )
    text = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # Attempt to pull JSON object from surrounding content
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                parsed = json.loads(text[start:end+1])
            except json.JSONDecodeError:
                parsed = {}
        else:
            parsed = {}
    return {
        "grammar_score": float(parsed.get("grammar_score", 80.0)),
        "technical_score": float(parsed.get("technical_score", 80.0)),
        "communication_score": float(parsed.get("communication_score", 80.0)),
        "confidence_score": float(parsed.get("confidence_score", 75.0)),
        "ai_feedback": parsed.get("ai_feedback", parsed.get("feedback", text)),
        "summary": parsed.get("summary", "AI analysis generated."),
        "recommendation": parsed.get("recommendation", "Needs Improvement"),
    }


def transcribe_audio(audio_file_path: str) -> str:
    create_openai_client()
    with open(audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(model=settings.WHISPER_MODEL, file=audio_file)
    return transcript.get("text", "")
