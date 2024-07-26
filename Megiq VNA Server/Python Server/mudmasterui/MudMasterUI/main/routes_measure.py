"""
*******************************************************************************
@file   MudMasterUI.main.routes_measure.py
@author Scott Thomason
@date   04 May 2022
@brief  Routes for the main section of the app. This is for the calibration 
        section.

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
from MudMasterUI import controller_vna, controller_mountingSystem, module_dielectric_manager, measurement_manager

""" Defines
*******************************************************************************
"""


""" Routes
*******************************************************************************
"""
@bp.route('/measure')
def measure():
    measurement_manager.start_measurement()

    return render_template(
        'main/measure.html',
        title='Tailings Measurement',
        year=datetime.now().year,
        showFooter = True,
    )


@bp.route('/measure/run', methods = ['GET', 'POST'])
def measure_start():
    print('starting calibration')
    measurement_manager.run_calibration()
    return jsonify(measurement_manager.get_calibration_progress())


@bp.route('/measure/stop', methods = ['GET'])
def measure_progress():
    return jsonify(measurement_manager.get_calibration_progress())