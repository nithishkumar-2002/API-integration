import json
import requests
import os
import pandas as pd
import numpy as np
import time
import gspread
from gspread_dataframe import set_with_dataframe

# Connect with google service account
gs = gspread.service_account(filename=r"Give you GCP Cerdentials")
# Opening the existing Google Sheet
sheet = gs.open("") # Give you google sheet name
# Get the specific sheet name
worksheet = sheet.worksheet('') # Give you worksheet name


# Podio API credentials and base URL
client_id = ''
client_secret = ''
username = ''
password = ''
app_id = ''
base_url = 'https://api.podio.com'

# Authenticate and obtain access token
auth_url = f'{base_url}/oauth/token'
auth_data = {
    'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password
}

# Function to retrieve filtered items
def get_filtered_items():
    auth_response = requests.post(auth_url, data=auth_data)
    auth_response_json = auth_response.json()
    access_token = auth_response_json.get('access_token')

    if not access_token:
        print('Failed to obtain access token')
        print(auth_response_json)
        return None

    filter_data = {
        'limit': 500,
        'offset': 0
    }

    items_url = f'{base_url}/item/app/{app_id}/filter/'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    items_response = requests.post(items_url, headers=headers, json=filter_data)
    items_response_json = items_response.json()

    if 'items' not in items_response_json:
        print('Error: Items not found in the API response')
        print(items_response_json)
        return None

    return items_response_json['items']

# Main loop to continuously update data every 5 minutes
while True:
    filtered_items = get_filtered_items()

    if filtered_items:
        # Process filtered items and update data
        created_on_list = []
        total_price_today = []
        credit_card_processing_fee_today = []
        items_sold_list = []
        Number_of_WISPS_to_Create = []
        number_of_computers_list = []
        Specific_IT_Related_Requests = []
        Sales_Agent = []
        Source = []
        Podio_Item_ID = []
        Is_This_New_Accountant_Client = []
        commission_calculation = []
        Total_Sale_Calc = []
        Full_Compliance_Monthly_Fee_for_New_Computer = []
        Full_Compliance_New_Computer_Setup_Fee = []
        Full_Compliance_Monthly_Processing_Fees =[]
        Full_Compliance_Monthly_Payments_Starting_Today = []

        #   created_on
        for item in filtered_items:
            if 'created_on' in item:
                created_on = item['created_on']
                date_only = created_on.split()[0]  
                created_on_list.append(date_only)

        #   Podio Item ID
        for item in filtered_items:
          if 'app_item_id' in item:
            app_item_id = item['app_item_id']
            Podio_Item_ID.append(app_item_id)
            (app_item_id)

            #   Total Price Today
            for field in item['fields']:
                if field['label'] == "Total Price Today":
                    if 'values' in field and len(field['values']) > 0:
                        value = field['values'][0]['value']
                        total_price_today.append(value)

                #   Items Sold
                elif field['label'] == "Items Sold":
                    values = field['values']
                    for value in values:
                        items_sold_list.append(value['value'])
                    if not values:
                        items_sold_list.append(" ")

                #   Number of Computers
                elif field['label'] == "Number of Computers":
                    values = field['values']
                    for value in values:
                        number_of_computers_list.append(value['value'])
                    if not values:
                        number_of_computers_list.append(" ")

                #   Specific IT Related Requests
                elif field['label'] == 'Specific IT Related Requests':
                    for value in field['values']:
                        Specific_IT_Related_Requests.append(value['value'])
                    if not field['values']:
                        Specific_IT_Related_Requests.append(" ") 
                        
                #   Sales Agent                    
                elif field['label'] == 'Sales Agent':
                    for value in field['values']:
                        if 'value' in value and 'text' in value['value']:
                            sales_agent_text = value['value']['text']
                            Sales_Agent.append(sales_agent_text)
                    if not field['values']:
                        Sales_Agent.append(" ")
                        
                #   Is This A New Accountant Client?                
                elif field['label'] == 'Is This A New Accountant Client?':
                    for value in field['values']:
                         if 'text' in value['value']:
                             source_text = value['value']['text']
                             Is_This_New_Accountant_Client.append(source_text)
                    if not field['values']:
                        Is_This_New_Accountant_Client.append(" ")

        #   Commission Calculation
        for item in filtered_items:
            is_present = False
            for field in item['fields']:
                if field['label'] == "Commission Calculation":
                    values = field['values']
                    for value in values:
                        if 'value' in value and value['value'] != "":
                            commission_calculation.append(value['value'])
                        else:
                            commission_calculation.append(" ")
                    is_present = True
                    break
            if not is_present:
                commission_calculation.append(" ")

        #   Full Compliance: Monthly Fee for New Computer (Contract)
        for item in filtered_items:
            is_present = False
            for field in item['fields']:
                if field['label'] == 'Full Compliance: Monthly Fee for New Computer (Contract)':
                    if 'values' in field and len(field['values']) > 0:
                        values = field['values']
                        for value in values:
                            if 'value' in value:
                                Full_Compliance_Monthly_Fee_for_New_Computer.append(value['value'])
                                is_present = True
            if not is_present:
                Full_Compliance_Monthly_Fee_for_New_Computer.append(" ")

        #   Full Compliance: New Computer Setup Fee (Contract)
        for item in filtered_items:
            is_present = False  
            for field in item['fields']:
                if field['label'] == 'Full Compliance: New Computer Setup Fee (Contract)':
                    is_present = True  # Field is present
                    if 'values' in field and len(field['values']) > 0:
                        values = field['values']
                        for value in values:
                            if 'value' in value:
                                Full_Compliance_New_Computer_Setup_Fee.append(value['value'])
            if not is_present:
                Full_Compliance_New_Computer_Setup_Fee.append(" ")

        #   Full Compliance: Monthly Processing Fees
        for item in filtered_items:
            is_present = False  
            for field in item['fields']:
                if field['label'] == 'Full Compliance: Monthly Processing Fees':
                    is_present = True  # Field is present
                    if 'values' in field and len(field['values']) > 0:
                        values = field['values']
                        for value in values:
                            if 'value' in value:
                                Full_Compliance_Monthly_Processing_Fees.append(value['value'])
            if not is_present:
                Full_Compliance_Monthly_Processing_Fees.append(" ")

        #   Total Sale Calc
        for item in filtered_items:
            is_present = False  
            for field in item['fields']:
                if field['label'] == 'Total Sale Calc':
                    is_present = True  # Field is present
                    if 'values' in field and len(field['values']) > 0:
                        values = field['values']
                        for value in values:
                            if 'value' in value:
                                Total_Sale_Calc.append(value['value'])
            if not is_present:
                Total_Sale_Calc.append(" ")

        #   Credit Card Processing Fee Today
        for item in filtered_items:
            is_present = False
            for field in item['fields']:
                if field['label'] == "Credit Card Processing Fee Today":
                    values = field['values']
                    for value in values:
                        if 'value' in value and value['value'] != "":
                            credit_card_processing_fee_today.append(value['value'])
                        else:
                            credit_card_processing_fee_today.append(" ")
                    is_present = True
                    break
            if not is_present:
                credit_card_processing_fee_today.append(None)

        #   Source
        for item in filtered_items:
            is_present = False
            for field in item['fields']:
                if field['label'] == "Source":
                    values = field['values']
                    for value in values:
                        if 'value' in value and value['value'] != "":
                            Source.append(value['value']['text'])
                        else:
                            Source.append(" ")
                    is_present = True
                    break
            if not is_present:
                Source.append(None)


        #   Number of WISPS to Create
        for item in filtered_items:
            is_present = False
            for field in item['fields']:
                if field['label'] == "Number of WISPS to Create":
                    values = field['values']
                    for value in values:
                        if 'value' in value and value['value'] != "":
                            Number_of_WISPS_to_Create.append(value['value'])
                        else:
                            Number_of_WISPS_to_Create.append(" ")
                    is_present = True
                    break
            if not is_present:
                Number_of_WISPS_to_Create.append(" ")

        #   Full Compliance: Monthly Payments Starting Today
        for item in filtered_items:
            is_present = False
            for field in item['fields']:
                if field['label'] == "Full Compliance: Monthly Payments Starting Today":
                    values = field['values']
                    for value in values:
                        if 'value' in value and value['value'] != "":
                            Full_Compliance_Monthly_Payments_Starting_Today.append(value['value'])
                        else:
                            Full_Compliance_Monthly_Payments_Starting_Today.append(" ")
                    is_present = True
                    break
            if not is_present:
                Full_Compliance_Monthly_Payments_Starting_Today.append(" ")

        data = {
            'Created On': created_on_list,
            'Total Price Today': total_price_today,
            'Credit Card Processing Fee Today': credit_card_processing_fee_today,
            'Items Sold': items_sold_list,
            'Number of WISPS to Create' : Number_of_WISPS_to_Create,
            'Number of Computers': number_of_computers_list,
            'Specific IT Related Requests': Specific_IT_Related_Requests,
            'Sales Agent': Sales_Agent,
            'Source': Source,
            'Is This New Accountant Client': Is_This_New_Accountant_Client,
            'Full Compliance: Monthly Payments Starting Today':Full_Compliance_Monthly_Payments_Starting_Today,
            'Full Compliance: Monthly Processing Fees' :  Full_Compliance_Monthly_Processing_Fees,
             'Full Compliance: New Computer Setup Fee (Contract)': Full_Compliance_New_Computer_Setup_Fee,
            'Full Compliance: Monthly Fee for New Computer (Contract)' :Full_Compliance_Monthly_Fee_for_New_Computer,
            'Total Sale Calc': Total_Sale_Calc,
            'Commission Calculation': commission_calculation,
            'Podio Item ID': Podio_Item_ID
        }
        
        final_data = pd.DataFrame(data)
        # Clear the existing content in the worksheet
        worksheet.clear()

        # Update the worksheet with the new data
        set_with_dataframe(worksheet, final_data)

        print('Data pushed successfully to the Google Sheet.')

    # Wait for 50sec before the next update
    time.sleep(50)  


