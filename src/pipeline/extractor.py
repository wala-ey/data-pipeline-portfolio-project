from db_utilities import SQLite3DatabaseConnection
import logging
import pandas as pd



class Extract:
    """Takes the argument of a source database path and extracts the data from the
        tables in the source database into DataFrames
    """

    def __init__(self, source_db:str):
        self.source_db = source_db
        self.logger = logging.getLogger(__name__)

    def _query_souce_db(self, query:str, *args):
        """Helper function, Context managed connection to source database
            Args:
                query string
                params
                
            Returns:    
                query_output
        """
        with SQLite3DatabaseConnection(self.source_db) as conn:
            return pd.read_sql_query(query, conn, params=args)

    def get_table_names(self):
        """Extract of list table names in source database"""
        self.logger.debug("Extracting table names from database '%s'", self.source_db)
        try: 
            self.table_names = self._query_souce_db("""SELECT tbl_name FROM sqlite_master WHERE type = 'table';""")['tbl_name'].tolist()
            self.logger.debug("Successfully extracted following %d tables from database '%s':\n %s", len(self.table_names), self.source_db, self.table_names)
            return self
        except Exception as e:
            self.logger.critical("Failed to extract table names from database '%s':\n    %s", self.source_db, e)
            raise e
        
    def return_raw_tables(self):
        """Extract data from databse tables"""

        self.raw_tables = {}
        self.logger.debug("Extracting data from tables in source database '%s' to dataframes...", self.source_db)
        try:
            for table_name in self.table_names:
                self.raw_tables[table_name] = self._query_souce_db(f"SELECT * FROM {table_name};")
            self.logger.debug("Successfully extracted data from tables in source database '%s'", self.source_db)
            return self.raw_tables
        except Exception as e:
            self.logger.critical("Failed to extract data from tables in source database '%s':\n    %s", self.source_db, e)
            raise e
        
    
    def run_extraction(self):
        """Orchestration of Extract methods"""
        self.logger.info("Extracting data source database '%s'...", self.source_db)
        self.get_table_names()
        self.return_raw_tables()
        self.logger.info("Extraction Complete")

        return self.raw_tables

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    #quick test_run
    raw_tables = Extract("data/raw/cademycode.db").run_extraction()
    print(raw_tables)
    