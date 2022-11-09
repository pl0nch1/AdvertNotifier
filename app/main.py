from user_management.user_manager import UserManager
from avito_driver import AvitoDriver
from drivers_manager import DriversManager

def main():
    manager = UserManager('data/')
    manager.load()

    manager.subscribe('tech9998', 2)
    manager.append_request('tech9998', 'https://www.avito.ru/sankt_peterburg_i_lo?q=rtx')


    print('starting drivers')
    drivers_manager = DriversManager()

    for tg_id, requests in manager.request_items():
        try:

            for request in requests:
                drivers_manager.drivers[request] = AvitoDriver(request, False)

        except Exception as e:
            print(e)
            continue



if __name__ == '__main__':
    main()
