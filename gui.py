import os
import platform
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

class SteamModCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam Mod Creator")
        self.root.geometry("400x300")

        # Steam Path Detection
        self.steam_path = self.detect_steam_path()

        # Create UI Elements
        self.create_ui()

    def detect_steam_path(self):
        try:
            steam_path = self.find_steam_installation_path()
            return steam_path
        except (FileNotFoundError, OSError) as e:
            # If automatic detection fails, prompt user
            steam_path = self.prompt_steam_path()
            return steam_path

    def find_steam_installation_path(self, custom_path=None):
        if platform.system() == "Windows":
            try:
                import winreg
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
                steam_path, _ = winreg.QueryValueEx(reg_key, "InstallPath")
                winreg.CloseKey(reg_key)
                return steam_path
            except FileNotFoundError:
                raise FileNotFoundError("Steam installation not found in the registry.")
        elif platform.system() == "Linux":
            if custom_path and os.path.exists(custom_path):
                return custom_path
            common_paths = [
                os.path.expanduser("~/.steam/steam"),
                os.path.expanduser("~/.local/share/Steam"),
                os.path.expanduser("~/Steam"),
                "/usr/local/games/Steam",
                "/usr/games/Steam"
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return path
            raise FileNotFoundError("Steam installation not found in the default Linux paths.")
        else:
            raise OSError("Unsupported operating system")

    def prompt_steam_path(self):
        steam_path = filedialog.askdirectory(title="Select Steam Installation Directory")
        if not steam_path:
            messagebox.showerror("Error", "Steam path is required to proceed.")
            self.root.quit()
        return steam_path

    def create_ui(self):
        # Mod Name Input
        tk.Label(self.root, text="Mod Name:").pack(pady=5)
        self.mod_name_entry = tk.Entry(self.root, width=40)
        self.mod_name_entry.pack(pady=5)

        # Short Mod Name Input
        tk.Label(self.root, text="Short Mod Name:").pack(pady=5)
        self.short_mod_name_entry = tk.Entry(self.root, width=20)
        self.short_mod_name_entry.pack(pady=5)

        # Create Mod Button
        create_button = tk.Button(self.root, text="Create Mod", command=self.create_mod)
        create_button.pack(pady=20)

        # Steam Path Display
        tk.Label(self.root, text=f"Steam Path: {self.steam_path}", wraplength=350).pack(pady=10)

    def create_mod(self):
        mod_name = self.mod_name_entry.get()
        short_mod_name = self.short_mod_name_entry.get()

        if not mod_name or not short_mod_name:
            messagebox.showerror("Error", "Please enter both Mod Name and Short Mod Name")
            return

        # Here you can add logic to actually create the mod
        messagebox.showinfo("Mod Creation", f"Creating mod:\nName: {mod_name}\nShort Name: {short_mod_name}")

def main():
    root = tk.Tk()
    app = SteamModCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()