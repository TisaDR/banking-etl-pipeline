from sqlalchemy import create_engine
import pandas as pd
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
print("Connected successfully");

df = pd.read_sql("SELECT * from transactions",engine);
print(df.shape)

df['transaction_date'] = pd.to_datetime(df['transaction_date'])
print(df.dtypes)

q1 = pd.read_sql("select transaction_type, COUNT(*) from transactions GROUP BY transaction_type", engine)
print(q1)

q2 = pd.read_sql("select transaction_type , SUM(amount) from transactions GROUP BY transaction_type", engine)
print(q2)

q3 = pd.read_sql("select account_number, sum(amount) from transactions where transaction_type = 'deposit' group by account_number ORDER BY sum(amount) DESC LIMIT 1;", engine)
print(q3)

q4 = pd.read_sql("select account_number , ROUND(AVG(amount), 2) as avg_amount from transactions group by account_number order by avg_amount",engine)
print(q4)

q5 = pd.read_sql(" select EXTRACT(month from transaction_date) as month , sum(amount) from transactions group by month order by sum(amount) desc LIMIT 1", engine)
print(q5)

q6 = pd.read_sql(""" WITH account_total AS SELECT account_number, SUM(amount) as total from transactions
                 group by account_number) select * from account_total where total > 3000 order by total DESC""", engine)
print("account with total > $3000:")
print(q6)

q7 = pd.read_sql("""
    SELECT c.name, t.amount, t.transaction_type, t.transaction_date
    FROM customers c
    INNER JOIN transactions t ON c.account_number = t.account_number
    WHERE t.amount > 1000
    ORDER BY t.amount DESC
""", engine)
print("\nCustomers with transactions over $1000:")
print(q7)


q8 = pd.read_sql("""
    SELECT account_number, amount, transaction_date,
           SUM(amount) OVER (PARTITION BY account_number 
                            ORDER BY transaction_date) as running_total
    FROM transactions
    ORDER BY account_number, transaction_date
""", engine)
print("\nRunning totals per account:")
print(q8)