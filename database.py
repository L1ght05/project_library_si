import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_path='library.db'):
        """
        Initialize the database with necessary tables
        """
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """
        Create all tables for the library management system
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables for library management system
        cursor.executescript('''
        -- Existing tables...

        -- Table: users
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        );

        -- Table: subscription_plans
        CREATE TABLE IF NOT EXISTS subscription_plans (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            duration_months INTEGER NOT NULL,
            description TEXT
        );

        -- Table: user_subscriptions
        CREATE TABLE IF NOT EXISTS user_subscriptions (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            plan_id INTEGER NOT NULL,
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL,
            payment_status TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users (username),
            FOREIGN KEY (plan_id) REFERENCES subscription_plans (id)
        );

        -- Table: livres
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_catalogue TEXT NOT NULL,
            cote TEXT NOT NULL,
            date_acquisition DATE NOT NULL,
            mote_cles TEXT,
            id_editeur TEXT,
            id_theme TEXT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publisher TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1
        );

        -- Table: loans
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscriber_id INTEGER NOT NULL,
            catalog_code TEXT NOT NULL,
            loan_date DATE NOT NULL,
            return_date DATE NOT NULL,
            is_renewed BOOLEAN DEFAULT 0,
            FOREIGN KEY (subscriber_id) REFERENCES users (id),
            FOREIGN KEY (catalog_code) REFERENCES livres (code_catalogue)
        );

        -- Table: waitlist
        CREATE TABLE IF NOT EXISTS waitlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscriber_id INTEGER NOT NULL,
            catalog_code TEXT NOT NULL,
            request_date DATE NOT NULL,
            priority_date DATE,
            FOREIGN KEY (subscriber_id) REFERENCES users (id),
            FOREIGN KEY (catalog_code) REFERENCES livres (code_catalogue)
        );
        ''')

        # Insert default subscription plans if not exists
        plans = [
            ('Basic Plan', 9.99, 1, 'Monthly access to library resources'),
            ('Standard Plan', 19.99, 3, 'Quarterly access with additional benefits'),
            ('Premium Plan', 29.99, 12, 'Full year access with all features')
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO subscription_plans 
            (name, price, duration_months, description) 
            VALUES (?, ?, ?, ?)
        ''', plans)

        conn.commit()
        conn.close()

    def add_user(self, username, hashed_password, email, is_admin=False):
        """
        Add a new user to the system
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users 
                (username, password, email, is_admin) 
                VALUES (?, ?, ?, ?)
            ''', (username, hashed_password, email, is_admin))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"User {username} or email already exists.")
            return False
        finally:
            conn.close()

    def get_user(self, username):
        """
        Retrieve a user by username
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving user: {e}")
            return None
        finally:
            conn.close()

    def update_last_login(self, username):
        """
        Update the last login timestamp for a user
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE users 
                SET last_login = ? 
                WHERE username = ?
            ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating last login: {e}")
        finally:
            conn.close()

    def get_subscription_plans(self):
        """
        Retrieve all subscription plans
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM subscription_plans')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving subscription plans: {e}")
            return []
        finally:
            conn.close()

    def add_subscription(self, username, plan_id, start_date, end_date, payment_status):
        """
        Add a new user subscription
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO user_subscriptions 
                (username, plan_id, start_date, end_date, payment_status) 
                VALUES (?, ?, ?, ?, ?)
            ''', (username, plan_id, start_date, end_date, payment_status))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding subscription: {e}")
            return False
        finally:
            conn.close()

    def get_current_subscription(self, username):
        """
        Get the current active subscription for a user
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT us.*, sp.name, sp.description 
                FROM user_subscriptions us
                JOIN subscription_plans sp ON us.plan_id = sp.id
                WHERE us.username = ? AND us.end_date > ? AND us.payment_status = 'abonne'
                ORDER BY us.end_date DESC
                LIMIT 1
            ''', (username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving subscription: {e}")
            return None
        finally:
            conn.close()

    def add_book(self, code_catalogue, cote, date_acquisition, mote_cles=None, id_editeur=None, id_theme=None, title=None, author=None, publisher=None, quantity=1):
        """
        Add a new book to the system
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO livres (code_catalogue, cote, date_acquisition, mote_cles, id_editeur, id_theme, title, author, publisher, quantity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (code_catalogue, cote, date_acquisition, mote_cles, id_editeur, id_theme, title, author, publisher, quantity))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")
            return False
        finally:
            conn.close()

    def get_books(self):
        """
        Retrieve all books from the system
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM livres')
            books = cursor.fetchall()
            return books
        except sqlite3.Error as e:
            print(f"Error retrieving books: {e}")
            return []
        finally:
            conn.close()
    
    def get_book(self, book_id):
        """
        Retrieve a book by its ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM livres WHERE id = ?', (book_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving book: {e}")
            return None
        finally:
            conn.close()

    def delete_book(self, book_id):
        """
        Delete a book from the system
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM livres WHERE id = ?', (book_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting book: {e}")
            return False
        finally:
            conn.close()

    def update_book(self, book_id, title, author, category, quantity, cote):
        """
        Update a book's information
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE livres
                SET title = ?, author = ?, mote_cles = ?, quantity = ?, cote = ?
                WHERE id = ?
            ''', (title, author, category, quantity, cote, book_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating book: {e}")
            return False
        finally:
            conn.close()
            
    def search_livres(self, search_term):
        """
        Search for books by title, author, publisher, or theme
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM livres
                WHERE title LIKE ? OR author LIKE ? OR mote_cles LIKE ? OR publisher LIKE ?
            ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            books = cursor.fetchall()
            return books
        except sqlite3.Error as e:
            print(f"Error searching books: {e}")
            return []
        finally:
            conn.close()

    def get_borrowed_books_with_users(self):
        """
        Get all borrowed books with user information
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT u.id, l.title, l.id, l.author
                FROM pret p
                JOIN users u ON p.username = u.username
                JOIN livres l ON p.book_id = l.id
            ''')
            borrowed_books = cursor.fetchall()
            return borrowed_books
        except sqlite3.Error as e:
            print(f"Error retrieving borrowed books with users: {e}")
            return []
        finally:
            conn.close()

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by their ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving user: {e}")
            return None
        finally:
            conn.close()

    def add_loan(self, subscriber_id: int, catalog_code: str, loan_date: datetime.date, return_date: datetime.date):
        """
        Add a new loan record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM loans WHERE subscriber_id = ? AND catalog_code = ?
            ''', (subscriber_id, catalog_code))
            existing_loan = cursor.fetchone()
            if existing_loan:
                print(f"Loan already exists for subscriber {subscriber_id} and book {catalog_code}")
                return False
            cursor.execute('''
                INSERT INTO loans (subscriber_id, catalog_code, loan_date, return_date)
                VALUES (?, ?, ?, ?)
            ''', (subscriber_id, catalog_code, loan_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d')))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding loan record: {e}")
            return False
        finally:
            conn.close()

    def get_loans_by_subscriber(self, subscriber_id: int):
        """
        Get all loans for a subscriber with book and user information
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT lo.loan_date, lo.return_date, l.title, l.author, u.username, u.id
                FROM loans lo
                JOIN livres l ON lo.catalog_code = l.code_catalogue
                JOIN users u ON lo.subscriber_id = u.id
                WHERE lo.subscriber_id = ?
            ''', (subscriber_id,))
            loans = cursor.fetchall()
            return loans
        except sqlite3.Error as e:
            print(f"Error retrieving loans for subscriber: {e}")
            return []
        finally:
            conn.close()

    def get_subscribers_by_book(self, catalog_code: str):
        """
        Get all subscribers who have borrowed a book
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM loans WHERE catalog_code = ?
            ''', (catalog_code,))
            loans = cursor.fetchall()
            return loans
        except sqlite3.Error as e:
            print(f"Error retrieving subscribers for book: {e}")
            return []
        finally:
            conn.close()

    def get_loan(self, subscriber_id: int, catalog_code: str):
        """
        Get a specific loan record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM loans WHERE subscriber_id = ? AND catalog_code = ?
            ''', (subscriber_id, catalog_code))
            loan = cursor.fetchone()
            return loan
        except sqlite3.Error as e:
            print(f"Error retrieving loan: {e}")
            return None
        finally:
            conn.close()

    def update_loan_return_date(self, subscriber_id: int, catalog_code: str, new_return_date: datetime.date):
        """
        Update the return date of a loan
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE loans SET return_date = ? WHERE subscriber_id = ? AND catalog_code = ?
            ''', (new_return_date, subscriber_id, catalog_code))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating loan return date: {e}")
            return False
        finally:
            conn.close()

    def update_loan_renewal(self, subscriber_id: int, catalog_code: str, is_renewed: bool):
        """
        Update the renewal status of a loan
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE loans SET is_renewed = ? WHERE subscriber_id = ? AND catalog_code = ?
            ''', (is_renewed, subscriber_id, catalog_code))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating loan renewal status: {e}")
            return False
        finally:
            conn.close()

    def add_waitlist_request(self, subscriber_id: int, catalog_code: str, request_date: datetime.date):
        """
        Add a new waitlist request
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO waitlist (subscriber_id, catalog_code, request_date)
                VALUES (?, ?, ?)
            ''', (subscriber_id, catalog_code, request_date))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding waitlist request: {e}")
            return False
        finally:
            conn.close()

    def get_waitlist_by_book(self, catalog_code: str):
        """
        Get all waitlist requests for a book
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM waitlist WHERE catalog_code = ? ORDER BY request_date ASC
            ''', (catalog_code,))
            waitlist = cursor.fetchall()
            return waitlist
        except sqlite3.Error as e:
            print(f"Error retrieving waitlist for book: {e}")
            return []
        finally:
            conn.close()

    def remove_waitlist_request(self, subscriber_id: int, catalog_code: str):
        """
        Remove a waitlist request
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                DELETE FROM waitlist WHERE subscriber_id = ? AND catalog_code = ?
            ''', (subscriber_id, catalog_code))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error removing waitlist request: {e}")
            return False
        finally:
            conn.close()

    def update_waitlist_priority(self, subscriber_id: int, catalog_code: str, priority_date: datetime.date):
        """
        Update the priority date of a waitlist request
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE waitlist SET priority_date = ? WHERE subscriber_id = ? AND catalog_code = ?
            ''', (priority_date, subscriber_id, catalog_code))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating waitlist priority: {e}")
            return False
        finally:
            conn.close()

    def clear_priority_waitlist(self, catalog_code: str):
        """
        Clear the priority date of all waitlist requests for a book
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE waitlist SET priority_date = NULL WHERE catalog_code = ?
            ''', (catalog_code,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error clearing waitlist priority: {e}")
            return False
        finally:
            conn.close()

    def has_waitlist_request(self, catalog_code: str, loan_date: datetime.date):
        """
        Check if there is a waitlist request for a book during a loan period
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM waitlist WHERE catalog_code = ? AND request_date <= ?
            ''', (catalog_code, loan_date))
            waitlist = cursor.fetchall()
            return len(waitlist) > 0
        except sqlite3.Error as e:
            print(f"Error checking waitlist request: {e}")
            return False
        finally:
            conn.close()
