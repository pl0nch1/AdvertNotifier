from user_management.user_manager import UserManager


def main():
    manager = UserManager('data/')
    manager.load()

    manager.subscribe('tech9998', 2)
    manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=rtx')




if __name__ == '__main__':
    main()
