# import requests
import openpyxl
from firebase_admin import auth
from firebase_admin import db
from _util import check_in_string

ALL_USERS = {
    'basic': True,
    'advanced': True,
    'admin': True
}
BASIC_USERS = {
    'basic': True,
    'advanced': False,
    'admin': False
}
ADVANCED_USERS = {
    'basic': False,
    'advanced': True,
    'admin': False
}
ADMIN_USERS = {
    'basic': False,
    'advanced': False,
    'admin': True
}
NOT_BASIC_USERS = {
    'basic': False,
    'advanced': True,
    'admin': True
}
USER_TYPES = {
    'all_users': ALL_USERS,
    'basic_users': BASIC_USERS,
    'advanced_users': ADVANCED_USERS,
    'admin_users': ADMIN_USERS,
    'not_basic_users': NOT_BASIC_USERS
}


class User:
    def __init__(self, name, last_name, email, user_type='basic', key=None, **kwargs):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.user_type = user_type
        self.image = kwargs.get('image')
        self.phone = kwargs.get('phone')
        self.info = kwargs.get('info')
        self._key = key
        self._password = kwargs.get('password')

    @property
    def key(self):
        return self._key

    @property
    def display_name(self):
        return self.name + " " + self.last_name

    @property
    def complete_profile(self):
        return self.name and self.last_name and self.email and self.phone

    def get_data(self):
        return {'name': self.name, 'lastName': self.last_name, 'email': self.email, 'type': self.user_type,
                'phone': self.phone, 'info': self.info, 'image': self.image, 'completeProfile': self.complete_profile}

    def upload(self):
        # TODO handle images
        self._validate()
        if self.key:
            db.reference('users').child(self.key).update(self.get_data())
        else:
            # TODO create user
            pass

    def delete(self):
        if self.key:
            db.reference('users').child(self.key).delete()
        self._delete_data()

    @staticmethod
    def load_from_db(key):
        user = db.reference('users').child(key).get()
        return User(user.get('name'), user.get('lastName'), user.get('email'), user.get('type'),
                    image=user.get('image'), phone=user.get('phone'), info=user.get('info'), key=key)

    def _delete_data(self):
        self._key = None
        self.name = None
        self.last_name = None
        self.email = None
        self.user_type = None
        self.image = None
        self.phone = None
        self.info = None
        self._password = None

    def _validate(self):
        if self.name is None or self.last_name is None or self.email is None or self.user_type is None:
            raise ValueError("Insufficient Data")


class Users:
    def __init__(self, users=None):
        if users:
            self._users = users
        else:
            self._users = []
        self._index = None

    @property
    def users(self):
        return self._users

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self.users):
            result = self.users[self._index]
            self._index += 1
            return result
        raise StopIteration

    def add_user(self, user):
        if user.key:
            self._users.append(user)
        else:
            raise ValueError("Insufficient Data")

    def load_from_db(self, complete_profile=True):
        users = []
        users_db = db.reference('users').get()
        if not users_db:
            raise ImportError('No users in database')
        for key, user in users_db.items():
            if complete_profile:
                if user.get('completeProfile'):
                    users.append(
                        User(user.get('name'), user.get('lastName'), user.get('email'), user.get('type'),
                             image=user.get('image'), phone=user.get('phone'), info=user.get('info'), key=key)
                    )
            else:
                users.append(
                    User(user.get('name'), user.get('lastName'), user.get('email'), user.get('type'),
                         image=user.get('image'), phone=user.get('phone'), info=user.get('info'), key=key)
                )
        self._users = users

    def load_from_file(self, file):
        users = []
        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        for row in range(2, sheet.max_row + 1):
            key = sheet.cell(row, 2).value
            name = sheet.cell(row, 3).value
            last_name = sheet.cell(row, 4).value
            email = sheet.cell(row, 5).value
            user_type = sheet.cell(row, 6).value
            phone = sheet.cell(row, 7).value
            info = sheet.cell(row, 8).value
            users.append(User(name, last_name, email, user_type, phone=phone, info=info, key=key))
        self._users = users

    def export_to_file(self, file, title="Users"):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = title
        cell_index = sheet.cell(1, 1, "N")
        cell_key = sheet.cell(1, 2, "KEY")
        cell_name = sheet.cell(1, 3, "NAME")
        cell_last_name = sheet.cell(1, 4, "LAST_NAME")
        cell_url = sheet.cell(1, 5, "EMAIL")
        cell_type = sheet.cell(1, 6, "TYPE")
        cell_phone = sheet.cell(1, 7, "PHONE")
        cell_info = sheet.cell(1, 8, "INFO")
        workbook.save(file)
        index = 2
        for user in self.users:
            cell_index = sheet.cell(index, 1, index - 1)
            cell_key = sheet.cell(index, 2, user.key)
            cell_name = sheet.cell(index, 3, user.name)
            cell_last_name = sheet.cell(index, 4, user.last_name)
            cell_url = sheet.cell(index, 5, user.email)
            cell_type = sheet.cell(index, 6, user.user_type)
            cell_phone = sheet.cell(index, 7, user.phone)
            cell_info = sheet.cell(index, 8, user.info)
            index += 1
            workbook.save(file)

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.key == user_id:
                return user
        return None

    def get_user_by_name_and_type(self, user_name='', user_type='basic_users', find_one=True):
        users = []
        for user in self.users:
            is_in_name = check_in_string(user_name, user.display_name)
            is_in_type = USER_TYPES[user_type][user.user_type]
            if is_in_name and is_in_type:
                users.append(user)
        if find_one:
            if len(users) > 1:
                return ValueError('To many coincidences')
            return users[0]
        return Users(users)

    def remove_user(self, user_id, remove_from_db=False):
        users = []
        for user in self.users:
            if user.key != user_id:
                users.append(user)
            else:
                if remove_from_db:
                    user.delete()
        self._users = users


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
