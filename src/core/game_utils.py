import os
import json
import tkinter as tk
from tkinter import messagebox
import traceback

class CK3GameUtils:
    @staticmethod
    def get_latest_ck3_version(steam_path):
        """
        Fetch the latest Crusader Kings III version from launcher-settings.json.
        
        Args:
            steam_path (str): Path to the Steam installation directory
        
        Returns:
            str: The latest game version, or None if unable to fetch
        """
        try:
            # Construct the path to the launcher-settings.json
            launcher_settings_path = os.path.join(
                steam_path, 
                'steamapps', 
                'common', 
                'Crusader Kings III', 
                'launcher', 
                'launcher-settings.json'
            )

            # Check if the file exists
            if not os.path.exists(launcher_settings_path):
                print(f"Launcher settings file not found at: {launcher_settings_path}")
                return None

            # Read the JSON file
            with open(launcher_settings_path, 'r', encoding='utf-8') as file:
                settings = json.load(file)

            # Extract the rawVersion
            version = settings.get('rawVersion')

            if version:
                print(f"Found CK3 Version: {version}")
                return version
            else:
                print("No rawVersion found in launcher-settings.json")
                return None

        except Exception as e:
            # Detailed error logging
            print("Full Error Traceback:")
            traceback.print_exc()
            
            # If there's any error (file reading, parsing, etc.), show a message
            messagebox.showwarning("Version Fetch Error", 
                                f"Could not fetch the game version:\n{str(e)}")
            return None

    @staticmethod
    def list_game_files(steam_path, status_callback=None):
        """
        List game files in the Crusader Kings III game directory.
        
        Args:
            steam_path (str): Path to the Steam installation directory
            status_callback (callable, optional): Callback to update status label
        
        Returns:
            list: List of game files found
        """
        try:
            # Construct the path to the game directory
            game_dir = os.path.join(
                steam_path, 
                'steamapps', 
                'common', 
                'Crusader Kings III'
            )

            # Check if game directory exists
            if not os.path.exists(game_dir):
                if status_callback:
                    status_callback("Game directory not found", is_error=True)
                return []

            # Walk through the directory and collect all files
            game_files = []
            for root, dirs, files in os.walk(game_dir):
                for file in files:
                    game_files.append(os.path.join(root, file))

            # Update status label with file count if callback is provided
            if status_callback:
                status_callback(f"Found {len(game_files)} game files")

            return game_files

        except Exception as e:
            # Detailed error logging
            print(f"Error listing game files: {e}")
            traceback.print_exc()
            
            if status_callback:
                status_callback(f"Error listing game files: {e}", is_error=True)
            
            return []