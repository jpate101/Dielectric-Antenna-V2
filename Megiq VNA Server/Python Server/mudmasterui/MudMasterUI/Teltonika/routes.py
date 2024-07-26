"""
*******************************************************************************
@file   MudMasterUI.eventStreams.routes.py
@author Scott Thomason
@date   28 Mar 2022
@brief  Routes for the app's event streams.

REFERENCE:

*******************************************************************************
    Functions
*******************************************************************************

*******************************************************************************
"""

""" Imports
*******************************************************************************
"""
import json
import time
import os

import requests
import json 

import random
import numpy as np

from datetime import datetime
from copy import deepcopy
from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify, make_response, abort, Blueprint, current_app, session, Response
from copy import deepcopy

from MudMasterUI import controller_vna, controller_mountingSystem, module_dielectric_manager, measurement_manager

from MudMasterUI.Teltonika import bp


""" Defines
*******************************************************************************
"""
token = None
DEVICE_IP = "192.168.1.1" 

""" Routes
*******************************************************************************
"""
@bp.route('/TeltonikaUI')
def home():
    """Renders the home page."""
    measurement_manager.set_idle()
    return render_template(
        'main/index.html',
        title='TeltonikaUI',
        year=datetime.now().year,
        showFooter = True
    )

@bp.route('/Teltonika/test', methods=['GET'])
def test_endpoint():
    # Replace this with any data you want to return
    data = {'message': 'This is a test endpoint'}

    # jsonify converts the dictionary into JSON format
    return jsonify(data)

#@bp.route('/Teltonika/login', methods=['POST'])





