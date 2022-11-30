class OutOfQuotaException(Exception):
    def __init__(self, message=f'User is out of request quota'):
        super(OutOfQuotaException, self).__init__(message)


class UserUnsubscribed(Exception):
    def __init__(self, message=f'User is not subscribed'):
        super(UserUnsubscribed, self).__init__(message)


class UserHasNoRequests(Exception):
    def __init__(self, message=f'User has no requests'):
        super(UserHasNoRequests, self).__init__(message)
