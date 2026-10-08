import unittest 
from src.pipeline.transformer import Transform
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

    def test_isolate_tables(self):
        pass
 
    def test_transform_student_time_spent(self):
        #test_dummy
        self.transformer.cademycode_students["time_spend_hrs"] = ["1.5", "55.6", "5", "0.3"]
        expected = Series([90, 3336, 300, 1.5])
        self.transformer.transform_student_time_spent()

        self.assert_series_equal(self.transformer.cademycode_students["time_spend_hrs"], expected)
        #check self.transformer.cademycode_students["time_spent_mins"]  existcst and is equal to expected
        #test exections and failures work 
    def test_coerce_student_data_types(self):
        
        self.transformer.cademycode_students['dob'] = ["1996-05-12", "2000-12-30"]
        expected_dob =  Series([datetime(year=1996, month=5, day=12), datetime(year=2000, month=12, day=30)])
        self.assert_series_equal(self.transformer.cademycode_students['dob'], expected_dob)
        
        self.transformer.cademycode_students['job_id'] = ["1", "7"]
        expected_job_id = [1, 7]
        self.assert_series_equal(self.transformer.cademycode_students['job_id'], expected_job_id)
    
        self.transformer.cademycode_students['num_courses_taken'] = ["5", "12"]
        expected_num_courses_taken = Series([2, 12])
        self.assert_series_equal(self.transformer.cademycode_students['num_courses_taken'], expected_num_courses_taken)

        self.transformer.cademycode_students['current_career_path_id'] = ["6", "3"]
        expected_num_courses_taken = [6, 3]
        self.assert_series_equal(self.transformer.cademycode_students['current_career_path_id'], expected_num_courses_taken)
        #test exections and failures work 

    def test_transform_student_contact_info(self):
        self.transformer.cademycode_students['contact_info'] = ['{"mailing_address": "123 Main Street, Anywhere, Somewhere, 4567", "email": "john.doe@example.com"}']
        self.transformer.transform_student_contact_info()
        expected_mailing_address = "123 Main Street, Anywhere, Somewhere, 4567"
        self.assert_series_equal(self.transformer.cademycode_students['mailing_address'], expected_mailing_address)

        expected_email = "john.doe@example.com"
        self.assert_series_equal(self.transformer.cademycode_students['email'], expected_email)
        #test exections and failures work 

    def test_validate_fk_vals(self):
        self.transformer.cademycode_students["job_id"] = [1, 2, 3, 4 ,5]
        self.transformer.cademycode_students["job_id"] = [1, None, 4, 7, 8]
        expected_job_id = Series([1, None, 4, NA, NA])
        
        self.transformer.cademycode_courses["career_path_id"] = [6, 7, 8, 9, 10]
        self.transformer.cademycode_students["current_career_path_id"] = [1, None, 6, 7, 0]
        expected_current_career_course_id = Series([NA, None, 6, 7, NA])

        self.transformer.validate_fk_vals()
        self.assert_series_equal(self.transformer.cademycode_students["job_id"], expected_job_id)
        self.assert_series_equal(self.transformer.cademycode_students["current_career_path_id"], expected_current_career_course_id)

    def test_normalise_name_to_first_and_last(self):
        self.transformer.cademycode_students["name"] = ["John Doe", "Mary-Ann Smith", "Li Boa Han", "Zain Al-Zainaby"]
        expected_firstname = Series(["John", "Mary-Ann", "Li", "Zain"])
        expected_lastname = Series(["Doe", "Smith", "Boa Han", "Al-Zainaby"])
        self.transformer.normalise_name_to_first_and_last()
        self.assert_series_equal(self.transformer.cademycode_students["first_name"], expected_firstname)
        self.assert_series_equal(self.transformer.cademycode_students["last_name"], expected_lastname)
        #check the old column was deleted by trying to call it and asserting the correct error pops up

if __name__ == "__main__":
    unittest.main()