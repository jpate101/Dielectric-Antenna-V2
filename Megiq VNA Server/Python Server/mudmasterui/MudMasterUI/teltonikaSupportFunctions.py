
import json
import time
#import os
import threading

import requests
import json 

#import random
#import numpy as np

#from datetime import datetime
#from copy import deepcopy
#from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify, make_response, abort, Blueprint, current_app, session, Response
#from copy import deepcopy
from MudMasterUI.config import Config
from MudMasterUI import globalErrorVar

""" Defines
*******************************************************************************
"""
token = None
DEVICE_IP = Config.CONFIG_SYSTEM['teltonika']['DEVICE_IP']

""" Functions
*******************************************************************************
"""


def login_endpoint():
    global token
    url = f'http://{DEVICE_IP}/api/login'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'username': Config.CONFIG_SYSTEM['teltonika']['username'],
        'password': Config.CONFIG_SYSTEM['teltonika']['password']
    }

    try:
        # Convert the data dictionary to JSON format
        json_data = json.dumps(data)

        # Make the POST request
        response = requests.post(url, headers=headers, data=json_data)

        # Check if the request was successful (status code 2xx)
        if response.ok:
            #print(f'Response Status Code: {response.status_code}')
            #print('Response Content:')
            #print(response.text)
            if(response.status_code == 200):
                    #saves token as variable 
                    # Convert response content to JSON
                    data = response.json()
                    token = data.get('data', {}).get('token')
            #print(token)
            #print("end of login")
            return token  # Return JSON response as Python dictionary
        else:
            globalErrorVar.ErrorFromTeltonika = True
            response.raise_for_status()  # Raise an HTTPError for non-2xx status codes

    except requests.exceptions.RequestException as e:
        globalErrorVar.ErrorFromTeltonika = True
        print(f'Error making request: {e}')  # Handle connection errors, timeouts, etc.
    
    return None  # Return None if request fails

def get_GPS_data_endpoint():
    global token
    url = f'http://{DEVICE_IP}/ubus'  # Adjust the URL as per your device's API endpoint
    headers = {

    }
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "call",
        "params": [
            f'{token}',
            "file",
            "exec",
            {
                "command": "gpsctl",
                "params": ["-ix"]
            }
        ]
    }
    
    #print(payload)
    
    try:
        # Make the POST request with JSON payload
        response = requests.post(url, headers=headers, json=payload)

        # Check if the request was successful (status code 2xx)
        if response.ok:
            #print(f'Response Status Code: {response.status_code}')
            #print('Response Content:')
            #print(response.json())  # Print the entire JSON response
            
            # Parse the response to get latitude and longitude
            result = response.json().get('result', [])
            if len(result) > 1:
                stdout = result[1].get('stdout', '')
                latitude, longitude = map(float, stdout.strip().split())
                #print(f'Latitude: {latitude}, Longitude: {longitude}')
                if(latitude == 0 and longitude == 0):
                    print("gps values are 0 and 0 likely no gps")
                    globalErrorVar.ErrorFromTeltonika = True
                    pass
                # Return the GPS data as a dictionary
                globalErrorVar.ErrorFromTeltonika = False
                return {"latitude": latitude, "longitude": longitude}
            else:
                globalErrorVar.ErrorFromTeltonika = True
                print('Unexpected response structure')
                return {"Response Structure Error"}
        else:
            globalErrorVar.ErrorFromTeltonika = True
            response.raise_for_status()  # Raise an HTTPError for non-2xx status codes
            return {"Response Not ok"}

    except requests.exceptions.RequestException as e:
        globalErrorVar.ErrorFromTeltonika = True
        print(f'Error making request: {e}')  # Handle connection errors, timeouts, etc.
        return {"Request Exception": str(e)}

    return {"Error from teltonika"}  # Return None if request fails


class Teltonika_Measurement_Manager(object):

    def init_app(self, app, vna):
        """ Initializes the Continuous_Measurement_Manager.
        
        Args:
            app (Flask): The Flask app object.
            vna: The object representing the VNA.

        Returns:
            None
        """
        self._app = app
        self._vna = vna


