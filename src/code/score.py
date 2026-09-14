#Inventory days: how many days worth of stock supplier has currently.
#Lead time days: how many days it takes for supplier to get new stock.
#example: inventory day is 5 and lead time day is 30. 
# It takes 30 days to manufacture/ship products in total for supplier, 
#but supplier has 5 days worth of stock, 
#so the total time to get new stock is 30-5=25 days, which is high risk.

from src.code.delay import add_delay


def criticality_score(criticality: int) -> int:
    return criticality * 4 # criticality 0-5

#Calculate inventory score based on the ratio of inventory days to lead time days
#how long does supplier have inventory vs how long it takes to get new inventory. The lower the ratio, the better the score.
def inventory_score(inventory_days: int, lead_time_days: int, delay_days: int = 0) -> int:
    lead_time_risk = min(15, lead_time_days // 5)   # longer lead time = a bit more baseline risk
    delay_risk = min(35, max(0, delay_days - inventory_days))   # days actually stuck with zero stock

    return lead_time_risk + delay_risk


def delivery_score(delivery_reliability: int) -> int:
    return round((1-delivery_reliability)*20) # delivery reliability 0-100

def single_source_score(single_source: bool) -> int:
    return 20 if single_source else 0

GEOPOLITICAL_SCORE={
    "Finland": 1,
    "China": 5,
    "Japan": 2,
    "Estonia": 1,
}
def geopolitical_score(country: str) -> int:
    return GEOPOLITICAL_SCORE.get(country, 20)



def score_supplier(node: dict) -> dict:
    scores = {
        "criticality_score": criticality_score(node["criticality"]),
        "inventory_score": inventory_score(node["inventory_days"], node["lead_time_days"], node.get("delay_days", 0)),
        "delivery_score": delivery_score(node["reliability"]),
        "single_source_score": single_source_score(node["single_source"]),
        "geopolitical_score": geopolitical_score(node["country"])
    }
    total = sum(scores.values())

    if total <= 25:
        risk_level = "LOW"
    elif total <= 50:
        risk_level = "MEDIUM"
    elif total <= 70:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return {
        "supplier_id": node["id"],
        "supplier_name": node["name"],
        "risk_score": total,
        "risk_level": risk_level,
        "breakdown": scores
    }

#does node have enough inventory after delay
def score_with_delay(node: dict, delay_days: int):
    new_inventory = node.copy()
    new_inventory["delay_days"] = delay_days
    return score_supplier(new_inventory)

#returns if escalation is needed based on the risk level of the supplier.
def escalation_management(score_supplier: dict) -> str:
    risk_level = score_supplier["risk_level"]
    if risk_level == "CRITICAL":
        return{
            "action":"auto escalate",
            "requires_human_action": False,
            "details": "Escalate automatically to senior management. Immediate action required.",
        }
    elif risk_level == "HIGH": #MODIFY LATER
        return {
            "action": "escalation recommended",
            "requires_human_action": True,
            "details": "Monitor closely. Review supplier performance and consider contingency plans."
        }
    else:
        return {
            "action": "no escalation needed",
            "requires_human_action": False,
            "details": "Low risk. No immediate action required."
        }
ESCALATION_CONTACTS ={
    "CRITICAL": ["senior management", "procurement"],
    "HIGH": ["supply chain manager"],
    "MEDIUM": [], "LOW": []
}
def get_escalation_contacts(score_supplier: dict) -> list:
    risk_level = score_supplier["risk_level"]
    return ESCALATION_CONTACTS.get(risk_level, [])













def analyze_delay_event(nodes, dep_id, start_id, delay_time):
    delays = add_delay(nodes, dep_id, start_id, delay_time)

    results = {}
    for node_id, leftover_delay in delays.items(): #loop how many delays in delays.item
        node = nodes[node_id]
        if "lead_time_days" in node:
            new_score_supplier = score_with_delay(node, leftover_delay)
            escalation = escalation_management(new_score_supplier)
            contacts = get_escalation_contacts(new_score_supplier)
            results[node_id] = {
                "incoming_delay_days": leftover_delay, **new_score_supplier,
                "escalation": escalation,
                "contacts": contacts
            }
        else:
            results[node_id] = {
                "incoming_delay_days": leftover_delay, **new_score_supplier,
                "has_risk_score": False,
            }
    return results

