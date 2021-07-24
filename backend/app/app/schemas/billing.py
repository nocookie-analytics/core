from pydantic.main import BaseModel
from pydantic.networks import HttpUrl


class StripeLink(BaseModel):
    url: HttpUrl
