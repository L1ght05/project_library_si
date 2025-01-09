import customtkinter as ctk
import tkinter.messagebox as messagebox

class ShowBooksPage:
    def __init__(self, app, library_app):
        self.app = app
        self.library_app = library_app
        self.frame = None

    def create_frame(self, username, search_term=None):
        # Retrieve books from database
        books = self.library_app.db.get_books()

        # Close previous window
        if self.library_app.current_frame:
            self.library_app.current_frame.withdraw()

        # Create books display window
        self.frame = self.library_app.register_window(ctk.CTkToplevel(self.app))
        self.frame.title("Available Books")
        self.frame.geometry("600x400")
        self.frame.protocol("WM_DELETE_WINDOW", self.library_app.create_main_library_frame)

        # Search functionality
        search_entry = ctk.CTkEntry(self.frame, placeholder_text="Search books...")
        search_entry.pack(pady=12, padx=10)

        search_button = ctk.CTkButton(self.frame, text="Search", command=lambda: self.search_books(books_frame, search_entry.get(), username))
        search_button.pack(pady=12, padx=10)

        # Create a frame to hold the books list
        books_frame = ctk.CTkScrollableFrame(self.frame)
        books_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.update_book_list(books_frame, search_term, username)

        # Back button
        back_button = ctk.CTkButton(self.frame, text="Back", command=self.library_app.create_main_library_frame)
        back_button.pack(pady=10, padx=10)

    def search_books(self, books_frame, search_term, username):
        subscription = self.library_app.db.get_current_subscription(username)
        if subscription:
            self.update_book_list(books_frame, search_term, username)
        else:
            messagebox.showerror("Error", "You must be a subscriber to search books.")

    def update_book_list(self, books_frame, search_term=None, username=None):
        # Clear previous book list
        for widget in books_frame.winfo_children():
            widget.destroy()

        # Retrieve books from database
        if search_term:
            books = self.library_app.db.search_livres(search_term)
        else:
            books = self.library_app.db.get_books()

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
                book_label.pack(pady=5, padx=10, anchor="w", side="left")

                borrow_button = ctk.CTkButton(books_frame, text="Borrow", command=lambda book_id=book[0], username=username: self.borrow_book(book_id, username))
                borrow_button.pack(pady=5, padx=10)


                delete_button = ctk.CTkButton(books_frame, text="Delete", command=lambda book_id=book[0]: self.delete_book(book_id))
                delete_button.pack(pady=5, padx=10)

                edit_button = ctk.CTkButton(books_frame, text="Edit", command=lambda book_id=book[0]: self.edit_book(book_id))
                edit_button.pack(pady=5, padx=10)

    def borrow_book(self, book_id, username):
        subscription = self.library_app.db.get_current_subscription(username)
        if subscription:
            if self.library_app.db.add_borrow(book_id, username):
                messagebox.showinfo("Success", "Book borrowed successfully!")
                self.update_book_list(self.frame, None, username)
            else:
                messagebox.showerror("Error", "Failed to borrow book.")
        else:
            messagebox.showerror("Error", "You must be a subscriber to borrow books.")

    def delete_book(self, book_id):
        if self.library_app.db.delete_book(book_id):
            messagebox.showinfo("Success", "Book deleted successfully!")
            self.library_app.show_books(self.library_app.logged_in_user)
        else:
            messagebox.showerror("Error", "Failed to delete book.")

    def edit_book(self, book_id):
        self.create_edit_book_dialog(book_id)

    def create_edit_book_dialog(self, book_id):
        edit_window = ctk.CTkToplevel(self.app)
        edit_window.title("Edit Book")
        edit_window.geometry("400x300")

        # Get book information
        book = self.library_app.db.get_book(book_id)

        if not book:
            messagebox.showerror("Error", "Book not found.")
            edit_window.destroy()
            return

        # Title
        ctk.CTkLabel(edit_window, text="Title:").pack(pady=5, padx=10, anchor="w")
        title_entry = ctk.CTkEntry(edit_window)
        title_entry.insert(0, book[7])
        title_entry.pack(pady=5, padx=10, fill="x")

        # Author
        ctk.CTkLabel(edit_window, text="Author:").pack(pady=5, padx=10, anchor="w")
        author_entry = ctk.CTkEntry(edit_window)
        author_entry.insert(0, book[8])
        author_entry.pack(pady=5, padx=10, fill="x")

        # Category
        ctk.CTkLabel(edit_window, text="Category:").pack(pady=5, padx=10, anchor="w")
        category_entry = ctk.CTkEntry(edit_window)
        category_entry.insert(0, book[4])
        category_entry.pack(pady=5, padx=10, fill="x")

        # Quantity
        ctk.CTkLabel(edit_window, text="Quantity:").pack(pady=5, padx=10, anchor="w")
        quantity_entry = ctk.CTkEntry(edit_window)
        quantity_entry.insert(0, book[10])
        quantity_entry.pack(pady=5, padx=10, fill="x")

        # Cote
        ctk.CTkLabel(edit_window, text="Cote:").pack(pady=5, padx=10, anchor="w")
        cote_entry = ctk.CTkEntry(edit_window)
        cote_entry.insert(0, book[2])
        cote_entry.pack(pady=5, padx=10, fill="x")

        # Save button
        save_button = ctk.CTkButton(edit_window, text="Save", command=lambda: self.save_edited_book(book_id, title_entry.get(), author_entry.get(), category_entry.get(), quantity_entry.get(), cote_entry.get(), edit_window))
        save_button.pack(pady=10, padx=10)

    def save_edited_book(self, book_id, title, author, category, quantity, cote, edit_window):
        if self.library_app.db.update_book(book_id, title, author, category, quantity, cote):
            messagebox.showinfo("Success", "Book updated successfully!")
            edit_window.destroy()
            self.library_app.create_show_books_frame(self.library_app.current_username)
        else:
            messagebox.showerror("Error", "Failed to update book.")
