from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

def extract_from_db():
     # pull all transactions from PostgreSQL
     df=pd.read_sql("select * from transactions", engine)
    # return DataFrame
     return(df)
 

def analyse(df):
    # 1. total deposits vs withdrawals
    total_by_type = df.groupby('transaction_type')['amount'].sum()
    
    # 2. average per account
    avg_per_account = df.groupby('account_number')['amount'].mean()
    # 3. flag suspicious transactions > $3000
    suspicious = df[df['amount']> 3000]
    # return a summary dictionary or DataFrame
    return total_by_type, avg_per_account, suspicious


def export_report(total_by_type, avg_per_account, suspicious):
    # write summary to report.csv
    """Summary """
    total_by_type.to_csv('report_totals.csv')
    avg_per_account.to_csv('report_average.csv')
    suspicious.to_csv('reported_suspicious.csv', index=False)
    print("Reports exported succesfully")
    # print confirmation

if __name__ == "__main__":
    df = extract_from_db()
    total_by_type, avg_per_account, suspicious = analyse(df)
    export_report(total_by_type, avg_per_account, suspicious)
    print("Reporting pipeline complete!")
    # call all three functions

 
 