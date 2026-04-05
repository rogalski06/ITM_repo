# Create an interactive, text-based dashboard using Pandas pivot tables
# The dashboard will allow users to explore and analyze sales data in various dimensions (e.g., by region, employee, product, and customer)
# The dashboard provides both predefined analytical tasks and custom pivot table exploration to analyze sales data.

# Individual Requirements:
# 1. For each result, ask the user if they want the results exported to an Excel file (that can be read directly into Excel). Ask the user what filename they want.
# 9. Instead of replacing missing data in the pivot table with zeroes, replace it with the mean value for that column. 

# Import necessary libraries
import time
import pandas as pd
import numpy as np
import pyarrow
import openpyxl

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows

# Requirement 1
# Defining "load_csv" function to load the CSV and review data to give users initial insights.
def load_csv(filepath):
    # Show that data is loading and start the timer
    print(f"Loading data from {filepath}...")
    start_time = time.time()
    try:
        # Initiate the CSV read and end the timer after loading is complete. Return appropiate messages/actions for success or failure.
        df = pd.read_csv(filepath, engine='python')
        end_time = time.time()
        load_time = end_time - start_time
        print(f"CSV file loaded succesfully in {load_time:.2f} seconds.") # Success message with load time
        print(f"number of rows: {len(df)}") # Counting rows
        print(f"Columns: {df.columns.tolist()}") # Listing columns

        df.fillna(df.mean(numeric_only=True), inplace=True)  # Individual Requirement 9: Replace missing data with the mean value for that column
        df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y', errors='coerce') # Converting order_date to proper date format
        df['sales'] = df['quantity'] * df['unit_price']  # Create a new 'sales' column as quantity * unit_price

        # Check the data has required fields and show warnings for what is missing
        required_columns = ['quantity', 'unit_price', 'order_date']
        # Check if required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Warning: Missing required columns: {missing_columns}")        
        else: 
            print("All required columns are present.")

        return df
    
    except Exception as e:
        print(f"Error loading CSV file: {e}") # Failure message with error details
        return None
    
# Define function to export pivot tables to Excel
def export_to_excel(dataframe):
    try:
        filename = input("\nWould you like to export the results to an Excel file? Enter filename (or press Enter to skip): ").strip()
        if filename:
            if not filename.endswith('.xlsx'):
                filename += '.xlsx'
            dataframe.to_excel(filename)
            print(f"\nResults successfully exported as {filename}")
    except Exception as e:
        print(f"Error exporting to Excel: {e}")

# Requirement 2
# Define functions for each function the user can select from the menu

# 1. Function to display the first n rows of the sales data
def display_initial_rows(dataframe):
    print("Enter rows to display:")
    print(f"- Enter a number 1 to {len(dataframe)}")
    print("- Enter 'all' to display all rows")
    print("- to skip preview, press Enter")
    user_input = input("Your choice: ").strip().lower()

    if user_input == '':
        print("Skipping preview.")
        return
    elif user_input == 'all':
        print("Displaying all rows:")
        print(dataframe)
    elif user_input.isdigit and 1 <= int(user_input) <= len(dataframe):
        print(f"Displaying first {user_input} rows:")
        print(dataframe.head(int(user_input)))
    else:
        print("Invalid input. Please try again.")

# 2. Function to show total sales by region and order type
def sales_by_region_and_ordertype(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='sales', index='sales_region', columns='order_type', aggfunc='sum', fill_value=0)
    print("\nTotal sales by region and order type:")
    print(pivot_table)
    export_to_excel(pivot_table)
    return

# 3. Function  to show average sales by region with average sales by state and sale type
def average_sales_by_region_state_ordertype(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='sales', index='sales_region', columns=['customer_state', 'order_type'], aggfunc='mean', fill_value=0)
    print("\nAverage sales by region, state, and order type:")
    print(pivot_table)
    export_to_excel(pivot_table)
    return

# 4. Function to show sales by customer type and order type by state.
def sales_by_customer_type_and_order_type_by_state(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='sales', index='customer_state', columns=['customer_type', 'order_type'], aggfunc='sum', fill_value=0)
    print("\nSales by customer type and order type by state:")
    print(pivot_table)
    export_to_excel(pivot_table)
    return

# 5. Function to show total sales quantity and price by region and product
def total_sales_by_region_and_product(dataframe):
    pivot_table = pd.pivot_table(dataframe, values=['quantity', 'unit_price'], index='produce_name', columns='sales_region', aggfunc='sum', fill_value=0)
    print("\nTotal sales by region and product:")
    print(pivot_table)
    export_to_excel(pivot_table)
    return

# 6. Function to show total sales quantity and price by customer and order type
def total_sales_by_customer_and_order_type(dataframe):
    pivot_table = pd.pivot_table(dataframe, values=['quantity', 'unit_price'], index=['customer_type', 'order_type'], aggfunc='sum', fill_value=0)
    print("\nTotal sales by customer type and order type:")
    print(pivot_table)
    export_to_excel(pivot_table)
    return

# 7. Function to show max and min sales price of sales by category
def max_min_sales_price_by_category(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='unit_price', index='produce_name', columns='sales_region', aggfunc=['max', 'min'], fill_value=0)
    print("\nMax and min sales price by category:")
    print(pivot_table)
    export_to_excel(pivot_table)
    return

# 8. Function to show the number of employees by region
def show_employees_by_region(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='employee_id', index='sales_region', aggfunc=pd.Series.nunique)
    pivot_table.columns = ['Number of Employees']
    print("\nNumber of employees by region:")
    print(pivot_table)
    export_to_excel(pivot_table)
    return

# Requirement 4

# 9. Create a custom pivot table
def custom_pivot_table(dataframe):
    # Define options for rows, columns, values, and aggregation functions
    row_options = {
        '1': 'employee_name',
        '2': 'sales_region',
        '3': 'product_category'
    }
    column_options = {
        '1': 'order_type',
        '2': 'customer_type'
    }
    value_options = {
        '1': 'quantity',
        '2': 'unit_price'
    }
    agg_options = {
        '1': 'sum',
        '2': 'mean',
        '3': 'count'
    }

    # Get user inputs and validate that they are an option
    while True:
        print("\nSelect rows:")
        for key, value in row_options.items():
            print(f"{key}. {value}")
        row_input = input("Enter the number(s) of your choice, separated by commas: ").strip().split(',')
        if row_input and not all(choice.strip() not in row_options for choice in row_input):
            break
        print("\nInvalid selection for rows. Please try again.")

    while True:
        print("\nSelect columns (optional):")
        for key, value in column_options.items():
            print(f"{key}. {value}")
        column_input = input("Enter the number(s) of your choice, separated by commas: ").strip()
        if column_input == '':
            column_input = []
            break
        column_input = column_input.split(',')
        if not all(choice.strip() not in column_options for choice in column_input):
            break
        print("\nInvalid selection for columns. Please try again.")

    while True:
        print("\nSelect values:")
        for key, value in value_options.items():
            print(f"{key}. {value}")
        value_input = input("Enter the number(s) of your choice, separated by commas: ").strip().split(',')
        if value_input and not all(choice.strip() not in value_options for choice in value_input):
            break
        print("\nInvalid selection for values. Please try again.")

    while True:
        print("\nSelect aggregation function:")
        for key, value in agg_options.items():
            print(f"{key}. {value}")
        agg_input = input("Enter the number(s) of your choice, separated by commas: ").strip().split(',')
        if agg_input and not all(choice.strip() not in agg_options for choice in agg_input):
            break
        print("\nInvalid selection for aggregation function. Please try again.")

    # Assign user values to variables for pivot table creation
    rows = [row_options.get(choice.strip()) for choice in row_input if choice.strip() in row_options]
    columns = [column_options.get(choice.strip()) for choice in column_input if choice.strip() in column_options]
    values = [value_options.get(choice.strip()) for choice in value_input if choice.strip() in value_options]
    aggfuncs = [agg_options.get(choice.strip()) for choice in agg_input if choice.strip() in agg_options]

    # Create the pivot table based on user selections
    pivot_table = pd.pivot_table(dataframe, values=values, index=rows, columns=columns if columns else None, aggfunc=aggfuncs[0], fill_value=0)
    print("\nCustom Pivot Table:")
    print(pivot_table)
    export_to_excel(pivot_table)
    return pivot_table

# 10. Function to exit the program
def exit_program(dataframe):
    print("Exiting the program. Goodbye!")
    exit(0)

# Define a function to display the menu and match the user input to the corresponding function
def display_menu(dataframe):
    menu_options = (
        ("Show the first n rows of sales data", display_initial_rows),
        ("Show total sales by region and order type", sales_by_region_and_ordertype),
        ("Show average sales by region with average sales by state and sale type", average_sales_by_region_state_ordertype),
        ("Show sales by customer type and order type by state", sales_by_customer_type_and_order_type_by_state),
        ("Show total sales quantity and price by region and product", total_sales_by_region_and_product),
        ("Show total sales quantity and price by customer type and order type", total_sales_by_customer_and_order_type),
        ("Show max and min sales price of sales by category", max_min_sales_price_by_category),
        ("Show the number of employees by region", show_employees_by_region),
        ("Create a custom pivot table", custom_pivot_table),
        ("Exit", exit_program)      
    )
    # Print the menu options for the user to choose from
    print("\nAvailable options:")
    for i, (description, _) in enumerate(menu_options, start=1):
        print(f"{i}. {description}")

    # Process the user's choice and call the corresponding function
    try:
        menu_len = len(menu_options)
        choice = int(input(f"Enter your choice (1-{menu_len}): "))
        if 1 <= choice <= menu_len:
            action = menu_options[choice - 1][1]
            action(dataframe)
        else:
            print("Invalid choice. Please enter a number corresponding to the options.")

    except ValueError:
        print("Invalid input. Please enter a number corresponding to the options.")


# Call load_csv to load the data
filename = "sales_data.csv"
sales_data = load_csv(filename)


# Run the main processing loop
def main():
    while True:
        print("\nSales Data Dashboard")
        display_menu(sales_data)

# Check if this is the main module being run
if __name__ == "__main__":
    main()