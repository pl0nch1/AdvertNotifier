from typing import List

from app.errors import OutOfRequestQuota, UserUnsubscribed
from .sub_managers import SubscriptionManager, RequestsManager


class UserManager:
    DATA_ENVVAR = 'DATA_PATH'

    def __init__(self, path: str):
        self.path = path
        self.subscription_manager = SubscriptionManager(path=self.path, filename='subscriptions.yaml')
        self.requests_manager = RequestsManager(path=self.path, filename='requests.yaml')
        if not self.path:
            raise RuntimeError(f'{self.DATA_ENVVAR} envvar not defined')

    def dump(self):
        self.subscription_manager.dump()
        self.requests_manager.dump()

    def load(self):
        self.subscription_manager.load()
        self.requests_manager.load()

    def append_request(self, tg_id, request):
        if not self.subscription_manager[tg_id]:
            raise UserUnsubscribed(f'{tg_id} not subscribed')
        if not self.requests_manager[tg_id]:
            self.requests_manager.populate_request(tg_id)
        if len(self.requests_manager[tg_id]) < self.subscription_manager[tg_id].quota:
            self.requests_manager[tg_id].append(request)
        else:
            raise OutOfRequestQuota(f'{tg_id} exceeded request quota')

    def list_requests(self, tg_id: str) -> List[str]:
        return self.requests_manager.list_requests(tg_id)

    def release_request(self, tg_id: str, index: int):
        self.requests_manager.release_request(tg_id, index)

    def subscribe(self, tg_id: str, amount: int):
        self.subscription_manager.subscribe(tg_id, amount)
