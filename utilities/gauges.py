import json 

with open("data/unit_weights.json", encoding="UTF-8") as file_in:
    unit_weights = json.load(file_in)

gauges = list(unit_weights.keys())

def get_gauge_shift(gauge: str, step: int) -> str | None:
    """
    Returns the gauge that is `step` positions away from `gauge` in the ordered list.
    `step` can be positive (forward) or negative (backward).
    Returns None if the resulting position is out of range.
    """
    idx = gauges.index(gauge)
    new_idx = idx + step
    if new_idx >= len(gauges):
        return gauges[-1]
    if new_idx < 0:
        return gauges[0]
    return gauges[new_idx]

def gauge_to_unit_weight(gauge: str) -> float:
    """
    Returns unit weight of the string that is corresponding to the given gauge.
    """
    return unit_weights[gauge]

def check_gauge(gauge: str):
    """
    Returns True if gauge is in the list of allowed gauges. Else returns False.
    """
    return gauge in gauges