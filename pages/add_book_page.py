import customtkinter as ctk
import tkinter.messagebox as messagebox

class AddBookPage:
    def __init__(self, app, library_app):
        self.app = app
        self.library_app = library_app
        self.frame = None

    def create_frame(self):
        # Close previous window
        if self.library_app.current_frame:
            self.library_app.current_frame.withdraw()

        # Create add book window
        self.frame = self.library_app.register_window(ctk.CTkToplevel(self.app))
        self.frame.title("Add Book")
        self.frame.geometry("400x400")
        self.frame.protocol("WM_DELETE_WINDOW", self.library_app.create_main_library_frame)

        code_catalogue_entry = ctk.CTkEntry(self.frame, placeholder_text="Code Catalogue")
        code_catalogue_entry.pack(pady=12, padx=10)

        cote_entry = ctk.CTkEntry(self.frame, placeholder_text="Cote")
        cote_entry.pack(pady=12, padx=10)

        date_acquisition_entry = ctk.CTkEntry(self.frame, placeholder_text="Date Acquisition (YYYY-MM-DD) e.g. 2023-10-27")
        date_acquisition_entry.pack(pady=12, padx=10)

        title_entry = ctk.CTkEntry(self.frame, placeholder_text="Title")
        title_entry.pack(pady=12, padx=10)

        author_entry = ctk.CTkEntry(self.frame, placeholder_text="Author")
        author_entry.pack(pady=12, padx=10)

        publisher_entry = ctk.CTkEntry(self.frame, placeholder_text="Publisher")
        publisher_entry.pack(pady=12, padx=10)

        mote_cles_entry = ctk.CTkEntry(self.frame, placeholder_text="Mote Cles (Optional)")
        mote_cles_entry.pack(pady=12, padx=10)

        id_editeur_entry = ctk.CTkEntry(self.frame, placeholder_text="ID Editeur (Optional)")
        id_editeur_entry.pack(pady=12, padx=10)

        id_theme_entry = ctk.CTkEntry(self.frame, placeholder_text="ID Theme (Optional)")
        id_theme_entry.pack(pady=12, padx=10)

        quantity_entry = ctk.CTkEntry(self.frame, placeholder_text="Quantity")
        quantity_entry.pack(pady=12, padx=10)

        save_button = ctk.CTkButton(self.frame, text="Save", 
            command=lambda: self.handle_save_book(
                code_catalogue_entry.get(),
                cote_entry.get(),
                date_acquisition_entry.get(),
                mote_cles_entry.get(),
                id_editeur_entry.get(),
                id_theme_entry.get(),
                title_entry.get(),
                author_entry.get(),
                publisher_entry.get(),
                quantity_entry.get(),
            ))
        save_button.pack(pady=12, padx=10)

        # Add back button
        back_button = ctk.CTkButton(self.frame, text="Back", command=self.library_app.create_main_library_frame)
        back_button.pack(pady=12, padx=10)

    def handle_save_book(self, code_catalogue, cote, date_acquisition, mote_cles, id_editeur, id_theme, title, author, publisher, quantity):
        # Check if any of the fields are empty
        if not code_catalogue or not cote or not date_acquisition or not title or not author or not publisher or not quantity:
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            if self.library_app.db.add_book(code_catalogue, cote, date_acquisition, mote_cles, id_editeur, id_theme, title, author, publisher, quantity):
                messagebox.showinfo("Success", "Book added successfully!")
                self.library_app.create_main_library_frame()
            else:
                messagebox.showerror("Error", "Failed to add book")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")
