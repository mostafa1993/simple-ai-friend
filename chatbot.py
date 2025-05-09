from llm_handler import LLMHandler
from colors import Color
from spinner import Spinner


color = Color()

print(color.cyan("🤖 Welcome to Your Simple AI Assistant!", bold=True))
print(color.yellow("Type 'exit' to end the chat.\n"))

ai_friend = LLMHandler(
    # provider="openai",
    # model="gpt-4o-mini",
    provider="ollama",
    model="gemma2:2b",
    name="Kishmish",
    role="Maltese dog",
)

while True:
    user_input = input(color.blue("You: ", bold=True))
    if user_input.lower() == "exit":
        print(color.cyan("👋 Goodbye!"))
        break

    try:
        with Spinner(color=color):
            reply = ai_friend.generate(user_input)

        print(color.magenta("Assistant: ", bold=True) + reply)
    except Exception as e:
        print(color.red(f"Error: {e}"))
        break
