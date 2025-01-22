"""
*******************************************************************************
@file   module_DielectricCalibration.py
@author Scott Thomason
@date   10 Nov 2021
@brief  VNA calibration module. This will be used for the calibration and 
        conversion of measurements from the VNA. This uses the Neural Network 
        that was developed by Nghia to convert the S parameter data to moisture 
        and density.

REFERENCE:

*******************************************************************************
    Functions
*******************************************************************************

*******************************************************************************
"""

""" Imports 
*******************************************************************************
"""

import os
import numpy as np
import cmath
import skrf as rf
import datetime
from copy import deepcopy
from MudMasterUI.supportFunctions import *
from skrf.io import Touchstone


import joblib  # For loading the model and scaler


""" Defines
*******************************************************************************
"""
DNN_Model = None
ElasticNet_Model_20CM = None
ElasticNet_Model_scaler_20CM = None
ElasticNet_Model_50CM = None
ElasticNet_Model_scaler_50CM = None
ElasticNet_Model_80CM = None
ElasticNet_Model_scaler_80CM = None

""" NN Functions
*******************************************************************************
"""


def nn_data_formatter(data_list, freq_min, freq_max):
    """ @brief  Formats the data for the neural network. This will take the s11_cal data and store it in a numpy array. The data will be stored in the following format:
                    [[s11_cal_real_1, s11_cal_real_2, ..., s11_cal_real_n, s11_cal_imag_1, s11_cal_imag_2, ..., s11_cal_imag_n],],
                    [[s11_cal_real_1, s11_cal_real_2, ..., s11_cal_real_n, s11_cal_imag_1, s11_cal_imag_2, ..., s11_cal_imag_n],],

                    Each row is a separate data entry.
                The freq_min and freq_max are used to specify the range of data to be used, data outside of these frequencies will not be included.
        @param  data_list - The data to format.
                freq_min - The minimum frequency to use.
                freq_max - The maximum frequency to use.
        @retval formatted_data - The formatted data as a numpy array.
    """
    formatted_data_x = []

    # use the first data entry and the freq_min and freq_max to find the indices to use
    freq_index_min = np.argmin(np.abs(data_list[0]['frequency'] - freq_min))#maybe here is the issue with sensor 
    freq_index_max = np.argmin(np.abs(data_list[0]['frequency'] - freq_max))

    # print out the indices
    print('Using indices: {} to {}'.format(freq_index_min, freq_index_max))

    print('Using data from {} to {}'.format(data_list[0]['frequency'][freq_index_min], data_list[0]['frequency'][freq_index_max]))

    # loop through the data and store the data in the correct format
    for data_entry in data_list:
        # now create an array of the real and imaginary components
        tmp_array = np.concatenate((data_entry['S11_cal_R'][freq_index_min:freq_index_max], data_entry['S11_cal_I'][freq_index_min:freq_index_max]), axis=0)
        # append the data to the list
        formatted_data_x.append(tmp_array)

    return np.array(formatted_data_x)


def nn_calculate_permittivity(Theta1, Theta2, s11_in, permittivity_min, permittivity_max):
    """ @brief  Calculates the permittivity of the material using the trained 
                neural network and the calibrated reflection coefficient.
        @param  Theta1 - The parameters for the first layer.
                Theta2 - The parameters for the second layer.
                s11_in - The input data - calibrated reflection coefficient.
                permittivity_min - The minimum permittivity of the material - used for scaling the NN output.
                permittivity_max - The maximum permittivity of the material - used for scaling the NN output.
        @retval permittivity - The permittivity of the material.

    """
    #print("nn_calculate_permittivity 1 ")
    pred_y = predict(Theta1, Theta2, s11_in)
    #print("nn_calculate_permittivity 2 ")

    # convert the predicted y values back to a permittivity value
    return scale_permittivity_from_nn(pred_y, permittivity_min, permittivity_max)


def scale_permittivity_from_nn(scaled_permittivity, permittivity_min, permittivity_max):
    """ @brief  Scales the permittivity from the range of the neural network.
        @param  scaled_permittivity - The scaled permittivity.
        @param  permittivity_min - The minimum permittivity.
        @param  permittivity_max - The maximum permittivity.
        @retval permittivity - The permittivity.
    """
    permittivity = scaled_permittivity * (permittivity_max - permittivity_min) + permittivity_min
    return permittivity


def predict(Theta1, Theta2, X):
    """ @brief  Predicts the output of the neural network.
        @param  Theta1 - The parameters for the first layer.
        @param  Theta2 - The parameters for the second layer.
        @param  X - The input data.
        @retval p - The predicted output.

    """
    m = X.shape[0]
    p = np.zeros((m, 1))
    h1 = sigmoid(np.hstack((np.ones((m, 1)), X)) @ Theta1.conj().T)
    p = sigmoid(np.hstack((np.ones((m, 1)), h1)) @ Theta2.conj().T)

    return p


def sigmoid(z):
    """ @brief  Computes the sigmoid of z.
        @param  z - The input value.
        @retval g - The sigmoid of z.

    """
    g = 1 / (1 + np.exp(-z))
    return g


""" Classes
*******************************************************************************
"""

class VNA_Cal(object):
    def __init__(self, app=None):
        """ @brief  Initialisation function for the VNA calibration module.
            @param  app - instance of the application.
            @retval None - Initialisation function.

        """
        self._calData = {} # dictionary of calibration data from the VNA - as {actuator_extension: {'frequency': np.array([]), 'S11R': np.array([]), 'S11I': np.array([])}}

        # neural network training parameters
        self._theta1 = None
        self._theta2 = None
        
        self.DNN_Model = None

        if(app != None):
            self.init_app(app)


    def init_app(self, app):
        """ @brief  Initialises the VNA manager. 
            @param  app - the flask app object
            @retval None

        """
        self._app = app

        # load the values for theta1 and theta2 from the nn/theta_file
        theta = np.load(self._app.config['CONFIG_SYSTEM']['nn']['theta_file'], allow_pickle=True).item()
        self._theta1 = theta['Theta1']
        self._theta2 = theta['Theta2']

        # check if there is any calibration data file, if so, load them in
        if(os.path.exists(self._app.config['CONFIG_DIRECTORY_VNA_CAL'])):
            # iterate through the files in the directory and load them into the calibration data
            for file in os.listdir(self._app.config['CONFIG_DIRECTORY_VNA_CAL']):
                if(file.endswith('.s1p')):
                    with open(os.path.join(self._app.config['CONFIG_DIRECTORY_VNA_CAL'], file), 'r') as infile:
                        # read the touchstone file using the skrf library - the file name is the actuator position
                        self._calData[int(file.split('.')[0])] = Touchstone(os.path.join(self._app.config['CONFIG_DIRECTORY_VNA_CAL'], file)).get_sparameter_data()

    
    def is_calibrated(self):
        """ @brief  Checks if the VNA is calibrated.
            @param  None
            @retval True if the VNA is calibrated, False otherwise.

        """
        return len(self._calData) > 0


    def get_calibration_positions(self):
        """ @brief  Returns the calibration data names.
            @param  None
            @retval self._calData - The calibration data.

        """
        return list(self._calData.keys())


    def add_calibration_measurement(self, actuator_extension, data_dict):
        """ @brief  Method used to set the calibration data to the internal reference. 
            @param  actuator_extension - the actuator extension that the data was taken at - in mm.
            @param  data_dict - dictionary of data retrieved from the VNA. Formatted as {'frequency': np.array([]), 'S11R': np.array([]), 'S11I': np.array([])}
            @retval None

        """
        self._calData[actuator_extension] = deepcopy(data_dict)
        print('Calibration data added for actuator extension: ' + str(actuator_extension))
        print('total number of calibration data points: ' + str(len(self._calData)))

        # if the calibration data directory doesn't exist, create it
        create_directories(self._app)

        save_s11_data(str(actuator_extension), self._app.config['CONFIG_DIRECTORY_VNA_CAL'], data_dict)


    # a function to save the current calibration data so that it can be used with the data at a later date
    def save_calibration_data(self, save_directory):
        """ @brief  Saves the calibration data to a file.
            @param  save_directory - the directory to save the calibration data to.
            @retval None

        """
        # create the save directory if it doesn't exist. The current date and time should be added to the directory name

        if(not os.path.exists(save_directory)):
            os.makedirs(save_directory)

        # save the calibration data as separate s1p files in a folder called calibration in the output data directory, they should be named with their actuator extension
        for actuator_extension in self._calData:
            save_s11_data(str(actuator_extension), save_directory, self._calData[actuator_extension])


    def clear_calibration_data(self):
        """ @brief  Clears the calibration data.
            @param  None
            @retval None

        """
        self._calData = {}

        # delete the calibration data directory if it exists
        if(os.path.exists(self._app.config['CONFIG_DIRECTORY_VNA_CAL'])):
            os.rmdir(self._app.config['CONFIG_DIRECTORY_VNA_CAL'])
            


    def convert_to_permittivity(self, data_dict, actuator_extension):
        """ @brief  Uses the calibration data to calculate the permittivity of the input data. 
            @param  data_dict - input data to convert. Formatted as {'frequency': np.array([]), 'S11R': np.array([]), 'S11I': np.array([])}
            @param  actuator_extension - the actuator extension that the data was taken at - in mm.
            @retval None

        """
        # find the calibration data with the closest actuator_extension
        closest_actuator_extension = min(self._calData.keys(), key=lambda x: abs(float(x) - float(actuator_extension)))
        print('Closest actuator extension: ' + str(closest_actuator_extension))

        # first need to calibrate the data using the relevant calibration data - matched using the actuator extension. This involves subtracting the calibration data from the input data
        data_dict['S11_cal_R'] = data_dict['S11R'] - self._calData[closest_actuator_extension]['S11R']
        data_dict['S11_cal_I'] = data_dict['S11I'] - self._calData[closest_actuator_extension]['S11I']
        data_x = nn_data_formatter([data_dict], freq_min=self._app.config['CONFIG_SYSTEM']['nn']['frequency_scale']['min'], freq_max=self._app.config['CONFIG_SYSTEM']['nn']['frequency_scale']['max'])
        #print("here from convert to permittivity 2 ")
        predicted_permittivity = nn_calculate_permittivity(Theta1=self._theta1, Theta2=self._theta2, s11_in=data_x, permittivity_min=self._app.config['CONFIG_SYSTEM']['nn']['permittivity_scale']['min'], permittivity_max=self._app.config['CONFIG_SYSTEM']['nn']['permittivity_scale']['max'])
        #print("here from convert to permittivity 3 ")
        print('Predicted permittivity: ' + str(predicted_permittivity[0][0]))

        return predicted_permittivity[0][0]
    
    
    
    
    
    
        """ DNN Functions or new model functions 
    *******************************************************************************
    """
    
    def load_model(self):
        global DNN_Model
        global ElasticNet_Model_50CM
        global ElasticNet_Model_scaler_50CM
        global ElasticNet_Model_20CM
        global ElasticNet_Model_scaler_20CM
        global ElasticNet_Model_80CM
        global ElasticNet_Model_scaler_80CM
        #change to config if decide to use 
        model_path_20 = self._app.config['ELASTICNET_MODEL_LOCATION_TWENTYCM']  # Hard-coded model path
        scaler_path_20 = self._app.config['ELASTICNET_SCALER_LOCATION_TWENTYCM']   # Hard-coded scaler path
        
        model_path_50 = self._app.config['ELASTICNET_MODEL_LOCATION_FIFITYCM']  # Hard-coded model path
        scaler_path_50 = self._app.config['ELASTICNET_SCALER_LOCATION_FIFITYCM']   # Hard-coded scaler path
        
        model_path_80 = self._app.config['ELASTICNET_MODEL_LOCATION_EIGHTYCM']  # Hard-coded model path
        scaler_path_80 = self._app.config['ELASTICNET_SCALER_LOCATION_EIGHTYCM']   # Hard-coded scaler path
        
            
        if ElasticNet_Model_50CM is None:
            try:
                ElasticNet_Model_50CM = joblib.load(model_path_50)
                print("50CM ElasticNet_Model loaded successfully.")
            except Exception as e:
                print(f"An error occurred while loading the 50CM ElasticNet_Model: {e}")
        else:
            print("50CM ElasticNet_Model is already loaded, skipping load.")
            
        if ElasticNet_Model_scaler_50CM is None:
            try:
                ElasticNet_Model_scaler_50CM = joblib.load(scaler_path_50)
                print("50CM ElasticNet_Model_scaler loaded successfully.")
            except Exception as e:
                print(f"An error occurred while loading the 50CM ElasticNet_Model_scaler: {e}")
        else:
            print("50CM ElasticNet_Model_scaler is already loaded, skipping load.")
            
        if ElasticNet_Model_20CM is None:
            try:
                ElasticNet_Model_20CM = joblib.load(model_path_20)
                print("20CM ElasticNet_Model loaded successfully.")
            except Exception as e:
                print(f"An error occurred while loading the 20CM ElasticNet_Model: {e}")
        else:
            print("20CM ElasticNet_Model is already loaded, skipping load.")
            
        if ElasticNet_Model_scaler_20CM is None:
            try:
                ElasticNet_Model_scaler_20CM = joblib.load(scaler_path_20)
                print("20CM ElasticNet_Model_scaler loaded successfully.")
            except Exception as e:
                print(f"An error occurred while loading the 20CM ElasticNet_Model_scaler: {e}")
        else:
            print("20CM ElasticNet_Model_scaler is already loaded, skipping load.")
            
        if ElasticNet_Model_80CM is None:
            try:
                ElasticNet_Model_80CM = joblib.load(model_path_80)
                print("80CM ElasticNet_Model loaded successfully.")
            except Exception as e:
                print(f"An error occurred while loading the 80CM ElasticNet_Model: {e}")
        else:
            print("80CM ElasticNet_Model is already loaded, skipping load.")
            
        if ElasticNet_Model_scaler_80CM is None:
            try:
                ElasticNet_Model_scaler_80CM = joblib.load(scaler_path_80)
                print("80CM ElasticNet_Model_scaler loaded successfully. ")
            except Exception as e:
                print(f"An error occurred while loading the 80CM ElasticNet_Model_scaler: {e}")
        else:
            print("80CM ElasticNet_Model_scaler is already loaded, skipping load.")

    
    def prepare_live_data( self, data_dict):
        """Prepare live data for model input, including magnitude and phase."""
        s11_real = data_dict['S11R']
        s11_imag = data_dict['S11I']
        
        # Calculate magnitudes and phases
        magnitudes = np.sqrt(s11_real**2 + s11_imag**2)
        phases = np.arctan2(s11_imag, s11_real)
        
        # Combine real, imaginary, magnitude, and phase
        formatted_data = np.concatenate([s11_real, s11_imag, magnitudes, phases]).reshape(1, -1)  # Reshape for single prediction
        return formatted_data

    
    def run_model_on_live_data_elasticNet(self, data_dict):
        """
        Run the ElasticNet model on live data and print the prediction.
        
        Parameters:
        model_path (str): Path to the trained ElasticNet model.
        scaler_path (str): Path to the saved StandardScaler.
        data_dict (dict): A dictionary containing live data to be processed.
        """
        global ElasticNet_Model_20CM
        global ElasticNet_Model_scaler_20CM
        
        global ElasticNet_Model_50CM
        global ElasticNet_Model_scaler_50CM
        
        global ElasticNet_Model_80CM
        global ElasticNet_Model_scaler_80CM

        # Step 1: Prepare the live data (assuming prepare_live_data function is available)
        formatted_data = VNA_Cal.prepare_live_data(self, data_dict)
        
        # Step 3: Preprocess (normalize) the live data using the loaded scaler
        formatted_data_normalized_50 = ElasticNet_Model_scaler_50CM.transform(formatted_data)
        
        # Step 4: Make prediction using the trained ElasticNet model
        prediction_50 = ElasticNet_Model_50CM.predict(formatted_data_normalized_50)
        
        # Step 3: Preprocess (normalize) the live data using the loaded scaler
        formatted_data_normalized_80 = ElasticNet_Model_scaler_80CM.transform(formatted_data)
        
        # Step 4: Make prediction using the trained ElasticNet model
        prediction_80 = ElasticNet_Model_80CM.predict(formatted_data_normalized_80)
        
        # Step 3: Preprocess (normalize) the live data using the loaded scaler
        formatted_data_normalized_20 = ElasticNet_Model_scaler_20CM.transform(formatted_data)
        
        # Step 4: Make prediction using the trained ElasticNet model
        prediction_20 = ElasticNet_Model_20CM.predict(formatted_data_normalized_20)
        
        # Step 5: Print the prediction result
        print(f"Predicted value for ElasticNet Model 20cm: {prediction_20[0]:.2f}")
        print(f"Predicted value for ElasticNet Model 50cm: {prediction_50[0]:.2f}")
        print(f"Predicted value for ElasticNet Model 80cm: {prediction_80[0]:.2f}")
        
        # Return the prediction
        #return prediction[0]
        return [prediction_20[0],prediction_50[0],prediction_80[0]]

    
    