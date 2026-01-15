import tkinter as tk
from app.i18n_manager import t
from app.services.reflection_service import save_reflection

class ReflectionScreen(tk.Frame):
    def __init__(self, master, user_id, on_complete):
        super().__init__(master)
        self.user_id = user_id
        self.on_complete = on_complete
        self.pack(fill="both", expand=True)

        tk.Label(
            self,
            text=t("reflection_pov_prompt"),
            wraplength=600,
            justify="left"
        ).pack(pady=(20, 5))

        self.pov_text = tk.Text(self, height=6, width=80)
        self.pov_text.pack(pady=5)

        tk.Label(
            self,
            text=t("reflection_challenges_prompt"),
            wraplength=600,
            justify="left"
        ).pack(pady=(20, 5))

        self.challenges_text = tk.Text(self, height=6, width=80)
        self.challenges_text.pack(pady=5)

        btns = tk.Frame(self)
        btns.pack(pady=20)

        tk.Button(
            btns,
            text=t("skip"),
            command=self.skip
        ).pack(side="left", padx=10)

        tk.Button(
            btns,
            text=t("continue"),
            command=self.submit
        ).pack(side="left", padx=10)

    def skip(self):
        self.on_complete()

    def submit(self):
        save_reflection(
            user_id=self.user_id,
            pov=self.pov_text.get("1.0", tk.END).strip(),
            challenges=self.challenges_text.get("1.0", tk.END).strip()
        )
        self.on_complete()
