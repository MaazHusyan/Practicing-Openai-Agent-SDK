import asyncio
from agents import Agent, Runner, RunContextWrapper,function_tool
from gemini_model import geminiModel, config


def quickAgent(agent_name=None, agent_instructions=None):
    """
    Create a quick interactive agent loop.
    Can be imported and run from any file.
    """
    # @function_tool
    def run_context(cts:RunContextWrapper, agent):
        print(cts)
        return "you are a help full assistant"

    anAgent = Agent(
        name=agent_name,
        instructions=run_context,
        model=geminiModel,
        # tool=[run_context]
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
