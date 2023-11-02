
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

def run_full_dl_master():
    table_name = input("Wie soll deine NEUE Tabelle heißen?")
    load_dotenv()
    print("Der Download startet nun, dies kann einige Zeit dauern, bitte schalte den PC nicht aus und sorge dafür das er durchgehend läuft.")
    
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

    # Download all data
    subs_api = pd.DataFrame()
    for page in pages:
        
        # Get the Subscriptions from API
        url = "https://app.webinargeek.com/api/v2/subscriptions"
        headers = {"Api-Token": os.getenv('webinargeek_api_key'),"Content-Type":"application/json"}
        querystring = {"per_page":1000, "page":page}

        # unpack the jason file
        response = requests.get(url, headers=headers, params=querystring) 
        subscription_json = response.json()

        #change relevant data to data_frame
        temporary_df = subscription_json.get("subscriptions")
        temporary_df = pd.DataFrame(temporary_df)

        #concat the data_frames
        subs_api = pd.concat([temporary_df,subs_api])
        
    subs_api_ids = subs_api['id'].to_list()

    # Download new Data with help of Sub Ids 
    new_data = pd.DataFrame()

    for id in subs_api_ids:

        # Get the Subscriptions from API
        url = f"https://app.webinargeek.com/api/v2/subscriptions/{id}"
        headers = {"Api-Token": os.getenv('webinargeek_api_key'),"Content-Type":"application/json"}

        # unpack the jason file
        response = requests.get(url, headers=headers) 
        
        time.sleep(800/1000) #One request every 800 ms. Results in 4500 requests in one hour or 75 in a minute. 
        
        subscription_json = response.json()

        #change relevant data to data_frame
        temporary_df = pd.json_normalize(subscription_json)

        #concat the data_frames
        new_data = pd.concat([temporary_df,new_data])

    new_data.reset_index(inplace=True,drop=True)
    print("Download fertig, Cleaning startet")

    # # Cleaning
    #make sure empty strings are "None"
    new_data.apply(lambda x: x.replace('', None, inplace=True))

    #change column names to use "_" instead of "."
    new_data.rename(columns=lambda x: x.replace('.', '_'), inplace=True)

    #create timestamps and delete old columns
    unix_to_timestamp(new_data,"created_at")
    new_data.drop(columns="created_at",inplace=True)
    new_data["created_at_timestamp"].replace({np.NaN:None},inplace=True)

    unix_to_timestamp(new_data,"email_verified_at")
    new_data.drop(columns="email_verified_at",inplace=True)
    new_data["email_verified_at_timestamp"].replace({np.NaN:None},inplace=True)

    unix_to_timestamp(new_data,"watch_end")
    new_data.drop(columns="watch_end",inplace=True)
    new_data["watch_end_timestamp"].replace({np.NaN:None},inplace=True)

    unix_to_timestamp(new_data,"watch_start")
    new_data.drop(columns="watch_start",inplace=True)
    new_data["watch_start_timestamp"].replace({np.NaN:None},inplace=True)

    unix_to_timestamp(new_data,"broadcast_date")
    new_data.drop(columns="broadcast_date",inplace=True)
    new_data["broadcast_date_timestamp"].replace({np.NaN:None},inplace=True)

    unix_to_timestamp(new_data,"broadcast_ended_at")
    new_data.drop(columns="broadcast_ended_at",inplace=True)
    new_data["broadcast_ended_at_timestamp"].replace({np.NaN:None},inplace=True)

    unix_to_timestamp(new_data,"broadcast_started_at")
    new_data.drop(columns="broadcast_started_at",inplace=True)
    new_data["broadcast_started_at_timestamp"].replace({np.NaN:None},inplace=True)

    # get rid of the whitespaces
    new_data = new_data.apply(lambda x: x.str.strip() if type(x) == "string" else x)

    #emails encrypten
    encrypt(new_data,"email")

    #List all unwanted columns
    new_data_columns = []
    for column in new_data.columns:
        new_data_columns.append(column)

    mastertable_columns = ["id","viewing_device","confirmation_link","watch_link","watched","watch_duration","watched_live","email_updated_at","broadcast_id","broadcast_has_ended","broadcast_duration","broadcast_subscriptions_count","broadcast_viewers_count","broadcast_live_viewers_count","episode_id","episode_title","episode_internal_title","episode_type","episode_subscriptions_count","webinar_id","webinar_title","webinar_internal_title","webinar_url","webinar_ondemand","created_at_timestamp","email_verified_at_timestamp","watch_end_timestamp","watch_start_timestamp","broadcast_date_timestamp","broadcast_ended_at_timestamp","broadcast_started_at_timestamp","email_encrypted"]
    drop_list = []

    for i in new_data_columns:
        if i not in mastertable_columns:
            drop_list.append(i)

    #drop unnecessary columns
    new_data.drop(columns=drop_list,inplace=True)

    # correct values of df['broadcast_duration'] of webinar 'Teil 1: Hypothesentest (1. – 7. Juni)' to 7260
    new_data.loc[new_data['webinar_title'] == 'Teil 1: Hypothesentest (1. – 7. Juni)', 'broadcast_duration'] = 7260

    #Creating column with watch_duration / broadcast_duration as watch_percentage
    new_data['watch_percentage'] = new_data['watch_duration']/ new_data['broadcast_duration']
    print("Cleaning fertig, Upload startet, bitte warten")

    # # Upload
    upload_dataframe(new_data,"public",table_name)
    print("Upload beendet, Programm kann geschlossen werden")