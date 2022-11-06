from datetime import datetime
from typing import List, Dict

from pydantic import Field, BaseModel


class Subscription(BaseModel):
    quota: int
    expiration_time: datetime


class SubscriptionCollection(BaseModel):
    """
        collection[tg_id] = subscription
    """
    collection: Dict[str, Subscription] = Field(default_factory=dict)


class RequestsCollection(BaseModel):
    """
        collection[tg_id] = requests_list
    """
    collection: Dict[str, List[str]] = Field(default_factory=dict)
