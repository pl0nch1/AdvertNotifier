from user_management.user_manager import UserManager
manager = UserManager('data/')
manager.load()
manager.release_request('quickly', 2)
manager.dump()
