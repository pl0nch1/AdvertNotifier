from app.scheduler import Scheduler
from user_management.user_manager import UserManager

def main():
    scheduler = Scheduler()
    scheduler.schedule()


if __name__ == '__main__':
    main()
