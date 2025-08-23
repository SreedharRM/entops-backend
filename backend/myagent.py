from browser_use.llm import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio
import os

# Load environment variables
load_dotenv()
llm = ChatOpenAI(model="gpt-5", api_key="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")

async def run_agent(task_text: str = None):
    """
    Run the agent with a provided task text.
    If no task_text is passed, it falls back to reading prompt.txt.
    """
    if not task_text:
        # Resolve prompt.txt relative to this file
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROMPT_FILE = os.path.join(BASE_DIR, "prompt.txt")
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            task_text = f.read().strip()

    agent = Agent(task=task_text, llm=llm)
    result = await agent.run()
    return result


# Allow standalone execution for testing
if __name__ == "__main__":
    output = asyncio.run(run_agent())
    print(output)
