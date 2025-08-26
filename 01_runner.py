import asyncio

from agents import Agent, Runner, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent

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
    # runResult =await Runner.run( #<==== Using .run method
    #     teacher,
    #     "Why kiwi bird can't fly ?",
    #     run_config=config
    # )
    # print(runResult.final_output)
    
    
    runStream = Runner.run_streamed(
        reasoner, 
        input="Please tell me 5 jokes.",
        run_config=config,
        
        )
   
    # print("=== Run starting ===")

    # async for event in runStream.stream_events():
    #     # We'll ignore the raw responses event deltas
    #     if event.type == "raw_response_event":
    #         continue
    #     # When the agent updates, print that
    #     elif event.type == "agent_updated_stream_event":
    #         print(f"Agent updated: {event.new_agent.name}")
    #         continue
    #     # When items are generated, print them
    #     elif event.type == "run_item_stream_event":
    #         if event.item.type == "tool_call_item":
    #             print("-- Tool was called")
    #         elif event.item.type == "tool_call_output_item":
    #             print(f"-- Tool output: {event.item.output}")
    #         elif event.item.type == "message_output_item":
    #             print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
    #         else:
    #             pass  # Ignore other event types

    # print("=== Run complete ===")

    
    async for event in runStream.stream_events():
        if event.type == "raw_response_event":
            # every raw response event has event.data.delta safely
            print(event.data.delta, end="", flush=True)
   
if __name__ == "__main__":
    asyncio.run(main())
    
    
   
