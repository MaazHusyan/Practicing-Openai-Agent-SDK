import asyncio
from dataclasses import dataclass

from agents import Agent, Runner, RunContextWrapper, function_tool, ModelSettings
from pydantic import BaseModel

from gemini_model import geminiModel, config


@dataclass   #<===== data class
class bestAnswer:
    answer: str
    reason: str
    quick_note: str


@function_tool
def getBestAnswer(wrapper: RunContextWrapper[bestAnswer])-> str:
    """this function get best posible answer.format output structure vertically"""
    return{
        f""" 
        The Answer is {wrapper.context.answer}\n
        The Reson is {wrapper.context.reason}
        Quick Note: {wrapper.context.quick_note}
        """
    }
    

teacher = Agent(
    name="Teacher Agent",
    # instructions=""" You are a skill-full teacher, you provide best way to solve queries. keep answer short and relevent. """,
    model=geminiModel,
    tools=[getBestAnswer],
    model_settings=ModelSettings(tool_choice="required"),
    # model_settings=ModelSettings(stop)
    tool_use_behavior=""
    # tool_use_behavior=""
    
)

async def main():
    context = bestAnswer(answer="kiwi has no wings", reason="it has legs instead", quick_note="what do you want ?")
    
    result =await Runner.run(
        teacher,
        "Why kiwi bird can't fly ?",
        run_config=config,
        context=context
    )
    
    
    print("User Input: ", result.input)
    print("=============================")
    print("LLM output: ", result.final_output)
    # print(result.new_items)
    # print("=============================")
    # print(result.raw_responses)
    # print("=============================")
    # print(result.input)

    
if __name__ == "__main__":
    asyncio.run(main())