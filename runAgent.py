from agents import Agent, Runner, SQLiteSession, function_tool, enable_verbose_stdout_logging
from agents.model_settings import ModelSettings
from agents.agent import StopAtTools
#  verbose means des=bbugging
import asyncio
import random


from gemini_model import geminiModel, config


# enable_verbose_stdout_logging()  # Enable verbose logging for debugging


@function_tool   # THIS DECORATOR IS USED TO MAKE SCHEMA AND MAKE THE FUNCTION AVAILABLE TO THE AGENT
def sum(a: int, b: int) -> int:
    """
    Returns the sum of two integers.
    """
    return a + b

@function_tool
def getJokes():
    """ This is the random jokes generator Expert. """
    jokes = [
        "1.Why did the trash can turn red? Because it saw the garbage truck!",
        "2.What did the garbage say to the other garbage? “You stink!”",
        "3.Why don’t trash cans ever fight? Because they always make up!"
    ]
    
    jokes = random.choice(jokes)
    return jokes
    

mathematician = Agent(
    name = "Mathematician",
    instructions = "You are a mathematician. use sum tool for addition",
    model = geminiModel,
    tools=[sum],  # Registering the sum function as a tool
    model_settings=ModelSettings(tool_choice='required'),
    # reset_tool_choice=False
)

joker = Agent(
    name= "Joker Agent",
    instructions= """
    You are a joker agent and very funny, you tell intersting jokes about user query. use getJokes tool for tell jokes.
    """,
    tools= [getJokes],
    model= geminiModel,
    model_settings= ModelSettings(tool_choice="required")
)

orchestrator = Agent(
    name= "Orchestrator Agent",
    instructions= """
    You are a main Orchestrator Agent you manages all sub agents like "mathematician agent, joker agent"
    use them wisely and in the end ask the user a related question about user query to engage user interest and to continue chat.
    """,
    tools= [],
    handoffs= [mathematician, joker],
    model= geminiModel,
    tool_use_behavior=StopAtTools(stop_on_first_tool=["getjokes"]),
    
)



async def run_main_agent():
    session = SQLiteSession("history.db")
       
    while True:
        query = input("😴: ").strip()
        
        if query.lower() in ["exit", "quit", "stop"]:
            break
        
      
        result = await Runner.run(
           starting_agent= orchestrator,
           input= query,
           run_config= config,
           session=session
          
        )
        
        print(f"🤖: {result.final_output}\n")
        
if __name__ == "__main__":
    asyncio.run(run_main_agent())