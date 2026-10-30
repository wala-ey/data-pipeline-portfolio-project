from pathlib import Path
import unittest
from pipeline.extractor import Extract
from pandas import DataFrame, Series
from pandas.testing import assert_frame_equal
from unittest.mock import Mock, patch, MagicMock
# mock _query_source_db so as not to actually connect to a db
# side_effect tests the error handling
# for dunder methods use MagicMock (e.g. context manager)
class TestExtract(unittest.TestCase):
    "Test the extraction works"

    def setUp(self):
        self.extractor = Extract("dud_path.db")

    def tearDown(self):
        del self.extractor
###################################TEST TABLE NAME EXTRACTION [get_table_names]###################################
    @patch.object(Extract, '_query_source_db')
    def test_get_table_names_success(self, mock_query_source_db):
        mock_query_source_db.return_value = DataFrame({'tbl_name': ["table_x"]})
        self.extractor.get_table_names()
        actual = self.extractor.table_names
        expected = ["table_x"]
        
        self.assertEqual(expected, actual)

    @patch.object(Extract, '_query_source_db')
    def test_get_table_names_exception_handling(self, mock_query_source_db):
        mock_query_source_db.side_effect = Exception
        with self.assertRaises(Exception):
            self.extractor.get_table_names()

    @patch.object(Extract, '_query_source_db')
    def test_get_table_names_logs_error_messages(self, mock_query_source_db):
        pass
###################################TEST RAW TABLES RETURNED [return_raw_tables]###################################
    @patch.object(Extract, '_query_source_db')
    def test_return_raw_tables_success(self, mock_query_source_db):
        mock_query_source_db.return_value = DataFrame({'col_x': [1, 2, 3]})
        self.extractor.table_names = ['table_x']
        self.extractor.return_raw_tables()
        actual = self.extractor.raw_tables
        expected = {'table_x': DataFrame({'col_x': [1, 2, 3]})}

        self.assertEqual(actual.keys(), expected.keys())

        assert_frame_equal(actual['table_x'], expected['table_x'])

    @patch.object(Extract, '_query_source_db')
    def test_return_raw_tables_exception_handling(self, mock_query_source_db):
        mock_query_source_db.side_effect = Exception
        self.extractor.table_names = ['table_x']
        with self.assertRaises(Exception):
            self.extractor.return_raw_tables()

    @patch.object(Extract, '_query_source_db')
    def test_return_raw_tables_logs_error_message(self, mock_query_source_db):
        pass
###################################TEST ORCHESTRATION [run_extraction]###################################
    @patch.object(Extract, 'get_table_names')
    @patch.object(Extract, 'return_raw_tables')
    def test_run_extraction_success(self, mock_return_raw_tables, mock_get_table_names):
        mock_get_table_names.return_value = {'table_x', 'table_y'}
        mock_return_raw_tables.return_value = {'table_x': MagicMock(), 'table_y': MagicMock()}

        self.extractor.run_extraction()

        mock_get_table_names.assert_called_once()
        mock_return_raw_tables.assert_called_once()

    @patch.object(Extract, 'get_table_names')
    @patch.object(Extract, 'return_raw_tables')
    def test_run_extraction_get_table_names_exception_handling(self, mock_return_raw_tables, mock_get_table_names):
        mock_get_table_names.side_effect = Exception
        with self.assertRaises(Exception):
            self.extractor.run_extraction()

        mock_get_table_names.assert_called_once()
        mock_return_raw_tables.assert_not_called()

    @patch.object(Extract, 'get_table_names')
    @patch.object(Extract, 'return_raw_tables')
    def test_run_extraction_retun_raw_tables_excepion_handling(self, mock_return_raw_tables, mock_get_table_names):
        mock_get_table_names.return_value = ['table_x']
        mock_return_raw_tables.side_effect = Exception

        with self.assertRaises(Exception):
            self.extractor.run_extraction()

        mock_get_table_names.assert_called_once()
        mock_return_raw_tables.assert_called_once()

    


    @patch.object(Extract, 'get_table_names')
    @patch.object(Extract, 'return_raw_tables')
    def test_run_orchestration_logs_error_message(self, mock_returrn_raw_tables, mock_get_table_names):
        pass