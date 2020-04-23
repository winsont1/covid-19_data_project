# Nucleus Wealth Assessment - Winson Tan
## Data used: 2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE

Challenge Description (based on url: https://www.seek.com.au/job/41223086?ref=saved) :

1. Python: Download a timeseries of daily deaths per country
2. Python: Convert the table so that each country and each day is a separate row
3. Python: Provide code to upload the table from step 3 into an SQL table named deaths_total
4. Python: From the data in step 2, calculate the daily change in deaths for each country
5. Python: Provide code to upload the table from step 4 into an SQL table named deaths_change_python
6. SQL: Provide SQL code to calculate the daily change for each country using only the data from deaths_total and save it into an SQL table named deaths_change_sql


### SYSTEM REQUIREMENTS
* Python >3
* Virtualenv python package
* PostgreSQL & PGAdmin (optional)

### KEY COMPLETED CODING CHALLENGE FILES:
1. covid_deaths_refactored.py (Requirements 1-5)
2. deaths_change_calculation.sql (Requirements 6)

### HOW TO RUN
1. In project folder, please activate virtualenv to use python packages (if virtualenv not installed, go here https://virtualenv.pypa.io/en/latest/ ). Enter into terminal:
    source env/bin/activate
2. Create PostgreSQL DB named `covid-19` in local environment, with user and password.
3. Configure the correct Database URL `engine = create_engine('postgresql://postgres:password@localhost:5432/covid-19')` in the `python3 covid_deaths_refactored.py` file. Refer to SQLAlchemy documentation: https://docs.sqlalchemy.org/en/13/core/engines.html.
4. Run in terminal:
    python3 covid_deaths_refactored.py
5. Enter PGAdmin to run code in `deaths_change_calculation.sql` file using the Query Tool.

#### ADDITIONAL FILES:
1. covid_deaths.ipynb (Jupyter Notebook working file for data manipulation - use `jupyter notebook` to launch IDE)
2. python_packages.txt (list of Python packages used)
3. time_series_covid19_deaths_global.csv (daily deaths data saved locally for reference)
