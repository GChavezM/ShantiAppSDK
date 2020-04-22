from config import initialize_app, remove_app
from admin import Admin
import _util
from requests.exceptions import ConnectionError
import time


def start():
    print('Start Project:')
    print('-' * 50)
    _app = initialize_app()
    return _app, _app.options.get('apiKey')


if __name__ == "__main__":
    app = None
    try:
        app, api_key = start()
        time.sleep(1)
        # admin = Admin(api_key)
        # _util.TOKEN = admin.token
        from offices import Office, Offices
        office1 = Office('Shanti', 'Obrajes', key="0001")
        office2 = Office('Shanti', 'Achumani', key="0002")
        office3 = Office('Shanti', 'Mallasilla', key="0003")
        office4 = Office('Shanti', 'Centro', key="0004")
        office5 = Office('Test', 'Sopocachi', key="0005")
        offices = Offices([office1, office2, office3, office4])
        for office in offices.offices:
            print(office.key)
        offices.add_office(office5)
        for office in offices.offices:
            print(office.key)
        print(offices.get_office_by_id("0005"))
        print(offices.get_office_by_id("0005").key)
        print("Test Offices")
        test_office = offices.get_office_by_name('Test')
        print(test_office)
        del office1
        print("Shanti Offices")
        test_offices = offices.get_office_by_name('Shanti', find_one=False)
        print(test_offices)
        for office in test_offices.offices:
            print(office.key)
        test_office = test_offices.get_office_by_id('0001')
        print(test_office)
        print(test_office.key)

        # image = util.get_image_base64("image.jpg")
        # token = auth.get_token()
        # print(token)
        # print(users.get_users('admin_users'))
        # url = 'https://us-central1-shantiapp-4eae1.cloudfunctions.net/uploadImage'
        # result = _util.fetch_cloud_functions(url, {}, fetch_type='get')
        # print(result)
        # print(result.get('imagePath'))
    except ConnectionError as error:
        print('No Internet', error)
    except Exception as ex:
        print(ex, type(ex))
        print('End with Errors')
    finally:
        remove_app(app)
        print('End')
