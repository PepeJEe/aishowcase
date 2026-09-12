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

def dependencyindex(nodes) -> list:
    dep = defaultdict(list)
    for node in nodes.values():
        for dep_id in node.get("dependencies", []):
            dep[dep_id].append(node["id"]) #when dependency add to empty list
    return dep

def add_delay(nodes):
    dep = dependencyindex(nodes)
