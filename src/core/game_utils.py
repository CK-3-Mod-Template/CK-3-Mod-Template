import os
import json
import logging
import re

class CK3GameUtils:
    @classmethod
    def get_latest_ck3_version(cls, steam_path):
        """
        Find the latest CK3 version by checking the launcher settings file.
        
        Args:
            steam_path (str): Path to Steam installation
        
        Returns:
            dict: Detected game version with full version and version numbers
        
        Raises:
            FileNotFoundError: If launcher settings file cannot be found
            ValueError: If version cannot be parsed from settings file
        """
        # Validate steam_path
        if not steam_path:
            raise ValueError("Steam path is not provided")

        # Construct path to launcher settings
        launcher_settings_path = os.path.join(
            steam_path, 
            'steamapps', 
            'common', 
            'Crusader Kings III', 
            'launcher', 
            'launcher-settings.json'
        )

        # Log the exact path being checked
        logging.info(f"Checking launcher settings at: {launcher_settings_path}")

        # Check if file exists
        if not os.path.exists(launcher_settings_path):
            # Detailed logging for debugging
            logging.error(f"Launcher settings file not found at: {launcher_settings_path}")
            
            # Check if Steam path is correct
            steamapps_path = os.path.join(steam_path, 'steamapps')
            ck3_path = os.path.join(steam_path, 'steamapps', 'common', 'Crusader Kings III')
            
            logging.info(f"Checking Steam path: {steam_path}")
            logging.info(f"Steamapps exists: {os.path.exists(steamapps_path)}")
            logging.info(f"CK3 path exists: {os.path.exists(ck3_path)}")
            
            raise FileNotFoundError(f"Launcher settings file not found at: {launcher_settings_path}")

        # Read launcher settings
        try:
            with open(launcher_settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                
            # Extract full version, with fallback
            full_version = settings.get('version', 
                                        settings.get('rawVersion', 
                                                    'Unknown'))
            
            # Extract version numbers
            version_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', full_version)
            if version_match:
                version_numbers = version_match.group(1)
            else:
                version_numbers = full_version
            
            # Log successful version detection
            logging.info(f"Detected CK3 version: {full_version}")
            logging.info(f"Version numbers: {version_numbers}")
            
            return {
                'full_version': full_version,
                'version_numbers': version_numbers
            }
        
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in launcher settings file: {launcher_settings_path}")
            raise ValueError("Could not parse launcher settings file")
        except Exception as e:
            logging.error(f"Unexpected error reading launcher settings: {e}")
            raise

    @classmethod
    def get_version_for_files(cls, version_info):
        """
        Get version numbers for file creation.
        
        Args:
            version_info (dict): Version information from get_latest_ck3_version
        
        Returns:
            str: Version numbers to use in files
        """
        return version_info['version_numbers']
        
    @staticmethod
    def list_game_files(steam_path, status_callback=None):
        """
        List game files in the Crusader Kings III game directory.
        
        Args:
            steam_path (str): Path to the Steam installation directory
            status_callback (callable, optional): Callback to update status label
        
        Returns:
            list: List of relative file paths in the game directory
        """
        try:
            # Construct the path to the game directory
            game_dir = os.path.join(
                steam_path, 
                'steamapps', 
                'common', 
                'Crusader Kings III', 
                'game'
            )

            # Check if game directory exists
            if not os.path.exists(game_dir):
                if status_callback:
                    status_callback("Game directory not found", is_error=True)
                return []

            # Create a list to store file paths
            file_list = []

            # Walk through the directory and its subdirectories
            for root, dirs, files in os.walk(game_dir):
                for file in files:
                    # Get the full path of the file
                    full_path = os.path.join(root, file)
                    # Get the relative path from the game directory
                    relative_path = os.path.relpath(full_path, game_dir)
                    file_list.append(relative_path)

            # Create a 'data' directory if it doesn't exist
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            os.makedirs(data_dir, exist_ok=True)

            # Define the output file path
            output_file = os.path.join(data_dir, 'vanilla_files.txt')

            # Write the file list to the text file
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"Total Files Found: {len(file_list)}\n\n")
                    for file_path in sorted(file_list):
                        f.write(file_path + "\n")
                
                # Show a success message via status callback if available
                if status_callback:
                    status_callback(f"Found {len(file_list)} game files. List saved to {output_file}")
            
            except Exception as e:
                # Show an error message if file writing fails
                if status_callback:
                    status_callback(f"Failed to save file list: {str(e)}", is_error=True)

            return file_list

        except Exception as e:
            # Detailed error logging
            print(f"Error listing game files: {e}")
            traceback.print_exc()
            
            if status_callback:
                status_callback(f"Error listing game files: {e}", is_error=True)
            
            return []