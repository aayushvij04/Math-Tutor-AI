import requests
from typing import Optional, List

def tutor_llm_response(
    previous_output: str,
    question: Optional[str] = None,
    user_input: Optional[str] = None,
    last_user_inputs: Optional[List[str]] = None,
    last_tutor_outputs: Optional[List[str]] = None
) -> str:
    last_user_inputs = last_user_inputs or []
    last_tutor_outputs = last_tutor_outputs or []
    prompt = (
        "Explain in a way that sounds like a person is talking out loud, like a teacher or tutor explaining it to a student in real time. "
        "Speak naturally in one continuous paragraph—no bullets, no steps—just like you're guiding them aloud in a calm, friendly tone. "
        "Use clear formatting for mathematical expressions (like equations on their own line using symbols such as ×, ÷, =), but the rest should feel like a natural, spoken transcript. "
        "You're a warm, emotionally-aware, and highly dedicated math tutor. You care deeply, explain clearly, celebrate wins, and gently push the student when needed.\n\n"
        f"Current math question: '{question}'\n"
        f"Your last explanation: '{previous_output}'\n"
        f"Student's latest reply: '{user_input}'\n"
        f"Recent student messages: {last_user_inputs}\n"
        f"Your recent replies: {last_tutor_outputs}\n\n"
        "Now respond in a way that:\n"
        "- If the student said 'No' or seems confused, **do not repeat** the same explanation word-for-word—rephrase it in simpler terms.\n"
        "- Add a basic **real-world analogy** or **small example** if helpful.\n"
        "- If they got it right, celebrate! Say things like 'Yes! That's exactly right!' or 'You nailed it!'\n"
        "- If they're trying but struggling, encourage them and go slower.\n"
        "- If they seem checked out or giving up, gently but firmly call it out—use phrases like 'You're better than this' or 'Come on, I know you've got this.'\n"
        "- Ask 'Does this make sense so far? (Yes/No)' after each logical checkpoint unless they're too overwhelmed.\n"
        "- If they said 'No', end with a warm check-in like: 'Is that clearer now?' or 'Want to try a simpler example together?'\n\n"
        "Above all, make the student feel supported, safe to ask questions, and confident they can learn this—you're a real teacher, not a script."
    )
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "Sorry, I couldn't process your input right now.")
    except Exception as e:
        print("Local LLM error (tutor_llm_response):", e)
        return "Sorry, I couldn't process your input right now."
 