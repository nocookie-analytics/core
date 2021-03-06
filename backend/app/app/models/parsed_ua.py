from __future__ import annotations
from app.models.event import DeviceType
from typing import Optional, Tuple
from pydantic.main import BaseModel
from user_agents import parse


browser_family_map = {
    "Chrome Mobile": "Chrome",
    "Chromium": "Chrome",
    "Firefox iOS": "Firefox",
    "Firefox Mobile": "Firefox",
    "Mobile Safari": "Safari",
}


class ParsedUA(BaseModel):
    browser_family: str
    browser_version_major: str

    os_family: str

    device_brand: Optional[str]

    device_type: Optional[DeviceType]
    is_bot: bool

    @classmethod
    def parse_version(cls, version: Tuple) -> Tuple:
        return version + (0,) * (2 - len(version))

    @classmethod
    def from_ua_string(cls, ua_string: str) -> ParsedUA:
        parsed_ua = parse(ua_string)
        browser = parsed_ua.browser
        os_family: str = parsed_ua.os.family
        device_brand: Optional[str] = parsed_ua.device.brand
        if os_family:
            if os_family == "Other" and parsed_ua.is_bot:
                os_family = "Bot"
            if os_family == "Mac OS X":
                os_family = "macOS"
        if device_brand:
            if device_brand.startswith("Generic"):
                device_brand = None
            elif device_brand == "Spider":
                device_brand = "Bot"

        browser_family = browser_family_map.get(browser.family, browser.family)

        device_type: Optional[DeviceType] = None
        if parsed_ua.is_mobile:
            device_type = DeviceType.MOBILE
        elif parsed_ua.is_pc:
            device_type = DeviceType.DESKTOP
        elif parsed_ua.is_tablet:
            device_type = DeviceType.TABLET

        return ParsedUA(
            # Browser
            browser_family=browser_family,
            browser_version_major=cls.parse_version(browser.version)[0],
            # OS
            os_family=os_family,
            # Device
            device_brand=device_brand,
            device_type=device_type,
            is_bot=parsed_ua.is_bot,
        )
