import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import datetime, timedelta

class SubscriptionPage:
    def __init__(self, app, library_app, logged_in_user):
        self.app = app
        self.library_app = library_app
        self.frame = None
        self.current_user = logged_in_user

    def check_existing_subscription(self):
        print("Checking existing subscription...")
        if self.current_user is not None:
            user = self.library_app.db.get_user(self.current_user)
            if user:
                subscription = self.library_app.db.get_current_subscription(user[0])
                if subscription:
                    messagebox.showinfo("Subscription Status", "You already have an active subscription.")
                    self.has_active_subscription = True
                    print(f"User has active subscription. self.has_active_subscription: {self.has_active_subscription}")
                else:
                    self.has_active_subscription = False
                    print(f"User does not have active subscription. self.has_active_subscription: {self.has_active_subscription}")
            else:
                self.has_active_subscription = False
                print(f"Invalid user data. self.has_active_subscription: {self.has_active_subscription}")
        else:
            self.has_active_subscription = False
            print(f"No user logged in. self.has_active_subscription: {self.has_active_subscription}")

    def create_frame(self):
        # Close previous window
        if self.library_app.current_frame:
            self.library_app.current_frame.destroy()

        # Create subscription window
        self.frame = self.library_app.register_window(ctk.CTkToplevel(self.app))
        self.library_app.current_frame = self.frame
        self.check_existing_subscription()
        self.frame.title("Subscription Plans")
        self.frame.geometry("600x500")
        self.frame.protocol("WM_DELETE_WINDOW", self.library_app.create_main_library_frame)

        # Subscription title
        label = ctk.CTkLabel(self.frame, text="Library Subscription Plans", font=("Helvetica", 20, "bold"))
        label.pack(pady=20, padx=10)

        if not self.has_active_subscription:
            no_subscription_label = ctk.CTkLabel(self.frame, text="You do not have an active subscription. Please select a plan.", font=("Helvetica", 12))
            no_subscription_label.pack(pady=10, padx=10)

        # Subscription Levels Frame
        plans_frame = ctk.CTkFrame(self.frame)
        plans_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Basic Plan
        basic_frame = ctk.CTkFrame(plans_frame)
        basic_frame.pack(pady=10, padx=10, fill="x")

        basic_label = ctk.CTkLabel(basic_frame, text="Basic Plan", font=("Helvetica", 16, "bold"))
        basic_label.pack(side="left", padx=10)

        basic_details = ctk.CTkLabel(basic_frame, text="Access to 5 books per month")
        basic_details.pack(side="left", padx=10)

        basic_price = ctk.CTkLabel(basic_frame, text="$9.99/month")
        basic_price.pack(side="right", padx=10)

        basic_button = ctk.CTkButton(basic_frame, text="Select", 
            command=lambda: self.select_subscription("Basic Plan", 9.99), state="disabled" if self.has_active_subscription else "normal")
        basic_button.pack(side="right", padx=10)

        # Premium Plan
        premium_frame = ctk.CTkFrame(plans_frame)
        premium_frame.pack(pady=10, padx=10, fill="x")

        premium_label = ctk.CTkLabel(premium_frame, text="Premium Plan", font=("Helvetica", 16, "bold"))
        premium_label.pack(side="left", padx=10)

        premium_details = ctk.CTkLabel(premium_frame, text="Access to 15 books per month")
        premium_details.pack(side="left", padx=10)

        premium_price = ctk.CTkLabel(premium_frame, text="$19.99/month")
        premium_price.pack(side="right", padx=10)

        premium_button = ctk.CTkButton(premium_frame, text="Select", 
            command=lambda: self.select_subscription("Premium Plan", 19.99),  state="disabled" if self.has_active_subscription else "normal")
        premium_button.pack(side="right", padx=10)

        # Enterprise Plan
        enterprise_frame = ctk.CTkFrame(plans_frame)
        enterprise_frame.pack(pady=10, padx=10, fill="x")

        enterprise_label = ctk.CTkLabel(enterprise_frame, text="VIP Plan", font=("Helvetica", 16, "bold"))
        enterprise_label.pack(side="left", padx=10)

        enterprise_details = ctk.CTkLabel(enterprise_frame, text="Unlimited book access")
        enterprise_details.pack(side="left", padx=10)

        enterprise_price = ctk.CTkLabel(enterprise_frame, text="$49.99/month")
        enterprise_price.pack(side="right", padx=10)

        enterprise_button = ctk.CTkButton(enterprise_frame, text="Select", 
            command=lambda: self.select_subscription("VIP Plan", 49.99),  state="disabled" if self.has_active_subscription else "normal")
        enterprise_button.pack(side="right", padx=10)

        # Back button
        back_button = ctk.CTkButton(self.frame, text="Back", command=self.library_app.create_main_library_frame)
        back_button.pack(pady=10, padx=10)

    def select_subscription(self, plan_name, price):
        self.library_app.select_subscription(plan_name, price)
