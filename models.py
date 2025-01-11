from database import get_db_connection
from datetime import datetime
import sqlite3


def update_data(resident_data):
    resident_id = resident_data[0]
    purok = resident_data[1]
    lastname = resident_data[2]
    middlename = resident_data[4]
    firstname = resident_data[3]
    suffix = resident_data[5]
    age = int(resident_data[6])
    sex = resident_data[7]
    civil_status = resident_data[8]
    blood_type = resident_data[9]
    dob = resident_data[10]
    place_of_birth = resident_data[11]
    occupation = resident_data[12]
    religion = resident_data[13]
    tribe_and_ethnicity = resident_data[14]
    educational_status = resident_data[15]
    comelec = resident_data[16]
    philsys = resident_data[17]
    pwd_member = resident_data[18]
    pwd_disability = resident_data[19]
    senior_member = resident_data[20]
    solo_parent_member = resident_data[21]
    kasambahay_salary = resident_data[22]
    four_ps = resident_data[23]
    salt_used = resident_data[24]
    garbage_disposal = resident_data[25]
    animals = resident_data[26]
    farmers_membership_FA = resident_data[27]
    farmers_membership_RSBSA = resident_data[28]
    source_of_water = resident_data[29]
    family_planning_used = resident_data[30]
    types_of_cr = resident_data[31]
    resident_status = resident_data[32]

    try:
        # Convert age and resident_id to int only if they are not empty strings
        age = int(age) if age else None
        resident_id = int(resident_id) if resident_id else None

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE residents_data SET
                purok = ?,
                lastname = ?,
                middlename = ?,
                firstname = ?,
                suffix = ?,
                age = ?,
                sex = ?,
                civil_status = ?,
                blood_type = ?,
                dob = ?,
                place_of_birth =?,
                occupation = ?,
                religion = ?,
                tribe_and_ethnicity = ?,
                educational_status = ?,
                comelec = ?,
                philsys = ?,
                pwd_member = ?,
                pwd_disability = ?,
                senior_member = ?,
                solo_parent_member = ?,
                kasambahay_salary = ?,
                four_ps = ?,
                salt_used = ?,
                garbage_disposal = ?,
                animals = ?,
                farmers_membership_FA = ?,
                farmers_membership_RSBSA = ?,
                source_of_water = ?,
                family_planning_used = ?,
                types_of_cr = ?,
                resident_status = ?
                WHERE resident_id = ?
            """, (purok, lastname, middlename, firstname, suffix, age, sex, civil_status, blood_type, dob, place_of_birth, occupation,
                  religion, tribe_and_ethnicity, educational_status, comelec, philsys, pwd_member, pwd_disability,
                  senior_member, solo_parent_member, kasambahay_salary, four_ps, salt_used, garbage_disposal, animals,
                  farmers_membership_FA, farmers_membership_RSBSA, source_of_water, family_planning_used, types_of_cr, resident_status,
                  resident_id))
            conn.commit()
    except Exception as e:
        print(f"Error updating data: {e}")


def update_birthdays():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT resident_id, dob FROM residents_data")
            residents = cursor.fetchall()

            for resident in residents:
                resident_id, dob_str = resident
                dob = datetime.strptime(dob_str, '%d-%m-%Y')
                age = (datetime.now() - dob).days // 365

                cursor.execute("UPDATE residents_data SET age=? WHERE resident_id=?", (age, resident_id))

            conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    except Exception as e:
        print(f"Error updating birthdays: {e}")


def get_barangay_captain(name_type):
    captain_name = ""

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT last_name, middle_name, first_name, suffix_name 
                FROM barangayOfficials_data WHERE official_position = ?
                """,
                ("Punong Barangay",))
            kapitan_info = cursor.fetchone()

            if kapitan_info is None:
                return 0

            last_name, middle_name, first_name, suffix_name = kapitan_info

            if name_type == "name":
                if suffix_name == "":
                    full_name = f"{first_name} {middle_name[0]}. {last_name}"
                    captain_name = full_name
                else:
                    full_name = f"{first_name} {middle_name[0]}. {last_name} {suffix_name}"
                    captain_name = full_name

            if name_type == "fullName":
                if suffix_name == "":
                    full_name = f"{first_name} {middle_name} {last_name}"
                    captain_name = full_name
                else:
                    full_name = f"{first_name} {middle_name} {last_name} {suffix_name}"
                    captain_name = full_name

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return 0

    except Exception as e:
        print(f"Error getting barangay captain: {e}")
        return 0

    return captain_name


def get_barangay_kagawad():
    officials_list = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT last_name, middle_name, first_name, suffix_name 
            FROM barangayOfficials_data WHERE official_position = ?""",
                           ("Kagawad",))
            officials = cursor.fetchall()

            for kagawad in officials:
                last_name, middle_name, first_name, suffix_name = kagawad
                if suffix_name == "":
                    full_name = f"{first_name} {middle_name[0]}. {last_name}"
                else:
                    full_name = f"{first_name} {middle_name[0]}. {last_name} {suffix_name}"
                officials_list.append(full_name)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return 0

    except Exception as e:
        print(f"Error getting barangay kagawad: {e}")
        return 0

    if not officials_list:
        return 0

    if len(officials_list) <= 6:
        return 0

    return officials_list


def get_barangay_pangkat_member():
    pangkat_list = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT last_name, middle_name, first_name, suffix_name 
                FROM barangayOfficials_data WHERE official_position = ?""",
                           ("Lupon",))
            officials = cursor.fetchall()

            for kagawad in officials:
                last_name, middle_name, first_name, suffix_name = kagawad
                if suffix_name == "":
                    full_name = f"{first_name} {middle_name[0]}. {last_name}"
                else:
                    full_name = f"{first_name} {middle_name[0]}. {last_name} {suffix_name}"
                pangkat_list.append(full_name)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return 0

    except Exception as e:
        print(f"Error getting barangay kagawad: {e}")
        return 0

    if not pangkat_list:
        return 0

    if len(pangkat_list) <= 6:
        return 0

    return pangkat_list


def get_barangay_pangkat_chairman():
    chairman_name = ""

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT last_name, middle_name, first_name, suffix_name 
                FROM barangayOfficials_data WHERE official_position = ?
                """,
                ("Pangkat Chairman",))
            chairman_info = cursor.fetchone()

            if chairman_info is None:
                return 0

            last_name, middle_name, first_name, suffix_name = chairman_info

            if suffix_name == "":
                full_name = f"{first_name} {middle_name[0]}. {last_name}"
                chairman_name = full_name
            else:
                full_name = f"{first_name} {middle_name[0]}. {last_name} {suffix_name}"
                chairman_name = full_name

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return 0

    except Exception as e:
        print(f"Error getting barangay captain: {e}")
        return 0

    return chairman_name


def get_barangay_sk():
    chairman_name = ""

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT last_name, middle_name, first_name, suffix_name 
                FROM barangayOfficials_data WHERE official_position = ?
                """,
                ("SK Chairman",))
            kapitan_info = cursor.fetchone()

            if kapitan_info is None:
                return 0

            last_name, middle_name, first_name, suffix_name = kapitan_info

            if suffix_name == "":
                full_name = f"{first_name} {middle_name[0]}. {last_name}"
                chairman_name = full_name
            else:
                full_name = f"{first_name} {middle_name[0]}. {last_name} {suffix_name}"
                chairman_name = full_name

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return 0

    except Exception as e:
        print(f"Error getting barangay captain: {e}")
        return 0

    return chairman_name


def get_barangay_secretary():
    secretary_name = ""

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT last_name, middle_name, first_name, suffix_name 
                FROM barangayOfficials_data WHERE official_position = ?
                """,
                ("Secretary",))
            secretary_info = cursor.fetchone()

            if secretary_info is None:
                return 0

            last_name, middle_name, first_name, suffix_name = secretary_info
            if suffix_name == "":
                full_name = f"{first_name} {middle_name[0]}. {last_name}"
                secretary_name = full_name
            else:
                full_name = f"{first_name} {middle_name[0]}. {last_name} {suffix_name}"
                secretary_name = full_name

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return 0

    except Exception as e:
        print(f"Error getting barangay secretary: {e}")
        return 0

    return secretary_name


def get_barangay_treasurer():
    treasurer_name = ""

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT first_name, middle_name, last_name, suffix_name 
                FROM barangayOfficials_data WHERE official_position = ?
                """,
                ("Treasurer",))
            treasurer_info = cursor.fetchone()

            if treasurer_info is None:
                return 0

            last_name, middle_name, first_name, suffix_name = treasurer_info
            if suffix_name == "":
                full_name = f"{first_name} {middle_name[0]}. {last_name}"
                treasurer_name = full_name
            else:
                full_name = f"{first_name} {middle_name[0]}. {last_name} {suffix_name}"
                treasurer_name = full_name

            first_name, middle_name, last_name, suffix_name = treasurer_info
            full_name = f"{first_name} {middle_name[0]}. {last_name} {suffix_name}"
            treasurer_name = full_name

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return 0

    except Exception as e:
        print(f"Error getting barangay treasurer: {e}")
        return 0

    return treasurer_name


def get_official_fullName(position):
    official_name = ""

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT first_name, middle_name, last_name, suffix_name 
                FROM barangayOfficials_data WHERE official_position = ?
                """,
                (position,))
            official_info = cursor.fetchone()

            if official_info is None:
                return 0

            first_name, middle_name, last_name, suffix_name = official_info
            full_name = f"{first_name} {middle_name} {last_name} {suffix_name}"
            official_name = full_name

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return 0

    except Exception as e:
        print(f"Error getting barangay treasurer: {e}")
        return 0

    return official_name


def get_officials_count(official_position):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM barangayOfficials_data WHERE official_position = ?",
                           (official_position,))
            return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None


def get_officials():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM barangayOfficials_data ORDER BY officials_id ASC")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting barangay officials: {e}")
        return None


def check_officials_exists(first_name, middle_name, last_name, suffix_name):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM barangayOfficials_data 
                WHERE first_name = ? AND middle_name = ? AND last_name = ? AND suffix_name = ?
                """,
                (first_name, middle_name, last_name, suffix_name))
            row = cursor.fetchone()
            return row is not None
    except Exception as e:
        print(f"Error check_name_exists: {e}")
        return None


def check_name_exists(last_name, middle_name, first_name, suffix):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM residents_data WHERE lastname = ? AND middlename = ? AND firstname = ?",
                           (last_name, middle_name, first_name))
            row = cursor.fetchone()
            return row is not None
    except Exception as e:
        print(f"Error check_name_exists: {e}")
        return None


def get_residentsData(
        filter_selected_purok,
        filter_age_from,
        filter_age_to,
        filter_gender_male,
        filter_gender_female,
        filter_comelec_registered,
        filter_comelec_not_registered,
        filter_status_single,
        filter_status_married,
        filter_status_widowed,
        filter_status_separated,
        filter_blood_a_plus,
        filter_blood_a_minus,
        filter_blood_b_plus,
        filter_blood_b_minus,
        filter_blood_ab_plus,
        filter_blood_ab_minus,
        filter_blood_o_plus,
        filter_blood_o_minus,
        filter_blood_unknown,
        filter_educ_no_grade,
        filter_educ_early_education,
        filter_educ_elementary,
        filter_educ_elementary_grad,
        filter_educ_high_school,
        filter_educ_high_school_grad,
        filter_educ_college,
        filter_educ_college_grad,
        filter_educ_post_baccalaureate,
        filter_philsys_registered,
        filter_philsys_not_registered,
        filter_membership_pwd,
        filter_membership_senior,
        filter_membership_solo,
        filter_membership_four,
        filter_membership_fa,
        filter_membership_rsbsa,
        filter_status_active,
        filter_status_transferred,
        filter_status_deceased,
        filter_status_transient
):
    base_query = "SELECT * FROM residents_data WHERE 1=1"

    if filter_selected_purok:
        purok_str = "', '".join(filter_selected_purok)
        base_query += f" AND purok IN ('{purok_str}')"

    base_query += f" AND age BETWEEN {filter_age_from} AND {filter_age_to}"

    gender_filters = []
    if filter_gender_male:
        gender_filters.append("sex = 'MALE'")
    if filter_gender_female:
        gender_filters.append("sex = 'FEMALE'")

    if gender_filters:
        base_query += " AND (" + " OR ".join(gender_filters) + ")"

    comelec_filters = []
    if filter_comelec_registered:
        comelec_filters.append("comelec = 'Registered'")
    if filter_comelec_not_registered:
        comelec_filters.append("comelec = 'Not Registered'")

    if comelec_filters:
        base_query += " AND (" + " OR ".join(comelec_filters) + ")"

    status_filters = []
    if filter_status_single:
        status_filters.append("civil_status = 'Single'")
    if filter_status_married:
        status_filters.append("civil_status = 'Married'")
    if filter_status_widowed:
        status_filters.append("civil_status = 'Widowed'")
    if filter_status_separated:
        status_filters.append("civil_status = 'Separated'")
    if status_filters:
        base_query += " AND (" + " OR ".join(status_filters) + ")"

    blood_filter = []
    if filter_blood_a_plus:
        blood_filter.append("blood_type = 'A+'")
    if filter_blood_a_minus:
        blood_filter.append("blood_type = 'A-'")
    if filter_blood_b_plus:
        blood_filter.append("blood_type = 'B+'")
    if filter_blood_b_minus:
        blood_filter.append("blood_type = 'B-'")
    if filter_blood_ab_plus:
        blood_filter.append("blood_type = 'AB+'")
    if filter_blood_ab_minus:
        blood_filter.append("blood_type = 'AB-'")
    if filter_blood_o_plus:
        blood_filter.append("blood_type = 'O+'")
    if filter_blood_o_minus:
        blood_filter.append("blood_type = 'O-'")
    if filter_blood_unknown:
        blood_filter.append("blood_type = 'Unknown'")
    if blood_filter:
        base_query += " AND (" + " OR ".join(blood_filter) + ")"

    education_filters = []
    if filter_educ_no_grade:
        education_filters.append("educational_status = 'No Grade Reported'")
    if filter_educ_early_education:
        education_filters.append("educational_status = 'Early Childhood Education'")
    if filter_educ_elementary:
        education_filters.append("educational_status = 'Elementary Level'")
    if filter_educ_elementary_grad:
        education_filters.append("educational_status = 'Elementary Graduate'")
    if filter_educ_high_school:
        education_filters.append("educational_status = 'High School Level'")
    if filter_educ_high_school_grad:
        education_filters.append("educational_status = 'High School Graduate'")
    if filter_educ_college:
        education_filters.append("educational_status = 'College Level'")
    if filter_educ_college_grad:
        education_filters.append("educational_status = 'College Graduate'")
    if filter_educ_post_baccalaureate:
        education_filters.append("educational_status = 'Post Baccalaureate'")
    if education_filters:
        base_query += " AND (" + " OR ".join(education_filters) + ")"

    philsys_filters = []
    if filter_philsys_registered:
        philsys_filters.append("philsys = 'Registered'")
    if filter_philsys_not_registered:
        philsys_filters.append("philsys = 'Not Registered'")

    if filter_membership_pwd:
        base_query += f" AND pwd_member = 'YES'"
    if filter_membership_senior:
        base_query += f" AND senior_member = 'YES'"
    if filter_membership_solo:
        base_query += f" AND solo_parent_member = 'YES'"
    if filter_membership_four:
        base_query += f" AND four_ps = 'YES'"
    if filter_membership_fa:
        base_query += f" AND farmers_membership_FA = 'YES'"
    if filter_membership_rsbsa:
        base_query += f" AND farmers_membership_RSBSA = 'YES'"

    residential_status_filters = []
    if filter_status_active:
        residential_status_filters.append("resident_status = 'Active'")
    if filter_status_transferred:
        residential_status_filters.append("resident_status = 'Transferred'")
    if filter_status_deceased:
        residential_status_filters.append("resident_status = 'Deceased'")
    if filter_status_transient:
        residential_status_filters.append("resident_status = 'Transient'")
    if residential_status_filters:
        base_query += " AND (" + " OR ".join(residential_status_filters) + ")"

    if philsys_filters:
        base_query += " AND (" + " OR ".join(philsys_filters) + ")"

    base_query += " ORDER BY lastname ASC"
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(base_query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching resident data: {e}")
        return None


def get_blotterData():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM blotter_data ORDER BY blotter_case_no ASC')
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching blotter data: {e}")
        return None


def get_residents(data_filter, data_order):
    try:
        with get_db_connection() as conn:  # Ensure get_db_connection() is defined
            cursor = conn.cursor()
            if data_filter == 'all' and data_order == 'default':
                cursor.execute('SELECT * FROM residents_data')
            elif data_filter != 'all' and data_order == 'default':
                if data_filter == 'comelec':
                    cursor.execute('SELECT * FROM residents_data WHERE Comelec = ?', ('Registered',))
                elif data_filter == 'philsys':
                    cursor.execute('SELECT * FROM residents_data WHERE Philsys = ?', ('Registered',))
                elif data_filter == 'all':
                    cursor.execute('SELECT * FROM residents_data')
                elif data_filter == 'pwd member':
                    cursor.execute('SELECT * FROM  residents_data WHERE pwd_member = ?', ('YES',))
                elif data_filter == 'senior member':
                    cursor.execute('SELECT * FROM residents_data WHERE senior_member = ?', ('YES',))
                elif data_filter == 'solo parent member':
                    cursor.execute('SELECT * FROM residents_data WHERE solo_parent_member = ?', ('YES',))
                elif data_filter == '4ps member':
                    cursor.execute('SELECT * FROM residents_data WHERE four_ps = ?', ('YES',))
                elif data_filter == 'farmer membership':
                    cursor.execute("""
                    SELECT * FROM residents_data WHERE farmers_membership_FA = ? OR farmers_membership_RSBSA = ?
                    """, ('YES', 'YES'))
                else:
                    raise ValueError("Invalid data_filter provided")  # Raises an exception for invalid filters
            elif data_filter == 'all' and data_order != 'default':
                if data_order == 'ascending':
                    cursor.execute('SELECT * FROM residents_data ORDER BY lastname ASC')
                elif data_order == 'descending':
                    cursor.execute('SELECT * FROM residents_data ORDER BY lastname DESC')
                else:
                    raise ValueError("Invalid data_filter provided")
            elif data_filter != 'all' and data_order != 'default':
                query_order = ""
                if data_order == 'ascending':
                    query_order = "ASC"
                elif data_order == 'descending':
                    query_order = "DESC"

                if data_filter == 'comelec':
                    cursor.execute('SELECT * FROM residents_data WHERE Comelec = ? ORDER BY lastname ' + query_order,
                                   ('Registered',))
                elif data_filter == 'philsys':
                    cursor.execute('SELECT * FROM residents_data WHERE Philsys = ? ORDER BY lastname ' + query_order,
                                   ('Registered',))
                elif data_filter == 'all':
                    cursor.execute('SELECT * FROM residents_data ORDER BY lastname ' + query_order)
                elif data_filter == 'pwd member':
                    cursor.execute("""
                    SELECT * FROM  residents_data WHERE pwd_member = ? ORDER BY lastname
                    """ + query_order, ('YES',))
                elif data_filter == 'senior member':
                    cursor.execute("""
                    SELECT * FROM residents_data WHERE senior_member = ? ORDER BY lastname
                    """ + query_order, ('YES',))
                elif data_filter == 'solo parent member':
                    cursor.execute("""
                    SELECT * FROM residents_data WHERE solo_parent_member = ? ORDER BY lastname 
                    """ + query_order, ('YES',))
                elif data_filter == '4ps member':
                    cursor.execute('SELECT * FROM residents_data WHERE four_ps = ? ORDER BY lastname ' + query_order,
                                   ('YES',))
                elif data_filter == 'farmer membership':
                    cursor.execute("""
                    SELECT * FROM residents_data 
                    WHERE farmers_membership_FA = ? OR farmers_membership_RSBSA = ? ORDER BY lastname 
                    """ + query_order,
                                   ('YES', 'YES'))
                else:
                    raise ValueError("Invalid data_filter provided")

            return cursor.fetchall()
    except sqlite3.Error as db_error:
        print(f"Database error fetching data: {db_error}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"Error fetching data: {e}")
    return None


def insert_data(resident_data):
    purok = resident_data[1]
    lastname = resident_data[2]
    middlename = resident_data[4]
    firstname = resident_data[3]
    suffix = resident_data[5]
    age = int(resident_data[6])
    sex = resident_data[7]
    civil_status = resident_data[8]
    blood_type = resident_data[9]
    dob = resident_data[10]
    pob = resident_data[11]
    occupation = resident_data[12]
    religion = resident_data[13]
    tribe_and_ethnicity = resident_data[14]
    educational_status = resident_data[15]
    comelec = resident_data[16]
    philsys = resident_data[17]
    pwd_member = resident_data[18]
    pwd_disability = resident_data[19]
    senior_member = resident_data[20]
    solo_parent_member = resident_data[21]
    kasambahay_salary = resident_data[22]
    four_ps = resident_data[23]
    salt_used = resident_data[24]
    garbage_disposal = resident_data[25]
    animals = resident_data[26]
    farmers_membership_FA = resident_data[27]
    farmers_membership_RSBSA = resident_data[28]
    source_of_water = resident_data[29]
    family_planning_used = resident_data[30]
    types_of_cr = resident_data[31]
    resident_status= resident_data[32]

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO residents_data(purok, lastname, middlename, firstname, suffix, age, sex, civil_status,
                blood_type, dob, place_of_birth, occupation, religion, tribe_and_ethnicity, educational_status, 
                comelec, philsys, pwd_member, pwd_disability, senior_member, solo_parent_member, kasambahay_salary,
                four_ps, salt_used, garbage_disposal, animals, farmers_membership_FA, farmers_membership_RSBSA, 
                source_of_water, family_planning_used, types_of_cr, resident_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (purok, lastname, middlename, firstname, suffix, int(age), sex, civil_status, blood_type, dob, pob,
                  occupation, religion, tribe_and_ethnicity, educational_status, comelec, philsys, pwd_member, pwd_disability,
                  senior_member, solo_parent_member, kasambahay_salary, four_ps, salt_used, garbage_disposal, animals,
                  farmers_membership_FA, farmers_membership_RSBSA, source_of_water, family_planning_used, types_of_cr, resident_status))
            conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")


def save_blotter_record(date_filed, case_no, reason, note):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO blotter_data(blotter_date_filed, blotter_case_no, blotter_reason, blotter_note) VALUES (?, ?, ?, ?)
            """, (date_filed, case_no, reason, note))
            conn.commit()
    except sqlite3.Error as db_error:
        print(f"Database error fetching data: {db_error}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    

def save_blotter_respondents(case_no, first_name, middle_name, last_name, suffix):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO blotter_respondents(blotter_case_no, first_name, middle_name, last_name, suffix) 
                           VALUES (?, ?, ?, ?, ?)
            """, (case_no, first_name, middle_name, last_name, suffix))
            conn.commit()
    except sqlite3.Error as db_error:
        print(f"Database error fetching data: {db_error}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    

def save_blotter_complainants(case_no, first_name, middle_name, last_name, suffix):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO blotter_complainants(blotter_case_no, first_name, middle_name, last_name, suffix) 
                           VALUES (?, ?, ?, ?, ?)
            """, (case_no, first_name, middle_name, last_name, suffix))
            conn.commit()
    except sqlite3.Error as db_error:
        print(f"Database error fetching data: {db_error}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def get_respondents_names(case_no):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM blotter_respondents
            WHERE blotter_case_no = ?
            """, (case_no,))
            return cursor.fetchall()
    except sqlite3.Error as db_error:
        print(f"Database error fetching data: {db_error}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def get_complainants_names(case_no):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM blotter_complainants
            WHERE blotter_case_no = ?
            """, (case_no,))
            return cursor.fetchall()
    except sqlite3.Error as db_error:
        print(f"Database error fetching data: {db_error}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def insert_official(first_name, middlename, last_name, suffix_name, position):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO barangayOfficials_data(first_name, middle_name, last_name, suffix_name, official_position) 
            VALUES (?, ?, ?, ?, ?)
            """,
                           (first_name, middlename, last_name, suffix_name, position))
            conn.commit()
            return cursor.fetchall()[0]
    except sqlite3.Error as db_error:
        print(f"Database error fetching data: {db_error}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except Exception as e:
        return None


def delete_official(official_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM barangayOfficials_data WHERE officials_id = ?", (official_id,))
            conn.commit()
            return True
    except sqlite3.Error as db_error:
        print(f"Database error deleting data: {db_error}")
        return False
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return False
    except Exception as e:
        print(f"Error deleting data: {e}")
        return False


def get_record_note(blotter_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT blotter_note FROM blotter_data WHERE blotter_id = ?", (blotter_id,))
            value = cursor.fetchone()
            if value:
                return value[0]
            else:
                return None
    except sqlite3.Error as db_error:
        print(f"Database error fetching data: {db_error}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def check_officials_count(official_type):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM barangayOfficials_data WHERE official_position = ?",
                           (official_type,))
            count = cursor.fetchone()[0]

            if official_type == 'Punong Barangay':
                if int(count) == 0:
                    return False
                else:
                    return True

            if official_type.capitalize() == 'Kagawad':
                if int(count) <= 6:
                    return False
                else:
                    return True

            if official_type.capitalize() == 'Secretary':
                if int(count) == 0:
                    return False
                else:
                    return True

            if official_type.capitalize() == 'Treasurer':
                if int(count) == 0:
                    return False
                else:
                    return True

            if official_type == 'SK Chairman':
                if int(count) == 0:
                    return False
                else:
                    return True

            if official_type == 'Pangkat Chairman':
                if int(count) == 0:
                    return False
                else:
                    return True

            if official_type.capitalize() == 'Lupon':
                if int(count) <= 9:
                    return False
                else:
                    return True

    except sqlite3.Error as db_error:
        return False
    except Exception as e:
        return False


def update_official(official_id, first_name, middlename, last_name, suffix_name, position):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE barangayOfficials_data SET
                first_name = ?,
                middle_name = ?,
                last_name = ?,
                suffix_name = ?,
                official_position = ?
                WHERE officials_id = ?
            """, (first_name,
                  middlename,
                  last_name,
                  suffix_name,
                  position,
                  official_id
                  )
                           )
            conn.commit()
    except Exception as e:
        print(f"Error updating data: {e}")


def count_residents():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM residents_data WHERE resident_status = 'Active'")
            result = cursor.fetchone()[0]
            return int(result) if result is not None else 0
    except sqlite3.Error as db_error:
        print(f"Database error fetching data: {db_error}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def count_gender():
    gender_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM residents_data WHERE sex = 'MALE' AND resident_status = 'Active'")
            result = cursor.fetchone()[0]
            gender_count.append(result) if result is not None else gender_count.append(0)

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM residents_data WHERE sex = 'FEMALE' AND resident_status = 'Active'")
            result = cursor.fetchone()[0]
            gender_count.append(result) if result is not None else gender_count.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return gender_count


def count_purok():
    purok_list = [
        "Vanda", "Walingwaling", "Bougainvillea", "Mercury", "Daisy",
        "Orchid", "Chrysanthenum", "Santan", "Rosas", "Sampaguita"
    ]
    purok_inhabitants = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for purok in purok_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE purok = ? AND resident_status = 'Active'", (purok,))
                result = cursor.fetchone()[0]
                purok_inhabitants.append(result) if result is not None else purok_inhabitants.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return purok_inhabitants


def count_age():
    age_list = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM residents_data WHERE age > 59 AND resident_status = 'Active'")
            result = cursor.fetchone()[0]
            age_list.append(result) if result is not None else age_list.append(0)

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM residents_data WHERE age > 18 and age < 60 AND resident_status = 'Active'")
            result = cursor.fetchone()[0]
            age_list.append(result) if result is not None else age_list.append(0)

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM residents_data WHERE age < 18 and age > 0 AND resident_status = 'Active'")
            result = cursor.fetchone()[0]
            age_list.append(result) if result is not None else age_list.append(0)

            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM residents_data WHERE age = 0 AND resident_status = 'Active'")
            result = cursor.fetchone()[0]
            age_list.append(result) if result is not None else age_list.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return age_list


def count_educational_attainment():
    education_list = [
        "Post Baccalaureate",
        "College Graduate",
        "College Level",
        "High School Graduate",
        "High School Level",
        "Elementary Graduate",
        "Elementary Level",
        "Early Childhood Education",
        "No Grade Reported",
    ]
    education_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for level in education_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE educational_status = ? AND resident_status = 'Active'", (level,))
                result = cursor.fetchone()[0]
                education_count.append(result) if result is not None else education_count.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return education_count


def count_comelec():
    comelect_list = [
        "Registered",
        "Not Registered"
    ]
    comelec_count = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for status in comelect_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE comelec = ? AND resident_status = 'Active'", (status,))
                result = cursor.fetchone()[0]
                comelec_count.append(result) if result is not None else comelec_count.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return comelec_count


def count_philsys():
    philsys_list = [
        "Registered",
        "Not Registered"
    ]
    philsys_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for status in philsys_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE philsys = ? AND resident_status = 'Active'", (status,))
                result = cursor.fetchone()[0]
                philsys_count.append(result) if result is not None else philsys_count.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return philsys_count


def count_pwd():
    pwd_list = [
        'YES', 'NO'
    ]
    pwd_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for status in pwd_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE pwd_member = ? AND resident_status = 'Active'", (status,))
                result = cursor.fetchone()[0]
                pwd_count.append(result) if result is not None else pwd_count.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return pwd_count


def count_senior():
    senior_list = [
        'YES', 'NO'
    ]
    senior_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for status in senior_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE senior_member = ? AND resident_status = 'Active'", (status,))
                result = cursor.fetchone()[0]
                senior_count.append(result) if result is not None else senior_count.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return senior_count


def count_solo_parent():
    solo_parent_list = [
        'YES', 'NO'
    ]
    solo_parent_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for status in solo_parent_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE solo_parent_member = ? AND resident_status = 'Active'", (status,))
                result = cursor.fetchone()[0]
                solo_parent_count.append(result) if result is not None else solo_parent_count.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return solo_parent_count


def count_4Ps():
    _4Ps_list = [
        'YES', 'NO'
    ]
    _4Ps_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for status in _4Ps_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE four_ps = ? AND resident_status = 'Active'", (status,))
                result = cursor.fetchone()[0]
                _4Ps_count.append(result) if result is not None else _4Ps_count.append(0)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return _4Ps_count


def count_farmers_membership():
    farmer_membership_list = [
        'YES', 'NO'
    ]
    farmer_membership_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for status in farmer_membership_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE farmers_membership_FA = ? AND resident_status = 'Active'", (status,))
                result = cursor.fetchone()[0]
                farmer_membership_count.append(result) if result is not None else farmer_membership_count.append(0)
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE farmers_membership_RSBSA = ? AND resident_status = 'Active'", (status,))
                result = cursor.fetchone()[0]
                farmer_membership_count.append(result) if result is not None else farmer_membership_count.append(0)
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return farmer_membership_count


def count_non_farmers():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM residents_data WHERE farmers_membership_FA = 'NO' AND farmers_membership_RSBSA = 'NO' AND resident_status = 'Active'")
            result = cursor.fetchone()[0]
            return int(result) if result is not None else 0
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None


def count_farmers_membership_FA():
    farmers_membership_FA_list = [
        'YES', 'NO'
    ]
    farmers_membership_FA_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for status in farmers_membership_FA_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE farmers_membership_FA = ? AND resident_status = 'Active'", (status,))
                farmers_membership_FA_count.append(cursor.fetchone()[0])

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return farmers_membership_FA_count


def count_farmers_membership_RSBSA():
    farmers_membership_RSBSA_list = [
        'YES', 'NO'
    ]
    farmers_membership_RSBSA_count = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for status in farmers_membership_RSBSA_list:
                cursor.execute("SELECT COUNT(*) FROM residents_data WHERE farmers_membership_RSBSA = ? AND resident_status = 'Active'", (status,))
                farmers_membership_RSBSA_count.append(cursor.fetchone()[0])

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return farmers_membership_RSBSA_count


def get_user_password(username, password):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return result
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting user password: {e}")
        return None


def get_user_info(username):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting user password: {e}")
        return None


def log_login(username, user_role, log_date):
    user_activity_done = "LOGGED IN"
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO user_activity(activity_username, activity_user_role, activity_date, activity_action)
            VALUES (?, ?, ?, ?)
            """, (username, user_role, log_date, user_activity_done))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def log_logout(username, user_role, log_date, logout_type):
    user_activity_done = ""
    if logout_type.upper() == 'NORMAL':
        user_activity_done = "LOGGED OUT"
    if logout_type.upper() == 'ATYPICAL':
        user_activity_done = "EXIT WITHOUT LOGOUT"

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO user_activity(activity_username, activity_user_role, activity_date, activity_action)
            VALUES (?, ?, ?, ?)
            """, (username, user_role, log_date, user_activity_done))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def log_user_activity(username, user_role, log_date, user_activity_done):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO user_activity(activity_username, activity_user_role, activity_date, activity_action)
            VALUES (?, ?, ?, ?)
            """, (username, user_role, log_date, user_activity_done))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_user_logs():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_activity ORDER BY activity_id DESC')
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def log_generate_residents_doc(username, doc_type, date, requestee):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO residents_activity(activity_username, activity_doc_type, activity_date, activity_requestee)
            VALUES (?, ?, ?, ?)
            """, (username, doc_type, date, requestee))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_residents_log():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM residents_activity ORDER BY activity_id DESC')
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_blotter_log():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM blotter_log ORDER BY log_id DESC')
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_resident_data(resident_id):
    resident_info = []
    columns = ["resident_id", "purok", "lastname", "firstname", "middlename", "suffix", "age", "sex", "civil_status", "blood_type", "dob", "place_of_birth", "occupation", "religion", "tribe_and_ethnicity", "educational_status", "comelec", "philsys", "pwd_member", "pwd_disability", "senior_member", "solo_parent_member", "kasambahay_salary", "four_ps", "salt_used", "garbage_disposal", "animals", "farmers_membership_FA", "farmers_membership_RSBSA", "source_of_water", "family_planning_used", "types_of_cr", "resident_status"]

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for item in columns:  
                cursor.execute(f"SELECT {item} FROM residents_data WHERE resident_id = ?", (resident_id,))
                resident_info.append(str(cursor.fetchone()[0]))
            return resident_info 
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def log_backup(log_date, filename, username):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO backup_log(backup_date, backup_filename, backup_username)
            VALUES (?, ?, ?)
            """, (log_date, filename, username))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_backup_log():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM backup_log ORDER BY backup_id DESC')
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def log_profiling(log_date, action, resident, changes, username):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO profiling_log(log_date, log_activity, log_residents, log_changes, log_username)
            VALUES (?, ?, ?, ?, ?)
            """, (log_date, action, resident, changes, username))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_profiling_log():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM profiling_log ORDER BY log_id DESC')
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def add_complainants_address(id, purok_name, barangay_name, city_name, province_name):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO blotter_complainants_address(blotter_case_no, purok_name, barangay_name, city_name, province_name)
            VALUES (?, ?, ?, ?, ?)
            """, (id, purok_name, barangay_name, city_name, province_name))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def add_respondents_address(id, purok_name, barangay_name, city_name, province_name):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO blotter_respondents_address(blotter_case_no, purok_name, barangay_name, city_name, province_name)
            VALUES (?, ?, ?, ?, ?)
            """, (id, purok_name, barangay_name, city_name, province_name))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def log_blotter(log_date, case_no, action, username):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO blotter_log(date_time, blotter_case_no, action, username)
            VALUES (?, ?, ?, ?)
            """, (log_date, case_no, action, username))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_complainants_address(case_no):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM blotter_complainants_address WHERE blotter_case_no = ?', (case_no,))
            return cursor.fetchall()[0]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_respondents_address(case_no):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM blotter_respondents_address WHERE blotter_case_no = ?', (case_no,))
            return cursor.fetchall()[0]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_resident_name(firstname, middlename, lastname, suffix):
    fullname = f"{firstname} {middlename[0]}. {lastname}"
    if not suffix == "":
        fullname += f" {suffix}"
    return fullname


def get_form_5_in_charge():
    in_charge_list = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM barangayOfficials_data WHERE official_position = ? OR official_position = ?',
                           ("Lupon", "Punong Barangay",))
            result = cursor.fetchall()
            for item in result:
                in_charge_list.append(
                    get_resident_name(
                        item[1],
                        item[2],
                        item[3],
                        item[4]
                    )
                )
            return in_charge_list
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_form_9_data():
    in_charge_list = []
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM barangayOfficials_data WHERE official_position = ?',
                           ("Lupon",))
            result = cursor.fetchall()
            for item in result:
                in_charge_list.append(
                    get_resident_name(
                        item[1],
                        item[2],
                        item[3],
                        item[4]
                    )
                )
            return in_charge_list
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def verify_residential_status(resident_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT resident_status FROM residents_data WHERE resident_id = ?',
                           (resident_id,))
            result = cursor.fetchone()[0]
            return result
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_generated_documents(blotter_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT date_time, action FROM blotter_log WHERE blotter_case_no = ?', (blotter_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_respondents_list():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT resident_id, purok, lastname, firstname, middlename, suffix FROM residents_data WHERE resident_status = 'Active'")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def count_officials():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM barangayOfficials_data")
            if int(cursor.fetchone()[0]) == 21:
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None
    

def get_user_accounts():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY id ASC")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting user accounts: {e}")
        return None
    
def do_reset_user_password(password, values):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password =? WHERE id =?", (password, values[0]))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    except Exception as e:
        print(f"Error resetting user password: {e}")
        return False


def do_remove_user(values):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (values[0],))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    except Exception as e:
        print(f"Error removing user: {e}")
        return False
    

def count_admin_users():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE user_role = 'admin_'")
            return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None


def add_new_user(role, desc, username, password):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_role, user_desc, username, password) VALUES (?, ?, ?, ?)", 
                           (role, desc, username, password))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    except Exception as e:
        print(f"Error adding new user: {e}")
        return False
    

def do_change_user_password(password, username):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password =? WHERE username =?", (password, username))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    except Exception as e:
        print(f"Error resetting user password: {e}")
        return False


def get_last_blotter_case():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT blotter_case_no FROM blotter_data ORDER BY blotter_case_no DESC LIMIT 1")
            result = cursor.fetchone()  # Fetch only one row
            return result[0] if result else None  # Check if result is not None
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting last blotter_case_no: {e}")
        return None


def count_comelec_gender():
    count_list = []
    gender_list = ['MALE', 'FEMALE']

    try:
        with get_db_connection() as conn:
            for gender in gender_list:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM residents_data WHERE comelec = 'Registered' AND sex = '{gender}' AND resident_status = 'Active'")
                count_list.append(cursor.fetchone()[0])
            for gender in gender_list:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM residents_data WHERE comelec = 'Not Registered' AND sex = '{gender}' AND resident_status = 'Active'")
                count_list.append(cursor.fetchone()[0])

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return count_list


def count_philsys_gender():
    count_list = []
    gender_list = ['MALE', 'FEMALE']

    try:
        with get_db_connection() as conn:
            for gender in gender_list:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM residents_data WHERE philsys = 'Registered' AND sex = '{gender}' AND resident_status = 'Active'")
                count_list.append(cursor.fetchone()[0])
            for gender in gender_list:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM residents_data WHERE philsys = 'Not Registered' AND sex = '{gender}' AND resident_status = 'Active'")
                count_list.append(cursor.fetchone()[0])

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return count_list


def count_pwd_gender():
    count_list = []
    gender_list = ['MALE', 'FEMALE']

    try:
        with get_db_connection() as conn:
            for gender in gender_list:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM residents_data WHERE pwd_member = 'YES' AND sex = '{gender}' AND resident_status = 'Active'")
                count_list.append(cursor.fetchone()[0])

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return count_list


def count_senior_gender():
    count_list = []
    gender_list = ['MALE', 'FEMALE']

    try:
        with get_db_connection() as conn:
            for gender in gender_list:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM residents_data WHERE senior_member = 'YES' AND sex = '{gender}' AND resident_status = 'Active'")
                count_list.append(cursor.fetchone()[0])

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return count_list


def count_solo_parent_gender():
    count_list = []
    gender_list = ['MALE', 'FEMALE']

    try:
        with get_db_connection() as conn:
            for gender in gender_list:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM residents_data WHERE solo_parent_member = 'YES' AND sex = '{gender}' AND resident_status = 'Active'")
                count_list.append(cursor.fetchone()[0])

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None

    return count_list


def get_latest_account():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE user_role = 'admin_' ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result is not None else None
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting user accounts: {e}")
        return None
    

def check_blotter_case_no(case_no):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM blotter_data WHERE blotter_case_no = ?", (case_no,))
            return cursor.fetchone()[0] == 1
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error getting officials count: {e}")
        return None