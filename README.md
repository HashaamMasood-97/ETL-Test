# ETL TASK

This github repository consists of the following file:
1. ETL.py - This is the main code where the data is extracted, transformed and loaded into MySQL DB.
2. Dimensional Modelling.xlsx - This is the file where the schema is being created (2.4).
3. dashboard folder - This consist of one screenshot of the dashboard and one power bi file which contains the dashboard.
4. MySQL Screenshot Folder - This folder contains the screenshot of the loaded data into the MySQL DB, for reference two tables pictures are attached.

I have choosen the chinook.db (sqlite) in the extraction phase of the task.

Before starting the ETL process, some of the business questions were being created and the entire process of ETL revolved around those question.
All the tables selection/transformations are being done to address those business questions.

Business Questions:
1. Identify the top five customers based on their total purchase value.
2. Identify the albums with the highest total revenue, considering the quantity of units sold for each album.
3. Identify the top three employees based on their sales performance in terms of revenue.
4. What is the cumulative revenue generated from sales in the top 10 countries?
5. What is the sales trend observed for each month across multiple years?

# Task 2.1 - Data Extraction

The required tables to answer the above questions are 'tracks', 'invoice_items', 'invoices', 'customers', 'albums', 'employees' and the database used is chinook.db (sqlite)

The data extraction process involves connecting to an SQLite database and extracting data from specified tables using the extract_data function. For each specified table in desired_tables, a SQL query is constructed to retrieve all data from that table. The extract_data function returns a dictionary (dataframes) containing Pandas DataFrames for each specified table, where the keys are table names and values are corresponding DataFrames.

# Task 2.2 - Data Transformation/Cleaning

Customer Table:
- First names, last names, and city names in the Customers table are processed using unidecode to handle any diacritics or special characters.
- Phone numbers are cleaned by removing parentheses, spaces, and hyphens.
- Unnecessary columns ('Company', 'State', 'Fax') are dropped.

Employees Table:
- The 'BirthDate' and 'HireDate' columns are converted to the date format from timestamp format.
- Phone and fax numbers are formatted to include a '+' if not present at the beginning to maintain the consistency.

Tracks Table:
- Unnecessary columns ('Milliseconds', 'Bytes', 'Composer', 'MediaTypeId', 'GenreId') in the Tracks table are dropped.

Invoice and Album Table:
- The 'ArtistId' column in the Albums table is dropped, no need of it since the artist table is not extracted.
- The 'InvoiceDate' column is converted to the date format.

  



   
