import pandas as pd
import logging
import json 

class Transform:
    """Transforms raw DataFrames into Normalised DataFrames"""
    def __init__(self, raw_tables: dict):
        self.raw_tables = raw_tables
        self.staged_tables: dict[str, pd.DataFrame] = {}
        self.cademycode_students: pd.DataFrame | None = None
        self.logger = logging.getLogger(__name__)

    def isolate_tables(self):
        """Isolate tables for data transformation"""
        self.logger.debug("Isolating table dataframes from dictionary for cleaning, wrangling and normalisation")
        try:
            for table, df in self.raw_tables.items():
                setattr(self, table, df)
            self.logger.debug("Successfully isolated tabbles and dataframes")
        except Exception as e:
            self.logger.critical("Failed to isolate tables dataframes from raw_tables '%s':\n    %s", self.raw_tables.keys(), e)
            raise e
        return self

    def transform_student_time_spent(self):
        """Converts string 'time_spent_hrs' to 'time_spent_mins' integer (Int64)
        """
        self.logger.debug("Transforming string hours to integer minutes")
        try:
            #time_spend_hrs to to minutes and save as integer to improve clarity and reduce RAM usage
            self.cademycode_students["time_spent_mins"] = (pd.to_numeric(self.cademycode_students["time_spent_hrs"]) * 60).round().astype('Int64')
            self.logger.debug("Successfully converted 'time_spent_hrs' string values to integer minutes in 'time_spent_mins'")
            try:          
                del self.cademycode_students["time_spent_hrs"]
                self.logger.debug("Deleted old formated 'time_spend_hrs' column")
            except Exception as e:
                self.logger.critical("Failed to delete old time column (time_spent_hrs):\n    %s", e)
        except Exception as e:
            self.logger.error("Failed to convert 'time_spent_hrs' string values to integer minutes in 'time_spent_mins':\n    %s", e)
            raise e
        
        return self

    def coerce_student_data_types(self):
        """Coerce datatypes"""
    
        try:
            self.cademycode_students['dob'] = pd.to_datetime(self.cademycode_students['dob'], format="%Y-%m-%d")
        except Exception as e:
            self.logger.error("Failed to set 'dob' datatype to datetime:\n    %s", e)

        try:
            for col in ["job_id", "num_course_taken", "current_career_path_id"]:
                self.cademycode_students[col] = pd.to_numeric(self.cademycode_students[col], errors="coerce")
            self.logger.debug("Datatypes of job_id, num_course_taken, current_career_path_id columns set to integers")
        except Exception as e:
            self.logger.error("Failed to change datatype for the columns :\n%s \n    %s", ["job_id", "num_course_taken", "current_career_path_id"], e)

        return self
        
    
    def transform_student_contact_info(self):
        """"Unpacks JSON-formatted 'contact_info' strings into distinct DataFrame columns.
            
            Arg:
                self.cademycode_students (pd.DataFrame): The isolated cademycode_students DataFrame
            
            Return:
                self.cademycode_students (pd.DataFrame): DataFrame with 'contact_info' dropped and unpacked keys as columns
        """
        #split the json contact_info into distinct columns 
        self.logger.debug("Parsing JSON strings into disitinct columns")
        def safe_json_loading(val):
            """Safe json loading
                Arg:
                    string

                Return:
                    dictionary
            """
            try:
                loaded = json.loads(val)
                return loaded

            except (json.JSONDecodeError, ValueError, TypeError) as e:
                return {}
        try:
            new_contact_info = self.cademycode_students['contact_info'].apply(safe_json_loading)
            self.logger.debug("Successfully parsed contact_info JSON strings into dictionary objects")

        except ValueError as v:
            self.logger.error("Failed to parse contact_info JSON strings into dictionaries:\n    %s", v)

        try:
            new_contact_info_df = pd.json_normalize(new_contact_info)
            self.cademycode_students = pd.concat([self.cademycode_students.drop(columns=["contact_info"]), new_contact_info_df], axis=1)
            self.logger.debug("Successfully unpacked 'contact_info' dictionary keys into distinct columns")
        except Exception as e:
            self.logger.error("Failed to unpack 'contact_info' dictionary keys into distinct columns:\n    %s", e)
            raise e
        return self



    def drop_null_n_duplicates(self):
        """Cleans the dataframes
        Returns:
            dict[str, Dataframe]: cleaned dataframes"""

        self.logger.debug("Overwriting dataframes with cleaned data...")

        for name, dataframe in self.raw_tables.items():
            self.raw_tables[name] = dataframe.drop_duplicates()
        self.logger.debug("Dropped all duplicate rows from all dataframes")

    def validate_fk_vals(self):
        """Ensures foreign key values are valid, if not save as Na"""
        self.logger.debug("Ensuring all foregin keys are valid")
        try:
            valid_job_ids = set(self.cademycode_student_jobs["job_id"])
            invalid_job_ids_mask = (
                ~self.cademycode_students["job_id"].isin(valid_job_ids)
                & self.cademycode_students["job_id"].notna()
            )
            self.cademycode_students.loc[invalid_job_ids_mask, "job_id"] = pd.NA
            if invalid_job_ids_mask.sum() > 0:
                self.logger.debug("Relpaced %d invalid job_ids with NA", invalid_job_ids_mask.sum())

        except Exception as e:
            self.logger.error("Failed to ensure all entries in foreign key column 'job_id' are valid:\n    %s", e)
        try:
            valid_course_ids = set(self.cademycode_courses["career_path_id"])
            invalid_course_ids_mask = (
                ~self.cademycode_students["current_career_path_id"].isin(valid_course_ids) 
                & self.cademycode_students["current_career_path_id"].notna()
            )

            self.cademycode_students.loc[invalid_course_ids_mask, "current_career_path_id"] = pd.NA
            if invalid_course_ids_mask.sum() > 0:
                self.logger.debug("Replaced %d invalid current_career_path_id with NA", invalid_course_ids_mask.sum())
        except Exception as e:
            self.logger.error("Failed to ensure all entries in foreign key column 'current_career_path_id' are valid:\n    %s", e)

        return self

    def normalise_name_to_first_and_last(self):
        """normalise name into first and last"""
        self.logger.debug("Splitting full name...")
        try: 
            split_names = self.cademycode_students["name"].str.split(" ", n=1, expand=True)
            del self.cademycode_students["name"]

            self.cademycode_students.insert(1, "first_name", split_names[0])
            self.cademycode_students.insert(2, "last_name", split_names[1])
            self.logger.debug("'name' column normalise into 'fist_name' and 'last_name' columns")
        except Exception as e:
            self.logger.critical("Failed to normalise 'name' column into 'first_name' and 'last_name' columns:\n%s", e)

    def return_staged_tables(self):
        """Load cleans df to clean dict"""
        self.logger.debug("")
        try:
            for table_name in self.raw_tables.keys():
                self.staged_tables[table_name] = getattr(self, table_name)
            self.logger.debug("Successfully set staged_tables")
        except Exception as e:
            self.logger.critical("Failed to set staged_tables:\n    %s", e)
            raise e
        return self.staged_tables


    def run_transform(self):
        self.logger.info("Transforming data...")
        self.isolate_tables()
        self.transform_student_time_spent()
        self.coerce_student_data_types()
        self.transform_student_contact_info()
        self.drop_null_n_duplicates()
        self.validate_fk_vals()
        self.normalise_name_to_first_and_last()
        self.return_staged_tables()
        self.logger.info("Transformation complete")

        return self.staged_tables

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s , %(message)s, %(lineno)d]")
    #quick test run
    raw_tables = {
        "cademycode_students": pd.DataFrame({
            "uuid": [1],
            "name": ["John Doe"], 
            "dob":["2000-05-15"],
            "sex": ["M"],
            "contact_info": ['{"mailing_address": "123 somestreet, Anywhere, Earth", "email": "john.doe@example.com"}'],
            "job_id": ["4"],
            "num_course_taken": ["6"],
            "current_career_path_id": ["3"],
            "time_spent_hrs": ["200"]
            }),
        "cademycode_courses": pd.DataFrame({
            "id": [1, 2, 3, 3, 4],
            "course_name": ["a", "b", "c", "c", "d"]
        }),
        "cademycode_student_jobs": pd.DataFrame({
            "id": [1, 1, 3, 3, 4],
            "job_name": ["a", "a", "c", "c", "d"]
        })
    }
    processed_tables = Transform(raw_tables).run_transform()
    print(processed_tables)
