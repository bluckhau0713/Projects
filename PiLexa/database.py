import pyodbc


def connectToDatebase():
    server = 'secretServer'
    database = 'secretDB'
    driver = '{SQL Server}'

    # connection_string = f"SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    return connection, cursor