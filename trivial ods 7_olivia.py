import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")

# =========================
# ESTILO VISUAL
# =========================
BG = "#070B14"
CARD = "#111827"
ACCENT = "#00F5FF"
GREEN = "#00FF9C"
RED = "#FF3B3B"
TEXT = "#E5E7EB"


class ODSGame(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("1000x750")
        self.title("ODS Neon Challenge")
        self.configure(fg_color=BG)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=30, pady=30)

        self.load_questions()
        self.show_start()

    # =========================
    # DATOS
    # =========================
    def load_questions(self):
        self.questions = [
            {"q": "¿Qué promueve el ODS 4?",
             "opts": ["Educación inclusiva", "Solo universidad", "Tecnología cara", "Exámenes difíciles"],
             "a": "Educación inclusiva"},

            {"q": "ODS 13 se centra en:",
             "opts": ["Cambio climático", "Educación", "Salud", "Industria"],
             "a": "Cambio climático"},

            {"q": "ODS 6 trata sobre:",
             "opts": ["Agua limpia", "Dinero", "Turismo", "Tecnología"],
             "a": "Agua limpia"},

            {"q": "ODS 5 busca:",
             "opts": ["Igualdad de género", "Más empresas", "Menos leyes", "Menos educación"],
             "a": "Igualdad de género"},

            {"q": "ODS 1 combate:",
             "opts": ["La pobreza", "La contaminación", "El clima", "La guerra"],
             "a": "La pobreza"},
        ]

    # =========================
    # UI UTIL
    # =========================
    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    # =========================
    # START SCREEN
    # =========================
    def show_start(self):
        self.clear()

        ctk.CTkLabel(
            self.container,
            text="ODS NEON CHALLENGE",
            font=("Orbitron", 44, "bold"),
            text_color=ACCENT
        ).pack(pady=50)

        ctk.CTkLabel(
            self.container,
            text="Responde rápido. Sube tu racha. Domina los ODS.",
            font=("Segoe UI", 18),
            text_color=TEXT
        ).pack(pady=10)

        self.neon_button("JUGAR", self.start_game).pack(pady=40)

    # =========================
    # START GAME
    # =========================
    def start_game(self):
        self.score = 0
        self.streak = 0
        self.index = 0

        self.game_questions = random.sample(self.questions, len(self.questions))

        self.show_question()

    # =========================
    # PREGUNTA
    # =========================
    def show_question(self):
        self.clear()

        if self.index >= len(self.game_questions):
            self.show_end()
            return

        self.time_left = 15
        self.running = True

        q = self.game_questions[self.index]

        # HEADER
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x")

        self.lbl_info = ctk.CTkLabel(
            header,
            text=f"Puntos: {self.score} | Racha: {self.streak} | {self.index+1}/{len(self.game_questions)}",
            text_color=TEXT,
            font=("Consolas", 16)
        )
        self.lbl_info.pack()

        self.timer_bar = ctk.CTkProgressBar(self.container, progress_color=ACCENT)
        self.timer_bar.set(1)
        self.timer_bar.pack(fill="x", pady=10)

        # CARD
        self.card = ctk.CTkFrame(self.container, fg_color=CARD, corner_radius=25)
        self.card.pack(expand=True, fill="both", pady=20)

        ctk.CTkLabel(
            self.card,
            text=q["q"],
            font=("Segoe UI", 26, "bold"),
            wraplength=700,
            text_color=TEXT
        ).pack(pady=40)

        # BOTONES
        self.buttons = []

        opts = q["opts"].copy()
        random.shuffle(opts)

        for opt in opts:
            btn = self.neon_button(opt, lambda o=opt: self.answer(o))
            btn.pack(pady=10, padx=40, fill="x")
            self.buttons.append(btn)

        self.update_timer()

    # =========================
    # TIMER
    # =========================
    def update_timer(self):
        if not self.running:
            return

        self.time_left -= 0.05
        self.timer_bar.set(self.time_left / 15)

        if self.time_left <= 0:
            self.answer(None)
            return

        self.after(50, self.update_timer)

    # =========================
    # RESPUESTA
    # =========================
    def answer(self, choice):
        if not self.running:
            return

        self.running = False

        q = self.game_questions[self.index]
        correct = q["a"]

        for b in self.buttons:
            b.configure(state="disabled")

        if choice == correct:
            self.streak += 1
            self.score += 100 + (self.streak * 20)
            self.flash(GREEN)
        else:
            self.streak = 0
            self.flash(RED)

        self.after(900, self.next_question)

    # =========================
    # SIGUIENTE
    # =========================
    def next_question(self):
        self.index += 1
        self.show_question()

    # =========================
    # EFECTO FLASH
    # =========================
    def flash(self, color):
        self.card.configure(fg_color=color)
        self.after(200, lambda: self.card.configure(fg_color=CARD))

    # =========================
    # FINAL
    # =========================
    def show_end(self):
        self.clear()

        ctk.CTkLabel(
            self.container,
            text="GAME OVER",
            font=("Orbitron", 42, "bold"),
            text_color=ACCENT
        ).pack(pady=50)

        ctk.CTkLabel(
            self.container,
            text=f"Puntuación: {self.score}",
            font=("Consolas", 28),
            text_color=TEXT
        ).pack(pady=10)

        ctk.CTkLabel(
            self.container,
            text=f"Mejor racha: {self.streak}",
            font=("Consolas", 20),
            text_color=TEXT
        ).pack(pady=10)

        self.neon_button("REINICIAR", self.show_start).pack(pady=40)

    # =========================
    # BOTÓN NEÓN
    # =========================
    def neon_button(self, text, cmd):
        btn = ctk.CTkButton(
            self.container,
            text=text,
            command=cmd,
            fg_color="#1F2937",
            hover_color=ACCENT,
            corner_radius=18,
            height=50,
            font=("Segoe UI", 16, "bold")
        )

        return btn


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app = ODSGame()
    app.mainloop()
