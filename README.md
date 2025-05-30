## Technical Task

### Description

The task is to implement an ETL (Extract, Transform, Load) client in `Python3` that will interact with csv files.

Preferred Python version >= 3.9 (https://devguide.python.org/versions/)

You may only use appropriately licensed and open source 3rd party libraries when necessary.

### Task details

1. Write a completely asynchronous backend application using the FastAPI framework.
2. Each API endpoint must be secured, for example using OAuth2 with Password (and hashing), Bearer with JWT tokens.
   It's possible to use a dictionary instead of creating a table in the database to simplify things.
3. Extract data from metabolites csv file `MetabolitesData_inputDataForTEst.csv` available in the data folder.
4. Ensure column naming and column type are adhering proper naming strategy and types: see the excel file `MetabolitesData_Upload_template.xlsx` ('Data guidelines' tab) in the data folder. 

In addition, you must check that:
- 1 feature can only be linked to a single ID_InChI/CAS_number
- 1 ID_InChI/CAS_number can only be linked to a single feature
- Either an ID_InChI or CAS_number must be entered.
- 1 feature can only be linked to one method
- Identification_level: Non mandatory, if not filled, automatically set to 3
- The rules are also available in the excel file `MetabolitesData_Upload_template.xlsx` ('Data guidelines' tab) in the data folder.

5. Load the data to a Postgres database (with the help of an ORM for example)
6. Finally, create a CRUD to interact with the metabolite data

Do not change the files in the `/data` .

### Assessment

The task will be assessed on design, implementation, functionality, documentation, and testability.

Treat this as a production release. For instance, use a containerization software and python package manager of your choice (by default, docker and poetry files are available in the test).

### Getting Started

Run all services with docker/docker-compose or podman/podman-compose: 

`docker-compose up`

`podman-compose up`

### Submission

After completing the assessment, please submit your code to: cedric.fraboulet@microbiomestudio.com and noemie.verscheure@microbiome.studio.

Any further questions required for clarification, please also reach out to cedric.fraboulet@microbiomestudio.com.

Good luck!

