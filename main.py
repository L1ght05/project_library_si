import customtkinter as ctk
import tkinter.messagebox as messagebox
import hashlib
import secrets
from datetime import datetime, timedelta
from database import Database
from loan_manager import LoanManager
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.main_library_page import MainLibraryPage
from pages.add_book_page import AddBookPage
from pages.show_books_page import ShowBooksPage
from pages.subscription_page import SubscriptionPage
from pages.payment_page import PaymentMethodPage, CardInformationPage

class LibraryApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Library Management System")
        self.app.geometry("800x600")

        self.db = Database()
        self.loan_manager = LoanManager(self.db)
        self._ensure_admin_exists()

        # Track current active frame/window
        self.current_frame = None
        self.previous_frame = None
        self.active_windows = []

        self.create_login_frame()

    def close_all_windows(self):
        """Close all active windows except the main application window"""
        for window in self.active_windows.copy():
            try:
                window.destroy()
            except:
                pass
        self.active_windows.clear()
        self.current_frame = None
        self.show_main_window()

    def hide_main_window(self):
        """Hide the main application window"""
        self.app.withdraw()

    def show_main_window(self):
        """Show the main application window"""
        self.app.deiconify()

    def register_window(self, window):
        """Register a window to be tracked and managed"""
        if window not in self.active_windows:
            self.active_windows.append(window)
        return window

    def create_login_frame(self):
        login_page = LoginPage(self.app, self)
        login_page.create_frame()
        self.current_frame = login_page.frame
        self.username_entry = login_page.username_entry
        self.password_entry = login_page.password_entry

    def create_register_frame(self):
        register_page = RegisterPage(self.app, self)
        register_page.create_frame()
        self.current_frame = register_page.frame

    def _ensure_admin_exists(self):
        """Ensure that at least one admin user exists"""
        admin = self.db.get_user('admin')
        if not admin:
            default_password = self._hash_password('admin123')
            self.db.add_user('admin', default_password, 'admin@library.com', is_admin=True)

    def _hash_password(self, password, salt=None):
        """Hash a password with optional salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        salted = password + salt
        hashed = hashlib.sha256(salted.encode()).hexdigest()
        
        return f"{salt}:{hashed}"

    def _verify_password(self, password, stored_password):
        """Verify a password against its hash"""
        salt, stored_hash = stored_password.split(':')
        test_hash = self._hash_password(password, salt).split(':')[1]
        return test_hash == stored_hash

    def register_user(self, username, password, email):
        """Register a new user"""
        hashed_password = self._hash_password(password)
        if self.db.add_user(username, hashed_password, email):
            user = self.db.get_user(username)
            if user:
                basic_plan = self.db.get_subscription_plans()[0]
                start_date = datetime.now()
                end_date = start_date + timedelta(days=30)
                self.db.add_subscription(username, basic_plan[0], start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S'), 'abonne')
                return True
        return False

    def login(self, username, password):
        """Authenticate user"""
        user = self.db.get_user(username)
        if user and self._verify_password(password, user[2]):  # password is at index 2
            return True
        return False

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.login(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            self.logged_in_user = username
            self.create_main_library_frame()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def handle_register(self, username, password, email):
        if self.register_user(username, password, email):
            messagebox.showinfo("Success", "Registration Successful!")
            self.create_login_frame()
        else:
            messagebox.showerror("Error", "Registration Failed")

    def create_main_library_frame(self):
        main_library_page = MainLibraryPage(self.app, self)
        main_library_page.create_frame()
        self.current_frame = main_library_page.frame

    def add_book(self):
        add_book_page = AddBookPage(self.app, self)
        add_book_page.create_frame()
        self.current_frame = add_book_page.frame

    def save_book(self, code_catalogue, cote, date_acquisition, mote_cles, id_editeur, id_theme, title, author, publisher, quantity, window):
        # Check if any of the fields are empty
        if not code_catalogue or not cote or not date_acquisition or not title or not author or not publisher or not quantity:
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            if self.db.add_book(code_catalogue, cote, date_acquisition, mote_cles, id_editeur, id_theme, title, author, publisher, quantity):
                messagebox.showinfo("Success", "Book added successfully!")
                self.create_main_library_frame()
            else:
                messagebox.showerror("Error", "Failed to add book")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")

    def show_books(self, username, search_term=None):
        show_books_page = ShowBooksPage(self.app, self)
        show_books_page.create_frame(username, search_term)
        self.current_frame = show_books_page.frame

    def update_book_list(self, books_frame, search_term=None):
        # Clear previous book list
        for widget in books_frame.winfo_children():
            widget.destroy()

        # Retrieve books from database
        if search_term:
            books = self.db.search_livres(search_term)
        else:
            books = self.db.get_books()

        # Display books
        if not books:
            no_books_label = ctk.CTkLabel(books_frame, text="No books available")
            no_books_label.pack(pady=20, padx=10)
        else:
            for book in books:
                book_label = ctk.CTkLabel(
                    books_frame,
                    text=f"Title: {book[7]}, Author: {book[8]}, Category: {book[4]}, Quantity: {book[10]}, Cote: {book[2]}"
                )
                book_label.pack(pady=5, padx=10, anchor="w")

    def manage_subscriptions(self):
        if not hasattr(self, 'logged_in_user') or self.logged_in_user is None:
            messagebox.showerror("Error", "Please log in to manage subscriptions.")
            return
        
        user = self.db.get_user(self.logged_in_user)
        if user:
            subscription = self.db.get_current_subscription(user[0])
            if subscription:
                messagebox.showinfo("Subscription Status", "You already have an active subscription.")
                return
        
        subscription_page = SubscriptionPage(self.app, self, self.logged_in_user)
        subscription_page.create_frame()
        self.current_frame = subscription_page.frame

    def select_subscription(self, plan_name, plan_price):
        """
        Proceed to payment method selection after plan selection
        
        Args:
            plan_name (str): Name of the selected subscription plan
            plan_price (float): Price of the selected subscription plan
        """
        # Close subscription window
        if self.current_frame:
            self.current_frame.destroy()
        
        # Proceed to payment method selection
        self.select_payment_method(plan_name, plan_price)

    def select_payment_method(self, plan_name, plan_price):
        payment_method_page = PaymentMethodPage(self.app, self, plan_name, plan_price)
        payment_method_page.create_frame()
        self.current_frame = payment_method_page.frame

    def collect_card_information(self, parent_window, payment_method, plan_name, plan_price):
        card_information_page = CardInformationPage(self.app, self, payment_method, plan_name, plan_price)
        card_information_page.create_frame(parent_window)
        self.current_frame = card_information_page.frame
        
        user = self.db.get_user(self.logged_in_user)
        if user:
            plan = self.db.get_subscription_plans()
            selected_plan = next((p for p in plan if p[1] == plan_name), None)
            if selected_plan:
                start_date = datetime.now()
                end_date = start_date + timedelta(days=selected_plan[3] * 30)
                self.db.add_subscription(user[1], selected_plan[0], start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S'), 'abonne')

    def show_borrowed_books(self):
        if not hasattr(self, 'logged_in_user') or self.logged_in_user is None:
            messagebox.showerror("Error", "Please log in to view borrowed books.")
            return

        loans = self.loan_manager.get_loans_by_subscriber(self.db.get_user(self.logged_in_user)[0])
        if not loans:
            messagebox.showinfo("Info", "No books have been borrowed yet.")
        else:
            borrowed_books_info = ""
            for loan in loans:
                book = self.db.get_book(loan[2])
                if book:
                    borrowed_books_info += f"Book Title: {book[7]}, Author: {book[8]}, Loan Date: {loan[3]}, Return Date: {loan[4]}\n"
            messagebox.showinfo("Borrowed Books", borrowed_books_info)
        self.create_main_library_frame()

    def borrow_book(self, book_id):
        if not hasattr(self, 'logged_in_user') or self.logged_in_user is None:
            messagebox.showerror("Error", "Please log in to borrow books.")
            return
        
        user = self.db.get_user(self.logged_in_user)
        book = self.db.get_book(book_id)
        if user and book:
            self.loan_manager.create_loan(user[0], book[1])
            messagebox.showinfo("Success", f"Book '{book[7]}' borrowed successfully!")
            self.create_main_library_frame()
        else:
            messagebox.showerror("Error", "Failed to borrow book.")

    def run(self):
        """Run the main application loop"""
        self.app.mainloop()

if __name__ == "__main__":
    app = LibraryApp()
    app.run()
