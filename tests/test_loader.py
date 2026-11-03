import unittest
import tempfile
from datetime import datetime
from pandas import DataFrame
from pipeline.loader import Load

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.staged_tables = {
            'cademycode_students': DataFrame({
                'uuid': [1,2,3],
                'first_name': ['John Doe', 'Mary-Sue', 'Jake'],
                'last_name': ['Doe', 'Smith', 'the Snake']
                'dob': [datetime(year=1999, month=1, day=1), datetime(year=2000, month=12, day=30), None],
                'sex': ['Male', 'Female', 'Snake'],
                'mailing_address': ["123 Main Street, Anywhere, Somewhere, 4567", "456 Elm Street, Springfield, IL, 62701", None],
                'email': ["john.doe@example.com", "sue@example.com", None]
                'job_id': [1, 2, None],
                'num_course_taken': [1, 2, None],
                'current_career_path_id': [1, 2, None],
                'time_spent_mins': [8418, 15600, None]
            }),
            'cademycode_courses': DataFrame({
                'careerpath_id': ['1', '2' ,'3'],
                'career_path_name': ['data scientist', 'ux/ui designer', 'iOS developer'],
                'hours_to_complete': ['20', '25', '30']
                }),
            'cademycode_student_jobs': DataFrame({
                'job_id': ['1', '2' ,'3'], 
                'job_category': ['software engineer', 'financial services', 'creative'],
                'avg_salary': ['65000', '70000', '60000']
                })
        }
        self.target_db = 'dummy.db'
        self.csv_file_path = 'dummy.csv'

        self.loader = Load(self.staged_tables)

    def tearDown(self):
        pass 
    