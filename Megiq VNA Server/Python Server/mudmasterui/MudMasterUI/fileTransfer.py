import os
import shutil
import time
import threading
import subprocess


class File_Transfer(object):
    """
    *****************************************************************************
    @file   file_transfer.py
    @author Joshua Paterson
    @date   20 August 2024
    @brief  Handles the transfer of new files from a source folder to a destination folder.
    REFERENCE:
        This module provides a class to monitor a source directory and copy any new
        files to a destination directory. It operates in a separate thread, periodically
        checking for new files to copy.
    
    *****************************************************************************
        Methods
    *****************************************************************************
        __init__(self, app):
            Initializes the File_Transfer object with application context and starts
            a background thread to handle file transfer operations.

        copy_new_files(self):
            Checks the source folder for new files and copies them to the destination
            folder if they are not already present there.

        run(self):
            Runs in a separate thread to continuously check for and transfer new files
            at regular intervals (currently every 30 minutes).
    *****************************************************************************
    """
    
    def __init__(self, app):
        """Initialize the File_Transfer object and start the file transfer thread."""
        
        self._app = app
        
        # Define source and destination folder paths
        self.src_folder = self._app.config['MACHINE_DIRECTORY']
        #self._app.config['CONFIG_SYSTEM']['mountingSystem']['actuator_min']
        self.dest_folder = self._app.config['TRANSFER_DIRECTORY']
        
        # Create and start a thread to run the file transfer process
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # This ensures the thread will exit when the main program exits
        print("- one drive start 1-")
        self.thread.start()
        
    def copy_new_files(self):
        """Copy new or updated files from src_folder to dest_folder and delete them from the source if they are not the latest.
        Also include subfolders while keeping the folder structure in both locations, excluding folders named 'calData'.
        """
        def process_directory(src_dir, dest_dir):
            # Ensure destination folder exists, create it if necessary
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            for item in os.listdir(src_dir):
                src_item = os.path.join(src_dir, item)
                dest_item = os.path.join(dest_dir, item)

                if os.path.isdir(src_item):
                    if item != 'calData':
                        process_directory(src_item, dest_item)
                    # Skip the 'calData' folder, no further processing needed
                    
                elif os.path.isfile(src_item):
                    try:
                        # If the file exists in the destination folder, check modification times
                        if os.path.isfile(dest_item):
                            src_mtime = os.path.getmtime(src_item)
                            dest_mtime = os.path.getmtime(dest_item)
                            
                            if src_mtime > dest_mtime:
                                # Source file is newer, copy and replace it in the destination
                                shutil.copy2(src_item, dest_item)
                                print(f"Updated and replaced: {item}")
                                # Do not delete the source file; it's the latest version.
                            
                            else:
                                # Destination file is newer or same, so delete the source file
                                os.remove(src_item)
                                print(f"Deleted (source was outdated): {item}")
                        
                        else:
                            # File does not exist in the destination, copy it
                            shutil.copy2(src_item, dest_item)
                            print(f"Copied: {item}")

                            # After copying, delete the source file as it is now redundant
                            os.remove(src_item)
                            print(f"Deleted: {item}")

                    except Exception as e:
                        print(f"Error processing file {item}: {e}")

        # Start processing from the root source and destination folders
        process_directory(self.src_folder, self.dest_folder)

    def run(self):
        """Continuously check for new files and copy them at regular intervals."""
        while True:
            self.copy_new_files()
            print("Waiting for 30 minutes...")
            # Sleep for 30 minutes to wait before checking again
            time.sleep(self._app.config['TRANSFER_DELAY'] * 60)  # Uncomment this line for actual 30 minutes delay
            #time.sleep(30)  # Comment out this line for actual 30 minutes delay during testing


            
            
    
