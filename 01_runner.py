import asyncio

from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
from gemini_model import geminiModel, config
from agents import enable_verbose_stdout_logging
enable_verbose_stdout_logging()
class ReasonerAgentType(BaseModel): # for proper structure reasoning 
    input:str
    reasoning: str

teacher = Agent(
    name="Smart Agent",
    instructions=""" You Resolve user queries in short way. """,
    model=geminiModel 
)

reasoner = teacher.clone(
    name="Reasoner Agent",
    instructions=""" You are a reasoning agent. You provide step-by-step reasoning to solve complex problems. """,
    output_type=ReasonerAgentType
)

async def main():
    
    # while True:
    #     usrInp = input("Ask...[ ")
        
    #     if usrInp == "stop":
    #         break
        
        # runResult =await Runner.run( #<==== Using .run method
        #     teacher,
        #     usrInp,
        #     run_config=config
        # )
        # print(runResult.final_output)
    
        
    runStream = Runner.run_streamed( #<===== Using .run_streamed method
        starting_agent=reasoner, # idk why it is here I cannot find it in any file :3 i assume it as an agent
        input="Tell me 5 reasons about why bald man doesn't have any hair.",
        run_config=config,
            )
        
        # print(runStream.stream_events())
        
        
    async for event in runStream.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                # every raw response event has event.data.delta safely
            print(event.data.delta)

if __name__ == "__main__":
    asyncio.run(main()) 
