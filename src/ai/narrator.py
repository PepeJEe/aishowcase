from src.ai.llm import receive_messages


async def narrator(parsed: dict, result: dict):
    prompt = f"""Write a short, professional situation report based on this data
    that is given to you, do not invent any numbers, use what's below to get the correct json information:
    Event: {parsed["start_id"]} delayed by {parsed["delay_time"]} days.

    Affected suppliers, components, products and the results:
    {result}

    Mention every affected node name and ID.
    Add a bit character to it, like you are actually high tech computer for risk and escalation management in supply chain control. No need to copy paste, but into your own words.
    Format the report into these categories: Issue, Affected sections, Risk levels, Recommended escalation, Recommended Action.
    If you can't find correct format of event, default to 0 delay days"""

    response = await receive_messages([{"role": "user", "content": prompt}])
    return response