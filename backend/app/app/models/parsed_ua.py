from __future__ import annotations
from typing import Optional, Tuple
from pydantic.main import BaseModel
from user_agents import parse


class ParsedUA(BaseModel):
    browser_family: str
    browser_version_major: str

    os_family: str

    device_brand: Optional[str]

    is_mobile: bool
    is_tablet: bool
    is_touch_capable: bool
    is_pc: bool
    is_bot: bool

    @classmethod
    def parse_version(cls, version: Tuple) -> Tuple:
        return version + (0,) * (2 - len(version))

    @classmethod
    def from_ua_string(cls, ua_string: str) -> ParsedUA:
        parsed_ua = parse(ua_string)
        browser = parsed_ua.browser
        os = parsed_ua.os
        device = parsed_ua.device
        return ParsedUA(
            # Browser
            browser_family=browser.family,
            browser_version_major=cls.parse_version(browser.version)[0],
            # OS
            os_family=os.family if os.family != "Linux" else "Generic Linux",
            # Device
            device_brand=device.brand,
            # Booleans
            is_mobile=parsed_ua.is_mobile,
            is_tablet=parsed_ua.is_tablet,
            is_touch_capable=parsed_ua.is_touch_capable,
            is_pc=parsed_ua.is_pc,
            is_bot=parsed_ua.is_bot,
        )
