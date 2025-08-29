import asyncio

from agents import  (
    Agent,
    Runner,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    GuardrailFunctionOutput,
    InputGuardrailResult,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
    output_guardrail
    )
from pydantic import BaseModel

from gemini_model import geminiModel, config
class isAboutAOT(BaseModel):
    isAboutAttackOnTitan: bool
    reasoning: str
    spoiler: str


guardrailAgent = Agent(
    name="Safety Check",
    instructions=""" Chech if user asking about Attack on Titan Anime """,
    model=geminiModel,
    output_type=isAboutAOT
  )

@input_guardrail
async def aotGuardrail(ctx: RunContextWrapper[None], agent: Agent, input: str|list[TResponseInputItem])->GuardrailFunctionOutput:
            
    runResult =await Runner.run(
        guardrailAgent,
        input,
        context=ctx.context,
        run_config=config
    )
    
    return GuardrailFunctionOutput(
        output_info=runResult.final_output,
        # tripwire_triggered=True #result.final_output.isAboutAttackOnTitan,
        tripwire_triggered=runResult.final_output.isAboutAttackOnTitan
    )
    
agent = Agent(
    name="Answering Agent",
    instructions="You are a smart agent assistant.",
    input_guardrails=[aotGuardrail]
)
   
async def main():
    try:
        while True:
            usrInp = input("Ask Something >>> ")
            
            if usrInp == "stop":
                break
                
            result =await Runner.run(
                starting_agent=agent,
                input=usrInp,
                run_config=config
            )
            
            print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("=======guardrail tripped========")
   
if __name__ == "__main__":
    asyncio.run(main())
    
    

    
    
   
