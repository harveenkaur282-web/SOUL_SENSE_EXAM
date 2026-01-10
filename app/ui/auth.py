import tkinter as tk
import logging

class AuthManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root

    def create_welcome_screen(self):
        """Create initial welcome screen with settings option"""
        self.app.clear_screen()
        
        # Header
        header_frame = self.app.create_widget(
            tk.Frame,
            self.app.root,
            height=80
        )
        header_frame.pack(fill="x", pady=20)
        
        title_label = self.app.create_widget(
            tk.Label,
            header_frame,
            text="Soul Sense",
            font=("Helvetica", 32, "bold")
        )
        title_label.pack()
        
        subtitle_label = self.app.create_widget(
            tk.Label,
            header_frame,
            text="Emotional Intelligence Assessment",
            font=("Arial", 16)
        )
        subtitle_label.pack(pady=5)
        
        # Main content area
        content_frame = self.app.create_widget(tk.Frame, self.app.root)
        content_frame.pack(expand=True, fill="both", padx=40)
        
        # Intro text
        intro_text = (
            "Welcome to Soul Sense. This application measures your Emotional Intelligence (EQ) "
            "through a series of situation-based questions.\n\n"
            "You will be presented with scenarios and asked to choose the most appropriate response. "
            "There is no time limit, so please answer honestly."
        )
        
        intro_label = self.app.create_widget(
            tk.Label,
            content_frame,
            text=intro_text,
            font=("Arial", 12),
            wraplength=500,
            justify="center"
        )
        intro_label.pack(pady=20)
        
        # Tips Carousel
        if hasattr(self.app, 'tips') and self.app.tips:
            import random
            tip_frame = self.app.create_widget(tk.Frame, content_frame, relief="sunken", borderwidth=1)
            tip_frame.pack(fill="x", pady=10, padx=20)
            
            tip_label = self.app.create_widget(
                tk.Label,
                tip_frame,
                text=f"💡 Tip: {random.choice(self.app.tips)}",
                font=("Arial", 10, "italic"),
                wraplength=450
            )
            tip_label.pack(pady=10)
        
        # Buttons
        button_frame = self.app.create_widget(tk.Frame, content_frame)
        button_frame.pack(pady=30)
        
        start_btn = self.app.create_widget(
            tk.Button,
            button_frame,
            text="Start Assessment",
            command=self.create_username_screen,
            font=("Arial", 14, "bold"),
            width=20,
            pady=10
        )
        start_btn.pack(pady=10)
        
        # Journal Button
        journal_btn = self.app.create_widget(
            tk.Button,
            button_frame,
            text="📖 Daily Journal",
            command=self.app.open_journal_flow,
            font=("Arial", 12),
            width=20,
            bg="#81C784", # Light Green accent
            fg="black"
        )
        journal_btn.pack(pady=5)

        # Dashboard Button (NEW)
        dashboard_btn = self.app.create_widget(
            tk.Button,
            button_frame,
            text="📊 Dashboard",
            command=self.app.open_dashboard_flow,
            font=("Arial", 12),
            width=15,
            bg="#29B6F6", # Light Blue accent
            fg="black"
        )
        dashboard_btn.pack(pady=5)
        
        # View History button
        history_btn = self.app.create_widget(
            tk.Button,
            button_frame,
            text="View History",
            command=self.app.show_history_screen,
            font=("Arial", 12),
            width=15
        )
        history_btn.pack(pady=5)
        
        settings_btn = self.app.create_widget(
            tk.Button,
            button_frame,
            text="Settings",
            command=self.app.show_settings,
            font=("Arial", 12),
            width=15
        )
        settings_btn.pack(pady=5)
        
        exit_btn = self.app.create_widget(
            tk.Button,
            button_frame,
            text="Exit",
            command=self.app.force_exit,
            font=("Arial", 12),
            width=15
        )
        exit_btn.pack(pady=5)

    def create_username_screen(self):
        self.app.clear_screen()
        
        # Username
        self.app.create_widget(
            tk.Label,
            self.app.root,
            text="Enter Your Name:",
            font=("Arial", 14)
        ).pack(pady=10)
        
        # We need to store entry ref in app or locally. 
        # Ideally app.name_entry since start_test uses it.
        # But for better encapsulation, we should get value here and pass it.
        # BUT start_test reads self.name_entry.
        # For Phase 2, we must replicate self.name_entry on the app to avoid breaking start_test
        
        self.app.name_entry = self.app.create_widget(
            tk.Entry,
            self.app.root,
            font=("Arial", 14)
        )
        self.app.name_entry.pack(pady=5)

        # Age
        self.app.create_widget(
            tk.Label,
            self.app.root,
            text="Enter Your Age (optional):",
            font=("Arial", 14)
        ).pack(pady=5)
        
        self.app.age_entry = self.app.create_widget(
            tk.Entry,
            self.app.root,
            font=("Arial", 14)
        )
        self.app.age_entry.pack(pady=5)
        self.root.bind("<Return>", self._enter_start)
        
        # Profession (optional, for benchmarking)
        self.app.create_widget(
            tk.Label,
            self.app.root,
            text="Your Profession (optional, for benchmarking):",
            font=("Arial", 14)
        ).pack(pady=5)
        
        self.app.profession_var = tk.StringVar()
        profession_frame = self.app.create_widget(tk.Frame, self.app.root)
        profession_frame.pack(pady=5)
        
        professions = ["Student", "Professional", "Manager", "Healthcare", "Education", "Technology", "Creative", "Other"]
        # OptionMenu doesn't support easy styling via create_widget wrapper args passing directly usually
        # But we can try or do post-config
        profession_menu = tk.OptionMenu(profession_frame, self.app.profession_var, *professions)
        # We access colors from app
        colors = self.app.colors if hasattr(self.app, 'colors') else {'button_bg':'white', 'button_fg':'black'}
        profession_menu.config(font=("Arial", 12), bg=colors.get("button_bg"), fg=colors.get("button_fg"))
        profession_menu.pack()

        # Start button
        self.app.create_widget(
            tk.Button,
            self.app.root,
            text="Start Test",
            command=self.app.start_test
        ).pack(pady=15)
        
        # Back button
        self.app.create_widget(
            tk.Button,
            self.app.root,
            text="Back to Main",
            command=self.create_welcome_screen
        ).pack(pady=5)

    def _enter_start(self, event):
        self.app.start_test()

    def validate_name_input(self, name):
        if not name:
            return False, "Please enter your name."
        if not all(c.isalpha() or c.isspace() for c in name):
            return False, "Name must contain only letters and spaces."
        return True, None

    def validate_age_input(self, age_str):
        if age_str == "":
            return True, None, None
        try:
            age = int(age_str)
            if not (1 <= age <= 120):
                return False, None, "Age must be between 1 and 120."
            return True, age, None
        except ValueError:
            return False, None, "Age must be numeric."
