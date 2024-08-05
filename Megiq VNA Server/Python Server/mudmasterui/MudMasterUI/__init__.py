"""
The flask application package.
"""
import threading

from flask import Flask
from MudMasterUI.config import Config
from MudMasterUI.supportFunctions import *
from MudMasterUI.config_site import Site_Config

from MudMasterUI.config_machine import Config_Machine

from MudMasterUI.interface_vna import VNA_Manager
from MudMasterUI.interface_mountingSystem import MountingSystem_Manager
from MudMasterUI.module_dielectricCalibration import VNA_Cal
from MudMasterUI.module_measurement_manager import Measurement_Manager

controller_vna = VNA_Manager()
controller_mountingSystem = MountingSystem_Manager()
module_dielectric_manager = VNA_Cal()
measurement_manager = Measurement_Manager()



def createApp(config_main=Config, config_machine=Config_Machine, site_config=Site_Config):
    app = Flask(__name__)
    app.config.from_object(config_main)
    app.config.from_object(config_machine)
    app.config.from_object(site_config)

    # configure the machine directory in the config dictionary
    app.config['MACHINE_DIRECTORY'] = app.config['MACHINE_DIRECTORY'].format(app.config['CONFIG_MACHINE']['machineNumber'], app.config['CONFIG_MACHINE']['machineNumber'])

    create_directories(app)
    load_run_config(app)

    controller_vna.init_app(app)
    controller_mountingSystem.init_app(app)
    module_dielectric_manager.init_app(app)
    
    measurement_manager.init_app(app, controller_mountingSystem, controller_vna, module_dielectric_manager)
    

    from MudMasterUI.main import bp as bp_main
    app.register_blueprint(bp_main)

    from MudMasterUI.eventStreams import bp as bp_eventStreams
    app.register_blueprint(bp_eventStreams)

    from MudMasterUI.vna import bp as bp_vna
    app.register_blueprint(bp_vna)

    #added be Joshua 
    from MudMasterUI.mountingSystemV2 import bp as bp_mountingSystemV2
    app.register_blueprint(bp_mountingSystemV2)
    
    return app
