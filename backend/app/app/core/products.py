from enum import Enum
from app.core.config import settings
from app.logger import logger


class Plan(Enum):
    LITE = "lite"
    MEDIUM = "medium"
    ENTERPRISE = "enterprise"
