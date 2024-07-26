"""
*******************************************************************************
@file   site_config.py
@author Scott Thomason
@date   01 May 2022
@brief  Configuration file for the different sites the machine is operating at.

        New sites can be added to the configuration using the following steps:
            1. Copy the default site configuration and paste it in after the 
                last site in the dictionary.
            2. Change the site id from 'default' to the new site id.
            3. Change the site name from 'Default' to the new site name.
            4. Change the country name to the country the site is located in.
            5. Fill the 'model_water' partial function parameters with the 
                gradient and intercept from the water model fitting.
            6. Fill the 'model_density' partial function parameters with:
                a. (G) - The gravimetric density in g/cm^3, and
                b. (S) - The saturation as a decimal between 0 and 1.

                Note: gamma_w doesn't need to be changed, it is acceleration 
                due to gravity.

        After adding a new site, the updated code will need to be pushed to the 
        repository. Then the updated code can be pulled on the machines to used.

REFERENCE:

*******************************************************************************
    Functions
*******************************************************************************

*******************************************************************************
"""

""" Imports 
*******************************************************************************
"""

from functools import partial
from MudMasterUI.supportFunctions import model_water_percentage, model_density

""" Defines
*******************************************************************************
"""


""" Site Config
*******************************************************************************
"""

class Site_Config(object):
    # sites are configured with the site name as the key, inside is the partial function for the model_water and model_density functions.
    SITE_CONFIG = {
        'default': {  # this is a placeholder for when the site is not known
            'name': 'Default',
            'country': 'Default',
            'calibration_date': None,
            'model_water': partial(  # needs permittivity as an input parameter
                model_water_percentage,
                gradient_value=0.16601,
                intercept_value=36.1093
            ),
            'model_density': partial(  # needs water percentage (0 - 100) as an input parameter
                model_density,
                G=2.57,  # gravimetric density (g/cm^3)
                gamma_w=9.81,  # m/s^2
                S=1.0,  # saturation (0 - 1)
            ),
        },
        'port_of_brisbane': {
            'name': 'Port of Brisbane',
            'country': 'Australia',
            'calibration_date': '20 July 2020',
            'model_water': partial(  # needs permittivity as an input parameter
                model_water_percentage,
                gradient_value=0.16601,
                intercept_value=36.1093
            ),
            'model_density': partial(  # needs water percentage (0 - 100) as an input parameter
                model_density,
                G=2.57,
                gamma_w=9.81,
                S=1.0,
            ),
        },
    }
