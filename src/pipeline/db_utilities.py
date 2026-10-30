import sqlite3 
import logging
from pathlib import Path



class SQLite3DatabaseConnection():
    """Context manager:
        Establishes a SQLite3 connection with the database, commits actions and closes the database.
    """
    def __init__(self, database):
        self.database = Path(database).resolve()
        self.connection: sqlite3.Connection | None = None
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        self.logger.info("Connecting to database '%s'...", self.database)
        try:
            self.connection = sqlite3.connect(self.database)
            if self.database.exists():
                self.logger.info("Successfully connected to existing database '%s'", self.database)
            else:
                self.logger.info("Successfully connected to new database '%s'", self.database)
        except sqlite3.Error as e:
            self.logger.critical("Failed to connect to database '%s' : %s", self.database,e)
            raise e
        
        return self.connection


    def __exit__(self, exc_type, exc_val, traceback):
        self.logger.debug("Exiting context manager for '%s'. Finalising transaction...", self.database)
        if self.connection:
            if exc_type is not None:   
                self.logger.error("Transaction aborted due to error: %s - %s", exc_type, exc_val)

                self.logger.info("Initialising rollback for '%s'", self.database)
                try:
                    self.connection.rollback()
                    self.logger.info("Rollback successful for '%s'", self.database)
                except sqlite3.Error as e:
                    self.logger.critical("Failed to rollback transacion on '%s': - %s", self.database, e)
                    raise e

            else:
                self.logger.debug("No errors detected. Commiting transaction...")
                try:
                    self.connection.commit()
                    self.logger.info("Transaction successfully committed to '%s'", self.database)
                except sqlite3.Error as e:
                    self.logger.critical("Failed to commit transaction to '%s': %s", self.database,e)
                    # attempt safety rollback if commit fails
                    try: 
                        self.connection.rollback()
                        self.logger.info("Rollback executed following commit failure")
                    except sqlite3.Error as e:
                        self.logger.critical("Rollback also FAILED! %s", e)
                        raise e

                    raise e
                
            self.logger.debug("Closing connection to '%s'...", self.database)            
            try:
                self.connection.close()
                self.logger.info("Connection to %s closed succesfully", self.database)
            except sqlite3.Error as e:
                self.logger.critical("Failed to close connection to database '%s': %s", self.database, e)
                raise e
            
        return False

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    with SQLite3DatabaseConnection("data/raw/cademycode.db") as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(cademycode_students);")
        print([row[1] for row in cur.fetchall()])



