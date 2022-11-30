from app.user_management.user_manager import UserManager

user_manager = UserManager()
user_manager.load()

ADMIN_LIST = ['tech9998', 'pl0nch1']


def is_admin(tg_id):
    return tg_id in ADMIN_LIST
