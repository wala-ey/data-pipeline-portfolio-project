# Cademycode ETL Pipeline

## Description
A robust, Python-based Extract, Transform, Load (ETL) pipeline designed to ingest, clean, normalize, and validate raw educational data. 

**Why build this:** 
Raw educational data is inherently messy—containing string-formatted dates, mixed numeric text, nested JSON contact info, and broken foreign key relationships. This pipeline automates the data wrangling process to transform raw data tables into clean, structured, and analysis-ready formats while implementing structured error logging and exception testing.

## Features
- **Automated Type Coercion:** Safely converts string dates into datetimes and parses numeric fields into nullable integers (`Int64`) to prevent silent data corruption.
- **JSON String Unpacking:** Dynamically flattens nested JSON `contact_info` strings into distinct, queryable DataFrame columns.
- **Foreign Key Integrity Validation:** Cross-references student records against course and job reference tables, safely isolating and neutralizing orphaned IDs with `NA`.
- **Structured Error Handling & Logging:** Implements comprehensive `try/except` blocks with custom error escalation and detailed debugging logs.

## Technologies Used
- **Python:** Core programming language.
- **Pandas:** For vectorized data manipulation, cleaning, and nullable extension dtypes (`Int64`).
- **Logging Module:** For tracking pipeline execution states and critical errors.
- **Git & GitHub:** For version control and project tracking.

## How to Use
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[wala]/data-pipeline-portfolio-project.git