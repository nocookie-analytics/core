from enum import Enum


class Plan(Enum):
    NO_PLAN = "no_plan"
    TRIAL = "trial"
    TRIAL_EXPIRED = "trial_expired"
    FREE = "free"
    LITE = "lite"
    MEDIUM = "medium"
    ENTERPRISE = "enterprise"
    CANCELLED = "cancelled"


SUBSCRIBABLE_PLANS = [Plan.LITE, Plan.MEDIUM, Plan.ENTERPRISE]
