import asyncio
import random

from agents import Agent, Runner, function_tool, ModelSettings

from gemini_model import geminiModel, config


@function_tool(is_enabled=True) # isse hum tool ko llm ke pas jane se roksate hai 
def randomFacts():
    facts = [
    "The Earth revolves around the Sun in one year.",
    "Water covers about seventy percent of the Earth’s surface.",
    "The human brain contains billions of active nerve cells.",
    "Honey never spoils and can last for thousands years.",
    "The tallest mountain on Earth is Mount Everest in Nepal.",
    "Octopuses have three hearts and blue-colored circulating blood.",
    "Bananas are berries, but strawberries are not true berries.",
    "Lightning is hotter than the surface of the Sun.",
    "The Moon causes ocean tides by pulling Earth’s water.",
    "Antarctica is the coldest place found on the planet.",
    "The human heart beats around one hundred thousand times daily.",
    "Sharks existed even before trees appeared on our Earth."
    ]
    facts = random.choice(facts)
    return facts

@function_tool(is_enabled=True)
def aboutCars():
    cars = [
    {"name": "Civic", "company": "Honda", "color": "White", "engine": "1.5L Turbo", "hp": 174},
    {"name": "Corolla", "company": "Toyota", "color": "Silver", "engine": "1.8L", "hp": 139},
    {"name": "Model S", "company": "Tesla", "color": "Red", "engine": "Electric", "hp": 670},
    {"name": "Mustang GT", "company": "Ford", "color": "Blue", "engine": "5.0L V8", "hp": 450},
    {"name": "Accord", "company": "Honda", "color": "Black", "engine": "2.0L Turbo", "hp": 252},
    {"name": "Camry", "company": "Toyota", "color": "White", "engine": "2.5L", "hp": 203},
    {"name": "Charger", "company": "Dodge", "color": "Yellow", "engine": "6.2L HEMI", "hp": 707},
    {"name": "A4", "company": "Audi", "color": "Grey", "engine": "2.0L Turbo", "hp": 261},
    {"name": "C-Class", "company": "Mercedes-Benz", "color": "Black", "engine": "2.0L Turbo", "hp": 255},
    {"name": "3 Series", "company": "BMW", "color": "Blue", "engine": "2.0L Turbo", "hp": 255},
    {"name": "911 Carrera", "company": "Porsche", "color": "Silver", "engine": "3.0L Twin-Turbo", "hp": 379},
    {"name": "Altima", "company": "Nissan", "color": "White", "engine": "2.5L", "hp": 188},
    {"name": "Elantra", "company": "Hyundai", "color": "Grey", "engine": "2.0L", "hp": 147},
    {"name": "CX-5", "company": "Mazda", "color": "Red", "engine": "2.5L Turbo", "hp": 250},
    {"name": "K5", "company": "Kia", "color": "Blue", "engine": "1.6L Turbo", "hp": 180}
    ]
    
    car = random.choice(cars)
    return car


    


smartAgent = Agent(
    name="Smart Agent",
    instructions=""" You Resolve user queries in short way.
    use tool "randomFacts" if user ask about facts about any thing. """,
    model=geminiModel,
    tools=[randomFacts, aboutCars],
    model_settings=ModelSettings(tool_choice="required"), # isse tool ahmesha call hoga 
    reset_tool_choice=True, # isko enable krne se tool choice reset krne se rok sakte hai
    tool_use_behavior="stop_on_first_tool",
    
)

async def main():
    
    while True:
        usrInp = input("Ask Something >>> ")
        
        if usrInp == "stop":
            break
        
        runResult =await Runner.run( #<==== Using .run method
            smartAgent,
            usrInp,
            run_config=config
        )
        print("LLM Output >>>",runResult.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
    
    
   
