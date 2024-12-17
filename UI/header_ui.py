import ttkbootstrap as ttk

class HeaderUI:
    @staticmethod
    def create_header(main_frame):
        """
        Create the header section of the UI.
        
        Args:
            main_frame (tk.Frame): Parent frame to add the header
        """
        # Title Label
        title_label = ttk.Label(
            main_frame, 
            text="CK3 Mod Creator", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(10, 20))