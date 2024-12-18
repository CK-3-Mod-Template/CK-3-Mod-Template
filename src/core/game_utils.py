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
    def list_game_files(steam_path):
        """
        List all game files in the Crusader Kings III game directory.
        
        Args:
            steam_path (str): Path to the Steam installation directory
        
        Returns:
            list: A list of relative file paths in the game directory
        """
        # Construct the path to the Crusader Kings III game directory
        game_dir = os.path.join(steam_path, 'steamapps', 'common', 'Crusader Kings III', 'game')
        
        # Check if the directory exists
        if not os.path.exists(game_dir):
            messagebox.showerror("Error", f"Game directory not found: {game_dir}")
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
            
            # Show a success message
            messagebox.showinfo("Success", f"Vanilla files list saved to:\n{output_file}")
        
        except Exception as e:
            # Show an error message if file writing fails
            messagebox.showerror("Error", f"Failed to save file list:\n{str(e)}")

        return file_list