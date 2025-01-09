import customtkinter as ctk
import tkinter.messagebox as messagebox

class RegisterPage:
    def __init__(self, app, library_app):
        self.app = app
        self.library_app = library_app
        self.frame = None

    def create_frame(self):
        # Close all existing windows
        self.library_app.close_all_windows()

        # Hide main window
        self.library_app.hide_main_window()

        # Create register window
        self.frame = self.library_app.register_window(ctk.CTkToplevel(self.app))
        self.frame.title("Register")
        self.frame.geometry("400x300")
        self.frame.protocol("WM_DELETE_WINDOW", self.library_app.create_login_frame)

        label = ctk.CTkLabel(self.frame, text="Create Account")
        label.pack(pady=12, padx=10)

        username_entry = ctk.CTkEntry(self.frame, placeholder_text="Username")
        username_entry.pack(pady=12, padx=10)

        password_entry = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        password_entry.pack(pady=12, padx=10)

        email_entry = ctk.CTkEntry(self.frame, placeholder_text="Email")
        email_entry.pack(pady=12, padx=10)

        register_button = ctk.CTkButton(self.frame, text="Register", 
            command=lambda: self.handle_register(
                username_entry.get(), 
                password_entry.get(), 
                email_entry.get()
            ))
        register_button.pack(pady=12, padx=10)

        # Add back button
        back_button = ctk.CTkButton(self.frame, text="Back", command=self.library_app.create_login_frame)
        back_button.pack(pady=12, padx=10)

    def handle_register(self, username, password, email):
        if self.library_app.register_user(username, password, email):
            messagebox.showinfo("Success", "Registration Successful!")
            self.library_app.create_login_frame()
        else:
            messagebox.showerror("Error", "Registration Failed")
