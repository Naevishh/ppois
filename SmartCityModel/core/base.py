import uuid
from .enums import Domain


class SmartDevice:
    def __init__(self, device_keyword: str, domain: Domain):
        self.device_id = device_keyword+str(uuid.uuid4())[:6]
        self.domain = domain
