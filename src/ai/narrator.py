from src.ai.llm import receive_messages


async def narrator(parsed: dict, result: dict):
    prompt = f"""Write a short, professional situation report based on this data
    that is given to you, do not invent any numbers, use what's below to get the correct json information:
    Event: {parsed["start_id"]} delayed by {parsed["delay_time"]} days.

    Affected suppliers, components, products and the results:
    {result}

    Add a bit character to it, like you are actually high tech computer for risk and escalation management in supply chain control.
    Format the report into these categories: Issue, Affected sections, Risk levels, Recommended escalation, Recommended Action"""

    response = await receive_messages([{"role": "user", "content": prompt}])
    return response 