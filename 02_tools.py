import asyncio

from agents import Agent, Runner

from gemini_model import geminiModel, config




teacher = Agent(
    name="Teacher Agent",
    instructions=""" You are a skill-full teacher, you provide best way to solve queries. keep answer short and relevent. """,
    model=geminiModel 
)

reasoner = Agent(
    name="Reasons giving Agent",
    instructions=""" You give reasons to user's queries. as user ask. and always ask how many reason on which thing.""",
    model=geminiModel,
    
)

async def main():
    runResult =await Runner.run( #<==== Using .run method
        teacher,
        "Why kiwi bird can't fly ?",
        run_config=config
    )
    print(runResult.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
    
    
   
