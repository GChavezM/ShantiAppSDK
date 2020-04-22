from xlrd import open_workbook
from firebase_admin import db
from _util import check_in_string


class Office:
    def __init__(self, name, address, url=None, key=None):
        self._name = name
        self._address = address
        self._google_map_url = url
        self._key = key

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def google_map_url(self):
        return self._google_map_url

    @google_map_url.setter
    def google_map_url(self, url):
        self._google_map_url = url

    @property
    def key(self):
        return self._key

    def get_data(self):
        return {'name': self.name, 'address': self.address, 'url': self.google_map_url}

    def upload(self):
        self._validate()
        if self.key is not None:
            raise ValueError('Office key already exists')
        self._key = db.reference('offices').push(self.get_data()).key

    def update(self):
        self._validate()
        db.reference('offices').child(self.key).update(self.get_data())

    def delete(self):
        if self.key:
            db.reference('offices').child(self.key).delete()
        self._delete_data()

    def _delete_data(self):
        self._key = None
        self._name = None
        self._address = None
        self._google_map_url = None

    def _validate(self):
        if self.name is None or self.address is None:
            raise ValueError("Insufficient Data")


class Offices:
    def __init__(self, offices=None):
        if offices:
            self._offices = offices
        else:
            self._offices = []

    @property
    def offices(self):
        return self._offices

    def add_office(self, office):
        if office.key:
            self._offices.append(office)
        else:
            raise ValueError("Insufficient Data")

    # def import_from_file_to_db(self, file):
    #     workbook = open_workbook(file)
    #     sheet = workbook.sheet_by_index(0)
    #     for row in range(1, sheet.nrows):
    #         name = sheet.cell_value(row, 0)
    #         address = sheet.cell_value(row, 1)
    #         url = sheet.cell_value(row, 2)
    #         office = Office(name, address, url)
    #         office.upload()
    #         self.add_office(office)

    def load_from_db(self):
        offices = []
        offices_db = db.reference('offices').get()
        if not offices_db:
            raise ImportError('No offices in database')
        for key, office in offices_db.items():
            office = Office(office['name'], office['address'], office['url'], key=key)
            offices.append(office)
        self._offices = offices

    def load_from_file(self, file):
        offices = []
        workbook = open_workbook(file)
        sheet = workbook.sheet_by_index(0)
        for row in range(1, sheet.nrows):
            key = sheet.cell_value(row, 0)
            name = sheet.cell_value(row, 1)
            address = sheet.cell_value(row, 2)
            url = sheet.cell_value(row, 3)
            office = Office(name, address, url, key=key)
            offices.append(office)
        self._offices = offices

    def export_to_file(self, file):
        workbook = open_workbook(file)
        sheet = workbook.sheet_by_index(0)
        for office in self.offices:
            # TODO write offices to file
            pass

    def get_office_by_id(self, office_id):
        for office in self.offices:
            if office.key == office_id:
                return office
        return None

    def get_office_by_name(self, office_name, find_one=True):
        offices = []
        for office in self.offices:
            is_in_name = check_in_string(office_name, office.name)
            if is_in_name:
                offices.append(office)
        if offices is None:
            return None
        if find_one:
            if len(offices) > 1:
                raise ValueError('To many coincidences')
            return offices[0]
        return Offices(offices)

    def remove_office(self, office_id, remove_from_db=False):
        offices = []
        for office in self.offices:
            if office.key != office_id:
                offices.append(office)
            else:
                if remove_from_db:
                    office.delete()
        self._offices = offices
