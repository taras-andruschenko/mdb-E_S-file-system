import sys
import pyodbc
import csv
from datetime import datetime


def extract_data_to_csv_file():
    conn = pyodbc.connect(
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Shiprite\Shiprite.mdb;"
    )
    cursor = conn.cursor()

    # Define the parameter to pass in to the query if it needed
    current_datetime = datetime.now().strftime("%Y-%m-%d")

    # Define the SQL query
    # Check if "-all" argument is passed
    if "-all" in sys.argv:
        sql = "SELECT * FROM manifest"
        # Extract all data from the table
        cursor.execute(sql)
    else:
        sql = "SELECT * FROM manifest WHERE Date = ?"

        # Extract the data from the table with current date only
        cursor.execute(sql, (current_datetime,))

    rows = cursor.fetchall()
    cnum = conn.cursor()
    cnum.execute("SELECT PostNetCDHL_CenterID FROM Setup2 WHERE id= 1")
    roz = cnum.fetchall()

    # convert datetime obj to string
    str_current_datetime = str(current_datetime)

    file_path = f"C:\\Shiprite\\{roz[0][0]}_Manifest_{current_datetime}.csv"

    # Save the data to a CSV file
    with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8",
    ) as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # write headers
        writer.writerows(rows)

        # Close the connection to the database
        conn.close()
        print("Table exported to CSV successfully")

        return file_path
