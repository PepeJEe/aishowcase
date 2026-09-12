from src.score import score_supplier
from src.score import get_escalation_contacts
import json
from src.delay import get_nodes, nodes
from src.delay import dependencyindex

with open("src/data/suppliers.json") as f:
    suppliers = json.load(f)

# Score first supplier
#for supplier in suppliers["suppliers"]:
 #   result = score_supplier(supplier)
  #  escal_contact = get_escalation_contacts(result)
    #print(result, "\n")
    #print(escal_contact, "\n")
   # print(nodes["SUP-001"])

test = dependencyindex(get_nodes())
print(test)