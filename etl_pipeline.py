from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
def extract(filepath):
    print("Extracting data..")
     # read the CSV file into a DataFrame
    df =pd.read_csv(filepath)
    # print how many rows were extracted
    print(df.shape)
    # return the DataFrame
    return(df)

def transform(df):
    print("Transforming data....")
     # 1. drop any rows with nulls
    df = df.dropna()
     
    
    # 2. convert transaction_date to datetime
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    
    # 3. lowercase and strip whitespace from transaction_type
    df['transaction_type'] = df['transaction_type'].str.lower().str.strip()
    
    
    # 4. add transaction_category column using this logic:
    #    amount > 5000  → 'LARGE'
    #    amount > 1000  → 'MEDIUM'
    #    anything else  → 'SMALL'
    #    hint: define a function and use .apply()
    
    def categorize(amount):
     if amount > 5000:
        return 'LARGE'
     elif amount > 1000:
        return 'MEDIUM'
     else:
        return 'SMALL'

    df['transaction_category'] = df['amount'].apply(categorize)
    
    # print how many rows after transform
    print(df.shape)
    # return cleaned DataFrame
    return(df)


def load(df, table_name):
    print(f"loading into {table_name}....")
    
    df.to_sql(
        table_name,
        engine,
        if_exists='replace',
        index=False
    )
    print(f"Successfully wrote {len(df)} rows to {table_name}")

     # write DataFrame to PostgreSQL
    # use if_exists='replace'
    # print confirmation
    

if __name__ == "__main__":
    # call extract with your csv path
  raw =  extract(r'C:\Users\patel\OneDrive\Documentos\Desktop\password-manager-api\transactions.csv')
    # call transform on the result
  transactions_clean=transform(raw)
    # call load with table name 'transactions_clean'
  load(transactions_clean, 'transactions_clean')  # ← correct
  print("Pipeline complete!")