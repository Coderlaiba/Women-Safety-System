import tkinter as tk
from tkinter import messagebox, ttk
import threading
import main  # Coordinator framework coupling

class ModernWomenSafetyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AURA - Women Safety System")
        self.root.geometry("450x650")
        self.root.configure(bg="#121824")  # Premium Dark Cyber Background
        self.root.resizable(False, False)

        # Multi-language dictionary packs
        self.current_lang = "English"
        self.translations = {
            "English": {
                "title": "AURA SAFETY SYSTEM",
                "mic_live": "🛡️ MIC ACTIVE (Always Listening)",
                "btn_sos": "PANIC\nSOS",
                "invalid_num": "Invalid Indian Number! Must be 10 digits.",
                "success_num": "Guardian registered successfully!",
                "add_btn": "Add Guardian"
            },
            "Hindi": {
                "title": "आभा सुरक्षा प्रणाली",
                "mic_live": "🛡️ माइक चालू है (सुन रहा है)",
                "btn_sos": "आपातकालीन\nSOS",
                "invalid_num": "अवैध नंबर! 10 अंकों का होना चाहिए।",
                "success_num": "अभिभावक सफलतापूर्वक पंजीकृत!",
                "add_btn": "नंबर जोड़ें"
            }
        }

        self.setup_styles()
        self.create_widgets()
        self.initialize_backend_pipelines()

    def setup_styles(self):
        self.font_title = ("Segoe UI", 18, "bold")
        self.font_sub = ("Segoe UI", 10, "bold")
        self.font_button = ("Segoe UI", 16, "bold")
        self.font_log = ("Consolas", 9)

    def create_widgets(self):
        # --- Top Bar: Language Dropdown ---
        top_frame = tk.Frame(self.root, bg="#121824")
        top_frame.pack(fill="x", padx=20, pady=10)

        self.lang_var = tk.StringVar(value=self.current_lang)
        lang_menu = ttk.Combobox(top_frame, textvariable=self.lang_var, values=["English", "Hindi"], state="readonly", width=8)
        lang_menu.pack(side="right")
        lang_menu.bind("<<ComboboxSelected>>", self.change_language)

        # --- Main Title ---
        self.lbl_title = tk.Label(self.root, text=self.translations[self.current_lang]["title"], bg="#121824", fg="#E2E8F0", font=self.font_title)
        self.lbl_title.pack(pady=10)

        # --- Status Banner: Mic Indicator (Sahi kiya: pady=8) ---
        self.lbl_status = tk.Label(self.root, text=self.translations[self.current_lang]["mic_live"], bg="#0F172A", fg="#10B981", font=self.font_sub, bd=1, relief="solid", pady=8)
        self.lbl_status.pack(fill="x", padx=30, pady=5)

        # --- Central Core: Big Modern PANIC SOS Button ---
        sos_frame = tk.Frame(self.root, bg="#121824")
        sos_frame.pack(pady=25)

        self.btn_sos = tk.Button(
            sos_frame, 
            text=self.translations[self.current_lang]["btn_sos"],
            font=self.font_button,
            bg="#EF4444", fg="white",
            activebackground="#DC2626", activeforeground="white",
            width=12, height=3, bd=0, cursor="hand2",
            relief="flat", command=self.trigger_manual_sos_async
        )
        self.btn_sos.pack()
        self.btn_sos.bind("<Enter>", lambda e: self.btn_sos.configure(bg="#DC2626"))
        self.btn_sos.bind("<Leave>", lambda e: self.btn_sos.configure(bg="#EF4444"))

        # --- Input Section: Register Guardians Card (Sahi kiya: padx=15, pady=15) ---
        card_frame = tk.LabelFrame(self.root, text=" Register Guardians (India) ", bg="#1E293B", fg="#94A3B8", font=("Segoe UI", 9, "bold"), padx=15, pady=15, bd=1, relief="solid")
        card_frame.pack(fill="x", padx=30, pady=10)

        # Entry configuration box (Sahi kiya: ipady=5)
        self.phone_entry = tk.Entry(card_frame, font=("Segoe UI", 12), bg="#0F172A", fg="#F1F5F9", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#334155", highlightcolor="#3B82F6")
        self.phone_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=5)
        self.phone_entry.insert(0, "+91")

        # Add Button configuration (Sahi kiya: padx=12, pady=5)
        self.btn_add = tk.Button(card_frame, text=self.translations[self.current_lang]["add_btn"], font=("Segoe UI", 9, "bold"), bg="#3B82F6", fg="white", activebackground="#2563EB", activeforeground="white", bd=0, padx=12, pady=5, cursor="hand2", command=self.save_guardian_number)
        self.btn_add.pack(side="right")
        self.btn_add.bind("<Enter>", lambda e: self.btn_add.configure(bg="#2563EB"))
        self.btn_add.bind("<Leave>", lambda e: self.btn_add.configure(bg="#3B82F6"))

        # --- Bottom Panel: System Hardware Output Feed ---
        feed_label = tk.Label(self.root, text="SYSTEM HARDWARE OUTPUT FEED", bg="#121824", fg="#64748B", font=("Segoe UI", 8, "bold"))
        feed_label.pack(anchor="w", padx=30, pady=(15, 0))

        feed_frame = tk.Frame(self.root, bg="#0F172A", bd=1, relief="solid")
        feed_frame.pack(fill="both", expand=True, padx=30, pady=(2, 20))

        # Text Console layout settings (Sahi kiya: padx=10, pady=10)
        self.txt_feed = tk.Text(feed_frame, bg="#0F172A", fg="#38BDF8", font=self.font_log, wrap="word", bd=0, state="disabled", padx=10, pady=10)
        self.txt_feed.pack(fill="both", expand=True)

    def write_to_feed(self, message):
        self.txt_feed.configure(state="normal")
        self.txt_feed.insert("end", f"{message}\n")
        self.txt_feed.see("end")
        self.txt_feed.configure(state="disabled")

    def change_language(self, event=None):
        self.current_lang = self.lang_var.get()
        pack = self.translations[self.current_lang]
        self.lbl_title.config(text=pack["title"])
        self.lbl_status.config(text=pack["mic_live"])
        self.btn_sos.config(text=pack["btn_sos"])
        self.btn_add.config(text=pack["add_btn"])
        self.write_to_feed(f"[SYS] Interface mapping language swapped to: {self.current_lang}")

    def save_guardian_number(self):
        input_num = self.phone_entry.get().strip()
        lang_pack = self.translations[self.current_lang]

        cleaned = input_num.replace(" ", "").replace("-", "")
        if len(cleaned) == 10 and cleaned.isdigit():
            cleaned = "+91" + cleaned

        if not cleaned.startswith("+91") or len(cleaned) != 13 or not cleaned[1:].isdigit():
            messagebox.showerror("Validation Fault", lang_pack["invalid_num"])
            self.write_to_feed(f"[REJECTED] Invalid Indian structure: '{input_num}'")
            return

        validated = cleaned
        try:
            import database
            conn = database.get_db_connection()
            conn.execute('INSERT INTO contacts (phone_text) VALUES (?)', (validated,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", lang_pack["success_num"])
            self.write_to_feed(f"[DB] Verified Contact Saved: {validated}")
            self.phone_entry.delete(0, 'end')
            self.phone_entry.insert(0, "+91")
        except Exception:
            messagebox.showwarning("Duplicate", "This mobile route record already exists persistently.")
            self.write_to_feed("⚠️ Contact skip: Record already present in SQLite database.")

    def trigger_manual_sos_async(self):
        threading.Thread(
            target=main.system_coordinator.route_incident_trigger,
            args=("MANUAL_PANIC_SOS", self.write_to_feed),
            daemon=True
        ).start()

    def initialize_backend_pipelines(self):
        self.write_to_feed("[SYSTEM] Initializing Multi-threaded Security Fabrics...")
        self.write_to_feed("[DB] Connecting SQLite secure context maps...")
        
        import database
        threading.Thread(
            target=main.deploy_audio_pipeline_safely,
            args=(main.system_coordinator, database.fetch_all_active_contacts),
            daemon=True
        ).start()
        self.write_to_feed("[THREADS] Isolated Audio listener sub-daemon spawned safely.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernWomenSafetyApp(root)
    root.mainloop()