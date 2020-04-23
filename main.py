import config
import util
import users
import programs
# import offices
import requests
from xlrd import open_workbook
# import firebase_admin
from firebase_admin import db
from firebase_admin import auth


def test_write_db(data):
    db.reference().child('python').push(data)
    print(data)


def test_read_db():
    data = db.reference('python').get()
    print(data)


def test_delete_db():
    db.reference('python').delete()
    print('Testing deleting in database')


def test_read_excel(file='Alumnos.xlsx'):
    wb = open_workbook(file)
    sheet = wb.sheet_by_index(0)
    print('Rows:', sheet.nrows)
    print('Columns:', sheet.ncols)
    # for r in range(1, sheet.nrows):
    #     for c in range(sheet.ncols):
    #         print(sheet.cell_value(r, c), end=' ')
    #     print()
    for r in range(1, sheet.nrows):
        name = sheet.cell_value(r, 3)
        last_name = sheet.cell_value(r, 4)
        if (name != '' and last_name != ''):
            # print(name, last_name)
            email = (name[:2].lower()
                     + last_name.lower().replace(" ", "")
                     + '@shanti.com')
            print(name + ' ' + last_name + ' ' + email)


def test_cloud_functions(url, data={}):
    token = users.get_test_token()
    response = requests.post(
        url=url,
        json=data,
        headers={'Authorization': 'Bearer ' + token}
    )
    if response.ok:
        print('Success')
        print(response.json())
        return True
    else:
        print(response.text)
        return False


def test_manage_user():
    data1 = {
        'userData': {
            'name': "Francesca",
            'lastName': "Traverso",
            'phone': 65171311,
            'email': "traverso_francesca@hotmail.com",
            'password': 'shanti123'
        }
    }
    data2 = {
        'userData': {
            'name': "Fabrizia",
            'lastName': "Traverso",
            'phone': 65171314,
            'email': "traverso.fabrizia@gmail.com",
            'password': 'shanti123'
        }
    }
    users.manage_user(data1, new_user=True)
    users.manage_user(data2, new_user=True)


def test_add_program():
    name = "Yoga Niños"
    office = {
        'officeId': "-M04f5gl2EcNIjt6iBOV",
        'officeName': "Shanti - Achumani"
    }
    # office = {
    #     'officeId': "-M04f5arIpZ3vUDWc3Le",
    #     'officeName': "Shanti - Centro"
    # }
    # office = {
    #     'officeId': "-M04f5mlTYcXwJ01HA5D",
    #     'officeName': "Shanti - Obrajes"
    # }
    # teacher = {
    #     'teacherId': "5xdCOp495zgw0exFEczPzP3Va8u1",
    #     'teacherName': "Francesca Traverso"
    # }
    teacher = {
        'teacherId': "OTiOq0ka3ERsAq2SzEQw6GROKrw1",
        'teacherName': "Fabrizia Traverso"
    }
    optional_teacher = {
        'teacherId': "",
        'teacherName': ""
    }
    dates = []
    date1 = {
        'dayIndex': 1,
        'startDate': util.convertDate(0, 0, 0, 16, 45),
        'endDate': util.convertDate(0, 0, 0, 18, 0)
    }
    dates.append(date1)
    date2 = {
        'dayIndex': 3,
        'startDate': util.convertDate(0, 0, 0, 16, 45),
        'endDate': util.convertDate(0, 0, 0, 18, 0)
    }
    dates.append(date2)
    date3 = {
        'dayIndex': 5,
        'startDate': util.convertDate(0, 0, 0, 16, 45),
        'endDate': util.convertDate(0, 0, 0, 18, 0)
    }
    dates.append(date3)
    packages = []
    program_package1 = {
        'key': util.convertDate(0, 0, 0, 15, 31),
        'active': True,
        'titlePackage': "Yoga Turno Fijo 1",
        'descriptionPackage': "4 asistencias a la misma clase por mes ",
        'daysPackage': 30,
        'sessionsPackage': 4,
        'pricePackage': 150,
        'favorite': False,
        'promotion': False,
        'showInfo': False,
    }
    packages.append(program_package1)
    program_package2 = {
        'key': util.convertDate(0, 0, 0, 15, 32),
        'active': True,
        'titlePackage': "Yoga Turno Fijo 2",
        'descriptionPackage': "8 asistencias a la misma clase por mes ",
        'daysPackage': 30,
        'sessionsPackage': 8,
        'pricePackage': 230,
        'favorite': False,
        'promotion': False,
        'showInfo': False,
    }
    packages.append(program_package2)
    program_package3 = {
        'key': util.convertDate(0, 0, 0, 15, 33),
        'active': True,
        'titlePackage': "Yoga Turno Fijo 3",
        'descriptionPackage': "12 asistencias a la misma clase por mes ",
        'daysPackage': 30,
        'sessionsPackage': 12,
        'pricePackage': 250,
        'favorite': False,
        'promotion': False,
        'showInfo': False,
    }
    packages.append(program_package3)
    program_data = {
        'type': 'program',
        'name': name,
        'teacher': teacher,
        'optionalTeacher': optional_teacher,
        'office': office,
        'dates': dates,
        'packages': packages
    }
    programs.add_program(program_data)


def test_subscribe_users(program_id, program_name, office_name):
    wb = open_workbook("Alumnos.xlsx")
    sheet = wb.sheet_by_index(0)
    print("Start Process")
    users_db = db.reference('users').get()
    for row in range(1, sheet.nrows):
        program_name_excel = sheet.cell_value(row, 1)
        office_name_excel = sheet.cell_value(row, 2)
        name = sheet.cell_value(row, 3)
        last_name = sheet.cell_value(row, 4)
        email = (name.replace(" ", "").lower()
                 + last_name.replace(" ", "").lower()
                 + '@shanti.com')
        price = sheet.cell_value(row, 8)
        sessions_left = sheet.cell_value(row, 9)
        day = sheet.cell_value(row, 11)
        month = sheet.cell_value(row, 12)
        year = sheet.cell_value(row, 13)
        user_id = None
        if ((program_name != program_name_excel)
                or (office_name != office_name_excel)):
            # print('Not Found')
            continue
        if (day == ''):
            continue
        for key, user in users_db.items():
            user_email = user.get('email')
            if (email == user_email):
                user_id = key
                break
        if (user_id is None):
            continue
        # print('Nombre:', name + " " + last_name)
        # print('userId', user_id)
        date = util.convertDate(int(year), int(month), int(day), 23, 0)
        completeRegistration = True
        print(sessions_left)
        if (sessions_left == ''):
            sessions_left = 12
            completeRegistration = False
            print('Incomplete')
        else:
            sessions_left = int(sessions_left)
        data = {
            'active': True,
            'isSubscribed': True,
            'completeRegistration': completeRegistration,
            'daysAvailable': 30,
            'sessionsLeft': sessions_left,
            'price': int(price),
            'expirationDate': date
        }
        db.reference('control/userControl/' + user_id).child(program_id).set(data)
    print("End Process")


def test_import_users_by_program(program_name, office_name):
    password = 'shanti123'
    phone = ''
    user_type = 'basic'
    wb = open_workbook("Alumnos.xlsx")
    sheet = wb.sheet_by_index(0)
    print("Start Process")
    for row in range(1, sheet.nrows):
        name = sheet.cell_value(row, 3)
        last_name = sheet.cell_value(row, 4)
        email = (name.replace(" ", "").lower()
                 + last_name.replace(" ", "").lower()
                 + '@shanti.com')
        program_name_excel = sheet.cell_value(row, 1)
        office_name_excel = sheet.cell_value(row, 2)
        if ((program_name != program_name_excel)
                or (office_name != office_name_excel)):
            continue
        try:
            if (name == '' or last_name == ''):
                raise ValueError('Incorrect Name or Last Name')

            user_record = auth.create_user(email=email, password=password)
            user_id = user_record.uid
            user = {
                'name': name,
                'lastName': last_name,
                'email': email,
                'type': user_type,
                'phone': phone
            }
            print(row, user)
            db.reference('users').child(user_id).set(user)
        except Exception as ex:
            print(row, end=' ')
            print(ex, end=': ')
            print(name + " " + last_name, email)
            pass
    print("End Process")


def main():
    # default_app = config.initialize_app()
    config.initialize_app()
    # test_read_excel()
    # offices.import_offices_from_excel()
    # users.get_users(user_type='all_users', name='ES')
    url = 'http://localhost:5000/shantiapp-4eae1/us-central1/users-getUsers'
    data = {
        'userType': 'basic_users',
        'userSearchName': 'trAv'
    }
    test_cloud_functions(url, data)
    # users.import_users_from_excel()
    # users.delete_users()
    # test_add_program()
    # test_subscribe_users("-M2KO3f6YGIeXnimrTO2", "Yoga Niños", "Achumani")
    # test_import_users_by_program("Yoga Niños", "Achumani")


if __name__ == "__main__":
    main()
