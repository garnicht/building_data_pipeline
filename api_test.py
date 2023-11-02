
#!/usr/bin/env python
# coding: utf-8

# # Import libs and methods
import pandas as pd
import os
import time
import requests
from sql_functions import unix_to_timestamp
import numpy as np
from sql_functions import encrypt
from sql_functions import upload_dataframe
from dotenv import load_dotenv #irgendwie muss das geladen werden und wir wissen nicht warum :D 


load_dotenv()
# # Download
# Define the maximum amount of pages exist in Subscriptions (just to make sure that we can dl everything in the future)
url = "https://app.webinargeek.com/api/v2/subscriptions"
headers = {"Api-Token": os.getenv('webinargeek_api_key'),"Content-Type":"application/json"}
querystring = {"per_page":1000} 

# unpack the jason file
response = requests.get(url, headers=headers, params=querystring) 
subscription_json = response.json()

#get number of pages
pages = subscription_json.get("pages").get("total_pages")
pages = list(range(1,pages + 1))

print(pages)