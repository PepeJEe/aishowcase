from collections import defaultdict
import json

with open("src/data/suppliers.json") as f:
    suppliers = json.load(f)["suppliers"]
with open("src/data/components.json") as f:
    components = json.load(f)["components"]
with open("src/data/products.json") as f:
    products = json.load(f)["products"]

nodes = {}
for i in suppliers + components + products:
    nodes[i["id"]] = i #nodes["SUP_001"] = {"id": ....

def get_nodes() -> dict:
    return nodes
def get_dep(nodes) -> list:
    return dependencies(nodes)

def dependencies(nodes) -> list:
    dep = defaultdict(list)
    for node in nodes.values():
        for i in node.get("dependencies", []):
            dep[i].append(node["id"]) #when dependency add to empty list
    return dep


def add_delay(nodes, dep_nodes, start_id, delay_time) -> dict:
    current = [start_id]
    results = {start_id: delay_time}

    while current:
        next_layer = []
        for node_i in current: #first node is start_id node e.g. "SUP-001"
            delay_time = results[node_i] #delay 15 first time
            for dependent in dep_nodes.get(node_i, []): #dependant SUP-002
                leftover_delay = max(0, delay_time - nodes[dependent]["inventory_days"]) #leftover delay time from inventory days
                if leftover_delay > results.get(dependent, -1): #Is this new delay bigger than the delay we already calculated for this node?"
                    results[dependent] = leftover_delay
                    if leftover_delay > 0:
                        next_layer.append(dependent) #move to next layer SUP-002
        current = next_layer
    return results