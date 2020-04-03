import util
from xlrd import open_workbook
from firebase_admin import db


def get_offices(office_name=None):
    offices = {}
    offices_db = db.reference('offices').get()
    for key, office in offices_db.items():
        is_in_name = util.check_in_string(office_name, office.get('name'))
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
    wb = open_workbook(file)
    sheet = wb.sheet_by_index(0)
    print('Rows:', sheet.nrows)
    print('Columns:', sheet.ncols)
    db.reference('offices').delete()
    for r in range(1, sheet.nrows):
        name = sheet.cell_value(r, 0)
        address = sheet.cell_value(r, 1)
        google_map = sheet.cell_value(r, 2)
        office = {
            'name': name,
            'address': address,
            'url': google_map
        }
        print(office)
        db.reference('offices').push(office)
