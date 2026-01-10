import tkinter as tk
from tkinter import ttk

class UIStyles:
    def __init__(self, app):
        self.app = app
        self.root = app.root

    def apply_theme(self, theme_name):
        """Apply the selected theme to the application"""
        self.app.current_theme = theme_name
        self.app.colors = self.app.color_schemes.get(theme_name, self.app.color_schemes["light"])
        
        # Configure root window
        self.root.configure(bg=self.app.colors["bg"])
        
        # Configure default widget styles
        self.root.option_add("*Background", self.app.colors["bg"])
        self.root.option_add("*Foreground", self.app.colors["fg"])
        self.root.option_add("*Button.Background", self.app.colors["button_bg"])
        self.root.option_add("*Button.Foreground", self.app.colors["button_fg"])
        self.root.option_add("*Entry.Background", self.app.colors["entry_bg"])
        self.root.option_add("*Entry.Foreground", self.app.colors["entry_fg"])
        self.root.option_add("*Label.Background", self.app.colors["label_bg"])
        self.root.option_add("*Label.Foreground", self.app.colors["label_fg"])
        self.root.option_add("*Radiobutton.Background", self.app.colors["radiobutton_bg"])
        self.root.option_add("*Radiobutton.Foreground", self.app.colors["radiobutton_fg"])
        self.root.option_add("*Radiobutton.selectColor", self.app.colors["bg"])
        self.root.option_add("*Frame.Background", self.app.colors["frame_bg"])

    def create_widget(self, widget_type, *args, **kwargs):
        """Create a widget with current theme colors"""
        # Override colors if not specified
        if widget_type == tk.Label:
            kwargs.setdefault("bg", self.app.colors["label_bg"])
            kwargs.setdefault("fg", self.app.colors["label_fg"])
        elif widget_type == tk.Button:
            kwargs.setdefault("bg", self.app.colors["button_bg"])
            kwargs.setdefault("fg", self.app.colors["button_fg"])
            kwargs.setdefault("activebackground", self.darken_color(self.app.colors["button_bg"]))
            kwargs.setdefault("activeforeground", self.app.colors["button_fg"])
        elif widget_type == tk.Entry:
            kwargs.setdefault("bg", self.app.colors["entry_bg"])
            kwargs.setdefault("fg", self.app.colors["entry_fg"])
            kwargs.setdefault("insertbackground", self.app.colors["fg"])
        elif widget_type == tk.Radiobutton:
            kwargs.setdefault("bg", self.app.colors["radiobutton_bg"])
            kwargs.setdefault("fg", self.app.colors["radiobutton_fg"])
            kwargs.setdefault("selectcolor", self.app.colors["bg"])
        elif widget_type == tk.Frame:
            kwargs.setdefault("bg", self.app.colors["frame_bg"])
        
        return widget_type(*args, **kwargs)

    def darken_color(self, color):
        """Darken a color for active button state"""
        if color.startswith("#"):
            # Convert hex to rgb, darken, then back to hex
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color

    def toggle_tooltip(self, event, text):
        """Toggle tooltip visibility on click/enter"""
        # Note: Tooltip window logic relies on storing state on the app or local logic
        # Here we store it on self.app.tooltip_win to maintain state
        if hasattr(self.app, 'tooltip_win') and self.app.tooltip_win:
            self.app.tooltip_win.destroy()
            self.app.tooltip_win = None
            return

        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 25

        self.app.tooltip_win = tk.Toplevel(self.root)
        self.app.tooltip_win.wm_overrideredirect(True)
        self.app.tooltip_win.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.app.tooltip_win,
            text=text,
            justify='left',
            background="#ffffe0", # Light yellow for tooltip
            foreground="#000000",
            relief='solid',
            borderwidth=1,
            font=("Arial", 10)
        )
        label.pack(ipadx=1)
        
        # Auto-hide after 3 seconds
        self.root.after(3000, lambda: self.app.tooltip_win.destroy() if hasattr(self.app, 'tooltip_win') and self.app.tooltip_win else None)
