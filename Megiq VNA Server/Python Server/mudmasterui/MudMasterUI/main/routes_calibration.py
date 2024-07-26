"""
*******************************************************************************
@file   MudMasterUI.main.routes_calibration.py
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
@bp.route('/calibration')
def calibration():
    progress = measurement_manager.get_calibration_progress()
    return render_template(
        'main/calibration.html',
        title='System Calibration',
        year=datetime.now().year,
        showFooter = True,
        progress = progress['progress'],
    )


@bp.route('/calibration/progress', methods = ['GET'])
def calibration_progress():
    return jsonify(measurement_manager.get_calibration_progress())


@bp.route('/calibration/run', methods = ['GET', 'POST'])
def calibration_start():
    print('starting calibration')
    measurement_manager.run_calibration()
    return jsonify(measurement_manager.get_calibration_progress())


@bp.route('/calibration/clear', methods = ['GET', 'POST'])
def calibration_clear():
    measurement_manager.clear_calibration()
    return jsonify(measurement_manager.get_calibration_progress())