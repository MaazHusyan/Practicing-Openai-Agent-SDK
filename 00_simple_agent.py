import asyncio

from agents import Agent, Runner, RunContextWrapper

from gemini_model import geminiModel, config



def run_context(ctx:RunContextWrapper, agent:Agent):
    print(ctx.context, "\n")
    print(agent)
    return "you are a help full assistant"


masterAgent = Agent(
    name="Master Agent",
    instructions=run_context,
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
    
    
   
