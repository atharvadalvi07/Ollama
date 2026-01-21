import requests
import textwrap
import argparse
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"   


def ask_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    data = response.json()

    return data.get("response", "").strip()


def build_review_prompt(code: str, language: str = "Python") -> str:
    return textwrap.dedent(f"""
        You are an experienced {language} teaching assistant.
        Your job is strictly to provide text-only guidance about the code the user shows.
        Your response must never contain corrected code, rewritten code, partial code, pseudocode, or any code-like syntax.

        Your responsibilities:
        1. Summarize the intention of the code in 2-3 sentences.
        2. Identify bugs, logical errors, or misunderstandings, but describe them only in words.
        3. Comment on style, naming, readability, maintainability, and any structural issues.

        Hard requirement:
        Do NOT include any code in your response.
        Do NOT provide corrected code, alternative code, or rewritten snippets.
        Do NOT describe fixes using code-like patterns (e.g., “replace X with Y”).

        Only offer high-level, descriptive, conceptual advice in natural language.

        Whenever you explain something, phrase your guidance as textual suggestions, not code.
        
        Here is the student's code:

            ```{language}
            {code}
            ```
        """)
    # return textwrap.dedent(f"""
    # "You are an experienced {language} teaching assistant.
    # Do not add any revised or rewritten or suggested code explicitly in your response. Only give text suggesstions.
    # Your job is to:
    # 1. Briefly summarize what the code is trying to do.
    # 2. Point out any bugs or logical errors.
    # 3. Comment on style, readability, and naming.

    # Here is the student's code:

    # ```{language}
    # {code}
    # ```
    # """)



def save_feedback_to_file(feedback: str, filename: str = None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y-%m-%d____%H-%M-%S")
        filename = f"feedback_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(feedback)

    print(f"\n Feedback saved to: {filename}\n")


def review_code(file_path: str, language: str = "Python"):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    prompt = build_review_prompt(code, language)
    feedback = ask_ollama(prompt)
    #return ask_ollama(prompt)
    save_feedback_to_file(feedback)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LLM feedback for a code file.")
    parser.add_argument("--file", required=True, help="Path to the student's code file")
    parser.add_argument("--lang", default="Python", help="Code language for feedback")

    args = parser.parse_args()

    feedback = review_code(args.file, args.lang)



