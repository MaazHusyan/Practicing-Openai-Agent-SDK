import asyncio

from agents import  (
    Agent,
    Runner,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    GuardrailFunctionOutput,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
    output_guardrail
    )
from pydantic import BaseModel

from gemini_model import geminiModel, config


class llmOutput(BaseModel):
    response: str

class IsAboutAOT(BaseModel):
    isAboutAttackOnTitan: bool
   

inputGuardrailAgent = Agent(
    name="input Checker",
    instructions=""" Chech if user asking about Attack on Titan Anime """,
    model=geminiModel,
    output_type=IsAboutAOT
  )

@input_guardrail
async def inputGuardrail(ctx: RunContextWrapper, agent: Agent, input: str|list[TResponseInputItem])->GuardrailFunctionOutput:
            
    runResult =await Runner.run(
        inputGuardrailAgent,
        input,
        context=ctx.context,
        run_config=config
    )
    
    return GuardrailFunctionOutput(
        output_info=runResult.final_output,
        # tripwire_triggered=True #result.final_output.isAboutAttackOnTitan,
        tripwire_triggered= runResult.final_output.isAboutAttackOnTitan
    )
    
    
outputGuardrailAgent = Agent(
    name="output checker",
    instructions="check if there any thin about Attack on titan in output.",
    model=geminiModel,
    output_type=IsAboutAOT
)

@output_guardrail
async def outputGuardrail(ctx: RunContextWrapper, agent: Agent, output: llmOutput):
    runResult =await Runner.run(
        outputGuardrailAgent,
        output.response,
        run_config=config,
        context=ctx.context
    )
    
    return GuardrailFunctionOutput(
        output_info=runResult.final_output,
        tripwire_triggered=runResult.final_output.isAboutAttackOnTitan
    )
    
masterAgent = Agent(
    name="Answering Agent",
    instructions="You are a smart agent assistant.",
    input_guardrails=[inputGuardrail],
    output_guardrails=[outputGuardrail],
    output_type=llmOutput
)
   
def main():
    try:
        while True:
            usrInp = input("Ask Something >>> ")
            
            if usrInp == "stop":
                break
                
            result =Runner.run_sync(
                starting_agent=masterAgent,
                input=usrInp,
                run_config=config
            )
            
            print(result.to_input_list())
    except InputGuardrailTripwireTriggered:
        print("====Alert: Guardrail input tripwire was triggered!====")
    except OutputGuardrailTripwireTriggered:
        print("====Alert: Guardrail output tripwire was triggered!====")
        
if __name__ == "__main__":
    main()
    
    

    
    
   
