

import json
from typing import Optional


class Message:
    message_type: str
    exchange: Optional[str]
    routing_key: str
    payload: dict | str

    def dict(self):
        return {"message_type": self.message_type, "exchange": self.exchange, "payload": self.payload}

    def str(self):
        return json.dumps(self.dict())
