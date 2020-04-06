from xlrd import open_workbook
from firebase_admin import db
from util import validate_data, check_in_string


def manage_office(office_data=None, office_key=None, action='create'):
    if action == 'create' and validate_data(office_data, 'office'):
        db.reference('offices').push(office_data)
        print('Office Created')
        return True
    if action == 'update' and office_key:
        db.reference('offices').child(office_key).update(office_data)
        print('Office Updated')
        return True
    if action == 'delete' and office_key:
        db.reference('offices').child(office_key).delete()
        print('Office Deleted')
        return True
    print('Insufficient Data')
    return False


def get_offices(office_name=None):
    offices = {}
    offices_db = db.reference('offices').get()
    if not offices_db:
        return offices
    for key, office in offices_db.items():
        is_in_name = check_in_string(office_name, office.get('name'))
        if is_in_name:
            offices[key] = office
    return offices


def get_office_by_id(office_id=None):
    if office_id:
        return db.reference('offices').child(office_id).get()
    return None


def get_office_by_name(office_name=None):
    if office_name:
        office = get_offices(office_name)
        print(len(office))
        if len(office) == 1:
            return [*office.items()][0]
    return None, None


def import_offices_from_excel(file='Sucursales.xlsx'):
    workbook = open_workbook(file)
    sheet = workbook.sheet_by_index(0)
    print('Rows:', sheet.nrows)
    print('Columns:', sheet.ncols)
    db.reference('offices').delete()
    for row in range(1, sheet.nrows):
        name = sheet.cell_value(row, 0)
        address = sheet.cell_value(row, 1)
        google_map = sheet.cell_value(row, 2)
        office = {
            'name': name,
            'address': address,
            'url': google_map
        }
        print(office)
        manage_office(office)
