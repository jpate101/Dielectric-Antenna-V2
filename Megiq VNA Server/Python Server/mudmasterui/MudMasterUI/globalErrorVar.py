"""
*******************************************************************************
@file   interface_MountingSystem.py
@author Joshua Paterson
@date   30 Sep 2024
@brief  stores variable for error logging for UI 
REFERENCE:
"""

"""

*******************************************************************************
    Functions
*******************************************************************************

*******************************************************************************
"""

ErrorFromMeasurementManager = False # error for timeout when reading VNA 
ErrorFromActuatorReadWrite = False # read write errors from sending actuator command 
ErrorFromTeltonika = False # error due to cant find teltonika on network or recieved a none 200 response  

CurrentlyExtending = False # used to show on ui when actuator is extending 
CurrentlyRetracting = False # used to show on ui when actuator is Retracting 
CurrentlyCalibrating = False # used to show on ui when actuator is calibrating 
CurrentlyLogging = False # # used to show on ui when actuator is Logging 

#will need errors for 
# VNA refused connection 
# 
# indicators for 
