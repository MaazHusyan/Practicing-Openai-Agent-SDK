import asyncio

from agents import Agent, Runner
from dataclasses import dataclass

from gemini_model import geminiModel, config


@dataclass
class myContext:
    isResponseGood: bool


masterAgent = Agent(
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
            masterAgent,
            usrInp,
            run_config=config
        )
        print("LLM Output >>>",runResult.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
    
    
   
