import os
import platform
import winreg

class SteamPathFinder:
    """
    A utility class for finding Steam installation paths across different platforms.
    """
    @staticmethod
    def detect_steam_path():
        """
        Detect the Steam installation path based on the current operating system.
        
        Returns:
            str: Path to the Steam installation, or None if not found.
        """
        if platform.system() == "Windows":
            return SteamPathFinder.find_steam_installation_path()
        elif platform.system() == "Darwin":  # macOS
            return SteamPathFinder.find_steam_path_mac()
        elif platform.system() == "Linux":
            return SteamPathFinder.find_steam_path_linux()
        return None

    @staticmethod
    def find_steam_installation_path(custom_path=None):
        """
        Find Steam installation path on Windows.
        
        Args:
            custom_path (str, optional): Custom path to check first.
        
        Returns:
            str: Path to Steam installation, or None if not found.
        """
        # Check custom path first if provided
        if custom_path and os.path.exists(custom_path):
            return custom_path

        # Try common Steam installation paths
        possible_paths = [
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Steam'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Steam'),
            os.path.join(os.path.expanduser('~'), 'Steam'),
        ]

        # Try Windows Registry
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam') as key:
                steam_path, _ = winreg.QueryValueEx(key, 'SteamPath')
                if os.path.exists(steam_path):
                    return steam_path
        except FileNotFoundError:
            pass

        # Check possible paths
        for path in possible_paths:
            if os.path.exists(path):
                return path

        return None

    @staticmethod
    def find_steam_path_mac():
        """
        Find Steam installation path on macOS.
        
        Returns:
            str: Path to Steam installation, or None if not found.
        """
        mac_steam_paths = [
            os.path.expanduser('~/Library/Application Support/Steam'),
            '/Applications/Steam.app/Contents'
        ]
        
        for path in mac_steam_paths:
            if os.path.exists(path):
                return path
        
        return None

    @staticmethod
    def find_steam_path_linux():
        """
        Find Steam installation path on Linux.
        
        Returns:
            str: Path to Steam installation, or None if not found.
        """
        linux_steam_paths = [
            os.path.expanduser('~/.steam/steam'),
            os.path.expanduser('~/.local/share/Steam'),
            '/usr/local/share/Steam',
            '/usr/share/Steam'
        ]
        
        for path in linux_steam_paths:
            if os.path.exists(path):
                return path
        
        return None