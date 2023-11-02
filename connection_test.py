from sql_functions import get_dataframe
from dotenv import load_dotenv

load_dotenv()

def run_connection_test():
    try:
        get_dataframe("SELECT * FROM public.test_csv")
        print("!!Connection zur Database funktionsfähig!!")
    except:
        print("!!Connection funktioniert nicht, überprüfe deine Credentials und ggf. IP!!")


