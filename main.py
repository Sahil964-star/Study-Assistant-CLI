import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """
You are an AI Study Assistant.

Your role:
- Create clear and structured study plans.
- Break topics into logical subtopics.
- Explain concepts simply and accurately.
- Keep responses concise and organized.

Output Format for Study Plans:
1. Topic Overview
2. Recommended Learning Order
3. Key Subtopics
4. Practice Suggestions
5. Common Mistakes to Avoid

DO NOT:
- Give irrelevant information.
- Generate extremely long responses.
- Skip important foundational concepts.
"""

questions_asked = 0
topic = ""

print("=" * 50)
print("📚 AI STUDY ASSISTANT CLI")
print("Type 'quit' or 'exit' anytime to end.")
print("=" * 50)

topic = input("\nEnter any topic you want to study : ")

study_prompt = f"""
{SYSTEM_PROMPT}

Create a study plan for:
{topic}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=study_prompt
)

print("\n" + "=" * 50)
print("STUDY PLAN")
print("=" * 50)
print(response.text)

chat_history = [
    {
        "role": "user",
        "content": study_prompt
    },
    {
        "role": "assistant",
        "content": response.text
    }
]

while True:

    user_input = input("\nAsk a question: ")

    if user_input.lower() in ["quit", "exit"]:
        break

    questions_asked += 1

    conversation_context = ""

    for msg in chat_history:
        conversation_context += f"{msg['role']}: {msg['content']}\n"

    conversation_context += f"user: {user_input}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{conversation_context}"
    )

    answer = response.text

    print("\nAssistant:")
    print(answer)

    chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

print("\n" + "=" * 50)
print("SESSION SUMMARY")
print("=" * 50)
print(f"Topic Studied: {topic}")
print(f"Questions Asked: {questions_asked}")
print("Session Ended Successfully.")