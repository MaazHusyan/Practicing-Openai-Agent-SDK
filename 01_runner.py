import asyncio

from agents import Agent, Runner
from agents.stream_events import RawResponsesStreamEvent
from openai.types.responses import response_text_delta_event

from gemini_model import geminiModel, config

   
joker = Agent(
    name="Funny Agent",
    instructions="""  """,
    model=geminiModel
)
async def stream():
    while True:
        usrInp = input("Ask>>> ")   
        if usrInp == "stop":
            break
            
        streamResult = Runner.run_streamed(
            joker,
            usrInp,
            run_config=config
        )        
        
        async for event in streamResult.stream_events():
            print(f"\n[EVENT] {event.type}\n")
            
            if event.type  == "raw_response_event" and event.type == "agent_updated_stream_event" and isinstance(event.data, response_text_delta_event):
                print(f"\n[DAATA] {event.data.delta}\n")
                
                
            
            
asyncio.run(stream())

# agent = Agent(
#     name="smart assistant",
#     instructions=""" You are a helpfull assistant. """,
#     model=geminiModel
# )
# while True:
#     usrInp = input("Ask>>> ")
        
#     if usrInp == "stop":
#         break
    
#     syncResult = Runner.run_sync(
#         starting_agent=agent,
#         input=usrInp,
#         run_config=config
#     )
    
#     print(syncResult.final_output)


# teacher = Agent(
#     name="Smart Agent",
#     instructions=""" You Resolve user queries in short way. """,
#     model=geminiModel 
# )
# async def run():
    
#     while True:
#         usrInp = input("Ask...[ ")
        
#         if usrInp == "stop":
#             break
        
#         runResult =await Runner.run( #<==== Using .run method
#             teacher,
#             usrInp,
#             run_config=config
#         )
#         print(runResult.final_output)
# if __name__ == "__main__":
#     asyncio.run(run())