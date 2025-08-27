import asyncio
from agents import Agent, Runner
from gemini_model import geminiModel, config


def quickAgent(agent_name=None, agent_instructions=None):
    """
    Create a quick interactive agent loop.
    Can be imported and run from any file.
    """

    anAgent = Agent(
        name=agent_name,
        instructions=agent_instructions,
        model=geminiModel
    )

    async def main():
        while True:
            userInp = input("Ask Something: ")
            if userInp.lower() in {"exit", "quit"}:
                print("Exiting agent...")
                break

            runResult = await Runner.run(
                anAgent,
                userInp,
                run_config=config
            )
            print("🤖:", runResult.final_output)

    asyncio.run(main())
