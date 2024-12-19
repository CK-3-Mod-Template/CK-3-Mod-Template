import os
import platform

class ModCreator:
    @staticmethod
    def create_mod_structure(mod_name, short_mod_name, selected_tags, supported_version, debug=False, status_callback=None):
        """
        Create the basic mod structure and files.
        
        Args:
            mod_name (str): Full name of the mod
            short_mod_name (str): Short identifier for the mod
            selected_tags (list): List of mod tags
            supported_version (str): Game version supported by the mod
            debug (bool, optional): Whether to use debug output path. Defaults to False.
            status_callback (callable, optional): Function to report status or errors
        
        Returns:
            dict: A dictionary containing mod creation details
        """
        try:
            # Determine mod paths based on debug flag
            if debug:
                # Use local debug output path
                documents_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'debug', 'output')
            else:
                # Use Paradox Interactive Documents folder
                if platform.system() == "Windows":
                    documents_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Paradox Interactive', 'Crusader Kings III', 'mod')
                elif platform.system() == "Linux":
                    documents_path = os.path.join(os.path.expanduser('~'), '.local', 'share', 'Paradox Interactive', 'Crusader Kings III', 'mod')
                else:
                    raise OSError("Unsupported operating system")

            # Ensure the mod directory exists
            os.makedirs(documents_path, exist_ok=True)

            # Create mod folder
            mod_folder_path = os.path.join(documents_path, short_mod_name)
            os.makedirs(mod_folder_path, exist_ok=True)

            # Create .mod file
            mod_file_path = os.path.join(documents_path, f"{short_mod_name}.mod")
            
            # Prepare mod file content
            mod_file_content = (
                f'version="1"\n'
                f'tags={{\n'
                + "\n".join(f'\t"{tag}"' for tag in selected_tags) + 
                "\n}\n"
                f'name="{mod_name}"\n'
                f'supported_version="{supported_version or "TODO"}"\n'
                f'path="{mod_folder_path.replace(os.sep, "/")}"\n'
            )

            # Write .mod file
            with open(mod_file_path, 'w', encoding='utf-8') as mod_file:
                mod_file.write(mod_file_content)

            # Create descriptor.mod inside the mod folder
            descriptor_file_path = os.path.join(mod_folder_path, "descriptor.mod")
            descriptor_file_content = (
                f'version="1"\n'
                f'tags={{\n'
                + "\n".join(f'\t"{tag}"' for tag in selected_tags) + 
                "\n}\n"
                f'name="{mod_name}"\n'
                f'supported_version="{supported_version or "TODO"}"\n'
            )

            # Write descriptor.mod file
            with open(descriptor_file_path, 'w', encoding='utf-8') as descriptor_file:
                descriptor_file.write(descriptor_file_content)

            # Optional status callback
            if status_callback:
                status_callback(f"Mod '{mod_name}' created successfully in {mod_folder_path}")

            return {
                'success': True,
                'documents_path': documents_path,
                'mod_folder_path': mod_folder_path,
                'mod_file_path': mod_file_path,
                'descriptor_file_path': descriptor_file_path,
                'message': f"Mod '{mod_name}' created successfully"
            }

        except Exception as e:
            # Optional error callback
            if status_callback:
                status_callback(f"Error creating mod: {str(e)}", is_error=True)

            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def copy_and_replace(src, dst, short_mod_name, mod_name, status_callback=None):
        """
        Recursively copy files and replace placeholders.
        
        Args:
            src (str): Source directory path
            dst (str): Destination directory path
            short_mod_name (str): Short mod name to replace placeholders
            mod_name (str): Full mod name to replace placeholders
            status_callback (callable, optional): Function to report status
        """
        try:
            # Ensure destination directory exists
            os.makedirs(dst, exist_ok=True)
            
            # Iterate through all items in source directory
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item.replace('your_mod_name_here', short_mod_name).replace('your_long_mod_name_here', mod_name))
                
                if os.path.isdir(s):
                    # Recursively copy subdirectories
                    ModCreator.copy_and_replace(s, d, short_mod_name, mod_name, status_callback)
                else:
                    # Copy and replace placeholders for files
                    with open(s, 'r', encoding='utf-8') as source_file:
                        content = source_file.read()
                    
                    # Replace placeholders
                    content = content.replace('<your_mod_name_here>', short_mod_name)
                    content = content.replace('<your_long_mod_name_here>', mod_name)
                    
                    # Write to destination
                    with open(d, 'w', encoding='utf-8') as dest_file:
                        dest_file.write(content)
            
            # Optional status callback
            if status_callback:
                status_callback(f"Successfully copied essentials for mod '{mod_name}'")

            return {
                'success': True,
                'message': f"Essentials copied for mod '{mod_name}'"
            }

        except Exception as e:
            # Optional error callback
            if status_callback:
                status_callback(f"Error copying essentials: {str(e)}", is_error=True)

            return {
                'success': False,
                'error': str(e)
            }