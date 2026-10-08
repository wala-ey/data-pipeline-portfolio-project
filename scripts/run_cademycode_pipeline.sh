#!/bin/bash
#move updated files from working directory to production directory 

logs=/dev/logs/cademycode_ETL_logs.log
#run the pipeline
# read the previous version from the change log and compare it ot current 
# if the database has a different verson copy to /opt/database (replacing old one)
