import sqlite3
from contextlib import contextmanager
import os
import bcrypt
import sys



def resources_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    return full_path



# DATABASE NAME
DATABASE_LOC = 'database/main/current_db.db'
DATABASE_NAME = resources_path(DATABASE_LOC)


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.close()


def initialize_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Resident Information Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS residents_data (
            resident_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            purok TEXT,
            lastname TEXT,
            middlename TEXT,
            firstname TEXT,
            suffix TEXT,
            age INTEGER,
            sex TEXT,
            civil_status TEXT,
            blood_type TEXT,
            dob TEXT,
            place_of_birth TEXT,
            occupation TEXT,
            religion TEXT,
            tribe_and_ethnicity TEXT,
            educational_status TEXT,
            comelec TEXT,
            philsys TEXT,
            pwd_member TEXT,
            pwd_disability TEXT,
            senior_member TEXT,
            solo_parent_member TEXT,
            kasambahay_salary TEXT,
            four_ps TEXT,
            salt_used TEXT,
            garbage_disposal TEXT,
            animals TEXT,
            farmers_membership_FA TEXT,
            farmers_membership_RSBSA TEXT,
            source_of_water TEXT,
            family_planning_used TEXT,
            types_of_cr TEXT,
            resident_status TEXT
            )
            ''')

        # Barangay Officials and Personnel Information Table
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS barangayOfficials_data (
                    officials_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    first_name TEXT,
                    middle_name TEXT,
                    last_name TEXT,
                    suffix_name TEXT,
                    official_position TEXT
                    )
                    ''')

        # Blotter Records
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS blotter_data (
                            blotter_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            blotter_date_filed TEXT,
                            blotter_case_no TEXT,
                            blotter_reason TEXT,
                            blotter_note TEXT
                            )
                            ''')

        # Blotter Complainants
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS blotter_complainants (
                            complainant_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            blotter_case_no TEXT,
                            first_name TEXT,
                            middle_name TEXT,
                            last_name TEXT,
                            suffix TEXT
                            )
                            ''')
        
        # Blotter Complainants Address
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS blotter_complainants_address (
                            add_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            blotter_case_no INTEGER NOT NULL,
                            purok_name TEXT,
                            barangay_name TEXT,
                            city_name TEXT,
                            province_name TEXT
                            )
                            ''')

        # Blotter Respondents
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS blotter_respondents (
                            respondents_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            blotter_case_no TEXT,
                            first_name TEXT,
                            middle_name TEXT,
                            last_name TEXT,
                            suffix TEXT
                            )
                            ''')
        
        # Blotter Respondents Address
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS blotter_respondents_address (
                            add_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            blotter_case_no INTEGER NOT NULL,
                            purok_name TEXT,
                            barangay_name TEXT,
                            city_name TEXT,
                            province_name TEXT
                            )
                            ''')

        # User Accounts
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            user_role TEXT,
                            user_desc TEXT,
                            username TEXT,
                            password TEXT
                            )
                            ''')

        # User Logs
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS user_activity (
                            activity_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            activity_username TEXT,
                            activity_user_role TEXT,
                            activity_date TEXT,
                            activity_action TEXT
                            )
                            ''')

        # Resident Documents Logs
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS residents_activity (
                            activity_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            activity_username TEXT,
                            activity_doc_type TEXT,
                            activity_date TEXT,
                            activity_requestee TEXT
                            )
                            ''')

        # Backup Log
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS backup_log (
                            backup_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            backup_date TEXT,
                            backup_filename TEXT,
                            backup_username TEXT
                            )
                            ''')
        
        # Profiling Log
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS profiling_log (
                            log_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            log_date TEXT,
                            log_activity TEXT,
                            log_residents TEXT,
                            log_changes TEXT,
                            log_username TEXT
                            )
                            ''')

         # Blotter Log
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS blotter_log (
                            log_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            date_time TEXT,
                            blotter_case_no TEXT,
                            action TEXT,
                            username TEXT
                            )
                            ''')
        conn.commit()

        if not check_users():
            create_accounts()



def check_users():
    try:
        with get_db_connection() as con:
            cursor = con.cursor()
            cursor.execute('SELECT * FROM users WHERE user_role = "sysadmin_"')
            users = cursor.fetchall()
            if not users:
                return False
            else:
                return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error updating birthdays: {e}")


def create_accounts():
    user_role, user_desc, username, password = ("sysadmin_", "NDMC-CITE", "sysadmin_ndmc", bcrypt.hashpw("123".encode('utf-8'), bcrypt.gensalt()))

    try:
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute('INSERT INTO users (user_role, user_desc, username, password) VALUES (?, ?, ?, ?)',
                        (user_role, user_desc, username, password))
            con.commit()
    except sqlite3.Error as error:
        print(f"Sqlite Error: {error}")
    except ValueError as ve:
        print(f"Value Error: {ve}")
    except Exception as e:
        print(f"Exception Error: {e}")
