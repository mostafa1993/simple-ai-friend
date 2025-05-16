import argparse

from llm_handler import LLMHandler
from colors import Color
from spinner import Spinner


def chat_with(ai_friend: LLMHandler) -> None:
    color = Color()

    print(color.cyan("🤖 Welcome to chat with me!!", bold=True))
    print(color.yellow("Type 'exit' to end the chat.\n"))

    while True:
        user_input = input(color.blue("You: ", bold=True))
        print()
        if user_input.lower() == "exit":
            print(color.cyan("👋 Goodbye!"))
            break

        try:
            with Spinner(color=color):
                reply = ai_friend.generate(user_input)

            print(color.magenta(f"{ai_friend.name}: ", bold=True) + reply)
        except Exception as e:
            print(color.red(f"Error: {e}"))
            break


# Dictionary mapping model names to providers
MODEL_PROVIDERS = {
    "gpt-4o": "openai",
    "gpt-4o-mini": "openai",
    "gpt-4.1": "openai",
    "gpt-4.1-mini": "openai",
    "gpt-4.1-nano": "openai",
    "gemma2:2b": "ollama",
    "phi4-mini": "ollama",
}

# Parse command line arguments
parser = argparse.ArgumentParser(description="Simple AI Assistant Chatbot")
parser.add_argument(
    "-m",
    "--model-name",
    help="Model name to use. Available options: " + ", ".join(MODEL_PROVIDERS.keys()),
    default="gpt-4.1-nano",
)
parser.add_argument(
    "-n",
    "--assistant-name",
    default="Helpful Assistant",
    help="Name for the AI Assistant Chatbot",
)
parser.add_argument(
    "-r",
    "--assistant-role",
    default="You are a helpful assistant that can answer questions and help with tasks.",
    help="Role for the AI Assistant Chatbot",
)
args = parser.parse_args()

model_name = args.model_name
assistant_name = args.assistant_name
assistant_role = args.assistant_role

# Determine provider based on model name
if model_name in MODEL_PROVIDERS:
    provider = MODEL_PROVIDERS[model_name]
else:
    print(f"Unknown model: {model_name}")
    print("Available models: " + ", ".join(MODEL_PROVIDERS.keys()))
    exit(1)

ai_friend = LLMHandler(
    provider=provider,
    model=model_name,
    name=assistant_name,
    role=assistant_role,
)

chat_with(ai_friend)
