import asyncio
import random

from agents import Agent, Runner, handoffs

from gemini_model import geminiModel, config


boyAgent = Agent(
    name="Boy Agent",
    instructions="""you always reply to boy, use lots of emojis like [😡🤬💀👺👹👿😈] in response.
    don't use [😻🥰😘😍❤💕💖💋]""",
    model=geminiModel
)

girlAgent = Agent(
    name="Girl Agent",
    instructions="""you always reply to girl, use lots of emojis like [😻🥰😘😍❤💕💖💋] in response.
    don't use  [😡🤬💀👺👹👿😈] """,
    model=geminiModel
)

masterAgent = Agent(
    name="Master Agent",
    instructions=""" You are a Master agent you have two sub agent (girlAgent, boyAgent). 
    You can use them upon user request.
    Always ask users gender first then handoff the relevent agent for batter results.""",
    model=geminiModel,
    handoffs=[boyAgent, girlAgent]
)

async def main():
    
    while True:
        usrInp = input("Ask Something >>> ")
        
        if usrInp == "stop":
            break
        
        runResult =await Runner.run( #<==== Using .run method
            masterAgent,
            usrInp,
            run_config=config
        )
        print("LLM Output >>>",runResult.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
    
    
   
