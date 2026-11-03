import unittest 
from pipeline.transformer import Transform
from datetime import datetime
from pandas import NA, DataFrame, Series
from pandas.testing import assert_series_equal
from unittest.mock import MagicMock, patch


class TestTransform(unittest.TestCase):

    def setUp(self):
        self.raw_tables = {
            'cademycode_students': DataFrame({
                'uuid': [1,2,3],
                'name': ['John Doe', 'Mary-Sue Smith', 'Jake the Snake'],
                'dob': ['1999-01-01', '2000-12-30', 'i_wasn\'t_born_yesterday'],
                'sex': ['Male', 'Female', 'Snake'],
                'contact_info': [
                    '{"mailing_address":"123 Main Street, Anywhere, Somewhere, 4567","email":"john.doe@example.com"}',
                    '{"mailing_address":"456 Elm Street, Springfield, IL, 62701","email":"sue@example.com"}',
                    'The Amazon'
                    ],
                'job_id': ['1','2','hss'],
                'num_course_taken': ['1', '2', 'hss'],
                'current_career_path_id': ['1', '2', 'hss'],
                'time_spent_hrs': ['140.3', '260', 'asleep'],
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
        self.transformer = Transform(self.raw_tables)
        self.transformer.cademycode_students = self.raw_tables['cademycode_students']


    def tearDown(self):
        del self
########################################################TEST TABLE ISOLATION########################################################
    def test_isolate_tables_success(self):
        expected = self.raw_tables.keys()
        actual = self.transformer.isolate_tables()
        for table in expected:
            self.assertHasAttr(actual, table)
        

    def test_isolate_tables_error_handling(self):
        del self.transformer.raw_tables
        with self.assertRaises(Exception):
            self.transformer.isolate_tables()

    def test_isolate_tables_logs_error_message(self):
        pass
########################################################TEST DATA TRANSFORMATION########################################################
############################TEST [calculate_time_spent]############################
    def test_calculate_time_spent_success(self):
        actual = self.transformer.cademycode_students
        expected = Series([8418, 15600, None], dtype='Int64', name="time_spent_mins")
        self.transformer.calculate_time_spent()
        assert_series_equal(actual["time_spent_mins"], expected)
     
    def test_calculate_spent_error_handling(self):
        del self.transformer.cademycode_students['time_spent_hrs']
        with self.assertRaises(Exception):
            self.transformer.calculate_time_spent()

    def test_calculate_time_spent_logs_error_message(self):
        pass
############################TEST [parse_dob]############################
    def test_parse_dob_success(self):
        actual = self.transformer.cademycode_students  
        self.transformer.parse_dob()
        expected_dob =  Series([datetime(year=1999, month=1, day=1), datetime(year=2000, month=12, day=30), None], name='dob')
        assert_series_equal(actual["dob"], expected_dob)

    def test_parse_dob_error_handling(self):
        del self.transformer.cademycode_students['dob']
        with self.assertRaises(Exception):
            self.transformer.parse_dob()

    def test_parse_dob_logs_error_message(self):
        pass
############################TEST [parse_numeric_feilds]############################

    def test_parse_numeric_feilds_success(self):
        actual = self.transformer.cademycode_students  
        self.transformer.parse_numeric_feilds()
        expected_job_id = Series([1, 2, None], dtype='Int64', name='job_id')
        expected_num_course_taken = Series([1, 2, None], dtype='Int64', name='num_course_taken')
        expected_career_path_id = Series([1, 2, None], dtype='Int64', name='current_career_path_id')

        assert_series_equal(actual["job_id"], expected_job_id)
        assert_series_equal(actual["num_course_taken"], expected_num_course_taken)
        assert_series_equal(actual["current_career_path_id"], expected_career_path_id)


    def test_parse_numeric_feilds_error_handling(self):
        del self.transformer.cademycode_students['job_id']
        with self.assertRaises(Exception):
            self.transformer.parse_numeric_feilds()

    def test_parse_numeric_feilds_logs_error_message(self):
        pass

############################TEST [parse_contact_info]############################
    def test_parse_contact_info_success(self):
        actual = self.transformer.cademycode_students
        self.transformer.parse_contact_info()
        expected_mailing_address = Series(["123 Main Street, Anywhere, Somewhere, 4567", "456 Elm Street, Springfield, IL, 62701", None], name='mailing_address')
        assert_series_equal(actual['mailing_address'], expected_mailing_address)

        expected_email = Series(["john.doe@example.com", "sue@example.com", None], name='email')
        assert_series_equal(actual['email'], expected_email)

    def test_parse_contact_info_error_handling(self):
        del self.transformer.cademycode_students['contact_info']
        with self.assertRaises(Exception):
            self.transformer.parse_contact_info()

    def test_parse_student_contact_info_logs_error_message(self):
        pass


############################TEST [normalise_name_to_first_and_last]############################
    def test_normalise_name_to_first_and_last(self):
        actual = self.transformer.cademycode_students
        self.transformer.normalise_name_to_first_and_last()
        expected_firstname = Series(["John", "Mary-Sue", "Jake"], name='first_name')
        expected_lastname = Series(["Doe", "Smith", "the Snake"], name='last_name')

        assert_series_equal(actual["first_name"], expected_firstname)
        assert_series_equal(actual["last_name"], expected_lastname)
        #check the old column was deleted by trying to call it and asserting the correct error pops up
    def test_normalise_name_to_first_and_last_error_handling(self):
        del self.transformer.cademycode_students['name']
        with self.assertRaises(Exception):
            self.transformer.normalise_name_to_first_and_last()

    def test_normalise_name_to_first_and_last_logs_error_mesage(self):
        pass
########################################################TEST ORCHESTRATION########################################################
    @patch.object(Transform, 'normalise_name_to_first_and_last')
    @patch.object(Transform, 'return_staged_tables')
    @patch.object(Transform, 'validate_fk_values')
    @patch.object(Transform, 'drop_null_and_duplicates')
    @patch.object(Transform, 'parse_contact_info')
    @patch.object(Transform, 'parse_numeric_feilds')
    @patch.object(Transform, 'parse_dob')
    @patch.object(Transform, 'calculate_time_spent')
    @patch.object(Transform, 'isolate_tables')
    def test_run_transformation_success(
        self,
        mock_isolate_tables,
        mock_calculate_time_spent,
        mock_parse_dob,
        mock_parse_numeric_feilds,
        mock_parse_contact_info,
        mock_drop_null_and_duplicates,
        mock_validate_fk_values,
        mock_normalise_name_to_first_and_last,
        mock_return_staged_tables
    ):
        mocked_methods = [
            ('isolate_tables', mock_isolate_tables),
            ('calculate_time_spent', mock_calculate_time_spent),
            ('parse_dob', mock_parse_dob),
            ('parse_numeric_feilds', mock_parse_numeric_feilds),
            ('parse_contact_info', mock_parse_contact_info),
            ('drop_null_and_duplicates', mock_drop_null_and_duplicates),
            ('validate_fk_values', mock_validate_fk_values),
            ('return_staged_tables', mock_return_staged_tables),
            ('normalise_name_to_first_and_last', mock_normalise_name_to_first_and_last)
        ]

        for mocked_method in mocked_methods:
            mocked_method[1].return_value = MagicMock()
        
        self.transformer.run_transformation()

        for  mocked_method_name, mocked_method in mocked_methods:
            mocked_method.assert_called_once()

    @patch.object(Transform, 'normalise_name_to_first_and_last')
    @patch.object(Transform, 'return_staged_tables')
    @patch.object(Transform, 'validate_fk_values')
    @patch.object(Transform, 'drop_null_and_duplicates')
    @patch.object(Transform, 'parse_contact_info')
    @patch.object(Transform, 'parse_numeric_feilds')
    @patch.object(Transform, 'parse_dob')
    @patch.object(Transform, 'calculate_time_spent')
    @patch.object(Transform, 'isolate_tables')
    def test_run_transformation_error_handling(
        self,
        mock_isolate_tables,
        mock_calculate_time_spent,
        mock_parse_dob,
        mock_parse_numeric_feilds,
        mock_parse_contact_info,
        mock_drop_null_and_duplicates,
        mock_validate_fk_values,
        mock_normalise_name_to_first_and_last,
        mock_return_staged_tables
    ):
        mocked_methods = [
            ('isolate_tables', mock_isolate_tables),
            ('calculate_time_spent', mock_calculate_time_spent),
            ('parse_dob', mock_parse_dob),
            ('parse_numeric_feilds', mock_parse_numeric_feilds),
            ('parse_contact_info', mock_parse_contact_info),
            ('drop_null_and_duplicates', mock_drop_null_and_duplicates),
            ('validate_fk_values', mock_validate_fk_values),
            ('return_staged_tables', mock_return_staged_tables),
            ('normalise_name_to_first_and_last', mock_normalise_name_to_first_and_last)
        ]
        for failing_step_name, failing_mock in mocked_methods:
            with self.subTest(failing_step=failing_step_name):
                for _, m in mocked_methods:
                    m.reset_mokc()
                    m.return_value = MagicMock()

                failing_mock.side_effect = Exception

                with self.assertRaises(Exception):
                    self.transformer.run_transformation()

                failing_mock.side_effect = None
