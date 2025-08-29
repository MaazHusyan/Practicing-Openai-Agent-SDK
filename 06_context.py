import asyncio
import time

from agents import Agent, Runner, function_tool, RunContextWrapper
from dataclasses import dataclass

from gemini_model import geminiModel, config


@dataclass
class UserContext:
    userNname: str
    Email: str | None = None
    
@function_tool
async def searchUser(localContext: RunContextWrapper[UserContext], query: str)-> str:
    time.sleep(30)
    return "No User Found Unfortunatily..."

async def specialPrompt(specialContext: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    
    print(f"User Name = {specialContext.context},\n Agent Name = {agent.name}.")
    
    return f"You are a Maths expert. User: {specialContext.context.userName}, {agent.name}. Please assist with math-related queries. "


teacherAgent: Agent = Agent(
    name="Maths Teacher",
    instructions=specialPrompt,
    model=geminiModel,
    tools=[searchUser]
  )

async def main():
    userContext = UserContext(userNname="Kaizen")
    
    while True:
        usrInp = input("Ask Something >>> ")
        
        if usrInp == "stop":
            break
        
        runResult =await Runner.run(
            teacherAgent,
            usrInp,
            run_config=config,
            context=userContext
        )
        print("LLM Output >>>",runResult.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
    
    
   
