import datetime
from database import Database

class LoanManager:
    def __init__(self, db: Database):
        self.db = db

    def create_loan(self, subscriber_id: int, catalog_code: str):
        loan_date = datetime.date.today()
        return_date = loan_date + datetime.timedelta(days=15)
        self.db.add_loan(subscriber_id, catalog_code, loan_date, return_date)

    def get_loans_by_subscriber(self, subscriber_id: int):
        return self.db.get_loans_by_subscriber(subscriber_id)

    def get_subscribers_by_book(self, catalog_code: str):
        return self.db.get_subscribers_by_book(catalog_code)

    def renew_loan(self, subscriber_id: int, catalog_code: str):
        loan = self.db.get_loan(subscriber_id, catalog_code)
        if not loan:
            return False
        if self.db.has_waitlist_request(catalog_code, loan[3]):
            return False
        new_return_date = loan[4] + datetime.timedelta(days=15)
        self.db.update_loan_return_date(subscriber_id, catalog_code, new_return_date)
        self.db.update_loan_renewal(subscriber_id, catalog_code, True)
        return True

    def add_waitlist_request(self, subscriber_id: int, catalog_code: str):
        request_date = datetime.date.today()
        self.db.add_waitlist_request(subscriber_id, catalog_code, request_date)

    def get_waitlist_by_book(self, catalog_code: str):
        return self.db.get_waitlist_by_book(catalog_code)

    def remove_waitlist_request(self, subscriber_id: int, catalog_code: str):
        self.db.remove_waitlist_request(subscriber_id, catalog_code)

    def assign_priority_waitlist(self, catalog_code: str):
        waitlist = self.db.get_waitlist_by_book(catalog_code)
        if not waitlist:
            return None
        subscriber_id = waitlist[0][1]
        return_date = datetime.date.today()
        self.db.update_waitlist_priority(subscriber_id, catalog_code, return_date)
        return subscriber_id

    def clear_priority_waitlist(self, catalog_code: str):
        self.db.clear_priority_waitlist(catalog_code)
