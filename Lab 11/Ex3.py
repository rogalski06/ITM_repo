# Read in a DSCV file and create a dataframe
# Pivot the dataframe, aggregating sales by region, with columns defined by order_type and totals.
# Add in sub-columns showing the average sales by state and by sale type (retail or wholesale)

import pandas as pd
import numpy as np
import pyarrow
import ssl

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

pd.set_option('display.max_columns', None)  # Show all columns in the output
pd.set_option('display.float_format', '{:,.2f}'.format)  # Format floats to 2 decimal places

df = pd.read_csv(filename, engine='pyarrow')
df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y', errors='coerce')

# Coerce quantity and unit_price to numeric, setting errors to NaN
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df['sales'] = df['quantity'] * df['unit_price']

pivot_table = pd.pivot_table(df,
                             index='customer_state',
                             values='sales',
                             columns=['customer_type', 'order_type'], 
                             aggfunc=np.mean,
                             margins=True,
                             margins_name='Total Sales')
print(pivot_table)