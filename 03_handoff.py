import asyncio
import random

from agents import Agent, Runner, handoffs

from gemini_model import geminiModel, config


smartAgent = Agent(
    name="Smart Agent",
    instructions=""" You Resolve user queries in short way.
    use tool "randomFacts" if user ask about facts about any thing. """,
    model=geminiModel,
    handoffs=handoffs(
        
    )
)

async def main():
    
    while True:
        usrInp = input("Ask Something >>> ")
        
        if usrInp == "stop":
            break
        
        runResult =await Runner.run( #<==== Using .run method
            smartAgent,
            usrInp,
            run_config=config
        )
        print("LLM Output >>>",runResult.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
    
    
   
