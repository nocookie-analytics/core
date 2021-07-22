from enum import Enum
from typing import List


class Plan(Enum):
    NO_PLAN = "no_plan"
    FREE = "free"
    LITE = "lite"
    MEDIUM = "medium"
    ENTERPRISE = "enterprise"


SUBSCRIBABLE_PLANS = [Plan.LITE, Plan.MEDIUM, Plan.ENTERPRISE]
