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

CurrentlyExtending = False
CurrentlyRetracting = False
CurrentlyReadingVNA = False 

#will need errors for 
# port permission error # may not need as actuator permissions are fixed 
# Failed to read GPS data 
# VNA refused connection 
# 
# indicators for 
# currently extending/retracting 
# currently reading VNA 
# 
# #