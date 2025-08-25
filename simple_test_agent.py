from agents import Agent, Runner, SQLiteSession, function_tool, ModelSettings

from typing import Optional
from pydantic import BaseModel, Field
import asyncio

from gemini_model import geminiModel, config

@function_tool
def tellName(name: str):
    """Return User name from chat"""
    return {"name": name}

@function_tool
def tellAge(age: int):
    """Return User Age from chat"""
    return {"age": age}

class getStructuredOutput(BaseModel):
    name: Optional[str] = Field(default=None, description="The user's name")
    age: Optional[int] = Field(default=None, description="The user's age in years")



myAgent = Agent(
name="assistant",
model=geminiModel,
instructions="""You are a help full assistant. Use tools to get information""",
tools=[tellName, tellAge],
model_settings=ModelSettings(tool_choice="auto"),
output_type=getStructuredOutput
)

async def runner():
    session = SQLiteSession("Kaizen", "chat.db")
    
    while True:
        userInput = input("User: ").strip()
    
        if userInput.lower() == "stop":
            print("=======================")
            break
            
            
        result = await Runner.run(
        starting_agent=myAgent,
        input=userInput,
        session=session,
        run_config=config,
        max_turns=10
        )
                
        print(result.final_output)
        
if __name__ == "__main__":
    asyncio.run(runner())