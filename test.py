from config import initialize_app, remove_app
from admin import Admin
import _util
from requests.exceptions import ConnectionError
import time


def test_offices():
    from offices import Office, Offices
    office1 = Office('Shanti', 'Obrajes', key="0001")
    office2 = Office('Shanti', 'Achumani', key="0002")
    office3 = Office('Shanti', 'Mallasilla', key="0003")
    office4 = Office('Shanti', 'Centro', key="0004")
    office5 = Office('Test', 'Sopocachi', key="0005")
    offices = Offices([office1, office2, office3, office4])
    for office in offices:
        print(office.key)
    offices.add_office(office5)
    for office in offices:
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
    for office in test_offices:
        print(office.key)
    test_office = test_offices.get_office_by_id('0001')
    print(test_office)
    print(test_office.key)


def test_offices_database():
    from offices import Offices, Office
    offices = Offices()
    offices.load_from_db()
    print("Original Office List")
    for office in offices:
        print("Nombre:", office.name)
        print("Dirección:", office.address)
        print("Url:", office.google_map_url)
        print("Key:", office.key)
    time.sleep(10)
    new_office = Office('Test', "Centro", "test.com")
    new_office.upload()
    print(new_office.key)
    print(new_office.get_data())
    offices.load_from_db()
    print("New Office")
    for office in offices:
        print("Nombre:", office.name)
        print("Dirección:", office.address)
        print("Url:", office.google_map_url)
        print("Key:", office.key)
    time.sleep(10)
    new_office.google_map_url = None
    print(new_office.key)
    print(new_office.get_data())
    new_office.upload()
    offices.load_from_db()
    print("Modified new Office")
    for office in offices:
        print("Nombre:", office.name)
        print("Dirección:", office.address)
        print("Url:", office.google_map_url)
        print("Key:", office.key)
    time.sleep(10)
    new_office.delete()
    print(new_office.key)
    print(new_office.get_data())
    offices.load_from_db()
    print("New Office Deleted")
    for office in offices:
        print("Nombre:", office.name)
        print("Dirección:", office.address)
        print("Url:", office.google_map_url)
        print("Key:", office.key)
    time.sleep(10)


def test_office_file(file_name):
    from offices import Offices
    offices = Offices()
    # offices.load_from_db()
    # offices.export_to_file(file_name, "Sucursales")
    offices.load_from_file(file_name)
    for office in offices:
        print("Nombre:", office.name)
        print("Dirección:", office.address)
        print("Url:", office.google_map_url)
        print("Key:", office.key)


def test_users_database():
    from users import User, Users
    users = Users()
    users.load_from_db(complete_profile=False)
    admin_users = users.get_user_by_name_and_role(user_name='', user_role='admin_users', find_one=False)
    print("Original Users List")
    for user in admin_users:
        print("Key:", user.key)
        print("Nombre:", user.display_name)
        print("Email:", user.email)
        print("Rol:", user.user_role)
        print("Imagen", user.image)
        print(user.get_data())


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
        # test_offices()
        # test_offices_database()
        # test_office_file("Sucursales.xlsx")
        test_users_database()

        # office = {'name': 'Test', 'address': 'Centro', 'url': None}
        # key = "{'name': 'Test', 'address': 'Centro', 'url': None}"
        # from firebase_admin import db
        # db.reference('offices').child(key).update(office)
    except ConnectionError as error:
        print('No Internet', error)
    except Exception as ex:
        print(ex, type(ex))
        print('End with Errors')
    finally:
        remove_app(app)
        print('End')
