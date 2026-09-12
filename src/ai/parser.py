

import json
import re

from src.ai.llm import receive_messages


async def parse_event(text: str, supplier_ids: list):
    prompt = f"""You are JSON extraction tool. Extract only the delayed suppliers ID and number of days from this message
    
    Known supplier IDs: {supplier_ids}
    Message: "{text}"

    Respond ONLY a JSON object, absolutely nothing else and in this format:
    {{"start_id": "SUP-001", "delay_time": 15}}"""

    response = await receive_messages([{"role": "user", "content": prompt}])
    print("RAW MODEL RESPONSE:", response)

    match = re.search(r"\{.*\}", response, re.DOTALL)
    if not match:
        raise ValueError("Could not find JSON format: {response}")
    parsed = json.loads(match.group())

    if parsed["start_id"] not in supplier_ids:
        raise ValueError(f"Model returned unknown supplier id: {parsed['start_id']}")
    return parsed