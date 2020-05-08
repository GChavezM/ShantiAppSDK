from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from firebase_admin import db
from util import check_in_string, upload_image
from offices import Office
from users import User


class Program:
    def __init__(self, name, description, office, teacher, key=None):
        self.name = name
        self.description = description
        if not isinstance(office, Office) or not isinstance(teacher, User):
            raise ValueError('Incorrect Data')
        self.office = office
        self.teacher = teacher
        self._key = key

    @property
    def key(self):
        return self._key


# def manage_program(program_data=None, image=None, program_key=None, action=' create'):
#     if action == 'create' and validate_data(program_data, ' program'):
#         image_data = upload_image(image, 'program')
#         if image_data:
#             program_data['image'] = image_data
#         db.reference('programs').push(program_data)
#         print('Program Created')
#         return True
#     if action == 'update' and program_key:
#         image_data = upload_image(image, 'program')
#         if image_data:
#             program_data['image'] = image_data
#         db.reference('programs').child(program_key).update(program_data)
#         print('Program Updated')
#         return True
#     if action == 'delete' and program_key:
#         db.reference('programs').child(program_key).delete()
#         print('Program Deleted')
#         return True
#     print('Insufficient Data')
#     return False
#
#
# def get_programs(program_name=None):
#     programs = {}
#     programs_db = db.reference('programs').get()
#     if not programs_db:
#         return programs
#     for key, program in programs_db.items():
#         is_in_name = check_in_string(program_name, program.get('name'))
#         if is_in_name:
#             programs[key] = program
#     return programs
#
#
# def get_program_by_id(program_id=None):
#     if program_id:
#         return db.reference('program').child(program_id).get()
#     return None
