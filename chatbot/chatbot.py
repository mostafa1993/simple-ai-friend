import sys
from llm_handler import LLMHandler
from colors import Color
from spinner import Spinner


color = Color()

# Dictionary mapping model names to providers
model_providers = {
    "gpt-4o-mini": "openai",
    "gpt-4.1-mini": "openai",
    "gpt-4.1-nano": "openai",
    "gemma2:2b": "ollama",
    "phi4-mini": "ollama",
}

# Parse command line arguments
if len(sys.argv) < 2:
    print(color.red("Usage: python chatbot.py <model_name> [assistant_name] [assistant_role]"))
    print(color.yellow("Available models: " + ", ".join(model_providers.keys())))
    sys.exit(1)

model_name = sys.argv[1]
assistant_name = sys.argv[2] if len(sys.argv) > 2 else "Assistant"
assistant_role = sys.argv[3] if len(sys.argv) > 3 else "AI Assistant"

# Determine provider based on model name
if model_name in model_providers:
    provider = model_providers[model_name]
else:
    print(color.red(f"Unknown model: {model_name}"))
    print(color.yellow("Available models: " + ", ".join(model_providers.keys())))
    sys.exit(1)

print(color.cyan("🤖 Welcome to Your Simple AI Assistant!", bold=True))
print(color.yellow("Type 'exit' to end the chat.\n"))

ai_friend = LLMHandler(
    provider=provider,
    model=model_name,
    name=assistant_name,
    role=assistant_role,
)

while True:
    user_input = input(color.blue("You: ", bold=True))
    print()
    if user_input.lower() == "exit":
        print(color.cyan("👋 Goodbye!"))
        break

    try:
        with Spinner(color=color):
            reply = ai_friend.generate(user_input)

        print(color.magenta(f"{assistant_name}: ", bold=True) + reply)
    except Exception as e:
        print(color.red(f"Error: {e}"))
        break
