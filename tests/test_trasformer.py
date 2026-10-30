import unittest 
from pipeline.transformer import Transform
from datetime import datetime
from pandas import NA, DataFrame, Series


class TestTransform(unittest.TestCase):

    def setUp(self):
        self.raw_tables = {
            "cademycode_students": DataFrame(),
            "cademycode_courses": DataFrame(),
            "cademycode_stundent_jobs": DataFrame()
        }
        self.transformer = Transform(self.raw_tables)

    def tearDown(self):
        def self.raw_tables
    
    def test_isolate_tables_success(self):
        self.transformer.isolate_tables()
        expected = self.raw_tables.keys()

        for table in expected:
            self.assertHasAttr(table)
        

    def test_isolate_tables_error_handling(self):
        with self.assertRaises(Exception):
            self.transformer.isolate_tables()

    def test_isolate_tables_
    def test_transform_student_time_spent(self):
        #test_dummy
        self.raw_tables["cademycode_students"] = {"time_spent_hrs": ["1.5", "55.6", "5", "0.3"]}
        self.cademycode_students = self.raw_tables["cademycode_students"]
        expected = Series([90, 3336, 300, 1.5])
        actual = self.transformer.transform_student_time_spent()

        self.assert_series_equal(actual["time_spent_mins"], expected)
        #check self.transformer.cademycode_students["time_spent_mins"]  existcst and is equal to expected
        #test exections and failures work 
    def test_coerce_student_data_types(self):
        #set test df
        self.raw_tables["cademycode_students"] = {
            "dob": ["1996-05-12", "2000-12-30"],
            "job_id": ["1", "7"],
            "num_courses_taken": ["5", "12"],
            "current_career_path_id": ["2", "9"]
            }
        
        self.cademycode_students = self.raw_tables["cademycode_students"]

        actual_df = self.transformer.coerce_student_data_types()

        expected_dob =  Series([datetime(year=1996, month=5, day=12), datetime(year=2000, month=12, day=30)])
        expected_job_id = Series([1, 7])
        expected_num_courses_taken = Series([5, 12])
        expected_career_path_id = Series([2, 9])

        self.assert_series_equal(actual_df["dob"], expected_dob)
        self.assert_series_equal(actual_df["job_id"], expected_job_id)
        self.assert_series_equal(actual_df["num_courses_taken"], expected_num_courses_taken)
        self.assert_series_equla(actual_df["current_career_path_id", expected_career_path_id])


        #test exections and failures work 

    def test_transform_student_contact_info(self):
        self.raw_tables["cademycode_students"] = {"contact_info": [
            '{"mailing_address": "123 Main Street, Anywhere, Somewhere, 4567", "email": "john.doe@example.com"}'
            ]}

        self.cademycode_students = self.raw_tables["cademycode_students"]

        
        actual = self.transformer.transform_student_contact_info()
        
        expected_mailing_address = "123 Main Street, Anywhere, Somewhere, 4567"
        self.assert_series_equal(actual['mailing_address'], expected_mailing_address)

        expected_email = "john.doe@example.com"
        self.assert_series_equal(actual['email'], expected_email)
        #test exections and failures work 

    def test_normalise_name_to_first_and_last(self):
        self.raw_tables["cademycode_students"] = {"name": ["John Doe", "Mary-Ann Smith", "Li Boa Han", "Zain Al-Zainaby"]}
        
        self.cademycode_students = self.raw_tables["cademycode_students"]

        
        actual = self.transformer.normalise_name_to_first_and_last()
        expected_firstname = Series(["John", "Mary-Ann", "Li", "Zain"])
        expected_lastname = Series(["Doe", "Smith", "Boa Han", "Al-Zainaby"])

        self.assert_series_equal(actual["first_name"], expected_firstname)
        self.assert_series_equal(actual["last_name"], expected_lastname)
        #check the old column was deleted by trying to call it and asserting the correct error pops up

if __name__ == "__main__":
    unittest.main()