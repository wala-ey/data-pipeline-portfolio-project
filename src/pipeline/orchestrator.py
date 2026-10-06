import root_logger
import logging
from extractor import Extract
from transformer import Transform
from loader import Load


class ETLPipeline:
    def __init__(self, source_db:str, target_db:str, csv_file_path:str):
        self.source_db = source_db
        self.target_db = target_db
        self.csv_file_path = csv_file_path
        self.logger = logging.getLogger(__name__)
    
    def orchestrate(self):
        self.logger.info("Starting ETL Pipeline Execution...")
        try: 
            raw_tables = Extract(self.source_db).run_extraction()
            staged_tables = Transform(raw_tables).run_transform()
            Load(staged_tables, self.target_db, self.csv_file_path).run_load()
            self.logger.info("Successfully executed ETL Pipeline")
        except Exception as e:
            self.logger.critical("Failed to run ETL Pipeline:\n    %s", e)
        
if __name__ == "__main__":
   root_logger.setup_logger()
   pipeline =  ETLPipeline("/home/wala-elsadig/Projects/subscriber-pipeline-starter-kit/dev/data/raw/cademycode.db", "/home/wala-elsadig/Projects/subscriber-pipeline-starter-kit/dev/data/processed/analytics_cademycode.db", "/home/wala-elsadig/Projects/subscriber-pipeline-starter-kit/dev/data/processed/analytics_cademycode.csv")
   pipeline.orchestrate()