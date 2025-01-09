import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import datetime, timedelta

class PaymentPage:
    def __init__(self, app, library_app):
        self.app = app
        self.library_app = library_app
        self.frame = None

class PaymentMethodPage(PaymentPage):
    def __init__(self, app, library_app, plan_name, plan_price):
        super().__init__(app, library_app)
        self.plan_name = plan_name
        self.plan_price = plan_price

    def create_frame(self):
        # Create payment method selection window
        self.frame = self.library_app.register_window(ctk.CTkToplevel(self.app))
        self.library_app.current_frame = self.frame
        self.frame.title("Payment Method")
        self.frame.geometry("600x500")
        self.frame.protocol("WM_DELETE_WINDOW", self.library_app.manage_subscriptions)

        # Payment method selection title
        title_label = ctk.CTkLabel(self.frame, 
                                   text=f"Select Payment Method for {self.plan_name} Plan (${self.plan_price})", 
                                   font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20, padx=10)

        # Payment method selection frame
        payment_methods_frame = ctk.CTkFrame(self.frame)
        payment_methods_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Payment method options
        payment_methods = [
            "Visa Card", 
            "MasterCard", 
            "Carte El-Dahabia"
        ]

        selected_method = ctk.StringVar()

        def on_payment_method_select():
            method = selected_method.get()
            if not method:
                messagebox.showerror("Error", "Please select a payment method")
                return
            self.library_app.collect_card_information(self.frame, method, self.plan_name, self.plan_price)

        def go_back():
            self.frame.destroy()
            self.library_app.manage_subscriptions()

        for method in payment_methods:
            radio_button = ctk.CTkRadioButton(
                payment_methods_frame, 
                text=method, 
                variable=selected_method, 
                value=method
            )
            radio_button.pack(pady=10, padx=10, anchor="w")

        # Button frame
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="x")

        # Back button
        back_button = ctk.CTkButton(
            button_frame, 
            text="Back", 
            command=go_back
        )
        back_button.pack(side="left", padx=10)

        # Confirm button
        confirm_button = ctk.CTkButton(
            button_frame, 
            text="Proceed", 
            command=on_payment_method_select
        )
        confirm_button.pack(side="right", padx=10)

class CardInformationPage(PaymentPage):
    def __init__(self, app, library_app, payment_method, plan_name, plan_price):
        super().__init__(app, library_app)
        self.payment_method = payment_method
        self.plan_name = plan_name
        self.plan_price = plan_price

    def create_frame(self, parent_window):
        """
        Collect card information based on the selected payment method
        
        Args:
            parent_window (ctk.CTkToplevel): Parent window to withdraw
            payment_method (str): Selected payment method
            plan_name (str): Name of the selected subscription plan
            plan_price (float): Price of the selected subscription plan
        """
        # Close previous window
        parent_window.destroy()

        # Create card information collection window
        self.frame = self.library_app.register_window(ctk.CTkToplevel(self.app))
        self.library_app.current_frame = self.frame
        self.frame.title(f"{self.payment_method} Information")
        self.frame.geometry("600x500")
        self.frame.protocol("WM_DELETE_WINDOW", self.library_app.manage_subscriptions)

        # Card information title
        title_label = ctk.CTkLabel(
            self.frame, 
            text=f"Enter {self.payment_method} Details", 
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=20, padx=10)

        # Card information frame
        card_info_frame = ctk.CTkFrame(self.frame)
        card_info_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Common card information fields
        fields = [
            ("Cardholder's Name", "name"),
            ("Card Number", "number"),
            ("Expiration Date (MM/YY)", "expiry"),
            ("CVV", "cvv")
        ]

        # Additional fields for specific payment methods
        if self.payment_method == "Visa Card":
            fields.append(("Billing Address (Optional)", "billing_address"))
        elif self.payment_method == "MasterCard":
            fields.append(("Billing Address (Optional)", "billing_address"))
        elif self.payment_method == "Credit Card":
            fields.append(("Billing Address", "billing_address"))
            fields.append(("Type Specification (Visa, MasterCard, etc.)", "type_specification"))
        elif self.payment_method == "Carte El-Dahabia":
            fields.append(("Billing Address (Optional)", "billing_address"))

        # Create entry fields
        card_entries = {}
        for label_text, entry_key in fields:
            label = ctk.CTkLabel(card_info_frame, text=label_text)
            label.pack(pady=(10, 5), padx=10, anchor="w")
            
            entry = ctk.CTkEntry(card_info_frame, width=400)
            entry.pack(pady=(0, 10), padx=10, fill="x")
            card_entries[entry_key] = entry

        def validate_and_process_payment():
            # Basic validation (you can enhance this)
            card_info = {key: entry.get().strip() for key, entry in card_entries.items()}
            
            # Simple validation example
            if not all(card_info.values()):
                messagebox.showerror("Error", "Please fill in all card details")
                return

            # Here you would typically integrate with a payment gateway
            # For now, we'll just show a success message
            messagebox.showinfo("Payment Successful", 
                                f"Successfully subscribed to {self.plan_name} plan!")
            
            # Get the plan ID from the database
            plans = self.library_app.db.get_subscription_plans()
            plan_id = None
            for plan in plans:
                if plan[1] == self.plan_name:
                    plan_id = plan[0]
                    break
            if plan_id:
                # Calculate the end date based on the plan duration
                start_date = datetime.now()
                duration_months = 0
                for plan in plans:
                    if plan[1] == self.plan_name:
                        duration_months = plan[3]
                        break
                end_date = start_date +  timedelta(days=duration_months*30)
            # Get the plan ID from the database
            plans = self.library_app.db.get_subscription_plans()
            plan_id = None
            for plan in plans:
                if plan[1] == self.plan_name:
                    plan_id = plan[0]
                    break
            if plan_id:
                # Calculate the end date based on the plan duration
                start_date = datetime.now()
                duration_months = 0
                for plan in plans:
                    if plan[1] == self.plan_name:
                        duration_months = plan[3]
                        break
                end_date = start_date +  timedelta(days=duration_months*30)
                # Save the subscription to the database
                if hasattr(self.library_app, 'logged_in_user') and self.library_app.logged_in_user:
                    user = self.library_app.db.get_user(self.library_app.logged_in_user)
                    if user:
                        self.library_app.db.add_subscription(user[0], plan_id, start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S'), "abonne")
                        # Close the card info window and return to main window
                        self.frame.destroy()
                        self.library_app.create_main_library_frame()
                    else:
                        messagebox.showerror("Error", "User not found.")
                else:
                    messagebox.showerror("Error", "Please log in to subscribe.")
            else:
                messagebox.showerror("Error", "Could not find the selected plan.")

        def go_back():
            self.frame.destroy()
            self.library_app.select_payment_method(self.plan_name, self.plan_price)

        # Button frame
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="x")

        # Back button
        back_button = ctk.CTkButton(
            button_frame, 
            text="Back", 
            command=go_back
        )
        back_button.pack(side="left", padx=10)

        # Confirm payment button
        confirm_payment_button = ctk.CTkButton(
            button_frame, 
            text="Confirm Payment", 
            command=validate_and_process_payment
        )
        confirm_payment_button.pack(side="right", padx=10)
