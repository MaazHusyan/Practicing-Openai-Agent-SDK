from agents import Agent, Runner, SQLiteSession, function_tool , StopAtTools, enable_verbose_stdout_logging, ModelSettings
import asyncio
from gemini_model import geminiModel, config

# enable_verbose_stdout_logging()

@function_tool(is_enabled=False)
def color_checker():
    """check if color is original."""
    return "color is original"

@function_tool(is_enabled=False)
def repairable():
    """check if it is repairable."""
    return "yes it's repairabele"


doctor_agent = Agent(
    name="Doctor",
    instructions="You are a helpfull assistant.",
    model=geminiModel,
    model_settings=ModelSettings(
        temperature=1.1,
        # top_p=1.0
    ),
)


machenic_agent = Agent(
    name = "Machenic",
    instructions= "You are a Auto Machenic",
    tools= [color_checker, repairable],
    model=geminiModel,
    model_settings=ModelSettings(
        temperature=0.2,
        tool_choice="required"
    ),
    tool_use_behavior="stop_on_first_tool",
    # tool_use_behavior=StopAtTools(stop_at_tool_names=["sad_tool"]),
    reset_tool_choice=False,
    )


triage_agent = Agent(
    name="Orchestrator",
    instructions="You are a orchestrator agent.be usefull, Choose agent according to user query.",
    model=geminiModel,
    handoffs=[doctor_agent, doctor_agent],
    
)


session = SQLiteSession("usr1")

async def main():
    while True:
            userInput = input("User: ").strip()
        
            if userInput.lower() == "stop":
                print("=======================")
                break
                
            agent_runner =await Runner.run(
                triage_agent,
                userInput,
                run_config=config,
                session=session,
                
                
            )
            
            print("\n ---------------------- \n",agent_runner.final_output,"---------------------- \n")
        
if __name__ == "__main__":
    asyncio.run(main())