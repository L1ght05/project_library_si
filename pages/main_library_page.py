import customtkinter as ctk
import tkinter.messagebox as messagebox

class MainLibraryPage:
    def __init__(self, app, library_app):
        self.app = app
        self.library_app = library_app
        self.frame = None

    def create_frame(self):
        # Close all existing windows
        self.library_app.close_all_windows()

        # Hide main window
        self.library_app.hide_main_window()

        # Create main library frame
        self.frame = self.library_app.register_window(ctk.CTkToplevel(self.app))
        self.frame.title("Library Management")
        self.frame.geometry("800x600")
        self.frame.protocol("WM_DELETE_WINDOW", self.library_app.create_login_frame)

        label = ctk.CTkLabel(self.frame, text="Library Management System")
        label.pack(pady=12, padx=10)

        add_book_button = ctk.CTkButton(self.frame, text="Add Book", command=self.library_app.add_book)
        add_book_button.pack(pady=12, padx=10)

        show_books_button = ctk.CTkButton(self.frame, text="Show Books", command=lambda: self.library_app.show_books(self.library_app.logged_in_user))
        show_books_button.pack(pady=12, padx=10)

        # Add Manage Subscriptions button
        subscription_button = ctk.CTkButton(self.frame, text="Manage Subscriptions", command=self.library_app.manage_subscriptions)
        subscription_button.pack(pady=12, padx=10)

        show_borrowed_books_button = ctk.CTkButton(self.frame, text="Show Borrowed Books", command=self.library_app.show_borrowed_books)
        show_borrowed_books_button.pack(pady=12, padx=10)

        logout_button = ctk.CTkButton(self.frame, text="Logout", command=self.library_app.create_login_frame)
        logout_button.pack(pady=12, padx=10)
