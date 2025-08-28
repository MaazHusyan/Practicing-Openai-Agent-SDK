import asyncio

from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent

from gemini_model import geminiModel, config




teacher = Agent(
    name="Smart Agent",
    instructions=""" You Resolve user queries in short way. """,
    model=geminiModel 
)

async def main():
    
    while True:
        usrInp = input("Ask...[ ")
        
        if usrInp == "stop":
            break
        
        runResult =await Runner.run( #<==== Using .run method
            teacher,
            usrInp,
            run_config=config
        )
        print(runResult.final_output)
    
        
        # runStream = Runner.run_streamed( #<===== Using .run_streamed method
        #     reasoner, 
        #     input="Tell me 5 reasons about why bald man doesn't have any hair.",
        #     run_config=config,
            
        #     )
        
        # print(runStream.stream_events())
        
        
        # async for event in runStream.stream_events():
        #     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        #         # every raw response event has event.data.delta safely
        #         print(event.data.delta)
        #         print(event.data.logprobs)

if __name__ == "__main__":
    asyncio.run(main())
    
    
   
