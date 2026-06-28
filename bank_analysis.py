import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:new_password@localhost:5432/banking_practice")
print("Connected successfully");

df = pd.read_sql("select * from transactions", engine)
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

q1 = df.groupby('account_number')['amount'].agg(['sum','count'])
q1 = q1.sort_values('sum', ascending=False)
print("Highest Total Transactions")
print(q1)

#average transaction per month
df['month'] = df['transaction_date'].dt.month
q2 = df.groupby('month')['amount'].mean().round(2)
print("\n=== Average Transaction Per Month ===")
print(q2)

print("Null check")
print(df.isnull().sum())
df_clean = df.fillna({'amount':df['amount'].mean(),'account_number':'Unknown'})
print("Nulls after handling:", df_clean.isnull().sum().sum())


trans = df[df['amount'] > 1000]
print(trans)

q5 = df.loc[df['transaction_type'] == 'withdrawal',['account_number','amount']]
print(q5)

q6 = df.groupby('transaction_type')['amount'].agg(['sum','mean','max'])
q6 = q6.sort_values('sum', ascending=False)
print(q6)

q7 = df.groupby('account_number')['transaction_type'].nunique()
q7 = q7[q7 == 2]
print(q7)
