import asyncio
from src.ai.parser import parse_event
from src.ai.narrator import narrator
from src.code.delay import get_nodes, dependencies
from src.code.score import analyze_delay_event

async def main():
    nodes = get_nodes()
    dep_index = dependencies(nodes)
    known_ids = list(nodes.keys())

    parsed = await parse_event("delay sup1 by 40 days", known_ids)
    result = analyze_delay_event(nodes, dep_index, parsed["start_id"], parsed["delay_time"])
    report = await narrator(parsed, result)

    print(report)

asyncio.run(main())