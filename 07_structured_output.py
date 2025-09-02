import asyncio

from agents import Agent, Runner
from pydantic import BaseModel

from gemini_model import geminiModel, config

YES = True
NO = False

class StrcOutput(BaseModel):
    shortAnswer: str
    detailedAnswer: str
    totalWordsInDetailedAnswer: int
    totalWordsInShortAnswer: int
    isQuestionHard: bool
    


agent = Agent(
    name="Agent",
    instructions="""  """,
    model=geminiModel,
    output_type=StrcOutput
  )

async def main():
    
    while True:
        usrInp = input("Ask Something >>> ")
        
        if usrInp == "stop":
            break
        
        runResult =await Runner.run(
            agent,
            usrInp,
            run_config=config
        )
        print("\t\t\tLLM Output")
        
        print("\nAnswer >>>",runResult.final_output)
        print("\nShort Answer >>>",runResult.final_output.shortAnswer)
        print("\nTotal Words>>>",runResult.final_output.totalWordsInShortAnswer)
        print("\nlong Answer >>>",runResult.final_output.detailedAnswer)
        print("\nTotal words >>>",runResult.final_output.totalWordsInDetailedAnswer)
        print("\nIs Question Hard >>>",runResult.final_output.isQuestionHard)
    
if __name__ == "__main__":
    asyncio.run(main())
    
    
   
