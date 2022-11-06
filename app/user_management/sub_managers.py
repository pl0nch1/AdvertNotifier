import datetime
import os

from typing import Dict, List

from pydantic import BaseModel, Field, Extra
from yaml import dump, load, Dumper, Loader

from app.models.user_info import SubscriptionCollection, RequestsCollection, Subscription


def read_collection(path: str, filename: str):
    try:
        with open(path + filename, 'r') as file:
            memory = {'collection': load(file, Loader=Loader)}
    except FileNotFoundError as e:
        os.makedirs(path, exist_ok=True)
        with open(path + filename, 'w') as file:
            dump(dict(), file, Dumper=Dumper)
            memory = {'collection': dict()}
    finally:
        return memory


def dump_collection(path: str, filename: str, obj: Dict):
    with open(path + filename, 'w') as file:
        dump(obj['collection'], file, Dumper=Dumper)


class SubscriptionManager(BaseModel, extra=Extra.allow):
    path: str
    filename: str

    _DEFAULT_DURATION = datetime.timedelta(days=30)

    _subscriptions: SubscriptionCollection

    def load(self):
        self._subscriptions = SubscriptionCollection.parse_obj(read_collection(self.path, self.filename))

    def dump(self):
        dump_collection(self.path, self.filename, self._subscriptions.dict())

    def __getitem__(self, item: str):
        return self._subscriptions.collection.get(item)

    def _populate_subscription(self, tg_id: str, amount: int):
        if self[tg_id]:
            raise ValueError(f'User {tg_id} already have subscription')

        expiration_time = datetime.datetime.utcnow() + self._DEFAULT_DURATION
        self._subscriptions.collection[tg_id] = Subscription(quota=amount, expiration_time=expiration_time)

    def subscribe(self, tg_id: str, amount: int):
        if self[tg_id]:
            self[tg_id].quota += amount
        else:
            self._populate_subscription(tg_id, amount)


class RequestsManager(BaseModel, extra=Extra.allow):
    path: str
    filename: str

    _requests: RequestsCollection = None

    def load(self):
        self._requests = RequestsCollection.parse_obj(read_collection(self.path, self.filename))

    def dump(self):
        dump_collection(self.path, self.filename, self._requests.dict())

    def __getitem__(self, item):
        return self._requests.collection.get(item)

    def init_requests(self, tg_id: str):
        if isinstance(self[tg_id], list) and self[tg_id]:
            raise ValueError(f'User {tg_id} already has some requests')
        self._requests.collection[tg_id] = []

    def release_request(self, tg_id: str, index: int):
        if index < 0 or index >= len(self[tg_id]):
            raise KeyError(f'There is no {index} request of {tg_id} user')

        del self[tg_id][index]

    def list_requests(self, tg_id: str) -> List[str]:
        return self[tg_id]
