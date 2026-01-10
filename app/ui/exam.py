import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime
from app.db import get_connection
from app.utils import compute_age_group

class ExamManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.answer_var = tk.IntVar()

    def start_test(self):
        # Reset test state completely on APP
        self.app.current_question = 0
        self.app.responses = []
        self.app.current_score = 0
        self.app.sentiment_score = 0.0
        self.app.reflection_text = ""
        
        # Access widgets created by AuthManager on app root/instance
        # We assume AuthManager attached name_entry/age_entry to app
        if hasattr(self.app, 'name_entry'):
            self.app.username = self.app.name_entry.get().strip()
            
        if hasattr(self.app, 'age_entry'):
            age_str = self.app.age_entry.get().strip()
        else:
            age_str = ""

        if hasattr(self.app, 'profession_var'):
            self.app.profession = self.app.profession_var.get() if self.app.profession_var.get() else None
        else:
            self.app.profession = None

        # Delegate validation back to app (which delegates to AuthManager) or call AuthManager directly if accessible
        # Since App has validate methods delegating to Auth, we can use App's methods
        ok, err = self.app.validate_name_input(self.app.username)
        if not ok:
            messagebox.showwarning("Input Error", err)
            return

        ok, age, err = self.app.validate_age_input(age_str)
        if not ok:
            messagebox.showwarning("Input Error", err)
            return

        self.app.age = age
        self.app.age_group = compute_age_group(age)

        logging.info(
            "Session started | user=%s | age=%s | age_group=%s | profession=%s | questions=%s",
            self.app.username, self.app.age, self.app.age_group, self.app.profession, len(self.app.questions)
        )

        self.show_question()

    def show_question(self):
        self.app.clear_screen()

        if self.app.current_question >= len(self.app.questions):
            self.finish_test()
            return

        q_data = self.app.questions[self.app.current_question]
        # Handle both tuple (new format) and string (legacy safety)
        if isinstance(q_data, tuple):
            q_text = q_data[0]
            q_tooltip = q_data[1]
        else:
            q_text = q_data
            q_tooltip = None

        # Question counter
        self.app.create_widget(
            tk.Label,
            self.app.root,
            text=f"Question {self.app.current_question + 1} of {len(self.app.questions)}",
            font=("Arial", 12)
        ).pack(pady=5)
        
        q_frame = self.app.create_widget(tk.Frame, self.app.root)
        q_frame.pack(pady=20)
        
        self.app.create_widget(
            tk.Label,
            q_frame,
            text=f"Q{self.app.current_question + 1}: {q_text}",
            wraplength=400,
            font=("Arial", 12)
        ).pack(side="left")
        
        # Tooltip content
        tooltip_text = q_tooltip if q_tooltip else "Select the option that best describes you.\nThere are no right or wrong answers."

        # Tooltip Icon
        info_btn = tk.Button(
            q_frame,
            text="ℹ️", 
            font=("Arial", 12),
            bg=self.app.colors["bg"],
            fg=self.app.colors["fg"],
            relief="flat",
            activebackground=self.app.colors["bg"],
            activeforeground=self.app.colors["fg"],
            bd=0,
            cursor="hand2",
            command=lambda: self.app.toggle_tooltip(None, tooltip_text)
        )
        info_btn.pack(side="left", padx=5)
        
        # Bind event to toggle tooltip
        info_btn.bind("<Enter>", lambda e: self.app.toggle_tooltip(e, tooltip_text))
        info_btn.bind("<Leave>", lambda e: self.app.toggle_tooltip(None, None))

        # Bind Enter to Next
        self.root.bind("<Return>", lambda e: self.save_answer())

        # Options
        options_frame = self.app.create_widget(tk.Frame, self.app.root)
        options_frame.pack(pady=10)
        
        self.answer_var.set(0) # Reset selection
        
        # Correct EQ Options
        options = ["Never", "Sometimes", "Often", "Always"]
        
        for i, text in enumerate(options, 1):
             self.app.create_widget(
                tk.Radiobutton,
                options_frame,
                text=text,
                variable=self.answer_var,
                value=i,
                font=("Arial", 12)
            ).pack(anchor="w", pady=5)
            
        # Navigation Buttons
        nav_frame = self.app.create_widget(tk.Frame, self.app.root)
        nav_frame.pack(pady=20)
        
        if self.app.current_question > 0:
            self.app.create_widget(
                tk.Button,
                nav_frame,
                text="< Previous",
                command=self.previous_question,
                width=12
            ).pack(side="left", padx=10)
            
        self.app.create_widget(
            tk.Button,
            nav_frame,
            text="Next >" if self.app.current_question < len(self.app.questions) - 1 else "Finish",
            command=self.save_answer,
            width=12,
            bg=self.app.colors["button_bg"],
            fg=self.app.colors["button_fg"]
        ).pack(side="left", padx=10)

    def previous_question(self):
        if self.app.current_question > 0:
            self.app.current_question -= 1
            # We don't reload the previous answer into answer_var in the original code?
            # Original code just decrement q and show_question.
            # show_question resets answer_var to 0. So history editing is not supported purely by UI?
            # Wait, verify original code.
            # Original code: self.current_question -= 1; self.show_question().
            # show_question: self.answer_var.set(0).
            # So yes, going back clears selection. We mimic that.
            self.show_question()

    def save_answer(self):
        ans = self.answer_var.get()
        if ans == 0:
            messagebox.showwarning("Input Error", "Please select an answer.")
            return

        # Save or update the response
        if self.app.current_question < len(self.app.responses):
            self.app.responses[self.app.current_question] = ans
        else:
            self.app.responses.append(ans)
        
        # Save individual response
        conn = get_connection()
        cursor = conn.cursor()

        qid = self.app.current_question + 1
        ts = datetime.utcnow().isoformat()

        try:
            cursor.execute(
                """
                INSERT INTO responses
                (username, question_id, response_value, age_group, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (self.app.username, qid, ans, self.app.age_group, ts)
            )
            conn.commit()
        except Exception:
            logging.error("Failed to store response", exc_info=True)

        self.app.current_question += 1
        
        if self.app.current_question >= len(self.app.questions):
            self.show_reflection_screen()
        else:
            self.show_question()

    def show_reflection_screen(self):
        """Show the open-ended reflection question"""
        self.app.clear_screen()
        
        # Header
        self.app.create_widget(
            tk.Label, 
            self.app.root, 
            text="Final Reflection", 
            font=("Arial", 24, "bold")
        ).pack(pady=20)
        
        self.app.create_widget(
            tk.Label, 
            self.app.root, 
            text="Describe a recent situation where you felt challenged emotionally.\nHow did you handle it?", 
            font=("Arial", 14),
            wraplength=600
        ).pack(pady=10)
        
        # Text Area
        # Need to store reference to retrieve text later
        self.reflection_entry = tk.Text(self.app.root, height=10, width=60, font=("Arial", 12))
        self.reflection_entry.pack(pady=20, padx=20)
        
        # Submit Button
        self.app.create_widget(
            tk.Button,
            self.app.root,
            text="Submit & See Results",
            command=self.submit_reflection,
            font=("Arial", 14, "bold")
        ).pack(pady=20)
        
    def submit_reflection(self):
        """Analyze reflection and finish test"""
        text = self.reflection_entry.get("1.0", tk.END).strip()
        
        if not text:
            if not messagebox.askyesno("Skip?", "You haven't written anything. Do you want to skip?"):
                return
            self.app.sentiment_score = 0.0
            self.app.reflection_text = ""
        else:
            self.app.reflection_text = text
            # Analyze sentiment
            try:
                # Use app.sia (SentimentIntensityAnalyzer)
                if hasattr(self.app, 'sia') and self.app.sia:
                    scores = self.app.sia.polarity_scores(text)
                    # Convert compound (-1 to 1) to -100 to 100
                    self.app.sentiment_score = scores['compound'] * 100
                else:
                    self.app.sentiment_score = 0.0
            except Exception as e:
                logging.error(f"Error analyzing sentiment: {e}")
                self.app.sentiment_score = 0.0
        
        self.finish_test()

    def finish_test(self):
        self.app.current_score = sum(self.app.responses)
        self.app.current_max_score = len(self.app.responses) * 4
        self.app.current_percentage = (self.app.current_score / self.app.current_max_score) * 100 if self.app.current_max_score > 0 else 0
        
        conn = get_connection() # Get clean session
        cursor = conn.cursor() # Get cursor explicitly
        
        try:
            # Save to Database with new columns
            cursor.execute(
                "INSERT INTO scores (username, age, total_score, sentiment_score, reflection_text, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (self.app.username, self.app.age, self.app.current_score, self.app.sentiment_score, self.app.reflection_text, datetime.utcnow().isoformat())
            )
            conn.commit()
        except Exception:
            logging.error("Failed to store final score", exc_info=True)

        self.app.results.show_visual_results()
