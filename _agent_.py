import asyncio

from agents import Agent, Runner, enable_verbose_stdout_logging

from gemini_model import geminiModel, config

enable_verbose_stdout_logging()

agent = Agent(
    name="Master Agent",
    instructions="""  """,
    model=geminiModel,
  )

async def main():
    
    while True:
        usrInp = input("Ask Something >>> ")
        
        if usrInp == "stop":
            break
        
        runResult =await Runner.run(
            agent,
            usrInp,
            run_config=config
        )
        print("LLM Output >>>",runResult.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
    
    
   
