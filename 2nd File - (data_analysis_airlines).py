
# Objective
#The goal of this data analysis project using sql would be to identify opportunities to increase the occupancy rate on low-performing flights, which can ultimately lead to increased profitability for the airline.

# Importing Libraries

from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Database Connection"""

server = 'ADS_G15\\SQLEXPRESS'
database = 'MyDatabase'
connection = create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server")

# extracting table names from the database
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
tables = pd.read_sql("SELECT name FROM sys.tables", connection)
print('List of Tables present in the Database')
for table in tables['name']:
    print("-"*50,table,"-"*50)
    print(pd.read_sql(f'select top 8 * from {table}',connection))



# Data Exploration

aircrafts_data = pd.read_sql_query(f"""SELECT * FROM aircrafts_data""", connection)

airports_data = pd.read_sql_query(f"""SELECT * FROM airports_data""", connection)

boarding_passes = pd.read_sql_query(f"""SELECT * FROM boarding_passes""", connection)

bookings = pd.read_sql_query(f"""SELECT * FROM bookings """, connection)

flights = pd.read_sql_query(f"""SELECT * FROM flights  """, connection)

seats = pd.read_sql_query(f"""SELECT * FROM seats  """, connection)

ticket_flights = pd.read_sql_query(f"""SELECT * FROM ticket_flights  """, connection)

tickets = pd.read_sql_query(f"""SELECT * FROM tickets  """, connection)


df = pd.read_sql("""SELECT TABLE_NAME,COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_NAME;""", connection)
print(df)

# Data Cleaning

# checking for missing values in each column for every table
for table in tables['name']:
    print(f'\nMissing Values in table {table}')
    df_table = pd.read_sql_query(f"""SELECT * FROM {table}""", connection)
    print(df_table.isnull().sum())

# Basic Analysis

#How many planes have more than 100 seats?


print(pd.read_sql_query(f"""SELECT aircraft_code, COUNT(*) as num_seats FROM seats
                        GROUP BY aircraft_code
                        HAVING COUNT(*) > 100
                        ORDER BY num_seats DESC""", connection))

#How the number of tickets booked and total amount earned changed with the time.

tickets = pd.read_sql_query(f"""SELECT *
                                    FROM tickets
                                    INNER JOIN bookings
                                    ON tickets.book_ref=bookings.book_ref;""", connection)
tickets['book_date'] = pd.to_datetime(tickets['book_date'])
tickets['date'] = tickets['book_date'].dt.date
x =  tickets.groupby('date')['ticket_no'].count().reset_index()
print(x)
plt.figure(figsize = (18,6))
plt.plot(x['date'],x['ticket_no'], marker = '^')
plt.xlabel('Date', fontsize = 20)
plt.ylabel('Number of Tickets', fontsize = 20)
plt.grid()
plt.show()

bookings = pd.read_sql_query(f"""SELECT * FROM bookings""", connection)
bookings['book_date'] = pd.to_datetime(bookings['book_date'])
bookings['date'] = bookings['book_date'].dt.date
y =  bookings.groupby('date')['total_amount'].sum().reset_index()
print(y)
plt.figure(figsize = (18,6))
plt.plot(y['date'],y['total_amount'], marker = 'o')
plt.xlabel('Date', fontsize = 20)
plt.ylabel('Total Amount', fontsize = 20)
plt.grid('b')
plt.show()

#Calculate the average charges for each aircraft with different fare conditions.

df = pd.read_sql_query(f"""SELECT fare_conditions, aircraft_code, AVG(amount) as avg_amount FROM ticket_flights
                        JOIN flights
                        ON ticket_flights.flight_id=flights.flight_id
                        GROUP BY aircraft_code, fare_conditions""", connection)

sns.barplot(data = df, x = 'aircraft_code', y ='avg_amount', hue = 'fare_conditions')
plt.show()
# Analyzing occupancy rate

#For each aircraft, calculate the total revenue and the average revenue per ticket.


pd.set_option('display.float_format', str)

print(pd.read_sql_query("""SELECT aircraft_code, total_revenue, ticket_count, total_revenue/ticket_count as avg_revenue_per_ticket
                        FROM
                        (SELECT aircraft_code, COUNT(*) as ticket_count, SUM(amount) as total_revenue  FROM ticket_flights
                        JOIN flights
                        ON ticket_flights.flight_id=flights.flight_id
                        GROUP BY aircraft_code)as a""", connection))

#Calculate the average occupancy per aircraft.

occupancy_rate = pd.read_sql_query(f"""SELECT a.aircraft_code, AVG(a.seats_count) as booked_seats, b.num_seats,
 CAST(AVG(a.seats_count) AS FLOAT)/b.num_seats as occupancy_rate
                            FROM (
                                SELECT aircraft_code, flights.flight_id, COUNT(*) as seats_count
                                FROM boarding_passes
                                INNER JOIN flights
                                ON boarding_passes.flight_id=flights.flight_id
                                GROUP BY aircraft_code, flights.flight_id
                                ) as a INNER JOIN
                                (
                                SELECT aircraft_code, COUNT(*) as num_seats FROM seats
                                GROUP BY aircraft_code
                                ) as b
                                ON a.aircraft_code = b.aircraft_code
                            GROUP BY a.aircraft_code,b.num_seats""", connection)
print(occupancy_rate)

#Calculate by how much the total annual turnover could increase by giving all aircraft a 10% higher occupancy rate.



occupancy_rate['Inc_occupancy_rate'] = occupancy_rate['occupancy_rate'] + occupancy_rate['occupancy_rate']*0.1
print(occupancy_rate)

total_revenue = pd.read_sql_query("""SELECT aircraft_code, SUM(amount) as total_revenue  FROM ticket_flights
                        JOIN flights
                        ON ticket_flights.flight_id=flights.flight_id
                        GROUP BY aircraft_code""", connection)

occupancy_rate['Inc_Total_Annual_Turnover'] = (occupancy_rate['Inc_occupancy_rate']/occupancy_rate['occupancy_rate'])*total_revenue['total_revenue']
print(occupancy_rate)


