from __future__ import annotations
from typing import Tuple
from pydantic.main import BaseModel
from user_agents import parse


class ParsedUA(BaseModel):
    browser_family: str
    browser_version_major: str
    browser_version_minor: str

    os_family: str
    os_version_major: str
    os_version_minor: str

    device_family: str
    device_brand: str
    device_model: str

    is_mobile: bool
    is_table: bool
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
            browser_version_minor=cls.parse_version(browser.version)[1],
            # OS
            os_family=os.family,
            os_version_major=cls.parse_version(os.version)[0],
            os_version_minor=cls.parse_version(os.version)[1],
            # Device
            device_family=device.family,
            device_brand=device.brand,
            device_model=device.model,
            # Booleans
            is_mobile=parsed_ua.is_mobile,
            is_tablet=parsed_ua.is_tablet,
            is_touch_capable=parsed_ua.is_touch_capable,
            is_pc=parsed_ua.is_pc,
            is_bot=parsed_ua.is_bot,
        )
