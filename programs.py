# from xlrd import open_workbook
from firebase_admin import db
from util import check_in_string


def get_programs(program_name=None):
    programs = {}
    programs_db = db.reference('programs').get()
    if not programs_db:
        return programs
    for key, program in programs_db.items():
        is_in_name = check_in_string(program_name, program.get('name'))
        if is_in_name:
            programs[key] = program
    return programs


def get_program_by_id(program_id=None):
    if program_id:
        return db.reference('program').child(program_id).get()
    return None
