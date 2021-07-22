from pydantic.main import BaseModel
from pydantic.networks import HttpUrl


class SignupLink(BaseModel):
    url: HttpUrl
