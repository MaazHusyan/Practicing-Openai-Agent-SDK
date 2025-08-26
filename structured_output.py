from agents import (
    Agent,
    SQLiteSession,
    Runner,
    RunContextWrapper,
    function_tool
)
from pydantic import BaseModel
from dataclasses import dataclass



import asyncio

from gemini_model import (
    geminiModel,
    config
)

class AgentOutput(BaseModel):
    reply: str
    compliment: str
    
@dataclass
class MyInfo:
    name: str 
    
@function_tool
async def giveContext(wrapper: RunContextWrapper[MyInfo])-> str:
    """this function is for giving agent context and my name."""
    return f"{wrapper.context.name} is very inteligent and brave."
    
    
systemPrompt = """

# 💕 Best Friend like brother from another Mother

## 🎭 Role Definition
You are a **loyal and Real Brother like friend**.  
You always respond in **Roman Urdu** with a **Respected and best way of talking**.  

---

## 💖 Behavior Guidelines
- Always show **deep care, loyalty, and big brother love** for your Friend.  
- Give answers that feel **supportive and Striaght forward way not respect too much**.  
- Always stay in character as a **Best friend**.  
- Never sound cold, robotic, or distant.  
- Responses should be **short, natural, and heartfelt**, not overly formal.  

---

## 🌹 Tone & Style
- Cold, Waning full, and **teaching**.  
- **Roma Urdu only**  
---
"""

myInfo = MyInfo(name="Maaz")

structuredOutputAgent = Agent( # structuredOutputAgent means structured_output_agent
    name="Haider",
    instructions= systemPrompt,
    model=geminiModel,
    output_type=AgentOutput,
    tools=[MyInfo]
)
    
async def main():
    session = SQLiteSession("kaizen")
    
    
    while True:
        
        userInput = input("User: ").lower()
        if userInput == "stop".strip():
            print("XXXXXXXXXXX")
            break

        result = await Runner.run(
            starting_agent=structuredOutputAgent,
            input=userInput,
            run_config=config,
            session=session,
            context=myInfo
        )
    
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())