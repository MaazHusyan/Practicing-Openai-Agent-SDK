from agents import Agent, Runner, SQLiteSession, function_tool, ModelSettings

# from pydantic import BaseModel
import asyncio

from gemini_model import geminiModel, config


@function_tool
def tellAge(age: int):
    """Return User Age from chat"""
    return {"age": age}

@function_tool
def tellName(name: str):
    """Return User name from chat"""
    return {"name": name}

# class getStructuredOutput(BaseModel):
#     name: str |None = None
#     age: str |None = None


myAgent = Agent(
name="assistant",
model=geminiModel,
instructions="""You are a help full assistant. Use tools to get information""",
tools=[tellAge, tellName],
tool_use_behavior="stop_on_first_tool",
model_settings=ModelSettings(tool_choice="required"),
# output_type=getStructuredOutput
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
        max_turns=10,
        
        )
                
        print(result.final_output)
        
if __name__ == "__main__":
    asyncio.run(runner())