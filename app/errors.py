class OutOfRequestQuota(Exception):
    def __init__(self, message=f'User is out of request quota'):
        super(OutOfRequestQuota, self).__init__(message)


class UserUnsubscribed(Exception):
    def __init__(self, message=f'User is not subscribed'):
        super(UserUnsubscribed, self).__init__(message)