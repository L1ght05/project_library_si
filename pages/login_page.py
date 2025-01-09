import customtkinter as ctk
import tkinter.messagebox as messagebox

class LoginPage:
    def __init__(self, app, library_app):
        self.app = app
        self.library_app = library_app
        self.frame = None
        self.username_entry = None
        self.password_entry = None

    def create_frame(self):
        # Close all existing windows
        self.library_app.close_all_windows()

        # Create login frame
        self.frame = self.library_app.register_window(ctk.CTkFrame(self.app))
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(self.frame, text="Library Login")
        label.pack(pady=12, padx=10)

        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.username_entry.pack(pady=12, padx=10)

        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        login_button = ctk.CTkButton(self.frame, text="Login", command=self.handle_login)
        login_button.pack(pady=12, padx=10)

        register_button = ctk.CTkButton(self.frame, text="Register", command=self.library_app.create_register_frame)
        register_button.pack(pady=12, padx=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.library_app.login(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            self.library_app.logged_in_user = username
            self.library_app.create_main_library_frame()
        else:
            messagebox.showerror("Error", "Invalid credentials")
