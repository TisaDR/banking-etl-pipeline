import pandas as pd
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import psycopg2

# ── CONNECTION ──────────────────────────────────────────
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# ── GENERATE 100 FAKE TRANSACTIONS ──────────────────────
def generate_fake_transactions(n=100):
    """Generate n fake transactions using random module"""
    print(f"Generating {n} fake transactions...")

    account_numbers = [f"ACC-00{i}" for i in range(1, 9)]
    transaction_types = ['deposit', 'withdrawal']

    transactions = []
    start_date = datetime(2024, 1, 1)

    for i in range(1, n + 1):
        transaction = {
            'id': i,
            'account_number': random.choice(account_numbers),
            'amount': round(random.uniform(-500, 10000), 2),  # intentional negatives
            'transaction_type': random.choice(transaction_types),
            'transaction_date': start_date + timedelta(days=random.randint(0, 365))
        }
        transactions.append(transaction)

    df = pd.DataFrame(transactions)
    print(f"Generated {len(df)} rows")
    return df

# ── VALIDATE + CLEAN ────────────────────────────────────
def clean_and_validate(df):
    """Remove invalid rows"""
    print("Cleaning and validating...")
    original_count = len(df)

    # Rule 1 — no negative amounts
    df = df[df['amount'] > 0]

    # Rule 2 — no null account numbers
    df = df[df['account_number'].notna()]

    # Rule 3 — no null transaction types
    df = df[df['transaction_type'].notna()]

    # Rule 4 — standardize dates
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])

    # Rule 5 — reset index after filtering
    df = df.reset_index(drop=True)

    removed = original_count - len(df)
    print(f"Removed {removed} invalid rows")
    print(f"Clean rows remaining: {len(df)}")
    return df

# ── WRITE TO POSTGRESQL ─────────────────────────────────
def write_to_db(df, table_name):
    """Write DataFrame to PostgreSQL"""
    print(f"Writing to {table_name}...")

    df.to_sql(
        table_name,
        engine,
        if_exists='replace',  # replace if table exists
        index=False
    )
    print(f"Successfully wrote {len(df)} rows to {table_name}")

# ── VERIFY ──────────────────────────────────────────────
def verify(table_name):
    """Read back from DB to confirm it worked"""
    print(f"Verifying {table_name}...")
    df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", engine)
    print(df)

    count = pd.read_sql(f"SELECT COUNT(*) FROM {table_name}", engine)
    print(f"Total rows in database: {count.iloc[0,0]}")


def write_with_upsert(df):
    """Write rows one by one with ON CONFLICT handling"""
    conn = psycopg2.connect(
        dbname="banking_practice",
        user="postgres",
        password="new_password",
        host="localhost",
        port="5432"
        
    )
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS transactions_generated;")
    conn.commit()
    
    # Create table with proper primary key if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions_generated (
        id               INTEGER PRIMARY KEY,
        account_number   VARCHAR(20),
        amount           NUMERIC(10,2),
        transaction_type VARCHAR(20),
        transaction_date DATE
    )
    """)
    conn.commit()
    
    query = """INSERT INTO transactions_generated (id,account_number,amount,transaction_type, transaction_date)
    values (%s, %s, %s ,%s, %s)
    ON CONFLICT (id) DO UPDATE SET
        account_number = EXCLUDED.account_number,
        amount = EXCLUDED.amount,
        transaction_type =  EXCLUDED.transaction_type,
        transaction_date = EXCLUDED.transaction_date;
               """    
               
    for index, row in df.iterrows():
        cursor.execute(query, (
          row['id'],
          row['account_number'],
          row['amount'],
          row['transaction_type'],
          row['transaction_date']
        ))
        
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Upserted {len(df)} rows successfully")
    

if __name__ == "__main__":
    raw_df = generate_fake_transactions(100)
    clean_df = clean_and_validate(raw_df)
    write_with_upsert(clean_df)  # ← call it here, pass the DataFrame in