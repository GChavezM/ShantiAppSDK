import util
import requests
from xlrd import open_workbook
from firebase_admin import auth
from firebase_admin import db

all_users = {
    'basic': True,
    'advanced': True,
    'admin': True
}
basic_users = {
    'basic': True,
    'advanced': False,
    'admin': False
}
advanced_users = {
    'basic': False,
    'advanced': True,
    'admin': False
}
admin_users = {
    'basic': False,
    'advanced': False,
    'admin': True
}
not_basic_users = {
    'basic': False,
    'advanced': True,
    'admin': True
}
user_types = {
    'all_users': all_users,
    'basic_users': basic_users,
    'advanced_users': advanced_users,
    'admin_users': admin_users,
    'not_basic_users': not_basic_users
}

# def change_user_password():
#     url = 'https://identitytoolkit.googleapis.com/v1/'\
#           'accounts:update?key=' +\
#            API_KEY
#     return url


# def manage_user(data, new_user=False, local=False, token=None):
#     min_data = ["email", "password"]
#     if not(
#         data.get("userData") and
#         all(key in data.get("userData") for key in min_data)
#     ):
#         print('Insufficient Data')
#         return False
#     if new_user:
#         print('Add User')
#         url = 'http://localhost:5000/shantiapp-4eae1/'\
#               'us-central1/users-addUser'\
#               if local else 'https://us-central1-shantiapp-4eae1.'\
#               'cloudfunctions.net/users-addUser'
#     else:
#         if not(data.get("userId")):
#             print('No User Id')
#             return False
#         print('Edit User')

#         url = 'http://localhost:5000/shantiapp-4eae1/'\
#               'us-central1/users-updateUser'\
#               if local else 'https://us-central1-shantiapp-4eae1.'\
#               'cloudfunctions.net/users-updateUser'
#     if token is None:
#         token = get_test_token()
#     response = requests.post(
#         url=url,
#         json=data,
#         headers={'Authorization': 'Bearer ' + token}
#     )
#     if response.ok:
#         print('Success')
#         return True
#     else:
#         print(response.text)
#         return False


# def import_users_from_excel(file="Alumnos.xlsx", user_type="basic"):
#     password = 'shanti123'
#     phone = 65171311
#     wb = open_workbook(file)
#     sheet = wb.sheet_by_index(0)
#     print("Start Process")
#     for row in range(1, sheet.nrows):
#         name = sheet.cell_value(row, 3)
#         last_name = sheet.cell_value(row, 4)
#         email = (name.replace(" ", "").lower()
#                  + last_name.replace(" ", "").lower()
#                  + '@shanti.com')
#         try:
#             if (name == '' or last_name == ''):
#                 raise ValueError('Incorrect Name or Last Name')

#             user_record = auth.create_user(email=email, password=password)
#             user_id = user_record.uid
#             user = {
#                 'name': name,
#                 'lastName': last_name,
#                 'email': email,
#                 'type': user_type,
#                 'phone': phone
#             }
#             print(row, user)
#             db.reference('users').child(user_id).set(user)
#         except Exception as ex:
#             print(row, end=' ')
#             print(ex, end=': ')
#             print(name + " " + last_name, email)
#             pass
#     print("End Process")


# def delete_users(user_type='basic_users'):
#     print("Delete Users in Database")
#     users_db = db.reference('users').get()
#     for key, user in users_db.items():
#         is_user_type = util.user_types[user_type][user.get('type')]
#         if (is_user_type):
#             db.reference('users').child(key).delete()
#             print(user.get('email'), 'deleted')
def get_users(user_type='basic_users', user_name=None):
    users = {}
    users_db = db.reference('users').get()
    for key, user in users_db.items():
        is_user_type = user_types[user_type][user.get('type')]
        is_in_user_name = False
        if user.get('name') and user.get('lastName'):
            is_in_user_name = (util.check_in_string(user_name, user.get('name') + " " + user.get('lastName')))
        # print(is_user_type, is_in_user_name)
        if is_user_type and is_in_user_name:
            users[key] = user
    return users


def get_user_by_id(user_id=None):
    if user_id:
        return db.reference('users').child(user_id).get()
    return None


def get_user_by_name(user_name=None):
    if user_name:
        user = get_users(user_type='all_users', user_name=user_name)
        if len(user) == 1:
            return [*user.items()][0]
    return None, None
