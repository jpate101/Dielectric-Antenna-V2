"""
*******************************************************************************
@file   MudMasterUI.main.routes.py
@author Scott Thomason
@date   02 Feb 2022
@brief  Routes for the main section of the app.

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

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify, make_response, abort, Blueprint, current_app, session

from MudMasterUI.main import bp
from MudMasterUI.supportFunctions import save_run_config
from MudMasterUI import controller_vna, controller_mountingSystem, module_dielectric_manager, measurement_manager

""" Defines
*******************************************************************************
"""


""" Routes
*******************************************************************************
"""
@bp.route('/')
@bp.route('/home')
def home():
    """Renders the home page."""
    measurement_manager.set_idle()
    return render_template(
        'main/index.html',
        title='Home Page',
        year=datetime.now().year,
        showFooter = True
    )


@bp.route('/settings', methods=['GET'])
def settings():
    """Renders the settings page."""
    # generate a list of sites from the site config
    sites = list(
        {
            'id': key,
            'name': current_app.config['SITE_CONFIG'][key]['name'],
            'country': current_app.config['SITE_CONFIG'][key]['country'],
            'calibration_date': current_app.config['SITE_CONFIG'][key]['calibration_date']
        } for key in current_app.config['SITE_CONFIG'].keys()
    )

    return render_template(
        'main/settings.html',
        title='Settings',
        year=datetime.now().year,
        showFooter = True,
        sites = sites,
        measurement_delays = current_app.config['CONFIG_SYSTEM']['measurement_manager']['measurement_delay_list'],
    )


@bp.route('/settings', methods=['POST'])
def settings_post():
    # receive the settings updates that have been sent as post requests
    print(request)
    received_data = json.loads(request.get_data().decode())

    print(received_data)

    # update the settings in the config file
    if('site' in received_data):
        if received_data['site'] in current_app.config['SITE_CONFIG'].keys():
            current_app.config['CONFIG_RUN']['site'] = received_data['site']
            
            # save run config
            save_run_config(current_app)

            # update the site in the measurement manager
            measurement_manager.set_site(current_app.config['CONFIG_RUN']['site'])

    if 'measurement_delay' in received_data:
        current_app.config['CONFIG_RUN']['measurement_manager']['measurement_delay'] = int(received_data.get('measurement_delay', 60))

        # save run config
        save_run_config(current_app)

    return jsonify({'success': True})




@bp.route('/run-menu')
def run_menu():
    """Renders the run menu page."""
    return render_template(
        'main/run_menu.html',
        title='Run Menu',
        year=datetime.now().year,
        showFooter = True
    )