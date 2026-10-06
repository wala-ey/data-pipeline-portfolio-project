from db_utilities import SQLite3DatabaseConnection
import pandas as pd 
import logging

class Load:
    """Load clean data onto new database and csv file"""
    def __init__(self, staged_tables: dict, target_db: str, csv_file_path: str):
        self.staged_tables = staged_tables
        self.target_db = target_db
        self.csv_file_path = csv_file_path
        self.logger = logging.getLogger(__name__)

    def _query_target_db(self, query:str , *args):
        """Helper function, queries target database"""
        with SQLite3DatabaseConnection(self.target_db) as conn:
            if query.strip().upper().startswith(('CREATE', 'INSERT', 'UPDATE', 'DROP', 'DELETE')):
                cursor = conn.cursor()
                cursor.execute(query, args)
                return None
            
            return pd.read_sql_query(query, conn, params=args)

    def load_to_target_db(self):
        """Load cleaned dataframes to target data base"""
        self.logger.debug("Loading clean dataframes to target database '%s'", self.target_db)
        try:
            with SQLite3DatabaseConnection(self.target_db) as conn:
                for table_name, df in self.staged_tables.items():
                    df.to_sql(table_name, conn, if_exists='replace')
            self.logger.debug("Successfully uploaded clean data to database '%s'", self.target_db)
        except Exception as e:
            self.logger.critical("Failed to upload clean data to databae '%s':\n    %s", self.target_db, e)
            raise e

    def create_analytics_view(self):
        """Created a view of joined tables for CSV extraction an analytics"""
        self.logger.debug("create analytics view in target database '%s'", self.target_db)
        query = """CREATE VIEW IF NOT EXISTS analytics_joined_cademycode_view AS
        SELECT 
            s.uuid,
            s.first_name,
            s.last_name,
            s.dob,
            s.sex,
            s.job_id,
            s.num_course_taken,
            s.current_career_path_id,
            s.time_spent_mins,
            s.mailing_address,
            s.email,
            c.career_path_name ,
            c.hours_to_complete ,
            j.job_category ,
            j.avg_salary
        FROM cademycode_students s 
        LEFT JOIN cademycode_courses c
        ON s.current_career_path_id = c.career_path_id
        LEFT JOIN cademycode_student_jobs j
        ON s.job_id = j.job_id;
        """
        try:
            self._query_target_db(query)
            self.logger.debug("Successfully created analytics view in databse '%s'", self.target_db)
        except Exception as e:
            self.logger.critical("Failed to create analytics view in target database '%s':\n    %s", self.target_db, e)
            raise e
            
    def load_to_csv_file_path(self):
        """Load analytics view from target database onto csv file"""
        self.logger.debug("Loading analytics view onto csv...")
        try:
            self._query_target_db("SELECT * FROM analytics_joined_cademycode_view").to_csv(self.csv_file_path)
            self.logger.debug("Successfully loaded analytics view from database '%s' to CSV file '%s'",self.target_db, self.csv_file_path)
        except Exception as e:
            self.logger.critical("Failed to load analytics view from database '%s' to CSV ile '%s':\n    %s", self.target_db, self.csv_file_path, e)

    def run_load(self):
        self.logger.info("Loading Data to target...")
        self.load_to_target_db()
        self.create_analytics_view()
        self.load_to_csv_file_path()
        self.logger.info("Load complete")
