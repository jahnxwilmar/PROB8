import multiprocessing
from datetime import date, datetime
from sys import platform
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import pandas as pd
import shutil
import re
import schedule
import time
import threading
from PIL import Image, ImageTk
from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
from database import initialize_database
from documents import (do_requirements, do_certificateLowIncome, do_certificateOfGoodMoral, do_jobSeeker,
                       do_barangayClearance, do_barangayResidency, check_document_exist, do_form_1, do_form_2,
                       do_form_3, do_form_4, do_form_5, do_form_6, do_form_7, do_form_8, do_form_9, do_form_10,
                       do_form_11, do_form_12, do_form_13, generate_reports, do_barangay_officials_list,
                       do_certificateLowIncome_on_duty, do_barangayClearance_on_duty, do_barangayResidency_on_duty)
from models import (get_residentsData, update_birthdays, check_name_exists, insert_data, update_data,
                    check_officials_count, get_barangay_captain, get_barangay_kagawad, get_barangay_secretary,
                    get_barangay_treasurer, get_barangay_pangkat_member, get_latest_account,
                    get_barangay_sk, get_officials, get_officials_count, check_officials_exists, insert_official,
                    update_official, count_gender, count_purok, count_age, count_educational_attainment, count_comelec,
                    count_philsys, count_pwd, count_senior, count_solo_parent, count_4Ps, count_farmers_membership,
                    count_residents, save_blotter_record, get_blotterData, get_record_note, get_user_info, log_login,
                    log_logout, get_user_logs, log_generate_residents_doc, get_residents_log, get_resident_data, 
                    log_backup, get_backup_log, log_profiling, get_profiling_log, save_blotter_complainants, 
                    save_blotter_respondents, get_respondents_names, get_complainants_names, add_complainants_address,
                    add_respondents_address, get_complainants_address, get_respondents_address, log_blotter,
                    get_form_5_in_charge, get_form_9_data, get_blotter_log, verify_residential_status, 
                    get_generated_documents, get_respondents_list, count_non_farmers, count_officials, 
                    get_user_accounts, do_reset_user_password, log_user_activity, do_remove_user, count_admin_users,
                    add_new_user, do_change_user_password, get_last_blotter_case, count_comelec_gender,
                    count_philsys_gender, count_pwd_gender, count_senior_gender, count_solo_parent_gender, 
                    check_blotter_case_no)
from auth import verify_user, hash_password, verify_password
from pathlib import Path


# APP CONSTANTS
# Main Application
BARANGAY_NAME = "BARANGAY POBLACION 8"
MAIN_APP_NAME = "PROB8 - A COMPUTERIZED BLOTTER AND PROFILING SYSTEM"
APP_NAME = "PROB8"
# Content Frame Color
CONTENT_BG = 'gray100'
# General Use
BG_CONTENT = 'gray100'

SIDEBAR_BG= '#8fb996'

LABELFRAME_FONT = ('Bahnschrift SemiBold', 30, 'normal')
CURRENT_RECORD_FONT = ('Bahnschrift SemiBold', 20, 'normal')
CURRENT_RECORD_FONT_SELECTED = ('Bahnschrift SemiBold', 20, 'bold')
SEARCHBAR_FONT = ('Bahnschrift SemiBold', 24, 'normal')
CONTENT_FONT = ('Bahnschrift SemiBold', 16, 'normal')
FILTER_LABEL_FONT = ('Bahnschrift SemiBold', 20, 'normal')
TK_CONTENT_FONT = ('Bahnschrift SemiBold', 11, 'normal')
TK_DATE_CONTENT_FONT = ('Bahnschrift SemiBold', 12, 'normal')
DATE_ENTRY_FONT = ('Bahnschrift SemiBold', 12, 'normal')

# Active User
ACTIVE_USER_ID = ""
ACTIVE_USERNAME = ""
ACTIVE_USER_ROLE = ""
ACTIVE_USER_TYPE = ""
LOGGED_OUT = True


def resources_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def clear_active_user_info():
    global ACTIVE_USER_ROLE
    global ACTIVE_USERNAME
    global ACTIVE_USER_ID
    ACTIVE_USER_ROLE = ""
    ACTIVE_USERNAME = ""
    ACTIVE_USER_ID = ""


def set_logged_out_true():
    global LOGGED_OUT
    LOGGED_OUT = True


def set_logged_out_false():
    global LOGGED_OUT
    LOGGED_OUT = False


def generate_username(user_role, count):
    str_count = ""
    temp_count = count + 1
    if temp_count < 10:
        str_count = f"0{temp_count}"
    else:
        str_count = str(temp_count)

    return f"{user_role}{str_count}"


def get_formatted_datetime():
    now = datetime.now()
    formatted_datetime = now.strftime("%B %d, %Y - %A - %I:%M:%S %p")
    return formatted_datetime


def system_logout(logout_type):
    log_logout(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime(), logout_type)


def get_statistics_data():
    data = {}
    data.update(get_residents_count())
    residents_count = data["residents_count"]

    data.update(get_sex_count(residents_count))
    data.update(get_purok_count(residents_count))
    data.update(get_age_count(residents_count))
    data.update(get_educational_count(residents_count))
    data.update(get_comelec_count(residents_count))
    data.update(get_philsys_count(residents_count))
    data.update(get_pwd_count(residents_count))
    data.update(get_senior_count(residents_count))
    data.update(get_solo_parent_count(residents_count))
    data.update(get_4Ps_count(residents_count))
    data.update(get_farmers(residents_count))

    return data


def get_residents_count():
    residents_count = count_residents()
    return {
        "residents_count": residents_count
    }


def split_names(values):
    return values.split(',')


def concatenate_names(names_list):
    return ", ".join(map(str, names_list))


def get_sex_count(total_count):
    gender_count = count_gender()
    male_count = gender_count[0]
    female_count = gender_count[1]
    male_percentage = 0.00
    if male_count != 0:
        male_percentage = male_count / total_count * 100
    female_percentage = 0.00
    if female_count!= 0:
        female_percentage = female_count / total_count * 100
    return {
        "sex": [
            {
                "male":
                    {
                        "count": male_count,
                        "percentage": float("{:.2f}".format(male_percentage))
                    },
                "female":
                    {
                        "count": female_count,
                        "percentage": float("{:.2f}".format(female_percentage))
                    }
            }
        ]
    }


def get_purok_count(total_count):
    purok_list = [
        "Vanda", "Walingwaling", "Bougainvillea", "Mercury", "Daisy",
        "Orchid", "Chrysanthemum", "Santan", "Rosas", "Sampaguita"
    ]
    purok_inhabitants = count_purok()
    purok_data = {
        "purok": {}
    }

    for i in range(len(purok_list)):
        percent = 0.00
        if purok_inhabitants[i] != 0:
            percent = purok_inhabitants[i] / total_count * 100
        new_entry = {
            purok_list[i]: {
                "count": purok_inhabitants[i],
                "percentage": float("{:.2f}".format(percent))
            }
        }
        purok_data["purok"].update(new_entry)

    return purok_data


def get_age_count(total_count):
    age_list = ["Senior", "Legal", "Children", "New Born"]
    age_count = count_age()
    age_data = {
        "age": []
    }
    for i in range(len(age_count)):
        percent = 0.00
        if age_count[i] != 0:
            percent = age_count[i] / total_count * 100
        new_entry = {
            age_list[i]: {
                "count": age_count[i],
                "percentage": float("{:.2f}".format(percent))
            }
        }
        age_data["age"].append(new_entry)
    return age_data


def get_educational_count(total_count):
    educational_count = count_educational_attainment()
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
    education_data = {
        "education": []
    }
    for i in range(len(education_list)):
        percent = 0.00
        if educational_count[i] != 0:
            percent = educational_count[i] / total_count * 100
        new_entry = {
            education_list[i]: {
                "count": educational_count[i],
                "percentage": float("{:.2f}".format(percent))
            }
        }
        education_data["education"].append(new_entry)
    return education_data


def get_comelec_count(total_count):
    comelec_count = count_comelec()
    comelect_list = [
        "Registered",
        "Not Registered"
    ]
    comelec_data = {
        "comelec": []
    }
    for i in range(len(comelec_count)):
        percent = 0.00
        if comelec_count[i] != 0:
            percent = comelec_count[i] / total_count * 100
        new_entry = {
            comelect_list[i]: {
                "count": comelec_count[i],
                "percentage": float("{:.2f}".format(percent))
            }
        }
        comelec_data["comelec"].append(new_entry)
    return comelec_data


def get_philsys_count(total_count):
    philsys_count = count_philsys()
    philsys_list = [
        "Registered",
        "Not Registered"
    ]
    philsys_data = {
        "philsys": []
    }
    for i in range(len(philsys_count)):
        percent = 0.00
        if philsys_count[i] != 0:
            percent = philsys_count[i] / total_count * 100
        new_entry = {
            philsys_list[i]: {
                "count": philsys_count[i],
                "percentage": float("{:.2f}".format(percent))
            }
        }
        philsys_data["philsys"].append(new_entry)
    return philsys_data


def get_pwd_count(total_count):
    pwd_count = count_pwd()
    pwd_list = [
        'YES', 'NO'
    ]
    pwd_data = {
        "pwd": []
    }
    for i in range(len(pwd_count)):
        percent = 0.00
        if pwd_count[i] != 0:
            percent = pwd_count[i] / total_count * 100
        new_entry = {
            pwd_list[i]: {
                "count": pwd_count[i],
                "percentage": float("{:.2f}".format(percent))
            }
        }
        pwd_data["pwd"].append(new_entry)
    return pwd_data


def get_senior_count(total_count):
    senior_count = count_senior()
    senior_list = [
        'YES', 'NO'
    ]
    senior_data = {
        "senior": []
    }
    for i in range(len(senior_count)):
        percent = 0.00
        if senior_count[i] != 0:
            percent = senior_count[i] / total_count * 100
        new_entry = {
            senior_list[i]: {
                "count": senior_count[i],
                "percentage": float("{:.2f}".format(percent))
            }
        }
        senior_data["senior"].append(new_entry)
    return senior_data


def get_solo_parent_count(total_count):
    solo_parent_count = count_solo_parent()
    solo_parent_list = [
        'YES', 'NO'
    ]
    solo_parent_data = {
        "solo_parent": []
    }
    for i in range(len(solo_parent_count)):
        percent = 0.00
        if solo_parent_count[i] != 0:
            percent = solo_parent_count[i] / total_count * 100
        new_entry = {
            solo_parent_list[i]: {
                "count": solo_parent_count[i],
                "percentage": float("{:.2f}".format(percent))
            }
        }
        solo_parent_data["solo_parent"].append(new_entry)
    return solo_parent_data


def get_4Ps_count(total_count):
    _4Ps_count = count_4Ps()
    _4Ps_list = [
        'YES', 'NO'
    ]
    _4ps_data = {
        "4Ps": []
    }
    for i in range(len(_4Ps_count)):
        percent = 0.00
        if _4Ps_count[i] != 0:
            percent = _4Ps_count[i] / total_count * 100
        new_entry = {
            _4Ps_list[i]: {
                "count": _4Ps_count[i],
                "percentage": float("{:.2f}".format(percent))
            }
        }
        _4ps_data["4Ps"].append(new_entry)
    return _4ps_data


def get_farmers(total_count):
    farmers_count = count_farmers_membership()
    get_residents_count = count_residents()
    FA_count = farmers_count[0]
    RSBSA_count = farmers_count[1]
    NON_count = count_non_farmers()
    FA_percentage = 0.00
    if FA_count != 0:
        FA_percentage = FA_count / total_count * 100
    RSBSA_percentage = 0.00
    if RSBSA_count != 0:
        RSBSA_percentage = RSBSA_count / total_count * 100
    None_Member = 0.00
    if None_Member != 0:
        None_Member = NON_count / total_count * 100
    farmers_list = [
        'YES', 'NO'
    ]
    return {
        "farmers": [
            {
                "FA": {
                    "count": FA_count,
                    "percentage": float("{:.2f}".format(FA_percentage))
                }
            },
            {
                "RSBSA": {
                    "count": RSBSA_count,
                    "percentage": float("{:.2f}".format(RSBSA_percentage))
                }
            },
            {
                "NONE": {
                    "count": (NON_count),
                    "percentage": abs(float("{:.2f}".format(None_Member)))
                }
            }
        ]
    }


def check_barangayCaptain():
    temp_barangayCaptain = ""
    if not check_officials_count('Punong Barangay'):
        temp_barangayCaptain = "N/A"
    else:
        temp_barangayCaptain = get_barangay_captain('name')

    return temp_barangayCaptain


def check_barangayKagawad():
    temp_barangayKagawad = []
    if not check_officials_count('Kagawad'):
        temp_barangayKagawad = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
    else:
        temp_barangayKagawad = get_barangay_kagawad()
    return temp_barangayKagawad


def check_secretary():
    temp_barangaySecretary = ""
    if not check_officials_count('Secretary'):
        temp_barangaySecretary = "N/A"
    else:
        temp_barangaySecretary = get_barangay_secretary()
    return temp_barangaySecretary


def check_treasurer():
    temp_barangayTreasurer = ""
    if not check_officials_count('Treasurer'):
        temp_barangayTreasurer = "N/A"
    else:
        temp_barangayTreasurer = get_barangay_treasurer()
    return temp_barangayTreasurer


def check_pangkat():
    temp_pangkatMember = []
    if not check_officials_count('Lupon'):
        temp_pangkatMember = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
    else:
        temp_pangkatMember = get_barangay_pangkat_member()
    return temp_pangkatMember


def check_sk_chairman():
    temp_skChairman = ""
    if not check_officials_count('SK Chairman'):
        temp_skChairman = "N/A"
    else:
        temp_skChairman = get_barangay_sk()
    return temp_skChairman


def check_officials():
    if not check_officials_count('Punong Barangay'):
        messagebox.showwarning(
            'Officials Data Incomplete',
            'Please complete the Barangay Officials Data')
        return False
    if not check_officials_count('Kagawad'):
        messagebox.showwarning(
            'Officials Data Incomplete',
            'Please complete the Barangay Officials Data')
        return False
    if not check_officials_count('Secretary'):
        messagebox.showwarning(
            'Officials Data Incomplete',
            'Please complete the Barangay Officials Data')
        return False
    if not check_officials_count('Treasurer'):
        messagebox.showwarning(
            'Officials Data Incomplete',
            'Please complete the Barangay Officials Data')
        return False
    return True


def residentFullName(name_type, firstName, middleName, lastName, suffix):
    post_middleName = ""

    if name_type == "fullName":
        post_middleName = middleName
    if name_type == "name":
        post_middleName = f"{middleName[0]}."

    if suffix != "":
        return f"{firstName} {post_middleName} {lastName} {suffix}"
    else:
        return f"{firstName} {post_middleName} {lastName}"


def validate_birthDate(date_string):
    try:
        entered_date = datetime.strptime(date_string, "%d-%m-%Y").date()
        today = date.today()

        if entered_date > today:
            return False
        else:
            return True
    except ValueError:
        return False


def get_year_today():
    today = datetime.today()
    formatted_date = today.strftime('%Y')
    return formatted_date


def get_date_today():
    today = datetime.today()
    formatted_date = today.strftime('%d-%m-%Y')
    return formatted_date


def clean_sentence(sentence):
    if sentence.lower() == 'n/a':
        return sentence
    
    raw_sentence = sentence.split()
    cleaned_sentence = ' '.join(raw_sentence)
    return cleaned_sentence


def capitalize_sentence(sentence):
    if sentence.lower() == 'n/a':
        return sentence

    new_sentence = []
    pre_capitalized = sentence.split()
    for word in pre_capitalized:
        word = word.lower()
        temp_arr = []
        for letter in word:
            temp_arr.append(letter)
        temp_arr[0] = temp_arr[0].upper()
        new_sentence.append(''.join(temp_arr))
    return ' '.join(map(str, new_sentence))


def get_resident_fullname(firstname, middlename, lastname, suffix):
    fullname = f"{firstname} {middlename} {lastname}"
    if not suffix == "":
        fullname += f" {suffix}"
    return fullname


def get_resident_name(firstname, middlename, lastname, suffix):
    fullname = f"{firstname} {middlename[0]}. {lastname}"
    if not suffix == "":
        fullname += f" {suffix}"
    return fullname


def get_formal_resident_name(firstname, middlename, lastname, suffix):
    if not suffix == "":
        lastname += f" {suffix}"
    fullname = f"{lastname}, {middlename} {firstname}"
    return fullname


def format_number(number):
    if number >= 1000:
        return f"{number:,}"
    else:
        return str(number)


def is_valid_string(s):
    return bool(re.fullmatch(r'[0-9\-]+', s))


class Dashboard(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            fg_color='#FFF'
        )
        self.parent = parent
        self.active_page = None
        self.create_constants()
        self.create_widgets()
        self.create_layouts()
        self.combined_action(Homepage, "Home")

        self.schedule_backup()

    def create_constants(self):
        # Dashboard Buttons
        self.BTN_INACTIVE = '#8fb996'
        self.BTN_ACTIVE = '#415d43'
        self.TEXT_INACTIVE = '#000'
        self.TEXT_ACTIVE = '#FAFAFA'
        self.BTN_HOVER = '#709775'
        self.BTN_LOGOUT = '#9d0208'
        self.BTN_LOGOUT_HOVER = '#e5383b'
        self.BTN_WIDTH = 100
        self.BTN_HEIGHT = 40
        self.BTN_GREEN = "#656D4A"
        self.BTN_HOVER_GREEN = "#A4AC86"
        self.BTN_BACKUP = "#7f4f24"
        self.BTN_BACKUP_HOVER = "#936639"

        # Get dashboard image
        self.IMAGE_PATH = resources_path('assets/images/Poblacion8Seal.png')
        self.IMAGE_WIDTH = 100
        self.IMAGE_HEIGHT = 100
        self.dashboard_img = CTkImage(
            light_image=Image.open(self.IMAGE_PATH), size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        )

        self.FONT_AUTHENTICATION =  ('Bahnschrift SemiBold', 20, 'normal')

        self.ACCOUNT_CONTENT_BG = "#dad7cd"

    def create_widgets(self):
        # - Sidebar Container
        self.frame_sidebar_container = CTkFrame(self, fg_color=SIDEBAR_BG)
        # - Content Container
        self.frame_content_container = CTkFrame(self, fg_color=CONTENT_BG)
        # -- Sidebar Buttons
        self.img_poblacion_seal = CTkLabel(
            self.frame_sidebar_container,
            image=self.dashboard_img,
            text='',
        )
        self.btn_home = CTkButton(
            self.frame_sidebar_container,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action(Homepage, "Home"),
            text='HOME'
        )
        self.btn_residents = CTkButton(
            self.frame_sidebar_container,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action(ResidentsPage, "Residents"),
            text='RESIDENTS'
        )
        self.btn_blotter = CTkButton(
            self.frame_sidebar_container,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action(BlotterPage, "Blotter"),
            text='BLOTTER'
        )
        self.btn_officials = CTkButton(
            self.frame_sidebar_container,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action(OfficialsPage, "Officials"),
            text='OFFICIALS'
        )
        self.btn_about = CTkButton(
            self.frame_sidebar_container,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action(AboutPage, "About"),
            text='ABOUT'
        )

        account_btn_name = ""
        if ACTIVE_USER_TYPE == "sysadmin_":
            account_btn_name = "Accounts"
        else:
            account_btn_name = "My Account"
        self.btn_account = CTkButton(
            self.frame_sidebar_container,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=SIDEBAR_BG,
            text_color=self.TEXT_INACTIVE,
            hover_color=SIDEBAR_BG,
            command=lambda: self.user_authentication("Account"),
            # command=lambda: self.combined_action(LogsPage, "Logs"),
            text=account_btn_name
        )
        self.btn_logs = CTkButton(
            self.frame_sidebar_container,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=SIDEBAR_BG,
            text_color=self.TEXT_INACTIVE,
            hover_color=SIDEBAR_BG,
            # command=lambda: self.user_authentication("Logs"),
            command=lambda: self.combined_action(LogsPage, "Logs"),
            text='Logs'
        )
        self.btn_backup = CTkButton(
            self.frame_sidebar_container,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_BACKUP,
            text_color=self.TEXT_ACTIVE,
            hover_color=self.BTN_BACKUP_HOVER,
            command=lambda: self.user_authentication("Backup"),
            text='BACKUP'
        )
        self.btn_logout = CTkButton(
            self.frame_sidebar_container,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_LOGOUT,
            text_color=self.TEXT_ACTIVE,
            hover_color=self.BTN_LOGOUT_HOVER,
            command=self.on_logout,
            text='LOGOUT'
        )

    def create_layouts(self):
        self.frame_sidebar_container.pack(side='left', fill='y', padx=(5, 3), pady=5)
        self.frame_content_container.pack(side='left', fill='both', expand=True, padx=(2, 5), pady=5)
        self.img_poblacion_seal.pack(anchor='center', padx=15, pady=(40, 20))
        self.btn_home.pack(anchor='center', pady=10)
        self.btn_residents.pack(anchor='center', pady=10)
        self.btn_blotter.pack(anchor='center', pady=10)
        self.btn_officials.pack(anchor='center', pady=10)
        self.btn_about.pack(anchor='center', pady=10)
        self.btn_logout.pack(side='bottom', pady=10)
        if (ACTIVE_USER_TYPE == "sysadmin_" or ACTIVE_USER_TYPE == "admin_"):
            self.btn_backup.pack(side='bottom', pady=10)
            self.btn_logs.pack(side='bottom', pady=10)
            self.btn_account.pack(side='bottom', pady=10)

    def combined_action(self, page, btn):
        if self.active_page == btn:
            return
        
        self.active_page = btn
        for widget in self.frame_content_container.winfo_children():
            widget.destroy()
        self.set_active(btn)
        page(self.frame_content_container).pack(fill='both', expand=True)

    def user_authentication(self, btn):
        if self.active_page == btn:
            return
        
        if btn == 'Account' and ACTIVE_USER_TYPE == 'admin_':
            self.view_user_account()
            return

        self.authentication_window = CTkToplevel(self)
        self._center_screen(400, 200)
        self.authentication_window.title("User Authentication")
        self.authentication_window.transient(self)
        self.authentication_window.grab_set()
        self.authentication_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.authentication_window.iconbitmap(default=self.authentication_window.iconPath)
        if platform.startswith("win"):
            self.after(200, lambda: self.authentication_window.iconbitmap(self.authentication_window.iconPath))

        # CREATE WIDGETS
        label_authentication = CTkLabel(
            self.authentication_window,
            text="Enter current users password:",
            font=self.FONT_AUTHENTICATION,
        )
        entry_password = CTkEntry(
            self.authentication_window,
            show="•",
            font=self.FONT_AUTHENTICATION,
            width=200
        )
        btn_confirm_password = CTkButton(
            self.authentication_window,
            text="Confirm",
            font=self.FONT_AUTHENTICATION,
            command=lambda: self.verify_authentication(entry_password.get(), btn),
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
        )
        btn_cancel = CTkButton(
            self.authentication_window,
            text="Cancel",
            font=self.FONT_AUTHENTICATION,
            command=self.close_user_authentication_window,
            fg_color=self.BTN_LOGOUT,
            hover_color=self.BTN_LOGOUT_HOVER
        )

        # CREATE LAYOUT
        label_authentication.pack(pady=(20, 0))
        entry_password.pack(anchor='center')
        btn_confirm_password.pack(anchor='center', pady=10)
        btn_cancel.pack(anchor='center')

    def verify_authentication(self, password, btn):
        if not verify_user(ACTIVE_USERNAME, password):
            messagebox.showerror("Authentication Error", "Incorrect password!")
            return
        
        if btn == "Account":
            messagebox.showinfo("Success", "Password correct! You will be redirected.")
            self.combined_action(AccountManagementPage, "Account")
        if btn == "Logs":
            messagebox.showinfo("Success", "Password correct! You will be redirected.")
            self.combined_action(LogsPage, "Logs")
        if btn == "Backup":
            self.on_backup()

        self.close_user_authentication_window()

    def close_user_authentication_window(self):
        self.authentication_window.grab_release()
        self.authentication_window.destroy()

    def _center_screen(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        self.authentication_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))

    def set_active(self, btn):
        # Reset all buttons to inactive
        self.set_inactive()
        # Set clicked button to active state
        if btn == "Home":
            self.btn_home.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Residents":
            self.btn_residents.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Blotter":
            self.btn_blotter.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Officials":
            self.btn_officials.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "About":
            self.btn_about.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Logs":
            self.btn_logs.configure(
                fg_color='#FAFAFA',
                text_color='#000',
                hover_color='#FAFAFA',
            )
        if btn == "Accounts":
            self.btn_account.configure(
                fg_color='#FAFAFA',
                text_color='#000',
                hover_color='#FAFAFA',
            )

    # Set all buttons to inactive colors
    def set_inactive(self):
        self.btn_home.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_residents.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_blotter.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_officials.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_about.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_logs.configure(
            fg_color=SIDEBAR_BG,
            text_color=self.TEXT_INACTIVE,
            hover_color=SIDEBAR_BG,
        )
        self.btn_account.configure(
            fg_color=SIDEBAR_BG,
            text_color=self.TEXT_INACTIVE,
            hover_color=SIDEBAR_BG,
        )
        self.img_poblacion_seal.configure(
            fg_color=self.BTN_INACTIVE
        )

    def on_logout(self):
        if not messagebox.askokcancel("Confirm Logout", "Are you sure you want to logout?"):
            return
        self.logout()

    def logout(self):
        system_logout('NORMAL')
        clear_active_user_info()
        set_logged_out_true()
        self.parent.show_login()

    def schedule_backup(self):
        schedule.every().day.at("14:00").do(self.on_scheduled_backup)

        def run_schedule():
            while True:
                schedule.run_pending()
                time.sleep(1)  # Wait for a second before checking again

        # Start the scheduling thread
        backup_thread = threading.Thread(target=run_schedule)
        backup_thread.daemon = True  # Daemon thread stops when the main thread exits
        backup_thread.start()

    def on_scheduled_backup(self):
        db_path = resources_path("database/main/current_db.db")

        default_backup_dir = os.path.expanduser(f"~/Desktop/{APP_NAME}/Database Backup/Scheduled Backup")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"auto_backup_{timestamp}.db"

        max_backups = 1

        if not os.path.exists(default_backup_dir):
            os.makedirs(default_backup_dir)

        backup_path = os.path.join(default_backup_dir, backup_filename)

        try:
            shutil.copy2(db_path, backup_path)

            backup_files = sorted(
                [f for f in os.listdir(default_backup_dir) if f.startswith('auto_backup_')],
                key=lambda x: os.path.getmtime(os.path.join(default_backup_dir, x))
            )

            if len(backup_files) > max_backups:
                for old_backup in backup_files[:-max_backups]:
                    os.remove(os.path.join(default_backup_dir, old_backup))

            log_backup(get_formatted_datetime(), backup_filename, ACTIVE_USERNAME)

        except Exception as e:
            return

    def on_backup(self):
        db_path = resources_path("database/main/current_db.db")

        default_backup_dir = os.path.expanduser(f"~/Desktop/{APP_NAME}/Database Backup")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{timestamp}.db"

        prompt_val = messagebox.askyesnocancel(
            "Save Destination", 
            "Do you want to save the backup to the default location?\n\nYES - file will be saved on Default location\nNO - Choose your preferred location\nCANCEL - Cancel Backup"
        )

        backup_dir = ""

        if prompt_val is None:
            return
        
        if prompt_val is True:
            backup_dir = default_backup_dir

        if prompt_val is False:
            backup_dir = filedialog.askdirectory(
                title="Select Backup Directory"
            )

            if not backup_dir:
                messagebox.showwarning("Error", "Backup Cancelled.")
                return

        max_backups = 10

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        backup_path = os.path.join(backup_dir, backup_filename)

        try:
            shutil.copy2(db_path, backup_path)

            backup_files = sorted(
                [f for f in os.listdir(backup_dir) if f.startswith('backup_')],
                key=lambda x: os.path.getmtime(os.path.join(backup_dir, x))
            )

            if len(backup_files) > max_backups:
                for old_backup in backup_files[:-max_backups]:
                    os.remove(os.path.join(backup_dir, old_backup))

            log_backup(get_formatted_datetime(), backup_filename, ACTIVE_USERNAME)
            messagebox.showinfo("Backup successful", f"Database Backup saved as {backup_filename}")

        except Exception as e:
            messagebox.showerror("Backup Error", "An error occurred during the backup process.")

    def _center_account_screen(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        self.user_account_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))

    def view_user_account(self):
        self.user_account_window = CTkToplevel(self)
        self._center_account_screen(500, 370)
        self.user_account_window.title("My Account")
        self.user_account_window.transient(self)
        self.user_account_window.grab_set()
        self.user_account_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.user_account_window.iconbitmap(default=self.user_account_window.iconPath)
        if platform.startswith("win"):
            self.after(200, lambda: self.user_account_window.iconbitmap(self.user_account_window.iconPath))

        self.user_account_window.configure(
            fg_color=self.ACCOUNT_CONTENT_BG
        )

        # CREATE WIDGETS
        self.window_container = CTkFrame(
            self.user_account_window,
            fg_color=self.ACCOUNT_CONTENT_BG
        )
        self.label_user_account = CTkLabel(
            self.window_container,
            text="User Account Info",
            font=LABELFRAME_FONT,
        )
        self.label_user_desc = CTkLabel(
            self.window_container,
            text="User Description:    " + ACTIVE_USER_ROLE,
            font=CONTENT_FONT,
        )
        self.label_username = CTkLabel(
            self.window_container,
            text="Username:                " + ACTIVE_USERNAME,
            font=CONTENT_FONT,
        )

        self.label_change_password = CTkLabel(
            self.window_container,
            text="Change Password",
            font=LABELFRAME_FONT,
        )
        self.frame_old_password = CTkFrame(
            self.window_container,
            fg_color=self.ACCOUNT_CONTENT_BG
        )
        self.label_old_password = CTkLabel(
            self.frame_old_password,
            text="Enter current password:",
            font=CONTENT_FONT,
        )
        self.entry_old_password = CTkEntry(
            self.frame_old_password,
            show="•",
            font=CONTENT_FONT,
            width=200
        )
        self.frame_new_password = CTkFrame(
            self.window_container,
            fg_color=self.ACCOUNT_CONTENT_BG
        )
        self.label_new_password = CTkLabel(
            self.frame_new_password,
            text="Enter new password:",
            font=CONTENT_FONT,
        )
        self.entry_new_password = CTkEntry(
            self.frame_new_password,
            show="•",
            font=CONTENT_FONT,
            width=200
        )
        btn_confirm_password = CTkButton(
            self.window_container,
            text="Confirm",
            font=CONTENT_FONT,
            command=lambda: self.finalize_change_password(self.entry_old_password.get(), self.entry_new_password.get()),
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
        )

        # CREATE LAYOUT
        self.window_container.pack(anchor='nw', expand='true', fill='both')
        self.label_user_account.pack(anchor='nw', padx=(55, 0), pady=(30, 10))
        self.label_user_desc.pack(anchor='nw', padx=(90, 0), pady=(0, 5))
        self.label_username.pack(anchor='nw', padx=(90, 0))
        self.label_change_password.pack(anchor='nw', padx=(55, 0), pady=(30, 10))
        self.frame_old_password.pack(anchor='nw', padx=(60, 0), pady=(0, 5))
        self.frame_new_password.pack(anchor='nw', padx=(60, 0))
        self.label_old_password.pack(side='left', padx=(0, 5))
        self.entry_old_password.pack(side='left')
        self.label_new_password.pack(side='left', padx=(0, 28))
        self.entry_new_password.pack(side='left')
        btn_confirm_password.pack(anchor='center', pady=20)

    def finalize_change_password(self, old_password, new_password):
        if not old_password or not new_password:
            messagebox.showwarning("Error", "Fields cannot be empty!")
            return
        
        if not verify_user(ACTIVE_USERNAME, old_password):
            messagebox.showerror("Authentication Error", "Incorrect password!")
            return
        
        if verify_password(ACTIVE_USERNAME, old_password, new_password):
            messagebox.showwarning("Warning", "New password is the same as the old password!")
            return
        
        hashed_password = hash_password(new_password)

        if do_change_user_password(hashed_password, ACTIVE_USERNAME):
            messagebox.showinfo("Success", "Password changed successfully!")
            log_user_activity(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime(), f"PASSWORD CHANGED")

        self.user_account_window.grab_release()
        self.user_account_window.destroy()


class Homepage(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            fg_color=CONTENT_BG
        )
        self.constants()
        self.create_widgets()
        self.create_layout()

    def constants(self):
        self.IMAGE_PATH = resources_path('assets/images/Poblacion8Seal.png')
        self.IMAGE_NDMC_PATH = resources_path('assets/images/NDMCSeal.png')
        self.IMAGE_CITE_PATH = resources_path('assets/images/CITESeal.png')
        self.IMAGE_CES_PATH = resources_path('assets/images/NDMCCMS.png')
        self.IMAGE_TEKNOW_PATH = resources_path('assets/images/TeKnowLogo.png')
        self.IMAGE_WIDTH = 400
        self.IMAGE_HEIGHT = 400
        self.IMAGE_DESC_WIDTH = 40
        self.IMAGE_DESC_HEIGHT = 40
        self.temp_img_home = CTkImage(
            light_image=Image.open(self.IMAGE_PATH), size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        )
        self.temp_img_ndmc = CTkImage(
            light_image=Image.open(self.IMAGE_NDMC_PATH), size=(self.IMAGE_DESC_WIDTH, self.IMAGE_DESC_HEIGHT)
        )
        self.temp_img_cite = CTkImage(
            light_image=Image.open(self.IMAGE_CITE_PATH), size=(self.IMAGE_DESC_WIDTH, self.IMAGE_DESC_HEIGHT)
        )
        self.temp_img_ces = CTkImage(
            light_image=Image.open(self.IMAGE_CES_PATH), size=(self.IMAGE_DESC_WIDTH, self.IMAGE_DESC_HEIGHT)
        )
        self.temp_img_teknow = CTkImage(
            light_image=Image.open(self.IMAGE_TEKNOW_PATH), size=(60, 17)
        )

    def create_widgets(self):
        self.app_name = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )
        self.frame_app_name = CTkFrame(
            self.app_name,
            fg_color=CONTENT_BG,
        )
        self.label_app_name = CTkLabel(
            self.frame_app_name,
            text='PROB8',
            font=('', 50, 'bold')
        )
        self.label_app_desc = CTkLabel(
            self.frame_app_name,
            text='A COMPUTERIZED BLOTTER AND PROFILING SYSTEM',
            font=('', 20, 'bold')
        )
        self.frame_time_date = CTkFrame(
            self.app_name,
            fg_color=CONTENT_BG,
        )
        self.label_time = CTkLabel(
            self.frame_time_date,
            font=('', 60, 'bold')
        )
        self.label_date = CTkLabel(
            self.frame_time_date,
            font=('', 30, 'bold')
        )
        self.label_day = CTkLabel(
            self.frame_time_date,
            font=('', 25, 'bold')
        )
        self.update_time()
        self.update_date()

        self.img_home = CTkLabel(
            self,
            image=self.temp_img_home,
            text='',
        )
        self.small_desc = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )
        self.img_ndmc = CTkLabel(
            self.small_desc,
            image=self.temp_img_ndmc,
            text='',
        )
        self.img_cite = CTkLabel(
            self.small_desc,
            image=self.temp_img_cite,
            text='',
        )
        self.img_ces = CTkLabel(
            self.small_desc,
            image=self.temp_img_ces,
            text='',
        )
        self.img_teknow = CTkLabel(
            self.small_desc,
            image=self.temp_img_teknow,
            text='',
        )
        self.label_desc = CTkLabel(
            self.small_desc,
            text="SA BARYO: A COMMUNITY EXTENSION PROGRAM OF NDMC COLLEGE OF INFORMATION TECHNOLOGY AND ENGINEERING",
            font=('', 13, 'bold')
        )

    def create_layout(self):
        self.app_name.pack(anchor='n', fill='x')
        self.frame_app_name.pack(side='left', pady=(10, 0), padx=(40, 0))
        self.frame_time_date.pack(side='right', pady=(10, 0), padx=(0, 40))

        self.label_app_name.pack(anchor='w')
        self.label_app_desc.pack(anchor='w')

        self.label_time.pack(anchor='center')
        self.label_date.pack(anchor='center')
        self.label_day.pack(anchor='center')

        self.img_home.pack(anchor='center', expand='True', fill='both')

        self.small_desc.pack(anchor='n', fill='x', pady=20, padx=20)
        self.img_ndmc.pack(side='left')
        self.img_cite.pack(side='left', padx=(10, 0))
        self.img_ces.pack(side='left', padx=(10, 0))
        self.img_teknow.pack(side='left', padx=(15, 0))
        self.label_desc.pack(side='left', padx=(5, 0))

    def update_time(self):
        current_time = datetime.now().strftime('%I:%M:%S %p')
        self.label_time.configure(text=current_time)
        self.after(1000, self.update_time)

    def update_date(self):
        current_date = datetime.now().strftime('%B %d, %Y')
        self.label_date.configure(text=current_date)

        current_day = datetime.now().strftime('%A')
        self.label_day.configure(text=str(current_day).upper())

        self.after(1000, self.update_date)


class AccountManagementPage(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            fg_color=CONTENT_BG
        )
        self.constants()
        self.create_widgets()
        self.create_layout()

    def constants(self):
        self.PAGE_TITLE_FONT = ('Bahnschrift SemiBold', 30, 'normal')
        self.WINDOW_TITLE_FONT = ('Bahnschrift SemiBold', 24, 'normal')

        self.MODIFY_BTN_HEIGHT = 40
        self.MODIFY_BTN_WIDTH = 170

        self.TEXT_COLOR = '#FAFAFA'
        self.TREE_HEADING_COLOR = "#344e41"
        self.TREE_SELECTED_COLOR = "#344e41"
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", font=("Bahnschrift SemiBold", 12, "normal"), rowheight=30)
        self.tree_style.configure("Treeview.Heading", font=("Bahnschrift SemiBold", 16, "bold"),padding=(0, 5), foreground=self.TREE_HEADING_COLOR)
        self.tree_style.map("Treeview",
                            background=[("selected", self.TREE_SELECTED_COLOR)],
                            foreground=[("selected", self.TEXT_COLOR)]
                            )
        
        self.FONT_AUTHENTICATION =  ('Bahnschrift SemiBold', 20, 'normal')

        
        self.BTN_LOGOUT = '#9d0208'
        self.BTN_LOGOUT_HOVER = '#e5383b'
        self.BTN_GREEN = "#656D4A"
        self.BTN_HOVER_GREEN = "#A4AC86"
    
    def create_widgets(self):
        # Page Container
        self.page_container = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )

        # Page Label
        self.page_label = CTkLabel(
            self.page_container,
            text='Users Account Management',
            font=self.PAGE_TITLE_FONT,
            anchor='w'
        )

        # Buttons Container
        self.frame_btn_container = CTkFrame(
            self.page_container,
            fg_color=CONTENT_BG,
        )

        # Buttons
        self.btn_remove_user = CTkButton(
            self.frame_btn_container,
            text='Remove User',
            width=self.MODIFY_BTN_WIDTH,
            height=self.MODIFY_BTN_HEIGHT,
            font=CONTENT_FONT,
            fg_color="#621708",
            hover_color="#941b0c",
            command=self.remove_user,
        )
        self.btn_reset_user_password = CTkButton(
            self.frame_btn_container,
            text='Reset Password',
            width=self.MODIFY_BTN_WIDTH,
            height=self.MODIFY_BTN_HEIGHT,
            font=CONTENT_FONT,
            fg_color="#805b10",
            hover_color="#a47e1b",
            command=self.reset_password,
        )
        self.btn_add_user = CTkButton(
            self.frame_btn_container,
            text='Add User',
            width=self.MODIFY_BTN_WIDTH,
            height=self.MODIFY_BTN_HEIGHT,
            font=CONTENT_FONT,
            fg_color="#4f772d",
            hover_color="#90a955",
            command=self.add_user,
        )

        # Accounts TreeView Container
        self.frame_accounts_data_container = CTkFrame(
            self.page_container,
            fg_color="#FAFAFA",
        )

        # Accounts TreeView
        self.tree_user_accounts = ttk.Treeview(self.frame_accounts_data_container)
        self.tree_user_accounts.configure()
        self.tree_user_accounts["columns"] = (
            "ID", "Role", "Description", "Username", "Password"
        )
        self.tree_user_accounts.heading("#0", text="", anchor='w')
        self.tree_user_accounts.column("#0", width=0, stretch=NO)
        self.tree_user_accounts.heading("ID", text="", anchor='w')
        self.tree_user_accounts.column("ID", width=0, stretch=NO)
        for column in self.tree_user_accounts["columns"][1:-1]:
            self.tree_user_accounts.heading(column, text=column)
            self.tree_user_accounts.column(column, width=150, stretch=YES)
        self.tree_user_accounts.heading("Password", text="", anchor='w')
        self.tree_user_accounts.column("Password", width=0, stretch=NO)

        self.tree_user_accounts_scroll = ttk.Scrollbar(
            self.frame_accounts_data_container,
            orient=VERTICAL,
            command=self.tree_user_accounts.yview
        )
        self.tree_user_accounts.configure(
            yscrollcommand=self.tree_user_accounts_scroll.set
        )

        self.btn_change_password = CTkButton(
            self.page_container,
            text='  Change System Administrator Password  ',
            height=self.MODIFY_BTN_HEIGHT,
            font=CONTENT_FONT,
            fg_color="#495057",
            hover_color="#6c757d",
            command=self.change_admin_password,
        )

        self.populate_tree()
        
    def create_layout(self):
        self.page_container.pack(
            anchor='nw',
            expand='true',
            fill='both',
            pady=100,
            padx=40
        )
        self.page_label.pack(anchor='nw', fill='x')

        self.frame_btn_container.pack(anchor='nw', fill='x')

        self.btn_remove_user.pack(side='right')
        self.btn_reset_user_password.pack(side='right', padx=5)
        self.btn_add_user.pack(side='right')

        self.frame_accounts_data_container.pack(
            anchor='center',
            fill='both',
            expand='True',
            pady=30
        )

        self.tree_user_accounts.pack(
            anchor='nw', fill='both', expand='true'
        )

        self.btn_change_password.pack(anchor='nw')

    def add_user(self):
        temp_admin_count = 0
        last_admin_username = get_latest_account()

        if last_admin_username is not None:
            temp_list = last_admin_username.split("_")
            temp_admin_count = int(temp_list[1])

        temp_user_role = "admin_"
        temp_username = generate_username(temp_user_role, temp_admin_count)
        temp_raw_password = "123"
        temp_password = hash_password(temp_raw_password)

        self.add_user_window = CTkToplevel(self)
        window_width = 400
        window_height = 320
        x_axis, y_axis = self._center_add_screen(window_width, window_height)
        self.add_user_window.title('Add Record')
        self.add_user_window.resizable(False, False)
        self.add_user_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.after(200, lambda: self.add_user_window.iconbitmap(self.add_user_window.iconPath))
        self.add_user_window.geometry("{}x{}+{}+{}".format(
            window_width, window_height, x_axis, y_axis
        ))
        self.add_user_window.transient(self)
        self.add_user_window.grab_set()
        self.add_user_window.focus()

        # CREATE WIDGETS
        self.window_container = CTkFrame(
            self.add_user_window,
            fg_color=CONTENT_BG,
        )
        self.label_add_user = CTkLabel(
            self.window_container,
            font=self.WINDOW_TITLE_FONT,
            text="ADD NEW USER"
        )

        # Username
        self.username_var = StringVar(value=temp_username)
        self.frame_username = CTkFrame(
            self.window_container,
            fg_color=CONTENT_BG,
        )
        self.label_username = CTkLabel(
            self.frame_username,
            font=CONTENT_FONT,
            text="Username: "
        )
        self.entry_username = CTkEntry(
            self.frame_username,
            font=CONTENT_FONT,
            width=200,
            textvariable=self.username_var
        )

        # Password
        self.password_var = StringVar(value=temp_raw_password)
        self.frame_password = CTkFrame(
            self.window_container,
            fg_color=CONTENT_BG,
        )
        self.label_password = CTkLabel(
            self.frame_password,
            font=CONTENT_FONT,
            text="Password: "
        )
        self.entry_password = CTkEntry(
            self.frame_password,
            font=CONTENT_FONT,
            width=200,
            textvariable=self.password_var
        )
        
        # Description
        self.frame_description = CTkFrame(
            self.window_container,
            fg_color=CONTENT_BG,
        )
        self.label_description = CTkLabel(
            self.frame_description,
            font=CONTENT_FONT,
            text="Description: "
        )
        self.entry_description = CTkEntry(
            self.frame_description,
            font=CONTENT_FONT,
            width=200,
        )

        # Confirm Button
        self.btn_add_user = CTkButton(
            self.window_container,
            font=CONTENT_FONT,
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
            text="ADD USER",
            command=lambda: self.finalize_add_user(
                temp_user_role,
                self.entry_description.get(),
                temp_username,
                temp_password
            )
        )

        # CREATE LAYOUTS
        self.window_container.pack(anchor='nw', expand='true', fill='both')
        self.label_add_user.pack(anchor='nw', fill='x', pady=(40, 10))
        self.frame_username.pack(anchor='nw', fill='x', pady=(20, 10), padx=(45, 0))
        self.label_username.pack(side='left', padx=(0, 18))
        self.entry_username.pack(side='left')
        self.frame_password.pack(anchor='nw', fill='x', pady=(0, 10), padx=(45, 0))
        self.label_password.pack(side='left', padx=(0, 22))
        self.entry_password.pack(side='left')
        self.frame_description.pack(anchor='nw', fill='x', pady=(0, 10), padx=(45, 0))
        self.label_description.pack(side='left', padx=(0, 10))
        self.entry_description.pack(side='left')
        self.btn_add_user.pack(anchor='center', pady=(10, 0))

        self.entry_username.configure(state="disabled")
        self.entry_password.configure(state="disabled")

    def finalize_add_user(self, role, desc, username, password):
        if not role or not desc or not username or not password:
            messagebox.showwarning("Error", "Fields cannot be empty!")
            return

        if not messagebox.askokcancel("Confirmation", f"Are you sure you want to add user with,\nDescription: {desc}"):
            return
        
        self.authentication_window = CTkToplevel(self)
        self._center_screen(400, 200)
        self.authentication_window.title("User Authentication")
        self.authentication_window.transient(self)
        self.authentication_window.grab_set()
        self.authentication_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.authentication_window.iconbitmap(default=self.authentication_window.iconPath)
        if platform.startswith("win"):
            self.after(200, lambda: self.authentication_window.iconbitmap(self.authentication_window.iconPath))

        # CREATE WIDGETS
        label_authentication = CTkLabel(
            self.authentication_window,
            text="Enter current users password:",
            font=self.FONT_AUTHENTICATION,
        )
        entry_password = CTkEntry(
            self.authentication_window,
            show="•",
            font=self.FONT_AUTHENTICATION,
            width=200
        )
        btn_confirm_password = CTkButton(
            self.authentication_window,
            text="Confirm",
            font=self.FONT_AUTHENTICATION,
            command=lambda: self.final_add_user(entry_password.get(), role, desc, username, password),
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
        )
        btn_cancel = CTkButton(
            self.authentication_window,
            text="Cancel",
            font=self.FONT_AUTHENTICATION,
            command=self.close_user_authentication_window,
            fg_color=self.BTN_LOGOUT,
            hover_color=self.BTN_LOGOUT_HOVER
        )

        # CREATE LAYOUT
        label_authentication.pack(pady=(20, 0))
        entry_password.pack(anchor='center')
        btn_confirm_password.pack(anchor='center', pady=10)
        btn_cancel.pack(anchor='center')

    def final_add_user(self, password, role, desc, username, new_password):
        if not verify_user(ACTIVE_USERNAME, password):
            messagebox.showerror("Authentication Error", "Incorrect password!")
            return

        if add_new_user(role, desc, username, new_password):
            messagebox.showinfo("Success", "User added successfully!")
            log_user_activity(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime(), f"NEW USER CREATED - {username}")

        self.close_user_authentication_window()
        self.add_user_window.grab_release()
        self.add_user_window.destroy()
        self.populate_tree()

        return

    def _center_add_screen(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        return x_axis, y_axis
    
    def change_admin_password(self):
        self.change_password_window = CTkToplevel(self)
        window_width = 400
        window_height = 260
        x_axis, y_axis = self._center_add_screen(window_width, window_height)
        self.change_password_window.title('Change Admin Password')
        self.change_password_window.resizable(False, False)
        self.change_password_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.after(200, lambda: self.change_password_window.iconbitmap(self.change_password_window.iconPath))
        self.change_password_window.geometry("{}x{}+{}+{}".format(
            window_width, window_height, x_axis, y_axis
        ))
        self.change_password_window.transient(self)
        self.change_password_window.grab_set()
        self.change_password_window.focus()

        # CREATE WIDGETS
        self.window_container = CTkFrame(
            self.change_password_window,
            fg_color=CONTENT_BG
        )
        label_old_password = CTkLabel(
            self.window_container,
            text="Enter current password:",
            font=CONTENT_FONT,
        )
        entry_old_password = CTkEntry(
            self.window_container,
            show="•",
            font=CONTENT_FONT,
            width=250
        )
        label_new_password = CTkLabel(
            self.window_container,
            text="Enter new password:",
            font=CONTENT_FONT,
        )
        entry_new_password = CTkEntry(
            self.window_container,
            show="•",
            font=CONTENT_FONT,
            width=250
        )
        btn_confirm_password = CTkButton(
            self.window_container,
            text="Confirm",
            font=CONTENT_FONT,
            command=lambda: self.finalize_change_password(entry_old_password.get(), entry_new_password.get()),
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
        )

        # CREATE LAYOUT
        self.window_container.pack(fill='both', expand=True)
        label_old_password.pack(anchor='nw', pady=(35, 5), padx=(75, 0))
        entry_old_password.pack(anchor='center')
        label_new_password.pack(anchor='nw', pady=(10, 5), padx=(75, 0))
        entry_new_password.pack(anchor='center')
        btn_confirm_password.pack(anchor='center', pady=20)

    def finalize_change_password(self, old_password, new_password):
        if not old_password or not new_password:
            messagebox.showwarning("Error", "Fields cannot be empty!")
            return
        
        if not verify_user(ACTIVE_USERNAME, old_password):
            messagebox.showerror("Authentication Error", "Incorrect password!")
            return
        
        if verify_password(ACTIVE_USERNAME, old_password, new_password):
            messagebox.showwarning("Warning", "New password is the same as the old password!")
            return
        
        hashed_password = hash_password(new_password)

        if do_change_user_password(hashed_password, ACTIVE_USERNAME):
            messagebox.showinfo("Success", "Password changed successfully!")
            log_user_activity(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime(), f"PASSWORD CHANGED")

        self.change_password_window.grab_release()
        self.change_password_window.destroy()

    def reset_password(self):
        selected = self.tree_user_accounts.focus()
        values = self.tree_user_accounts.item(selected, 'values')

        if not values:
            messagebox.showerror("Error", "There is no account selected!")
            return
        
        if not messagebox.askokcancel("Confirmation", "Are you sure you want to reset this account's password?"):
            return
        
        self.authentication_window = CTkToplevel(self)
        self._center_screen(400, 200)
        self.authentication_window.title("User Authentication")
        self.authentication_window.transient(self)
        self.authentication_window.grab_set()
        self.authentication_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.authentication_window.iconbitmap(default=self.authentication_window.iconPath)
        if platform.startswith("win"):
            self.after(200, lambda: self.authentication_window.iconbitmap(self.authentication_window.iconPath))

        # CREATE WIDGETS
        label_authentication = CTkLabel(
            self.authentication_window,
            text="Enter current users password:",
            font=self.FONT_AUTHENTICATION,
        )
        entry_password = CTkEntry(
            self.authentication_window,
            show="•",
            font=self.FONT_AUTHENTICATION,
            width=200
        )
        btn_confirm_password = CTkButton(
            self.authentication_window,
            text="Confirm",
            font=self.FONT_AUTHENTICATION,
            command=lambda: self.finalize_reset_password(entry_password.get(), values),
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
        )
        btn_cancel = CTkButton(
            self.authentication_window,
            text="Cancel",
            font=self.FONT_AUTHENTICATION,
            command=self.close_user_authentication_window,
            fg_color=self.BTN_LOGOUT,
            hover_color=self.BTN_LOGOUT_HOVER
        )

        # CREATE LAYOUT
        label_authentication.pack(pady=(20, 0))
        entry_password.pack(anchor='center')
        btn_confirm_password.pack(anchor='center', pady=10)
        btn_cancel.pack(anchor='center')

    def finalize_reset_password(self, password, values):
        if not verify_user(ACTIVE_USERNAME, password):
            messagebox.showerror("Authentication Error", "Incorrect password!")
            return
        
        default_password = ""
        if values[1] == "sysadmin_":
            default_password = hash_password("123")
        else:
            default_password = hash_password("123")

        if do_reset_user_password(default_password, values):
            messagebox.showinfo("Success", "Password reset successful!")
            log_user_activity(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime(), f"RESET PASSWORD - {values[3]}")
        
        self.close_user_authentication_window()

    def remove_user(self):
        selected = self.tree_user_accounts.focus()
        values = self.tree_user_accounts.item(selected, 'values')

        if not values:
            messagebox.showerror("Error", "There is no account selected!")
            return
        
        if values[1] == 'sysadmin_':
            messagebox.showerror("Error", "Cannot remove a system administrator account!")
            return
        
        if not messagebox.askokcancel("Confirmation", "Are you sure you want to remove this user"):
            return
        
        self.authentication_window = CTkToplevel(self)
        self._center_screen(400, 200)
        self.authentication_window.title("User Authentication")
        self.authentication_window.transient(self)
        self.authentication_window.grab_set()
        self.authentication_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.authentication_window.iconbitmap(default=self.authentication_window.iconPath)
        if platform.startswith("win"):
            self.after(200, lambda: self.authentication_window.iconbitmap(self.authentication_window.iconPath))

        # CREATE WIDGETS
        label_authentication = CTkLabel(
            self.authentication_window,
            text="Enter current users password:",
            font=self.FONT_AUTHENTICATION,
        )
        entry_password = CTkEntry(
            self.authentication_window,
            show="•",
            font=self.FONT_AUTHENTICATION,
            width=200
        )
        btn_confirm_password = CTkButton(
            self.authentication_window,
            text="Confirm",
            font=self.FONT_AUTHENTICATION,
            command=lambda: self.finalize_remove_user(entry_password.get(), values),
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
        )
        btn_cancel = CTkButton(
            self.authentication_window,
            text="Cancel",
            font=self.FONT_AUTHENTICATION,
            command=self.close_user_authentication_window,
            fg_color=self.BTN_LOGOUT,
            hover_color=self.BTN_LOGOUT_HOVER
        )

        # CREATE LAYOUT
        label_authentication.pack(pady=(20, 0))
        entry_password.pack(anchor='center')
        btn_confirm_password.pack(anchor='center', pady=10)
        btn_cancel.pack(anchor='center')

    def finalize_remove_user(self, password, values):
        if not verify_user(ACTIVE_USERNAME, password):
            messagebox.showerror("Authentication Error", "Incorrect password!")
            return

        if do_remove_user(values):
            messagebox.showinfo("Success", "User removed successfully!")
            log_user_activity(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime(), f"REMOVED USER - {values[3]}")
        
        self.close_user_authentication_window()
        self.populate_tree()
        
    def close_user_authentication_window(self):
        self.authentication_window.grab_release()
        self.authentication_window.destroy()

    def _center_screen(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        self.authentication_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))

    def populate_tree(self):
        for item in self.tree_user_accounts.get_children():
            self.tree_user_accounts.delete(item)
        global count
        count = 0
        for record in get_user_accounts():
            self.tree_user_accounts.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    record[4]
                )
            )
            count += 1
    

class UserAccountsPage(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            fg_color=CONTENT_BG
        )
        self.constants()
        self.create_widgets()
        self.create_layout()

    def constants(self):
        return
    
    def create_widgets(self):
        self.test_label = CTkLabel(
            self,
            text="My Account"
        )
    
    def create_layout(self):
        self.test_label.pack(anchor='center', expand='true', fill='both')


class LogsPage(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            fg_color=CONTENT_BG
        )
        self.active_btn = None
        self.constants()
        self.create_widgets()
        self.create_layout()
        self.combined_action(UserLogs, 'users')

    def constants(self):
        self.BTN_WIDTH = 220
        self.BTN_HEIGHT = 100
        self.BTN_FONT = ('Bahnschrift SemiBold', 20, 'normal')
        self.BTN_COLOR_INACTIVE = '#656D4A'
        self.BTN_COLOR_HOVER = '#A4AC86'
        self.BTN_COLOR_ACTIVE = '#333d29'
        self.BTN_FONT_COLOR_ACTIVE = '#FAFAFA'
        self.BTN_FONT_COLOR_INACTIVE = '#000'

    def create_widgets(self):
        self.frame_logs_sidebar = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )
        self.frame_logs_content = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )
        self.btn_users_activity = CTkButton(
            self.frame_logs_sidebar,
            text='Users\nActivity',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            font=self.BTN_FONT,
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
            command=lambda: self.combined_action(UserLogs, 'users')
        )
        self.btn_residents_documents = CTkButton(
            self.frame_logs_sidebar,
            text='Residents\nDocuments',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            font=self.BTN_FONT,
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
            command=lambda: self.combined_action(ResidentLogs, "residents")
        )
        self.btn_blotter_documents = CTkButton(
            self.frame_logs_sidebar,
            text='Blotter\nDocuments',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            font=self.BTN_FONT,
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
            command=lambda: self.combined_action(BlotterLogs, 'blotters')
        )
        self.btn_profiling_documents = CTkButton(
            self.frame_logs_sidebar,
            text='Profiling\nActivity',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            font=self.BTN_FONT,
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
            command=lambda: self.combined_action(ProfilingLogs, 'profiling')
        )
        self.btn_database_backup = CTkButton(
            self.frame_logs_sidebar,
            text='Database\nBackup',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            font=self.BTN_FONT,
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
            command=lambda: self.combined_action(BackupLogs, 'backup')
        )

    def create_layout(self):
        self.frame_logs_sidebar.pack(
            side='left',
            padx=10,
            pady=(10, 5),
        )
        self.frame_logs_content.pack(
            side='left',
            fill='both',
            expand=True,
            padx=10,
            pady=(5, 10),
        )
        self.btn_users_activity.pack(
            anchor='center',
            padx=10,
            pady=10,
        )
        self.btn_residents_documents.pack(
            anchor='center',
            padx=10,
            pady=10,
        )
        self.btn_blotter_documents.pack(
            anchor='center',
            padx=10,
            pady=10,
        )
        self.btn_profiling_documents.pack(
            anchor='center',
            padx=10,
            pady=10,
        )
        self.btn_database_backup.pack(
            anchor='center',
            padx=10,
            pady=10,
        )

    def combined_action(self, page, btn):
        if self.active_btn == btn:
            return
        self.active_btn = btn
        for widget in self.frame_logs_content.winfo_children():
            widget.destroy()
        page(self.frame_logs_content).pack(fill='both', expand=True)
        self.set_active(btn)

    def set_active(self, btn):
        self.set_inactive()
        if btn == 'users':
            self.btn_users_activity.configure(
                fg_color=self.BTN_COLOR_ACTIVE,
                hover_color=self.BTN_COLOR_ACTIVE,
                text_color=self.BTN_FONT_COLOR_ACTIVE,
            )
        if btn == 'residents':
            self.btn_residents_documents.configure(
                fg_color=self.BTN_COLOR_ACTIVE,
                hover_color=self.BTN_COLOR_ACTIVE,
                text_color=self.BTN_FONT_COLOR_ACTIVE,
            )
        if btn == 'blotters':
            self.btn_blotter_documents.configure(
                fg_color=self.BTN_COLOR_ACTIVE,
                hover_color=self.BTN_COLOR_ACTIVE,
                text_color=self.BTN_FONT_COLOR_ACTIVE,
            )
        if btn == 'profiling':
            self.btn_profiling_documents.configure(
                fg_color=self.BTN_COLOR_ACTIVE,
                hover_color=self.BTN_COLOR_ACTIVE,
                text_color=self.BTN_FONT_COLOR_ACTIVE,
            )
        if btn == 'backup':
            self.btn_database_backup.configure(
                fg_color=self.BTN_COLOR_ACTIVE,
                hover_color=self.BTN_COLOR_ACTIVE,
                text_color=self.BTN_FONT_COLOR_ACTIVE,
            )

    def set_inactive(self):
        self.btn_users_activity.configure(
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
        )
        self.btn_residents_documents.configure(
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
        )
        self.btn_blotter_documents.configure(
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
        )
        self.btn_profiling_documents.configure(
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
        )
        self.btn_database_backup.configure(
            fg_color=self.BTN_COLOR_INACTIVE,
            hover_color=self.BTN_COLOR_HOVER,
            text_color=self.BTN_FONT_COLOR_INACTIVE,
        )


class UserLogs(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.constants()
        self.create_widgets()
        self.create_layout()

    def constants(self):
        self.TREE_LABEL_FONT = ('Bahnschrift SemiBold', 30, 'normal')
        self.SELECTED_LOG_FONT = ('Bahnschrift SemiBold', 22, 'normal')

        self.SELECTED_FONT_COLOR = '#9d0208'

        self.TEXT_COLOR = '#FAFAFA'
        self.TREE_HEADING_COLOR = "#344e41"
        self.TREE_SELECTED_COLOR = "#344e41"
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", font=("Bahnschrift SemiBold", 12, "normal"), rowheight=30)
        self.tree_style.configure("Treeview.Heading", font=("Bahnschrift SemiBold", 16, "bold"),padding=(0, 5), foreground=self.TREE_HEADING_COLOR)
        self.tree_style.map("Treeview",
                            background=[("selected", self.TREE_SELECTED_COLOR)],
                            foreground=[("selected", self.TEXT_COLOR)]
                            )

    def create_widgets(self):
        self.label_users_log = CTkLabel(
            self,
            font=self.TREE_LABEL_FONT,
            text='USERS ACTIVITY LOG',
        )

        # SELECTED LOG INFO CONTAINER
        self.frame_selected_log = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )

        # DATE AND TIME
        self.frame_date_and_time = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_date_and_time = CTkLabel(
            self.frame_date_and_time,
            font=self.SELECTED_LOG_FONT,
            text='Date and Time: '
        )
        self.date_and_time_var = StringVar(value="N/A")
        self.entry_date_and_time = CTkLabel(
            self.frame_date_and_time,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.date_and_time_var,
        )

        # ACTION MADE
        self.frame_action_made = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_action_made = CTkLabel(
            self.frame_action_made,
            font=self.SELECTED_LOG_FONT,
            text='Action Made: '
        )
        self.action_made_var = StringVar(value="N/A")
        self.entry_action_made = CTkLabel(
            self.frame_action_made,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.action_made_var,
        )

        # USER LOGGED
        self.frame_user_logged = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text='User Logged: '
        )
        self.user_logged_var = StringVar(value="N/A")
        self.entry_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.user_logged_var,
        )

        # USER ROLE
        self.frame_user_role = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_user_role = CTkLabel(
            self.frame_user_role,
            font=self.SELECTED_LOG_FONT,
            text='User Description: '
        )
        self.user_role_var = StringVar(value="N/A")
        self.entry_user_role = CTkLabel(
            self.frame_user_role,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.user_role_var,
        )

        self.frame_tree = CTkFrame(self)
        self.tree_user_logs_data = ttk.Treeview(self.frame_tree)
        self.tree_user_logs_data.configure()
        self.tree_user_logs_data["columns"] = (
            "Activity ID", "Date and Time", "Action Made", "User Logged", "User Description"
        )
        self.tree_user_logs_data.heading("#0", text="", anchor='w')
        self.tree_user_logs_data.column("#0", width=0, stretch=NO)
        self.tree_user_logs_data.heading("Activity ID", text="", anchor='w')
        self.tree_user_logs_data.column("Activity ID", width=0, stretch=NO)
        for column in self.tree_user_logs_data["columns"][1:]:
            self.tree_user_logs_data.heading(column, text=column)
            self.tree_user_logs_data.column(column, width=100, stretch=YES)
        self.tree_user_logs_data_scroll = ttk.Scrollbar(
            self.frame_tree,
            orient=VERTICAL,
            command=self.tree_user_logs_data.yview
        )
        self.tree_user_logs_data.configure(
            yscrollcommand=self.tree_user_logs_data_scroll.set
        )
        self.tree_user_logs_data.bind("<ButtonRelease-1>", self.select_record)
        self.populate_tree()

    def create_layout(self):
        self.label_users_log.pack(anchor='center', fill='x', pady=(40, 20))
        self.frame_selected_log.pack(anchor='center', fill='x', pady=20, padx=50)
        self.frame_date_and_time.pack(anchor="nw")
        self.label_date_and_time.pack(side='left')
        self.entry_date_and_time.pack(side='left', padx=(43, 0))
        self.frame_action_made.pack(anchor="nw")
        self.label_action_made.pack(side='left')
        self.entry_action_made.pack(side='left', padx=(62, 0))
        self.frame_user_logged.pack(anchor="nw")
        self.label_user_logged.pack(side='left')
        self.entry_user_logged.pack(side='left', padx=(58, 0))
        self.frame_user_role.pack(anchor="nw")
        self.label_user_role.pack(side='left')
        self.entry_user_role.pack(side='left', padx=(20, 0))
        self.frame_tree.pack(side='left', fill='both', expand=True, pady=(20, 40), padx=40)
        self.tree_user_logs_data.pack(side='left', fill='both', expand=True)
        self.tree_user_logs_data_scroll.pack(side='right', fill='y')

    def select_record(self, e):
        selected = self.tree_user_logs_data.focus()
        values = self.tree_user_logs_data.item(selected, 'values')

        if not values:
            return

        self.date_and_time_var.set(values[1])
        self.action_made_var.set(values[2])
        self.user_logged_var.set(values[3])
        self.user_role_var.set(values[4])

    def populate_tree(self):
        for item in self.tree_user_logs_data.get_children():
            self.tree_user_logs_data.delete(item)
        global count
        count = 0
        for record in get_user_logs():
            self.tree_user_logs_data.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0], record[3], record[4], record[1], record[2]
                )
            )
            count += 1


class ResidentLogs(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.constants()
        self.create_widgets()
        self.create_layout()

    def constants(self):
        self.TREE_LABEL_FONT = ('Bahnschrift SemiBold', 30, 'normal')
        self.SELECTED_LOG_FONT = ('Bahnschrift SemiBold', 22, 'normal')

        self.SELECTED_FONT_COLOR = '#9d0208'

        self.TEXT_COLOR = '#FAFAFA'
        self.TREE_HEADING_COLOR = "#344e41"
        self.TREE_SELECTED_COLOR = "#344e41"
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", font=("Bahnschrift SemiBold", 12, "normal"), rowheight=30)
        self.tree_style.configure("Treeview.Heading", font=("Bahnschrift SemiBold", 16, "bold"),padding=(0, 5), foreground=self.TREE_HEADING_COLOR)
        self.tree_style.map("Treeview",
                            background=[("selected", self.TREE_SELECTED_COLOR)],
                            foreground=[("selected", self.TEXT_COLOR)]
                            )

    def create_widgets(self):
        self.label_residents_log = CTkLabel(
            self,
            font=self.TREE_LABEL_FONT,
            text='RESIDENTS DOCUMENTS ACTIVITY LOG',
        )

        # SELECTED LOG INFO CONTAINER
        self.frame_selected_log = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )

        # DATE AND TIME
        self.frame_date_and_time = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_date_and_time = CTkLabel(
            self.frame_date_and_time,
            font=self.SELECTED_LOG_FONT,
            text='Date and Time: '
        )
        self.date_and_time_var = StringVar(value="N/A")
        self.entry_date_and_time = CTkLabel(
            self.frame_date_and_time,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.date_and_time_var,
        )

        # USER LOGGED-IN
        self.frame_user_logged = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text='User Logged-in: '
        )
        self.user_logged_var = StringVar(value="N/A")
        self.entry_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.user_logged_var,
        )

        # TYPE OF DOCUMENT
        self.frame_document_type = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_document_type = CTkLabel(
            self.frame_document_type,
            font=self.SELECTED_LOG_FONT,
            text='Type of Document: '
        )
        self.document_type_var = StringVar(value="N/A")
        self.entry_document_type = CTkLabel(
            self.frame_document_type,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.document_type_var,
        )

        # REQUESTEE
        self.frame_requestee = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_requestee = CTkLabel(
            self.frame_requestee,
            font=self.SELECTED_LOG_FONT,
            text='Requestee: '
        )
        self.requestee_var = StringVar(value="N/A")
        self.entry_requestee = CTkLabel(
            self.frame_requestee,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.requestee_var,
        )

        self.frame_search_bar = CTkFrame(
            self,
            fg_color=CONTENT_BG
        )
        self.label_search_bar = CTkLabel(
            self.frame_search_bar,
            font=self.SELECTED_LOG_FONT,
            text='Search'
        )
        self.search_var = StringVar()
        self.entry_search_bar = CTkEntry(
            self.frame_search_bar,
            width=800,
            font=self.SELECTED_LOG_FONT,
            placeholder_text="Search here...",
            textvariable=self.search_var
        )
        self.entry_search_bar.bind("<KeyRelease>", self.on_search)

        self.frame_tree = CTkFrame(self)
        self.tree_resident_logs_data = ttk.Treeview(self.frame_tree)
        self.tree_resident_logs_data.configure()
        self.tree_resident_logs_data["columns"] = (
            "Activity ID", "Date and Time", "User Logged-in", "Type of Document", "Requestee"
        )
        self.tree_resident_logs_data.heading("#0", text="", anchor='w')
        self.tree_resident_logs_data.column("#0", width=0, stretch=NO)
        self.tree_resident_logs_data.heading("Activity ID", text="", anchor='w')
        self.tree_resident_logs_data.column("Activity ID", width=0, stretch=NO)
        for column in self.tree_resident_logs_data["columns"][1:]:
            self.tree_resident_logs_data.heading(column, text=column)
            self.tree_resident_logs_data.column(column, width=100, stretch=YES)
        self.tree_resident_logs_data_scroll = ttk.Scrollbar(
            self.frame_tree,
            orient=VERTICAL,
            command=self.tree_resident_logs_data.yview
        )
        self.tree_resident_logs_data.configure(
            yscrollcommand=self.tree_resident_logs_data_scroll.set
        )
        self.tree_resident_logs_data.bind("<ButtonRelease-1>", self.select_record)
        self.populate_tree()

    def create_layout(self):
        self.label_residents_log.pack(anchor='center', fill='x', pady=(40, 20))
        self.frame_selected_log.pack(anchor='center', fill='x', pady=20, padx=50)
        self.frame_date_and_time.pack(anchor="nw")
        self.label_date_and_time.pack(side='left')
        self.entry_date_and_time.pack(side='left', padx=(56, 0))
        self.frame_user_logged.pack(anchor="nw")
        self.label_user_logged.pack(side='left')
        self.entry_user_logged.pack(side='left', padx=(42, 0))
        self.frame_document_type.pack(anchor="nw")
        self.label_document_type.pack(side='left')
        self.entry_document_type.pack(side='left', padx=(20, 0))
        self.frame_requestee.pack(anchor="nw")
        self.label_requestee.pack(side='left')
        self.entry_requestee.pack(side='left', padx=(92, 0))
        self.frame_search_bar.pack(anchor='center')
        self.label_search_bar.pack(side='left')
        self.entry_search_bar.pack(side='left', padx=10)
        self.frame_tree.pack(anchor='center', fill='both', expand=True, pady=(20, 40), padx=40)
        self.tree_resident_logs_data.pack(side='left', fill='both', expand=True)
        self.tree_resident_logs_data_scroll.pack(side='right', fill='y')

    def on_search(self, e):
        search_data = self.search_var.get()
        self.update_tree(search_data)

    def update_tree(self, search_data):
        for item in self.tree_resident_logs_data.get_children():
            self.tree_resident_logs_data.delete(item)
        
        for item in get_residents_log():
            if (search_data.lower() in item[1].lower() or
                search_data.lower() in item[2].lower() or
                search_data.lower() in item[3].lower() or
                search_data.lower() in item[4].lower()
            ):
                self.tree_resident_logs_data.insert('', 'end', values=item)

    def select_record(self, e):
        selected = self.tree_resident_logs_data.focus()
        values = self.tree_resident_logs_data.item(selected, 'values')

        if not values:
            return

        self.date_and_time_var.set(values[1])
        self.user_logged_var.set(values[2])
        self.document_type_var.set(values[3])
        self.requestee_var.set(values[4])

    def populate_tree(self):
        for item in self.tree_resident_logs_data.get_children():
            self.tree_resident_logs_data.delete(item)
        global count
        count = 0
        for record in get_residents_log():
            self.tree_resident_logs_data.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0], record[3], record[1], record[2], record[4]
                )
            )
            count += 1


class BlotterLogs(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.constants()
        self.create_widgets()
        self.create_layout()

    def constants(self):
        self.TREE_LABEL_FONT = ('Bahnschrift SemiBold', 30, 'normal')
        self.SELECTED_LOG_FONT = ('Bahnschrift SemiBold', 22, 'normal')

        self.SELECTED_FONT_COLOR = '#9d0208'

        self.TEXT_COLOR = '#FAFAFA'
        self.TREE_HEADING_COLOR = "#344e41"
        self.TREE_SELECTED_COLOR = "#344e41"
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", font=("Bahnschrift SemiBold", 12, "normal"), rowheight=30)
        self.tree_style.configure("Treeview.Heading", font=("Bahnschrift SemiBold", 16, "bold"),padding=(0, 5), foreground=self.TREE_HEADING_COLOR)
        self.tree_style.map("Treeview",
                            background=[("selected", self.TREE_SELECTED_COLOR)],
                            foreground=[("selected", self.TEXT_COLOR)]
                            )
    def create_widgets(self):
        self.label_residents_log = CTkLabel(
            self,
            font=self.TREE_LABEL_FONT,
            text='RESIDENTS DOCUMENTS ACTIVITY LOG',
        )

        # SELECTED LOG INFO CONTAINER
        self.frame_selected_log = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )

        # DATE AND TIME
        self.frame_date_and_time = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_date_and_time = CTkLabel(
            self.frame_date_and_time,
            font=self.SELECTED_LOG_FONT,
            text='Date and Time: '
        )
        self.date_and_time_var = StringVar(value="N/A")
        self.entry_date_and_time = CTkLabel(
            self.frame_date_and_time,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.date_and_time_var,
        )

        # BLOTTER CASE NO
        self.frame_user_logged = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text='Blotter Case No.: '
        )
        self.user_logged_var = StringVar(value="N/A")
        self.entry_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.user_logged_var,
        )

        # ACTION
        self.frame_document_type = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_document_type = CTkLabel(
            self.frame_document_type,
            font=self.SELECTED_LOG_FONT,
            text='Action: '
        )
        self.document_type_var = StringVar(value="N/A")
        self.entry_document_type = CTkLabel(
            self.frame_document_type,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.document_type_var,
        )

        # USERNAME
        self.frame_requestee = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_requestee = CTkLabel(
            self.frame_requestee,
            font=self.SELECTED_LOG_FONT,
            text='Username: '
        )
        self.requestee_var = StringVar(value="N/A")
        self.entry_requestee = CTkLabel(
            self.frame_requestee,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.requestee_var,
        )

        self.frame_search_bar = CTkFrame(
            self,
            fg_color=CONTENT_BG
        )
        self.label_search_bar = CTkLabel(
            self.frame_search_bar,
            font=self.SELECTED_LOG_FONT,
            text='Search'
        )
        self.search_var = StringVar()
        self.entry_search_bar = CTkEntry(
            self.frame_search_bar,
            width=800,
            font=self.SELECTED_LOG_FONT,
            placeholder_text="Search here...",
            textvariable=self.search_var
        )
        self.entry_search_bar.bind("<KeyRelease>", self.on_search)

        self.frame_tree = CTkFrame(self)
        self.tree_blotter_logs_data = ttk.Treeview(self.frame_tree)
        self.tree_blotter_logs_data.configure()
        self.tree_blotter_logs_data["columns"] = (
            "Log ID", "Date and Time", "Blotter Case No.", "Action", "User"
        )
        self.tree_blotter_logs_data.heading("#0", text="", anchor='w')
        self.tree_blotter_logs_data.column("#0", width=0, stretch=NO)
        self.tree_blotter_logs_data.heading("Log ID", text="", anchor='w')
        self.tree_blotter_logs_data.column("Log ID", width=0, stretch=NO)
        for column in self.tree_blotter_logs_data["columns"][1:]:
            self.tree_blotter_logs_data.heading(column, text=column)
            self.tree_blotter_logs_data.column(column, width=100, stretch=YES)
        self.tree_blotter_logs_data_scroll = ttk.Scrollbar(
            self.frame_tree,
            orient=VERTICAL,
            command=self.tree_blotter_logs_data.yview
        )
        self.tree_blotter_logs_data.configure(
            yscrollcommand=self.tree_blotter_logs_data_scroll.set
        )
        self.tree_blotter_logs_data.bind("<ButtonRelease-1>", self.select_record)
        self.populate_tree()

    def create_layout(self):
        self.label_residents_log.pack(anchor='center', fill='x', pady=(40, 20))
        self.frame_selected_log.pack(anchor='center', fill='x', pady=20, padx=50)
        self.frame_date_and_time.pack(anchor="nw")
        self.label_date_and_time.pack(side='left')
        self.entry_date_and_time.pack(side='left', padx=(56, 0))
        self.frame_user_logged.pack(anchor="nw")
        self.label_user_logged.pack(side='left')
        self.entry_user_logged.pack(side='left', padx=(37, 0))
        self.frame_document_type.pack(anchor="nw")
        self.label_document_type.pack(side='left')
        self.entry_document_type.pack(side='left', padx=(135, 0))
        self.frame_requestee.pack(anchor="nw")
        self.label_requestee.pack(side='left')
        self.entry_requestee.pack(side='left', padx=(96, 0))
        self.frame_search_bar.pack(anchor='center')
        self.label_search_bar.pack(side='left')
        self.entry_search_bar.pack(side='left', padx=10)
        self.frame_tree.pack(anchor='center', fill='both', expand=True, pady=(20, 40), padx=40)
        self.tree_blotter_logs_data.pack(side='left', fill='both', expand=True)
        self.tree_blotter_logs_data_scroll.pack(side='right', fill='y')

    def on_search(self, e):
        search_data = self.search_var.get()
        self.update_tree(search_data)

    def update_tree(self, search_data):
        for item in self.tree_blotter_logs_data.get_children():
            self.tree_blotter_logs_data.delete(item)
        
        for item in get_blotter_log():
            if (
                search_data.lower() in item[1].lower() or
                search_data.lower() in item[2].lower() or
                search_data.lower() in item[3].lower() or
                search_data.lower() in item[4].lower()
            ):
                self.tree_blotter_logs_data.insert('', 'end', values=item)

    def select_record(self, e):
        selected = self.tree_blotter_logs_data.focus()
        values = self.tree_blotter_logs_data.item(selected, 'values')

        if not values:
            return

        self.date_and_time_var.set(values[1])
        self.user_logged_var.set(values[2])
        self.document_type_var.set(values[3])
        self.requestee_var.set(values[4])

    def populate_tree(self):
        for item in self.tree_blotter_logs_data.get_children():
            self.tree_blotter_logs_data.delete(item)
        global count
        count = 0
        for record in get_blotter_log():
            self.tree_blotter_logs_data.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0], record[1], record[2], record[3], record[4]
                )
            )
            count += 1


class ProfilingLogs(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.constants()
        self.create_widgets()
        self.create_layout()

    def constants(self):
        self.TREE_LABEL_FONT = ('Bahnschrift SemiBold', 30, 'normal')
        self.SELECTED_LOG_FONT = ('Bahnschrift SemiBold', 22, 'normal')

        self.SELECTED_FONT_COLOR = '#9d0208'

        self.TEXT_COLOR = '#FAFAFA'
        self.TREE_HEADING_COLOR = "#344e41"
        self.TREE_SELECTED_COLOR = "#344e41"
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", font=("Bahnschrift SemiBold", 12, "normal"), rowheight=30)
        self.tree_style.configure("Treeview.Heading", font=("Bahnschrift SemiBold", 16, "bold"),padding=(0, 5), foreground=self.TREE_HEADING_COLOR)
        self.tree_style.map("Treeview",
                            background=[("selected", self.TREE_SELECTED_COLOR)],
                            foreground=[("selected", self.TEXT_COLOR)]
                            )

    def create_widgets(self):
        self.label_residents_log = CTkLabel(
            self,
            font=self.TREE_LABEL_FONT,
            text='RESIDENTS DOCUMENTS ACTIVITY LOG',
        )
        self.frame_selected_log = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )

        # ACTIVITY DATE
        self.frame_activity_date = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,    
        )
        self.label_activity_date = CTkLabel(
            self.frame_activity_date,
            font=self.SELECTED_LOG_FONT,
            text="Date and Time: "
        )
        self.activity_date_var = StringVar(value="N/A")
        self.entry_activity_date = CTkLabel(
            self.frame_activity_date,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.activity_date_var,
        )

        # ACTION
        self.frame_action = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,    
        )
        self.label_action = CTkLabel(
            self.frame_action,
            font=self.SELECTED_LOG_FONT,
            text="Action: "
        )
        self.activity_action = StringVar(value="N/A")
        self.entry_action = CTkLabel(
            self.frame_action,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.activity_action
        )

        # RESIDENT NAME
        self.frame_resident_name = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,    
        )
        self.label_resident_name = CTkLabel(
            self.frame_resident_name,
            font=self.SELECTED_LOG_FONT,
            text="Resident Name: "
        )
        self.activity_resident_name = StringVar(value="N/A")
        self.entry_resident_name = CTkLabel(
            self.frame_resident_name,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.activity_resident_name
        )

        # COLUMNS CHANGED
        self.frame_columns_changed = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,    
        )
        self.label_columns_changed = CTkLabel(
            self.frame_columns_changed,
            font=self.SELECTED_LOG_FONT,
            text="Columns Changed: "
        )
        self.activity_columns_changed = StringVar(value="N/A")
        self.entry_columns_changed = CTkLabel(
            self.frame_columns_changed,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.activity_columns_changed
        )

        # USER LOGGED-IN
        self.frame_user_logged = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,    
        )
        self.label_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text="User Logged-in: "
        )
        self.activity_user_logged = StringVar(value="N/A")
        self.entry_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.activity_user_logged
        )

        self.frame_tree = CTkFrame(self)
        self.tree_profiling_logs_data = ttk.Treeview(self.frame_tree)
        self.tree_profiling_logs_data.configure()
        self.tree_profiling_logs_data["columns"] = (
            "Activity ID", "Date and Time", "Action", "Resident Name", "Columns Changed", "User Logged-in"
        )
        self.tree_profiling_logs_data.heading("#0", text="", anchor='w')
        self.tree_profiling_logs_data.column("#0", width=0, stretch=NO)
        self.tree_profiling_logs_data.heading("Activity ID", text="", anchor='w')
        self.tree_profiling_logs_data.column("Activity ID", width=0, stretch=NO)
        for column in self.tree_profiling_logs_data["columns"][1:]:
            self.tree_profiling_logs_data.heading(column, text=column)
            self.tree_profiling_logs_data.column(column, width=150, stretch=YES)
        self.tree_profiling_logs_data_scroll = ttk.Scrollbar(
            self.frame_tree,
            orient=VERTICAL,
            command=self.tree_profiling_logs_data.yview
        )
        self.tree_profiling_logs_data.configure(
            yscrollcommand=self.tree_profiling_logs_data_scroll.set
        )
        self.tree_profiling_logs_data.bind("<ButtonRelease-1>", self.select_record)
        self.populate_tree()

    def create_layout(self):
        self.label_residents_log.pack(anchor='center', fill='x', pady=(40, 20))
        self.frame_selected_log.pack(anchor='center', fill='x', pady=20, padx=50)
        self.frame_activity_date.pack(anchor='nw')
        self.label_activity_date.pack(side='left')
        self.entry_activity_date.pack(side='left', padx=(65, 0))
        self.frame_action.pack(anchor='nw')
        self.label_action.pack(side='left')
        self.entry_action.pack(side='left', padx=(144, 0))
        self.frame_resident_name.pack(anchor='nw')
        self.label_resident_name.pack(side='left')
        self.entry_resident_name.pack(side='left', padx=(56, 0))
        self.frame_columns_changed.pack(anchor='nw')
        self.label_columns_changed.pack(side='left')
        self.entry_columns_changed.pack(side='left', padx=(28, 0))
        self.frame_user_logged.pack(anchor='nw')
        self.label_user_logged.pack(side='left')
        self.entry_user_logged.pack(side='left', padx=(53, 0))
        self.frame_tree.pack(anchor='center', fill='both', expand=True, pady=(20, 40), padx=40)
        self.tree_profiling_logs_data.pack(side='left', fill='both', expand=True)
        self.tree_profiling_logs_data_scroll.pack(side='right', fill='y')

    def select_record(self, e):
        selected = self.tree_profiling_logs_data.focus()
        values = self.tree_profiling_logs_data.item(selected, 'values')

        if not values:
            return

        self.activity_date_var.set(values[1])
        self.activity_action.set(values[2])
        self.activity_resident_name.set(values[3])
        self.activity_columns_changed.set(values[4])
        self.activity_user_logged.set(values[5])

    def populate_tree(self):
        for item in self.tree_profiling_logs_data.get_children():
            self.tree_profiling_logs_data.delete(item)
        global count
        count = 0
        for record in get_profiling_log():
            self.tree_profiling_logs_data.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0], record[1], record[2], record[3], record[4], record[5]
                )
            )
            count += 1


class BackupLogs(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.create_constants()
        self.create_widgets()
        self.create_layout()

    def create_constants(self):
        self.TREE_LABEL_FONT = ('Bahnschrift SemiBold', 30, 'normal')
        self.SELECTED_LOG_FONT = ('Bahnschrift SemiBold', 22, 'normal')

        self.SELECTED_FONT_COLOR = '#9d0208'

        self.TEXT_COLOR = '#FAFAFA'
        self.TREE_HEADING_COLOR = "#344e41"
        self.TREE_SELECTED_COLOR = "#344e41"
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", font=("Bahnschrift SemiBold", 12, "normal"), rowheight=30)
        self.tree_style.configure("Treeview.Heading", font=("Bahnschrift SemiBold", 16, "bold"),padding=(0, 5), foreground=self.TREE_HEADING_COLOR)
        self.tree_style.map("Treeview",
                            background=[("selected", self.TREE_SELECTED_COLOR)],
                            foreground=[("selected", self.TEXT_COLOR)]
                            )
    
    def create_widgets(self):
        self.label_backup_log = CTkLabel(
            self,
            font=self.TREE_LABEL_FONT,
            text='DATABASE BACKUP LOG',
        )

        # SELECTED LOG INFO CONTAINER
        self.frame_selected_log = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )

        # DATE AND TIME
        self.frame_date_time = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_date_time = CTkLabel(
            self.frame_date_time,
            font=self.SELECTED_LOG_FONT,
            text='Date and Time: '
        )
        self.date_time_var = StringVar(value="N/A")
        self.entry_date_time = CTkLabel(
            self.frame_date_time,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.date_time_var,
        )

        # BACKUP NAME
        self.frame_backup_name = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_backup_name = CTkLabel(
            self.frame_backup_name,
            font=self.SELECTED_LOG_FONT,
            text='Backup Name: '
        )
        self.backup_name_var = StringVar(value="N/A")
        self.entry_backup_name = CTkLabel(
            self.frame_backup_name,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.backup_name_var,
        )

        # USER LOGGED-IN
        self.frame_user_logged = CTkFrame(
            self.frame_selected_log,
            fg_color=CONTENT_BG,
        )
        self.label_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text='User Logged-in: '
        )
        self.user_logged_var = StringVar(value="N/A")
        self.entry_user_logged = CTkLabel(
            self.frame_user_logged,
            font=self.SELECTED_LOG_FONT,
            text_color=self.SELECTED_FONT_COLOR,
            textvariable=self.user_logged_var,
        )

        self.frame_tree = CTkFrame(self)
        self.tree_backup_logs_data = ttk.Treeview(self.frame_tree)
        self.tree_backup_logs_data.configure()
        self.tree_backup_logs_data["columns"] = (
            "Log ID", "Date and Time", "File Name", "User Logged-in"
        )
        self.tree_backup_logs_data.heading("#0", text="", anchor='w')
        self.tree_backup_logs_data.column("#0", width=0, stretch=NO)
        self.tree_backup_logs_data.heading("Log ID", text="", anchor='w')
        self.tree_backup_logs_data.column("Log ID", width=0, stretch=NO)
        for column in self.tree_backup_logs_data["columns"][1:]:
            self.tree_backup_logs_data.heading(column, text=column)
            self.tree_backup_logs_data.column(column, width=100, stretch=YES)
        self.tree_backup_logs_data_scroll = ttk.Scrollbar(
            self.frame_tree,
            orient=VERTICAL,
            command=self.tree_backup_logs_data.yview
        )
        self.tree_backup_logs_data.configure(
            yscrollcommand=self.tree_backup_logs_data_scroll.set
        )
        self.tree_backup_logs_data.bind("<ButtonRelease-1>", self.select_record)
        self.populate_tree()
    
    def create_layout(self):
        self.label_backup_log.pack(anchor='center', fill='x', pady=(40, 20))
        self.frame_selected_log.pack(anchor='center', fill='x', pady=20, padx=50)
        self.frame_date_time.pack(anchor="nw")
        self.label_date_time.pack(side='left')
        self.entry_date_time.pack(side='left', padx=(32, 0))
        self.frame_backup_name.pack(anchor="nw")
        self.label_backup_name.pack(side='left')
        self.entry_backup_name.pack(side='left', padx=(35, 0))
        self.frame_user_logged.pack(anchor="nw")
        self.label_user_logged.pack(side='left')
        self.entry_user_logged.pack(side='left', padx=(19, 0))
        self.frame_tree.pack(anchor='center', fill='both', expand=True, pady=(20, 40), padx=40)
        self.tree_backup_logs_data.pack(side='left', fill='both', expand=True)
        self.tree_backup_logs_data_scroll.pack(side='right', fill='y')

    def select_record(self, e):
        selected = self.tree_backup_logs_data.focus()
        values = self.tree_backup_logs_data.item(selected, 'values')

        if not values:
            return

        self.date_time_var.set(values[1])
        self.backup_name_var.set(values[2])
        self.user_logged_var.set(values[3])

    def populate_tree(self):
        for item in self.tree_backup_logs_data.get_children():
            self.tree_backup_logs_data.delete(item)
        global count
        count = 0
        for record in get_backup_log():
            self.tree_backup_logs_data.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0], record[1], record[2], record[3]
                )
            )
            count += 1


class ResidentsPage(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            fg_color=CONTENT_BG
        )
        self.active_filters()
        self.constants()
        self.create_widgets()
        self.create_layout()

    def constants(self):
        # Font size for Actions Label
        self.LEGEND_ACTIONS_FONT = ('Bahnschrift SemiBold', 18, 'normal')
        # Form Entry size
        self.ENTRY_WIDTH = 165
        # Form Actions Button size
        self.BTN_WIDTH = 150
        self.BTN_HEIGHT = 40
        # Buttons Colors
        self.TEXT_COLOR = "#fafafa"
        self.BTN_GREEN = "#656D4A"
        self.BTN_HOVER_GREEN = "#A4AC86"
        self.BTN_BROWN = "#936639"
        self.BTN_HOVER_BROWN = "#A68A64"
        self.BTN_BLUE = "#023E7D"
        self.BTN_HOVER_BLUE = "#0466C8"
        self.BTN_BIRTH = "#979DA2"
        self.BTN_DARK = "#34312d"
        self.BTN_HOVER_DARK = "#7f7b82"
        self.BTN_YELLOW = "#a47e1b"
        self.BTN_HOVER_YELLOW = "#b69121"

        self.FONT_AUTHENTICATION =  ('Bahnschrift SemiBold', 20, 'normal')
        self.BTN_LOGOUT = '#9d0208'
        self.BTN_LOGOUT_HOVER = '#e5383b'

        self.BTN_FILTER_COLOR = "#254336"
        self.BTN_GENERATE_COLOR = "#6F4E37"

        self.TREE_HEADING_COLOR = "#344e41"
        self.TREE_SELECTED_COLOR = "#344e41"
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", font=("Bahnschrift SemiBold", 12, "normal"), rowheight=30)
        self.tree_style.configure("Treeview.Heading", font=("Bahnschrift SemiBold", 16, "bold"),padding=(0, 5), foreground=self.TREE_HEADING_COLOR)
        self.tree_style.map("Treeview",
                            background=[("selected", self.TREE_SELECTED_COLOR)],
                            foreground=[("selected", self.TEXT_COLOR)]
                            )

        self.topLevelDate = None
        self.selected_date = "00-00-0000"

        # Generate Document Toplevel Buttons
        self.DOC_HEIGHT = 70
        self.DOC_WIDTH = 250
        self.DOC_FONT = ('Bahnschrift SemiBold', 16, 'normal')

        self.var_selected_record = StringVar(value="")

        self.RESIDENTS_CONTENT_BG = "#dad7cd"

    def create_widgets(self):
        # - Profiling Form and Button Container
        self.profiling_container = CTkFrame(
            self,
        )
        # -- Profiling Form and Label Container
        self.profilingFormLabel_container = CTkFrame(
            self.profiling_container, fg_color=CONTENT_BG
        )
        # --- Profiling Form Label
        self.frame_profilingFormLabel = CTkFrame(
            self.profilingFormLabel_container, fg_color=CONTENT_BG
        )
        self.profilingForm_label = CTkLabel(
            self.frame_profilingFormLabel, text='Residents Profiling Form', font=LABELFRAME_FONT,
            fg_color=CONTENT_BG
        )
        self.check_edit_form_var = StringVar(value='locked')
        self.check_edit_form = CTkCheckBox(
            self.frame_profilingFormLabel,
            text='Form Locked',
            command=lambda: self.selected_form_action(self.check_edit_form_var.get()),
            variable=self.check_edit_form_var,
            onvalue='locked',
            offvalue='unlocked',
            font=CONTENT_FONT
        )
        self.btn_clearForm = CTkButton(
            self.frame_profilingFormLabel, text="Clear Form", font=CONTENT_FONT, fg_color=self.BTN_DARK,
            hover_color=self.BTN_HOVER_DARK, command=lambda: self.clear_residentFormBtn('clearBtn'),
        )
        self.frame_selected_record = CTkFrame(
            self.frame_profilingFormLabel, fg_color=CONTENT_BG
        )
        self.selected_label_selected_record = CTkLabel(
            self.frame_selected_record, text="Current Selected Record: ", font=CURRENT_RECORD_FONT,
            fg_color=CONTENT_BG
        )
        self.label_selected_record = CTkLabel(
            self.frame_selected_record, textvariable=self.var_selected_record, font=CURRENT_RECORD_FONT_SELECTED,
            text_color=self.TREE_SELECTED_COLOR
        )
        # --- Profiling Form Container
        self.profilingForm_container = CTkFrame(
            self.profilingFormLabel_container, fg_color=CONTENT_BG
        )
        # ---- Profiling Form First Column
        self.profilingForm_firstColumn = CTkFrame(
            self.profilingForm_container, fg_color=CONTENT_BG
        )
        # ----- Resident ID (Hidden)
        self.entry_residentID = CTkEntry(
            self.profilingForm_firstColumn,
        )
        # ----- Resident Purok
        purok_list = [
            "Vanda", "Walingwaling", "Bougainvillea", "Mercury", "Daisy",
            "Orchid", "Chrysanthenum", "Santan", "Rosas", "Sampaguita"
        ]
        self.label_residentPurok = CTkLabel(
            self.profilingForm_firstColumn,
            text='Purok',
            font=CONTENT_FONT
        )
        self.entry_residentPurok = CTkComboBox(
            self.profilingForm_firstColumn,
            values=purok_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Last Name
        self.label_residentLastName = CTkLabel(
            self.profilingForm_firstColumn,
            text='Last Name',
            font=CONTENT_FONT
        )
        self.entry_residentLastName = CTkEntry(
            self.profilingForm_firstColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident First Name
        self.label_residentFirstName = CTkLabel(
            self.profilingForm_firstColumn,
            text='First Name',
            font=CONTENT_FONT
        )
        self.entry_residentFirstName = CTkEntry(
            self.profilingForm_firstColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Middle Name
        self.label_residentMiddleName = CTkLabel(
            self.profilingForm_firstColumn,
            text='Middle Name',
            font=CONTENT_FONT
        )
        self.entry_residentMiddleName = CTkEntry(
            self.profilingForm_firstColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Suffix and Age
        self.frame_residentSuffixAge = CTkFrame(
            self.profilingForm_firstColumn,
            fg_color=BG_CONTENT,
        )
        # ------ Resident Suffix
        self.label_residentSuffix = CTkLabel(
            self.frame_residentSuffixAge,
            text='Suffix',
            font=CONTENT_FONT
        )
        self.entry_residentSuffix = CTkEntry(
            self.frame_residentSuffixAge,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH - 85
        )
        # ------ Resident Age
        self.label_residentAge = CTkLabel(
            self.frame_residentSuffixAge,
            text='Age',
            font=CONTENT_FONT
        )
        self.entry_residentAge = CTkEntry(
            self.frame_residentSuffixAge,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH - 85
        )
        self.entry_residentAge.bind('<FocusOut>', self.check_Age)

        # ---- Profiling Form Second Column
        self.profilingForm_secondColumn = CTkFrame(
            self.profilingForm_container, fg_color=CONTENT_BG
        )
        # ----- Resident Sex
        sex_list = ['MALE', 'FEMALE']
        self.label_residentSex = CTkLabel(
            self.profilingForm_secondColumn,
            text='Sex',
            font=CONTENT_FONT
        )
        self.entry_residentSex = CTkComboBox(
            self.profilingForm_secondColumn,
            values=sex_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Civil Status
        civil_status = ['Single', 'Married', 'Widowed', 'Separated']
        self.label_residentStatus = CTkLabel(
            self.profilingForm_secondColumn,
            text='Civil Status',
            font=CONTENT_FONT
        )
        self.entry_residentStatus = CTkComboBox(
            self.profilingForm_secondColumn,
            values=civil_status,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Blood Type
        blood_type = ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.label_residentBlood = CTkLabel(
            self.profilingForm_secondColumn,
            text='Blood Type',
            font=CONTENT_FONT
        )
        self.entry_residentBlood = CTkComboBox(
            self.profilingForm_secondColumn,
            values=blood_type,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Date of Birth
        self.label_residentDateOfBirth = CTkLabel(
            self.profilingForm_secondColumn,
            text='Date of Birth',
            font=CONTENT_FONT
        )
        self.frame_residentDateOfBirth = CTkFrame(
            self.profilingForm_secondColumn,
            fg_color=BG_CONTENT,
        )
        style = ttk.Style(self)
        style.configure('CustomDateEntry.TEntry',
                        foreground='gray14',
                        background=CONTENT_BG,
                        font=TK_CONTENT_FONT,
                        padding=(5, 6, 0, 6), )
        self.entry_residentDateOfBirth = DateEntry(
            self.frame_residentDateOfBirth,
            style='CustomDateEntry.TEntry',
            width=19,
            font=TK_CONTENT_FONT,
            pady=30,
            date_pattern='dd-mm-yyyy'
        )
        self.entry_residentDateOfBirth.bind("<<DateEntrySelected>>", self.check_birthDate)
        # ----- Resident Occupation
        self.label_residentPlaceOfBirth = CTkLabel(
            self.profilingForm_secondColumn,
            text='Place Of Birth',
            font=CONTENT_FONT
        )
        self.entry_residentPlaceOfBirth = CTkEntry(
            self.profilingForm_secondColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )

        # ---- Profiling Form Third Column
        self.profilingForm_thirdColumn = CTkFrame(
            self.profilingForm_container, fg_color=CONTENT_BG
        )
        # ----- Resident Occupation
        self.label_residentOccupation = CTkLabel(
            self.profilingForm_thirdColumn,
            text='Occupation',
            font=CONTENT_FONT
        )
        self.entry_residentOccupation = CTkEntry(
            self.profilingForm_thirdColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Religion
        self.label_residentReligion = CTkLabel(
            self.profilingForm_thirdColumn,
            text='Religion',
            font=CONTENT_FONT
        )
        self.entry_residentReligion = CTkEntry(
            self.profilingForm_thirdColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Tribe or Ethnicity
        self.label_residentTribeEthnicity = CTkLabel(
            self.profilingForm_thirdColumn,
            text='Tribe or Ethnicity',
            font=CONTENT_FONT
        )
        self.entry_residentTribeEthnicity = CTkEntry(
            self.profilingForm_thirdColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Educational Status
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
        self.label_residentEducation = CTkLabel(
            self.profilingForm_thirdColumn,
            text='Educational Status',
            font=CONTENT_FONT
        )
        self.entry_residentEducation = CTkComboBox(
            self.profilingForm_thirdColumn,
            values=education_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Comelec Registered
        comelec_list = ["Registered", "Not Registered"]
        self.label_residentComelec = CTkLabel(
            self.profilingForm_thirdColumn,
            text='COMELEC',
            font=CONTENT_FONT
        )
        self.entry_residentComelec = CTkComboBox(
            self.profilingForm_thirdColumn,
            values=comelec_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )

        # ---- Profiling Form Fourth Column
        self.profilingForm_fourthColumn = CTkFrame(
            self.profilingForm_container, fg_color=CONTENT_BG
        )
        # ----- Resident Philsys Registered
        philsys_list = ["Registered", "Not Registered"]
        self.label_residentPhilsys = CTkLabel(
            self.profilingForm_fourthColumn,
            text='PHILSYS',
            font=CONTENT_FONT
        )
        self.entry_residentPhilsys = CTkComboBox(
            self.profilingForm_fourthColumn,
            values=philsys_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident PWD and Disability
        self.frame_residentPwdDisability = CTkFrame(
            self.profilingForm_fourthColumn,
            fg_color=BG_CONTENT,
        )
        # ------ Resident PWD
        pwd_list = ["YES", "NO"]
        self.label_residentPwd = CTkLabel(
            self.frame_residentPwdDisability,
            text='PWD',
            font=CONTENT_FONT
        )
        self.entry_residentPwd = CTkComboBox(
            self.frame_residentPwdDisability,
            font=CONTENT_FONT,
            values=pwd_list,
            state='readonly',
            width=self.ENTRY_WIDTH - 93,
            command=self.on_pwd_select
        )
        self.label_residentDisability = CTkLabel(
            self.frame_residentPwdDisability,
            text='Disability',
            font=CONTENT_FONT
        )
        self.disability_placeholder = StringVar()
        self.entry_residentDisability = CTkEntry(
            self.frame_residentPwdDisability,
            font=CONTENT_FONT,
            state='disabled',
            width=self.ENTRY_WIDTH - 74,
            textvariable=self.disability_placeholder
        )
        # ----- Resident Senior Member
        senior_list = ['YES', 'NO']
        self.label_residentSenior = CTkLabel(
            self.profilingForm_fourthColumn,
            text='Senior Member',
            font=CONTENT_FONT
        )
        self.entry_residentSenior = CTkComboBox(
            self.profilingForm_fourthColumn,
            values=senior_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Solo Parent
        soloParent_list = ['YES', 'NO']
        self.label_residentSoloParent = CTkLabel(
            self.profilingForm_fourthColumn,
            text='Solo Parent Member',
            font=CONTENT_FONT
        )
        self.entry_residentSoloParent = CTkComboBox(
            self.profilingForm_fourthColumn,
            values=soloParent_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )

        # ---- Profiling Form Fifth Column
        self.profilingForm_fifthColumn = CTkFrame(
            self.profilingForm_container, fg_color=CONTENT_BG
        )
        # ----- Resident Kasambahay Salary
        self.label_residentKasambahay = CTkLabel(
            self.profilingForm_fifthColumn,
            text='Kasambahay Salary',
            font=CONTENT_FONT
        )
        self.entry_residentKasambahay = CTkEntry(
            self.profilingForm_fifthColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident 4ps Member
        _4ps_list = ['YES', 'NO']
        self.label_resident4ps = CTkLabel(
            self.profilingForm_fifthColumn,
            text='4ps Member',
            font=CONTENT_FONT
        )
        self.entry_resident4ps = CTkComboBox(
            self.profilingForm_fifthColumn,
            values=_4ps_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Salt used
        self.label_residentSalt = CTkLabel(
            self.profilingForm_fifthColumn,
            text='Salt Used',
            font=CONTENT_FONT
        )
        self.entry_residentSalt = CTkEntry(
            self.profilingForm_fifthColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Garbage Disposal
        self.label_residentGarbage = CTkLabel(
            self.profilingForm_fifthColumn,
            text='Garbage Disposal',
            font=CONTENT_FONT
        )
        self.entry_residentGarbage = CTkEntry(
            self.profilingForm_fifthColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )

        # ---- Profiling Form Sixth Column
        self.profilingForm_sixthColumn = CTkFrame(
            self.profilingForm_container, fg_color=CONTENT_BG
        )
        # ----- Resident Animals
        self.label_residentAnimals = CTkLabel(
            self.profilingForm_sixthColumn,
            text='Animals',
            font=CONTENT_FONT
        )
        self.entry_residentAnimals = CTkTextbox(
            self.profilingForm_sixthColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH,
            height=85
        )
        # ----- Farmer Membership
        farmer_list = ["YES", "NO"]
        self.label_residentFarmer = CTkLabel(
            self.profilingForm_sixthColumn,
            text='Farmers Membership',
            font=CONTENT_FONT
        )
        self.frame_residentFarmers = CTkFrame(
            self.profilingForm_sixthColumn,
            fg_color=CONTENT_BG
        )
        self.label_residentFarmer_FirstOrg = CTkLabel(
            self.frame_residentFarmers,
            text='F.A.',
            font=CONTENT_FONT
        )
        self.label_residentFarmer_LastOrg = CTkLabel(
            self.frame_residentFarmers,
            text='RSBSA',
            font=CONTENT_FONT
        )
        self.entry_residentFarmer_FirstOrg = CTkComboBox(
            self.frame_residentFarmers,
            values=farmer_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH - 88
        )
        self.entry_residentFarmer_LastOrg = CTkComboBox(
            self.frame_residentFarmers,
            values=farmer_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH - 88
        )

        # ---- Profiling Form Seventh Column
        self.profilingForm_seventhColumn = CTkFrame(
            self.profilingForm_container, fg_color=CONTENT_BG
        )
        # ----- Resident Water Source
        self.label_residentWater = CTkLabel(
            self.profilingForm_seventhColumn,
            text='Water Source',
            font=CONTENT_FONT
        )
        self.entry_residentWater = CTkEntry(
            self.profilingForm_seventhColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Family Planning Used
        self.label_residentFamilyPlan = CTkLabel(
            self.profilingForm_seventhColumn,
            text='Family Planning Used',
            font=CONTENT_FONT
        )
        self.entry_residentFamilyPlan = CTkEntry(
            self.profilingForm_seventhColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Tpe of CR
        self.label_residentCR = CTkLabel(
            self.profilingForm_seventhColumn,
            text='Type of CR',
            font=CONTENT_FONT
        )
        self.entry_residentCR = CTkEntry(
            self.profilingForm_seventhColumn,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )
        # ----- Resident Status
        status_list = ["Active", "Transferred", "Deceased", "Transient"]
        self.label_status = CTkLabel(
            self.profilingForm_seventhColumn,
            text='Resident Status',
            font=CONTENT_FONT
        )
        self.entry_status = CTkComboBox(
            self.profilingForm_seventhColumn,
            values=status_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH
        )

        # - Search and Buttons Container
        self.searchButtons_container = CTkFrame(
            self, fg_color=CONTENT_BG
        )
        # -- Search Bar Container
        self.frame_searchBar = CTkFrame(
            self.searchButtons_container,
            fg_color=CONTENT_BG
        )
        # --- Search Bar Label
        self.label_searchBar = CTkLabel(
            self.frame_searchBar,
            text='Search Bar',
            font=SEARCHBAR_FONT,
        )
        # --- Search Bar Entry
        self.search_data = StringVar()
        self.entry_searchBar = CTkEntry(
            self.frame_searchBar,
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH + 200,
            height=40,
            textvariable=self.search_data
        )
        self.entry_searchBar.bind("<KeyRelease>", self.on_search)
        self.label_filter_search = CTkLabel(
            self.frame_searchBar,
            text='Search By',
            font=CONTENT_FONT
        )
        search_filter_list = [
            "Default",
            "Last Name",
            "Middle Name",
            "First Name",
            "Suffix",
            "Date of Birth",
            "Place of Birth",
            "Occupation",
            "Religion",
            "Tribe and Ethnicity",
            "PWD Disability",
            "Kasambahay",
            "Salt Used",
            "Garbage Disposal",
            "Animals",
            "Source of Water",
            "Family Planning",
            "Types of CR",
        ]
        self.filter_search = CTkComboBox(
            self.frame_searchBar,
            values=search_filter_list,
            state='readonly',
            font=CONTENT_FONT,
            width=self.ENTRY_WIDTH,
            height=39
        )
        self.filter_search.set(search_filter_list[0])
        # -- Profiling Form Actions Container
        self.frame_profilingActions = CTkFrame(
            self.searchButtons_container,
            fg_color=CONTENT_BG
        )
        # --- Actions Label
        self.label_actions = CTkLabel(
            self.frame_profilingActions,
            text='Resident Form Actions',
            font=CONTENT_FONT,
        )
        # --- Buttons Container
        self.frame_actionsButton = CTkFrame(
            self.frame_profilingActions,
            fg_color=CONTENT_BG,
        )
        # ---- Profiling Button - Add Resident
        self.btn_addResident = CTkButton(
            self.frame_actionsButton, text='Add Resident', fg_color=self.BTN_GREEN, text_color=self.TEXT_COLOR,
            hover_color=self.BTN_HOVER_GREEN, font=CONTENT_FONT, width=self.BTN_WIDTH, height=self.BTN_HEIGHT,
            command=self.save_resident
        )
        # ---- Profiling Button - Update Resident
        self.btn_updateResident = CTkButton(
            self.frame_actionsButton, text='Update Resident', fg_color=self.BTN_BROWN,
            text_color=self.TEXT_COLOR, hover_color=self.BTN_HOVER_BROWN, font=CONTENT_FONT, width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT, command=self.update_resident
        )
        # -- Document Generation Container
        self.frame_generateActions = CTkFrame(
            self.searchButtons_container,
            fg_color=CONTENT_BG
        )
        # --- Actions Label
        self.label_generate = CTkLabel(
            self.frame_generateActions,
            text='Generate Documents/Certificates',
            font=CONTENT_FONT,
        )
        # --- Generate Button - Select Form
        self.btn_selectForm = CTkButton(
            self.frame_generateActions, text='Select Form', fg_color=self.BTN_BLUE, text_color=self.TEXT_COLOR,
            hover_color=self.BTN_HOVER_BLUE, font=CONTENT_FONT, width=self.BTN_WIDTH, height=self.BTN_HEIGHT,
            command=self.select_document
        )
        # -- Residents Data Statistics Container
        self.frame_residentsStatistics = CTkFrame(
            self.searchButtons_container,
            fg_color=CONTENT_BG
        )
        #--- Statistics Label
        self.label_statistics = CTkLabel(
            self.frame_residentsStatistics,
            text='Residents Statistics',
            font=CONTENT_FONT,
        )
        # --- View Statistics Button
        self.btn_statistics = CTkButton(
            self.frame_residentsStatistics, text='View', fg_color=self.BTN_YELLOW, text_color=self.TEXT_COLOR,
            hover_color=self.BTN_HOVER_YELLOW, font=CONTENT_FONT, width=self.BTN_WIDTH, height=self.BTN_HEIGHT,
            command=self.view_statistics
        )

        # - Filter and Generate Container
        self.filter_container = CTkFrame(
            self, fg_color=CONTENT_BG
        )
        self.btn_filter = CTkButton(
            self.filter_container, text='Filters', fg_color=self.BTN_FILTER_COLOR, text_color=self.TEXT_COLOR,
            hover_color=self.BTN_FILTER_COLOR, font=CONTENT_FONT, width=110, height=40, command=self.manage_filters
        )
        self.btn_generate = CTkButton(
            self.filter_container, text='Generate Report', fg_color=self.BTN_GENERATE_COLOR, text_color=self.TEXT_COLOR,
            hover_color=self.BTN_GENERATE_COLOR, font=CONTENT_FONT, width=150, height=40, command=self.manage_generate
        )

        # - Residents Data Treeview Container
        self.residentData_container = CTkFrame(
            self, fg_color=CONTENT_BG
        )
        self.tree_residentsData = ttk.Treeview(self.residentData_container)
        self.tree_residentsData.configure()
        self.tree_residentsData["columns"] = (
            "Resident ID", "Purok", "Last Name", "Middle Name", "First Name", "Suffix", "Age", "Sex",
            "Civil Status", "Blood Type", "Date of Birth", "Place of Birth", "Occupation", "Religion", 
            "Tribe or Ethnicity", "Educational Status", "Comelec Registered", "Philsys Registered",
            "PWD Member", "PWD Disability", "Senior Member", "Solo Parent Member", "Kasambahay Salary",
            "4PS Member", "Salt used", "Garbage Disposal", "Animals",
            "Farmers Member: F.A.", "Farmers Member: RSBSA", "Source of Water",
            "Family Planning Used", "Type of Cr", "Resident Status"
        )
        self.tree_residentsData.heading("#0", text="", anchor='w')
        self.tree_residentsData.column("#0", width=0, stretch=NO)
        self.tree_residentsData.heading("Resident ID", text="", anchor='w')
        self.tree_residentsData.column("Resident ID", width=0, stretch=NO)
        for column in self.tree_residentsData["columns"][1:]:
            self.tree_residentsData.heading(column, text=column)
            self.tree_residentsData.column(column, width=200, anchor='w')
        self.tree_residentsData_scrollY = ttk.Scrollbar(
            self.residentData_container,
            orient=VERTICAL,
            command=self.tree_residentsData.yview
        )
        self.tree_residentsData_scrollX = ttk.Scrollbar(
            self.residentData_container,
            orient=HORIZONTAL,
            command=self.tree_residentsData.xview
        )
        self.tree_residentsData.configure(
            yscrollcommand=self.tree_residentsData_scrollY.set,
            xscrollcommand=self.tree_residentsData_scrollX.set
        )

        self.tree_residentsData.bind("<ButtonRelease-1>", self.select_record)
        self.populate_residentsTree()

    def create_layout(self):
        # -
        self.profiling_container.grid(
            row=0, column=0, sticky='nsew'
        )
        # --
        self.profilingFormLabel_container.grid(
            row=0, column=0, sticky='nsew'
        )
        # ---
        self.frame_profilingFormLabel.grid(
            row=0, column=0, sticky='nsew', pady=(20, 10)
        )
        self.profilingForm_label.grid(
            row=0, column=0, sticky='w', padx=(15, 0)
        )
        self.btn_clearForm.grid(
            row=0, column=2, sticky='e'
        )
        self.frame_selected_record.grid(
            row=1, column=0, sticky='w', padx=(15, 0), pady=(10, 0)
        )
        self.selected_label_selected_record.grid(
            row=0, column=0, sticky='w', padx=(20, 0)
        )
        self.label_selected_record.grid(
            row=0, column=1, sticky='w', padx=(10, 0)
        )
        self.frame_profilingFormLabel.grid_rowconfigure(0, weight=4)
        self.frame_profilingFormLabel.grid_columnconfigure(1, weight=1)
        self.profilingForm_container.grid(
            row=1, column=0, sticky='nsew'
        )
        # ----
        self.profilingForm_firstColumn.grid(
            row=0, column=0, sticky='nsew', padx=(35, 0)
        )
        self.profilingForm_secondColumn.grid(
            row=0, column=1, sticky='nsew', padx=(20, 0)
        )
        self.profilingForm_thirdColumn.grid(
            row=0, column=2, sticky='nsew', padx=(20, 0)
        )
        self.profilingForm_fourthColumn.grid(
            row=0, column=3, sticky='nsew', padx=(20, 0)
        )
        self.profilingForm_fifthColumn.grid(
            row=0, column=4, sticky='nsew', padx=(20, 20)
        )
        self.profilingForm_sixthColumn.grid(
            row=0, column=5, sticky='nsew', padx=(20, 20)
        )
        self.profilingForm_seventhColumn.grid(
            row=0, column=6, sticky='nsew', padx=(20, 20)
        )
        # -----
        # First Column
        self.label_residentPurok.grid(
            row=0, column=0, sticky='nw'
        )
        self.entry_residentPurok.grid(
            row=1, column=0, sticky='nw'
        )
        self.label_residentLastName.grid(
            row=2, column=0, sticky='nw'
        )
        self.entry_residentLastName.grid(
            row=3, column=0, sticky='nw'
        )
        self.label_residentFirstName.grid(
            row=4, column=0, sticky='nw'
        )
        self.entry_residentFirstName.grid(
            row=5, column=0, sticky='nw'
        )
        self.label_residentMiddleName.grid(
            row=6, column=0, sticky='nw'
        )
        self.entry_residentMiddleName.grid(
            row=7, column=0, sticky='nw'
        )
        self.frame_residentSuffixAge.grid(
            row=8, column=0, sticky='nsew'
        )
        self.label_residentSuffix.grid(
            row=0, column=0, sticky='nw'
        )
        self.entry_residentSuffix.grid(
            row=1, column=0, sticky='nsew'
        )
        self.label_residentAge.grid(
            row=0, column=1, sticky='nw', padx=(6, 0)
        )
        self.entry_residentAge.grid(
            row=1, column=1, sticky='nw', padx=(6, 0)
        )

        # Second Column
        # -----
        self.label_residentSex.grid(
            row=0, column=0, sticky='nw',
        )
        self.entry_residentSex.grid(
            row=1, column=0, sticky='nw',
        )
        self.label_residentStatus.grid(
            row=2, column=0, sticky='nw',
        )
        self.entry_residentStatus.grid(
            row=3, column=0, sticky='nw',
        )
        self.label_residentBlood.grid(
            row=4, column=0, sticky='nw',
        )
        self.entry_residentBlood.grid(
            row=5, column=0, sticky='nw',
        )
        self.label_residentDateOfBirth.grid(
            row=6, column=0, sticky='nw',
        )
        self.frame_residentDateOfBirth.grid(
            row=7, column=0, sticky='nw', pady=(0, 1)
        )
        self.entry_residentDateOfBirth.grid(
            row=0, column=0, sticky='nw',
        )
        self.label_residentPlaceOfBirth.grid(
            row=8, column=0, sticky='nw',
        )
        self.entry_residentPlaceOfBirth.grid(
            row=9, column=0, sticky='nw',
        )


        # Third Column
        self.label_residentOccupation.grid(
            row=0, column=0, sticky='nw'
        )
        self.entry_residentOccupation.grid(
            row=1, column=0, sticky='nw'
        )
        self.label_residentReligion.grid(
            row=2, column=0, sticky='nw'
        )
        self.entry_residentReligion.grid(
            row=3, column=0, sticky='nw'
        )
        self.label_residentTribeEthnicity.grid(
            row=4, column=0, sticky='nw'
        )
        self.entry_residentTribeEthnicity.grid(
            row=5, column=0, sticky='nw'
        )
        self.label_residentEducation.grid(
            row=6, column=0, sticky='nw'
        )
        self.entry_residentEducation.grid(
            row=7, column=0, sticky='nw'
        )
        self.label_residentComelec.grid(
            row=8, column=0, sticky='nw'
        )
        self.entry_residentComelec.grid(
            row=9, column=0, sticky='nw'
        )

        # Fourth Column
        self.label_residentPhilsys.grid(
            row=0, column=0, sticky='nw'
        )
        self.entry_residentPhilsys.grid(
            row=1, column=0, sticky='nw'
        )
        self.frame_residentPwdDisability.grid(
            row=2, column=0, sticky='nw'
        )
        self.label_residentPwd.grid(
            row=0, column=0, sticky='nw'
        )
        self.entry_residentPwd.grid(
            row=1, column=0, sticky='nw'
        )
        self.label_residentDisability.grid(
            row=0, column=1, sticky='nw', padx=(5, 0)
        )
        self.entry_residentDisability.grid(
            row=1, column=1, sticky='nw', padx=(5, 0)
        )
        self.label_residentSenior.grid(
            row=4, column=0, sticky='nw'
        )
        self.entry_residentSenior.grid(
            row=5, column=0, sticky='nw'
        )
        self.label_residentSoloParent.grid(
            row=6, column=0, sticky='nw'
        )
        self.entry_residentSoloParent.grid(
            row=7, column=0, sticky='nw'
        )

        # Fifth Column
        self.label_residentKasambahay.grid(
            row=0, column=0, sticky='nw'
        )
        self.entry_residentKasambahay.grid(
            row=1, column=0, sticky='nw'
        )
        self.label_resident4ps.grid(
            row=2, column=0, sticky='nw'
        )
        self.entry_resident4ps.grid(
            row=3, column=0, sticky='nw'
        )
        self.label_residentSalt.grid(
            row=4, column=0, sticky='nw'
        )
        self.entry_residentSalt.grid(
            row=5, column=0, sticky='nw'
        )
        self.label_residentGarbage.grid(
            row=6, column=0, sticky='nw'
        )
        self.entry_residentGarbage.grid(
            row=7, column=0, sticky='nw'
        )

        # Sixth Column
        self.label_residentAnimals.grid(
            row=0, column=0, sticky='nw'
        )
        self.entry_residentAnimals.grid(
            row=1, column=0, sticky='nw'
        )
        self.label_residentFarmer.grid(
            row=2, column=0, sticky='ns', pady=(10, 0)
        )
        self.frame_residentFarmers.grid(
            row=3, column=0, sticky='nw'
        )
        self.label_residentFarmer_FirstOrg.grid(
            row=0, column=0, sticky='nw'
        )
        self.entry_residentFarmer_FirstOrg.grid(
            row=1, column=0, sticky='nw'
        )
        self.label_residentFarmer_LastOrg.grid(
            row=0, column=1, sticky='nw', padx=(8, 0)
        )
        self.entry_residentFarmer_LastOrg.grid(
            row=1, column=1, sticky='nw', padx=(8, 0)
        )

        # Seventh Column
        self.label_residentWater.grid(
            row=0, column=0, sticky='nw'
        )
        self.entry_residentWater.grid(
            row=1, column=0, sticky='nw'
        )
        self.label_residentFamilyPlan.grid(
            row=2, column=0, sticky='nw'
        )
        self.entry_residentFamilyPlan.grid(
            row=3, column=0, sticky='nw'
        )
        self.label_residentCR.grid(
            row=4, column=0, sticky='nw'
        )
        self.entry_residentCR.grid(
            row=5, column=0, sticky='nw'
        )
        self.label_status.grid(
            row=6, column=0, sticky='nw'
        )
        self.entry_status.grid(
            row=7, column=0, sticky='nw'
        )

        # -
        self.searchButtons_container.grid(
            row=1, column=0, sticky='ns', pady=(10, 10)
        )
        # --
        self.frame_searchBar.grid(
            row=0, column=0, sticky='nsew'
        )
        self.frame_profilingActions.grid(
            row=0, column=1, sticky='nsew', padx=(20, 10)
        )
        self.frame_generateActions.grid(
            row=0, column=2, sticky='nsew', padx=(10, 10)
        )
        self.frame_residentsStatistics.grid(
            row=0, column=3, sticky='nsew', padx=(10, 0)
        )
        # ---
        self.label_searchBar.grid(
            row=0, column=0, sticky='nw',
        )
        self.label_filter_search.grid(
            row=0, column=1, sticky='nw', padx=(5, 0)
        )
        self.entry_searchBar.grid(
            row=1, column=0, sticky='nw',
        )
        self.filter_search.grid(
            row=1, column=1, sticky='nw', padx=(5, 0)
        )
        self.label_actions.grid(
            row=0, column=0, sticky='n',
        )
        self.frame_actionsButton.grid(
            row=2, column=0, sticky='n'
        )
        self.label_generate.grid(
            row=0, column=0, sticky='n',
        )
        self.label_statistics.grid(
            row=0, column=0, sticky='n',
        )
        # ----
        self.btn_addResident.grid(
            row=0, column=0, sticky='nw', padx=(0, 3)
        )
        self.btn_updateResident.grid(
            row=0, column=1, sticky='nw', padx=(3, 0)
        )
        self.btn_selectForm.grid(
            row=1, column=0, sticky='n',
        )
        self.btn_statistics.grid(
            row=1, column=0, sticky='n',
        )

        self.filter_container.grid(row=2, column=0, sticky='w', padx=5)
        self.btn_filter.grid(row=0, column=0)
        self.btn_generate.grid(row=0, column=1, padx=(5, 0))

        # - Resident Treeview Container
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.residentData_container.grid(row=3, column=0, sticky='nsew', pady=(5, 10), padx=5)
        self.residentData_container.grid_columnconfigure(0, weight=1)
        self.residentData_container.grid_rowconfigure(0, weight=1)
        self.tree_residentsData.grid(row=0, column=0, sticky='nsew')
        self.tree_residentsData_scrollY.grid(row=0, column=1, sticky='ns')
        self.tree_residentsData_scrollX.grid(row=1, column=0, sticky='ew')

    def manage_generate(self):
        if not check_officials():
            return

        if not self.tree_residentsData.get_children():
            messagebox.showerror(
                "Error", "Cannot generate a list with an empty data!"
            )
            return

        if not messagebox.askokcancel(
            "Confirmation",
            "Are you sure you want to generate the list of residents based on the data present?"
        ):
            return
        
        tree_item = self.tree_residentsData.get_children()
        all_data = []
        for item_id in tree_item:
            item_values = self.tree_residentsData.item(item_id, 'values')
            all_data.append(item_values)
        list_values = []
        for item in all_data:
            list_values.append((get_formal_resident_name(item[3], item[4], item[2], item[5]), item[8], item[6], item[7], item[10]))
        
        # self.reports_window = CTkToplevel(self)
        # self.reports_window.title('Reports Description')
        # self.reports_window.resizable(False, False)
        # self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        # self.reports_window.iconbitmap(default=self.iconPath)
        # if platform.startswith("win"):
        #     self.reports_window.after(200, lambda: self.reports_window.iconbitmap(self.iconPath))
        # width = 400
        # height = 500
        # x_axis, y_axis = self._center_window(width, height)
        # self.reports_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))
        # self.reports_window.transient(self)
        # self.reports_window.grab_set()

        # CREATE WIDGET
        # frame_reports = CTkFrame(
        #     self.reports_window
        # )
        # label_title = CTkLabel(
        #     frame_reports,
        #     text='Report Description: ',
        #     font=CONTENT_FONT,
        # )
        # entry_title = CTkTextbox(
        #     frame_reports,
        #     font=CONTENT_FONT,
        #     width=300,
        #     height=100
        # )
        # submit_button = CTkButton(
        #     frame_reports,
        #     text='CONFIRM',
        #     font=CONTENT_FONT,
        #     width=100,
        #     height=40,
        #     command=lambda: self.finalize_reports(
        #         list_values,
        #         entry_title.get('1.0', 'end-1c')
        #     )
        # )

        # # CREATE LAYOUT
        # frame_reports.pack(anchor='center')
        # label_title.pack(anchor='nw', pady=(15, 5))
        # entry_title.pack(anchor='nw', pady=(5, 10))
        # submit_button.pack(anchor='center')

        self.finalize_reports(list_values)
        
    def finalize_reports(self, list_values):
        process = multiprocessing.Process(
            target=generate_reports,
            args=(list_values, self.get_active_filters())
        )
        process.start()

        log_generate_residents_doc(ACTIVE_USERNAME, "Reports - Residents List",
                                   get_formatted_datetime(), ACTIVE_USERNAME)
        messagebox.showinfo(
            "Success",
            "Generating Reports, Please wait..."
        )

    def get_active_filters(self):
        filter_list = {}
    
        temp_purok_list = []
        if self.filter_purok_vanda.get():
            temp_purok_list.append("Vanda")
        if self.filter_purok_walingwaling.get():
            temp_purok_list.append("Walingwaling")
        if self.filter_purok_buogainvillea.get():
            temp_purok_list.append("Bougainvillea")
        if self.filter_purok_mercury.get():
            temp_purok_list.append("Mercury")
        if self.filter_purok_daisy.get():
            temp_purok_list.append("Daisy")
        if self.filter_purok_orchid.get():
            temp_purok_list.append("Orchid")
        if self.filter_purok_chrysanthenum.get():
            temp_purok_list.append("Chrysanthenum")
        if self.filter_purok_santan.get():
            temp_purok_list.append("Santan")
        if self.filter_purok_rosas.get():
            temp_purok_list.append("Rosas")
        if self.filter_purok_sampaguita.get():
            temp_purok_list.append("Sampaguita")

        temp_age_list = []
        if self.filter_age_to.get() != "100":
            temp_age_list.append(str(self.filter_age_from.get()))
            temp_age_list.append(str(self.filter_age_to.get()))
                
        if self.filter_age_from.get() != "0":
            temp_age_list.append(str(self.filter_age_from.get()))
            temp_age_list.append(str(self.filter_age_to.get()))

        temp_gender_list = []
        if self.filter_gender_male.get():
            temp_gender_list.append("Male")
        if self.filter_gender_female.get():
            temp_gender_list.append("Female")

        temp_comelec_list = []
        if self.filter_comelec_registered.get():
            temp_comelec_list.append("Registered")
        if self.filter_comelec_not_registered.get():
            temp_comelec_list.append("Not Registered")

        temp_philsys_list = []
        if self.filter_philsys_registered.get():
            temp_philsys_list.append("Registered")
        if self.filter_philsys_not_registered.get():
            temp_philsys_list.append("Not Registered")

        temp_civil_list = []
        if self.filter_status_single.get():
            temp_civil_list.append("Single")
        if self.filter_status_married.get():
            temp_civil_list.append("Married")
        if self.filter_status_widowed.get():
            temp_civil_list.append("Widowed")
        if self.filter_status_separated.get():
            temp_civil_list.append("Separated")

        temp_blood_list = []
        if self.filter_blood_unknown.get():
            temp_blood_list.append("Unknown")
        if self.filter_blood_A_plus.get():
            temp_blood_list.append("A+")
        if self.filter_blood_A_minus.get():
            temp_blood_list.append("A-")
        if self.filter_blood_B_plus.get():
            temp_blood_list.append("B+")
        if self.filter_blood_B_minus.get():
            temp_blood_list.append("B-")
        if self.filter_blood_AB_plus.get():
            temp_blood_list.append("AB+")
        if self.filter_blood_AB_minus.get():
            temp_blood_list.append("AB-")
        if self.filter_blood_O_plus.get():
            temp_blood_list.append("O+")
        if self.filter_blood_O_minus.get():
            temp_blood_list.append("O-")

        temp_educ_list = []
        if self.filter_education_no_grade.get():
            temp_educ_list.append("No Grade Reported")
        if self.filter_education_early_educ.get():
            temp_educ_list.append("Early Education")
        if self.filter_education_elementary.get():
            temp_educ_list.append("Elementary Level")
        if self.filter_education_elementary_grad.get():
            temp_educ_list.append("Elementary Graduate")
        if self.filter_education_high.get():
            temp_educ_list.append("High School Level")
        if self.filter_education_high_grad.get():
            temp_educ_list.append("High School Graduate")
        if self.filter_education_college.get():
            temp_educ_list.append("College Level")
        if self.filter_education_college_grad.get():
            temp_educ_list.append("College Graduate")
        if self.filter_education_bacca.get():
            temp_educ_list.append("Post Baccalaureate")

        temp_mem_list = []
        if self.filter_membership_pwd.get():
            temp_mem_list.append("PWD")
        if self.filter_membership_senior.get():
            temp_mem_list.append("Senior Member")
        if self.filter_membership_solo.get():
            temp_mem_list.append("Solo Parent Member")
        if self.filter_membership_four.get():
            temp_mem_list.append("4Ps Member")
        if self.filter_membership_fa.get():
            temp_mem_list.append("Farmer's FA")
        if self.filter_membership_rsbsa.get():
            temp_mem_list.append("Farmer's RSBSA")

        temp_residential_status_list = []
        if self.filter_status_active.get():
            temp_residential_status_list.append("Active")
        if self.filter_status_transferred.get():
            temp_residential_status_list.append("Transferred")
        if self.filter_status_deceased.get():
            temp_residential_status_list.append("Deceased")
        if self.filter_status_transient.get():
            temp_residential_status_list.append("Transient")

        if 10 > len(temp_purok_list) > 0:
            filter_list["purok"] = ", ".join(map(str, temp_purok_list))

        if len(temp_age_list) > 0:
            filter_list["age"] = ", ".join(map(str, temp_age_list))

        if 2 > len(temp_gender_list) > 0:
            filter_list["sex"] = temp_gender_list[0]

        if 2 > len(temp_comelec_list) > 0:
            filter_list["comelec"] = temp_comelec_list[0]

        if 2 > len(temp_philsys_list) > 0:
            filter_list["philsys"] = temp_philsys_list[0]

        if 4 > len(temp_civil_list) > 0:
            filter_list["civil_status"] = ", ".join(map(str, temp_civil_list))

        if 9 > len(temp_blood_list) > 0:
            filter_list["blood_type"] = ", ".join(map(str, temp_blood_list))

        if 9 > len(temp_educ_list) > 0:
            filter_list["educational_status"] = ", ".join(map(str, temp_educ_list))

        if 6 > len(temp_mem_list) > 0:
            filter_list["memberships_orgs"] = ", ".join(map(str, temp_mem_list))

        if len(temp_residential_status_list) > 0:
            filter_list["resident_status"] = ", ".join(map(str, temp_residential_status_list))

        return filter_list
    
    def active_filters(self):
        self.filter_purok_vanda = BooleanVar(value=False)
        self.filter_purok_walingwaling = BooleanVar(value=False)
        self.filter_purok_buogainvillea = BooleanVar(value=False)
        self.filter_purok_mercury = BooleanVar(value=False)
        self.filter_purok_daisy = BooleanVar(value=False)
        self.filter_purok_orchid = BooleanVar(value=False)
        self.filter_purok_chrysanthenum = BooleanVar(value=False)
        self.filter_purok_santan = BooleanVar(value=False)
        self.filter_purok_rosas = BooleanVar(value=False)
        self.filter_purok_sampaguita = BooleanVar(value=False)
        self.filter_age_from = StringVar(value="0")
        self.filter_age_to = StringVar(value="100")
        self.filter_gender_male = BooleanVar(value=False)
        self.filter_gender_female = BooleanVar(value=False)
        self.filter_status_single = BooleanVar(value=False)
        self.filter_status_married = BooleanVar(value=False)
        self.filter_status_widowed = BooleanVar(value=False)
        self.filter_status_separated = BooleanVar(value=False)
        self.filter_comelec_registered = BooleanVar(value=False)
        self.filter_comelec_not_registered = BooleanVar(value=False)
        self.filter_philsys_registered = BooleanVar(value=False)
        self.filter_philsys_not_registered = BooleanVar(value=False)
        self.filter_blood_unknown = BooleanVar(value=False)
        self.filter_blood_A_plus = BooleanVar(value=False)
        self.filter_blood_A_minus = BooleanVar(value=False)
        self.filter_blood_B_plus = BooleanVar(value=False)
        self.filter_blood_B_minus = BooleanVar(value=False)
        self.filter_blood_AB_plus = BooleanVar(value=False)
        self.filter_blood_AB_minus = BooleanVar(value=False)
        self.filter_blood_O_plus = BooleanVar(value=False)
        self.filter_blood_O_minus = BooleanVar(value=False)
        self.filter_education_no_grade = BooleanVar(value=False)
        self.filter_education_early_educ = BooleanVar(value=False)
        self.filter_education_elementary = BooleanVar(value=False)
        self.filter_education_elementary_grad = BooleanVar(value=False)
        self.filter_education_high = BooleanVar(value=False)
        self.filter_education_high_grad = BooleanVar(value=False)
        self.filter_education_college = BooleanVar(value=False)
        self.filter_education_college_grad = BooleanVar(value=False)
        self.filter_education_bacca = BooleanVar(value=False)
        self.filter_membership_pwd = BooleanVar(value=False)
        self.filter_membership_senior = BooleanVar(value=False)
        self.filter_membership_solo = BooleanVar(value=False)
        self.filter_membership_four = BooleanVar(value=False)
        self.filter_membership_fa = BooleanVar(value=False)
        self.filter_membership_rsbsa = BooleanVar(value=False)
        self.filter_status_active = BooleanVar(value=True)
        self.filter_status_transferred = BooleanVar(value=False)
        self.filter_status_deceased = BooleanVar(value=False)
        self.filter_status_transient = BooleanVar(value=False)

    def manage_filters(self):
        self.filters_window = CTkToplevel(self)
        self.filters_window.title('Manage Filters')
        self.filters_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.filters_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.filters_window.after(200, lambda: self.filters_window.iconbitmap(self.iconPath))
        width = 1300
        height = 550
        x_axis, y_axis = self._center_window(width, height)
        self.filters_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))
        self.filters_window.transient(self)
        self.filters_window.grab_set()

        self.filters_window.configure(
            fg_color=self.RESIDENTS_CONTENT_BG
        )

        self.btn_reset_filter = CTkButton(
            self.filters_window,
            text="Reset Filter",
            font=CONTENT_FONT,
            fg_color=self.BTN_DARK,
            hover_color=self.BTN_HOVER_DARK,
            command=self.reset_filter
        )

        self.frame_filters_container = CTkFrame(
            self.filters_window,
            fg_color=self.RESIDENTS_CONTENT_BG
        )

        self.frame_first_column = CTkFrame(
            self.frame_filters_container,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.frame_second_column = CTkFrame(
            self.frame_filters_container,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.frame_third_column = CTkFrame(
            self.frame_filters_container,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.frame_fourth_column = CTkFrame(
            self.frame_filters_container,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.frame_fifth_column = CTkFrame(
            self.frame_filters_container,
            fg_color=self.RESIDENTS_CONTENT_BG
        )

        # Purok
        self.label_purok = CTkLabel(
            self.frame_first_column,
            font=FILTER_LABEL_FONT,
            text="PUROK"
        )
        self.checkbox_purok_vanda = CTkCheckBox(
            self.frame_first_column,
            text="Vanda",
            font=CONTENT_FONT,
            variable=self.filter_purok_vanda
        )
        self.checkbox_purok_walingwaling = CTkCheckBox(
            self.frame_first_column,
            text="Walingwaling",
            font=CONTENT_FONT,
            variable=self.filter_purok_walingwaling
        )
        self.checkbox_purok_buogainvillea = CTkCheckBox(
            self.frame_first_column,
            text="Bougainvillea",
            font=CONTENT_FONT,
            variable=self.filter_purok_buogainvillea
        )
        self.checkbox_purok_mercury = CTkCheckBox(
            self.frame_first_column,
            text="Mercury",
            font=CONTENT_FONT,
            variable=self.filter_purok_mercury
        )
        self.checkbox_purok_daisy = CTkCheckBox(
            self.frame_first_column,
            text="Daisy",
            font=CONTENT_FONT,
            variable=self.filter_purok_daisy
        )
        self.checkbox_purok_orchid = CTkCheckBox(
            self.frame_first_column,
            text="Orchid",
            font=CONTENT_FONT,
            variable=self.filter_purok_orchid
        )
        self.checkbox_purok_chrysanthenum = CTkCheckBox(
            self.frame_first_column,
            text="Chrysanthenum",
            font=CONTENT_FONT,
            variable=self.filter_purok_chrysanthenum
        )
        self.checkbox_purok_santan = CTkCheckBox(
            self.frame_first_column,
            text="Santan",
            font=CONTENT_FONT,
            variable=self.filter_purok_santan
        )
        self.checkbox_purok_rosas = CTkCheckBox(
            self.frame_first_column,
            text="Rosas",
            font=CONTENT_FONT,
            variable=self.filter_purok_rosas
        )
        self.checkbox_purok_sampaguita = CTkCheckBox(
            self.frame_first_column,
            text="Sampaguita",
            font=CONTENT_FONT,
            variable=self.filter_purok_sampaguita
        )

        # Age
        self.label_age = CTkLabel(
            self.frame_second_column,
            font=FILTER_LABEL_FONT,
            text="AGE"
        )
        self.frame_age_from = CTkFrame(
            self.frame_second_column,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.frame_age_to = CTkFrame(
            self.frame_second_column,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.label_age_from = CTkLabel(
            self.frame_age_from,
            font=CONTENT_FONT,
            text="FROM"
        )
        self.entry_age_from = CTkOptionMenu(
            self.frame_age_from,
            values=[str(i) for i in range(101)],
            variable=self.filter_age_from,
            font=CONTENT_FONT,
            fg_color="#FAFAFA",
            text_color="#000",
            width=100
        )
        self.label_age_to = CTkLabel(
            self.frame_age_to,
            font=CONTENT_FONT,
            text="TO"
        )
        self.entry_age_to = CTkOptionMenu(
            self.frame_age_to,
            values=[str(i) for i in range(101)],
            variable=self.filter_age_to,
            font=CONTENT_FONT,
            fg_color="#FAFAFA",
            text_color="#000",
            width=100
        )

        # Sex
        self.label_sex = CTkLabel(
            self.frame_second_column,
            font=FILTER_LABEL_FONT,
            text="SEX"
        )
        self.checkbox_sex_male = CTkCheckBox(
            self.frame_second_column,
            text="Male",
            font=CONTENT_FONT,
            variable=self.filter_gender_male
        )
        self.checkbox_sex_female = CTkCheckBox(
            self.frame_second_column,
            text="Female",
            font=CONTENT_FONT,
            variable=self.filter_gender_female
        )

        # Comelec
        self.label_comelec = CTkLabel(
            self.frame_second_column,
            font=FILTER_LABEL_FONT,
            text="COMELEC"
        )
        self.checkbox_comelec_registered = CTkCheckBox(
            self.frame_second_column,
            text="Registered",
            font=CONTENT_FONT,
            variable=self.filter_comelec_registered
        )
        self.checkbox_comelec_not_registered = CTkCheckBox(
            self.frame_second_column,
            text="Not Registered",
            font=CONTENT_FONT,
            variable=self.filter_comelec_not_registered
        )

        # Civil Status
        self.label_status = CTkLabel(
            self.frame_third_column,
            font=FILTER_LABEL_FONT,
            text="CIVIL STATUS"
        )
        self.checkbox_status_single = CTkCheckBox(
            self.frame_third_column,
            text="Single",
            font=CONTENT_FONT,
            variable=self.filter_status_single
        )
        self.checkbox_status_married = CTkCheckBox(
            self.frame_third_column,
            text="Married",
            font=CONTENT_FONT,
            variable=self.filter_status_married
        )
        self.checkbox_status_widowed = CTkCheckBox(
            self.frame_third_column,
            text="Widowed",
            font=CONTENT_FONT,
            variable=self.filter_status_widowed
        )
        self.checkbox_status_separated = CTkCheckBox(
            self.frame_third_column,
            text="Separated",
            font=CONTENT_FONT,
            variable=self.filter_status_separated
        )
        
        # Philsys
        self.label_philsys = CTkLabel(
            self.frame_fourth_column,
            font=FILTER_LABEL_FONT,
            text="PHILSYS"
        )
        self.checkbox_philsys_registered = CTkCheckBox(
            self.frame_fourth_column,
            text="Registered",
            font=CONTENT_FONT,
            variable=self.filter_philsys_registered
        )
        self.checkbox_philsys_not_registered = CTkCheckBox(
            self.frame_fourth_column,
            text="Not Registered",
            font=CONTENT_FONT,
            variable=self.filter_philsys_not_registered
        )

        # Blood Type
        self.label_blood = CTkLabel(
            self.frame_third_column,
            font=FILTER_LABEL_FONT,
            text="BLOOD TYPE",
        )
        self.frame_blood_first_row = CTkFrame(
            self.frame_third_column,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.frame_blood_second_row = CTkFrame(
            self.frame_third_column,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.frame_blood_third_row = CTkFrame(
            self.frame_third_column,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.frame_blood_fourth_row = CTkFrame(
            self.frame_third_column,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        self.checkbox_a_plus = CTkCheckBox(
            self.frame_blood_first_row,
            text="A⁺",
            font=CONTENT_FONT,
            variable=self.filter_blood_A_plus
        )
        self.checkbox_a_minus = CTkCheckBox(
            self.frame_blood_first_row,
            text="A⁻",
            font=CONTENT_FONT,
            variable=self.filter_blood_A_minus
        )
        self.checkbox_b_plus = CTkCheckBox(
            self.frame_blood_second_row,
            text="B⁺",
            font=CONTENT_FONT,
            variable=self.filter_blood_B_plus
        )
        self.checkbox_b_minus = CTkCheckBox(
            self.frame_blood_second_row,
            text="B⁻",
            font=CONTENT_FONT,
            variable=self.filter_blood_B_minus
        )
        self.checkbox_ab_plus = CTkCheckBox(
            self.frame_blood_third_row,
            text="AB⁺",
            font=CONTENT_FONT,
            variable=self.filter_blood_AB_plus
        )
        self.checkbox_ab_minus = CTkCheckBox(
            self.frame_blood_third_row,
            text="AB⁻",
            font=CONTENT_FONT,
            variable=self.filter_blood_AB_minus
        )
        self.checkbox_o_plus = CTkCheckBox(
            self.frame_blood_fourth_row,
            text="O⁺",
            font=CONTENT_FONT,
            variable=self.filter_blood_O_plus
        )
        self.checkbox_o_minus = CTkCheckBox(
            self.frame_blood_fourth_row,
            text="O⁻",
            font=CONTENT_FONT,
            variable=self.filter_blood_O_minus
        )
        self.checkbox_unknown = CTkCheckBox(
            self.frame_third_column,
            text="Unknown",
            font=CONTENT_FONT,
            variable=self.filter_blood_unknown
        )

        # Educational Status
        self.label_education = CTkLabel(
            self.frame_fourth_column,
            font=FILTER_LABEL_FONT,
            text="EDUCATIONAL STATUS"
        )
        self.checkbox_education_no_grade = CTkCheckBox(
            self.frame_fourth_column,
            text="No Grade Reported",
            font=CONTENT_FONT,
            variable=self.filter_education_no_grade
        )
        self.checkbox_education_early_educ = CTkCheckBox(
            self.frame_fourth_column,
            text="Early Childhood Education",
            font=CONTENT_FONT,
            variable=self.filter_education_early_educ
        )
        self.checkbox_education_elementary = CTkCheckBox(
            self.frame_fourth_column,
            text="Elementary Level",
            font=CONTENT_FONT,
            variable=self.filter_education_elementary
        )
        self.checkbox_education_elementary_grad = CTkCheckBox(
            self.frame_fourth_column,
            text="Elementary Graduate",
            font=CONTENT_FONT,
            variable=self.filter_education_elementary_grad
        )
        self.checkbox_education_high = CTkCheckBox(
            self.frame_fourth_column,
            text="High School Level",
            font=CONTENT_FONT,
            variable=self.filter_education_high
        )
        self.checkbox_education_high_grad = CTkCheckBox(
            self.frame_fourth_column,
            text="High School Graduate",
            font=CONTENT_FONT,
            variable=self.filter_education_high_grad
        )
        self.checkbox_education_college = CTkCheckBox(
            self.frame_fourth_column,
            text="College Level",
            font=CONTENT_FONT,
            variable=self.filter_education_college
        )
        self.checkbox_education_college_grad = CTkCheckBox(
            self.frame_fourth_column,
            text="College Graduate",
            font=CONTENT_FONT,
            variable=self.filter_education_college_grad
        )
        self.checkbox_education_bacca = CTkCheckBox(
            self.frame_fourth_column,
            text="Post Baccalaureate",
            font=CONTENT_FONT,
            variable=self.filter_education_bacca
        )

        # Memberships
        self.label_memberships = CTkLabel(
            self.frame_fifth_column,
            font=FILTER_LABEL_FONT,
            text="MEMBERSHIP/ORGANIZATIONS"
        )
        self.checkbox_pwd = CTkCheckBox(
            self.frame_fifth_column,
            text="PWD",
            font=CONTENT_FONT,
            variable=self.filter_membership_pwd
        )
        self.checkbox_senior = CTkCheckBox(
            self.frame_fifth_column,
            text="Senior Member",
            font=CONTENT_FONT,
            variable=self.filter_membership_senior
        )
        self.checkbox_solo = CTkCheckBox(
            self.frame_fifth_column,
            text="solo Parent Member",
            font=CONTENT_FONT,
            variable=self.filter_membership_solo
        )
        self.checkbox_four_ps = CTkCheckBox(
            self.frame_fifth_column,
            text="4Ps Member",
            font=CONTENT_FONT,
            variable=self.filter_membership_four
        )
        self.checkbox_fa = CTkCheckBox(
            self.frame_fifth_column,
            text="Farmer's F.A. Member",
            font=CONTENT_FONT,
            variable=self.filter_membership_fa
        )
        self.checkbox_rsbsa = CTkCheckBox(
            self.frame_fifth_column,
            text="Farmer's RSBSA Member",
            font=CONTENT_FONT,
            variable=self.filter_membership_rsbsa
        )

        # Resident Status
        self.label_residential_status = CTkLabel(
            self.frame_fifth_column,
            font=FILTER_LABEL_FONT,
            text="RESIDENT STATUS"
        )
        self.checkbox_active = CTkCheckBox(
            self.frame_fifth_column,
            text="Active",
            font=CONTENT_FONT,
            variable=self.filter_status_active
        )
        self.checkbox_transferred = CTkCheckBox(
            self.frame_fifth_column,
            text="Transferred",
            font=CONTENT_FONT,
            variable=self.filter_status_transferred
        )
        self.checkbox_deceased = CTkCheckBox(
            self.frame_fifth_column,
            text="Deceased",
            font=CONTENT_FONT,
            variable=self.filter_status_deceased
        )
        self.checkbox_transient = CTkCheckBox(
            self.frame_fifth_column,
            text="Transient",
            font=CONTENT_FONT,
            variable=self.filter_status_transient
        )

        self.btn_apply_filter = CTkButton(
            self.filters_window,
            text="Apply Filter",
            font=CONTENT_FONT,
            command=self.apply_filter
        )

        self.btn_reset_filter.pack(anchor="ne", pady=(20, 10), padx=(0, 20))

        self.frame_filters_container.pack(anchor="center")

        self.frame_first_column.pack(side='left', fill='y', padx=5)
        self.frame_second_column.pack(side='left', fill='y', padx=5)
        self.frame_third_column.pack(side='left', fill='y', padx=5)
        self.frame_fourth_column.pack(side='left', fill='y', padx=5)
        self.frame_fifth_column.pack(side='left', fill='y', padx=(20, 0))

        self.label_purok.pack(anchor='nw', pady=10)
        self.checkbox_purok_vanda.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_purok_walingwaling.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_purok_buogainvillea.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_purok_mercury.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_purok_daisy.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_purok_orchid.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_purok_chrysanthenum.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_purok_santan.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_purok_rosas.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_purok_sampaguita.pack(anchor='nw', pady=(0, 5), padx=(10, 0))

        self.label_age.pack(anchor='nw', pady=10)
        self.frame_age_from.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.frame_age_to.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.label_age_from.pack(side='left')
        self.entry_age_from.pack(side='left', padx=(10, 0))
        self.label_age_to.pack(side='left')
        self.entry_age_to.pack(side='left', padx=(32, 0))

        self.label_sex.pack(anchor='nw', pady=10)
        self.checkbox_sex_male.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_sex_female.pack(anchor='nw', pady=(0, 5), padx=(10, 0))

        self.label_comelec.pack(anchor='nw', pady=10)
        self.checkbox_comelec_registered.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_comelec_not_registered.pack(anchor='nw', pady=(0, 5), padx=(10, 0))

        self.label_status.pack(anchor='nw', pady=10)
        self.checkbox_status_single.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_status_married.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_status_widowed.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_status_separated.pack(anchor='nw', pady=(0, 5), padx=(10, 0))

        self.label_blood.pack(anchor='nw', pady=10)
        self.frame_blood_first_row.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.frame_blood_second_row.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.frame_blood_third_row.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.frame_blood_fourth_row.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_a_plus.pack(side='left')
        self.checkbox_a_minus.pack(side='left')
        self.checkbox_b_plus.pack(side='left')
        self.checkbox_b_minus.pack(side='left')
        self.checkbox_ab_plus.pack(side='left')
        self.checkbox_ab_minus.pack(side='left')
        self.checkbox_o_plus.pack(side='left')
        self.checkbox_o_minus.pack(side='left')
        self.checkbox_unknown.pack(anchor='nw', pady=(0, 5), padx=(10, 0))

        self.label_education.pack(anchor='nw', pady=10)
        self.checkbox_education_no_grade.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_education_early_educ.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_education_elementary.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_education_elementary_grad.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_education_high.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_education_high_grad.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_education_college.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_education_college_grad.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_education_bacca.pack(anchor='nw', pady=(0, 5), padx=(10, 0))

        self.label_philsys.pack(anchor='nw', pady=10)
        self.checkbox_philsys_registered.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_philsys_not_registered.pack(anchor='nw', pady=(0, 5), padx=(10, 0))

        self.label_memberships.pack(anchor='nw', pady=10)
        self.checkbox_pwd.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_senior.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_solo.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_four_ps.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_fa.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_rsbsa.pack(anchor='nw', pady=(0, 5), padx=(10, 0))

        self.label_residential_status.pack(anchor='nw', pady=10)
        self.checkbox_active.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_transferred.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_deceased.pack(anchor='nw', pady=(0, 5), padx=(10, 0))
        self.checkbox_transient.pack(anchor='nw', pady=(0, 5), padx=(10, 0))

        self.btn_apply_filter.pack(anchor='center', pady=(15, 0))

    def get_selected_purok(self):
        selected_purok = []

        if self.filter_purok_vanda.get():
            selected_purok.append('Vanda')
        if self.filter_purok_walingwaling.get():
            selected_purok.append('Walingwaling')
        if self.filter_purok_buogainvillea.get():
            selected_purok.append('Bougainvillea')
        if self.filter_purok_mercury.get():
            selected_purok.append('Mercury')
        if self.filter_purok_daisy.get():
            selected_purok.append('Daisy')
        if self.filter_purok_orchid.get():
            selected_purok.append('Orchid')
        if self.filter_purok_chrysanthenum.get():
            selected_purok.append('Chrysanthenum')
        if self.filter_purok_santan.get():
            selected_purok.append('Santan')
        if self.filter_purok_rosas.get():
            selected_purok.append('Rosas')
        if self.filter_purok_sampaguita.get():
            selected_purok.append('Sampaguita')

        return selected_purok
    
    def apply_filter(self):
        if int(self.filter_age_from.get()) > int(self.filter_age_to.get()):
            messagebox.showerror(
                "Error", "Age from cannot be greater than the age to."
            )
            return

        self.unlock_form()
        self.clear_residentForm()
        self.hide_edit_form()
        self.populate_residentsTree()
        messagebox.showinfo(
            "Success", "Filter applied."
        )

        self.filters_window.grab_release()
        self.filters_window.destroy()

    def reset_filter(self):
        if not messagebox.askokcancel(
            "Confirmation", "Do you really want to reset the filters?"
        ):
            return

        self.filter_purok_vanda.set(False)
        self.filter_purok_walingwaling.set(False)
        self.filter_purok_buogainvillea.set(False)
        self.filter_purok_mercury.set(False)
        self.filter_purok_daisy.set(False)
        self.filter_purok_orchid.set(False)
        self.filter_purok_chrysanthenum.set(False)
        self.filter_purok_santan.set(False)
        self.filter_purok_rosas.set(False)
        self.filter_purok_sampaguita.set(False)
        self.filter_age_from.set(0)
        self.filter_age_to.set(100)
        self.filter_gender_male.set(False)
        self.filter_gender_female.set(False)
        self.filter_comelec_registered.set(False)
        self.filter_comelec_not_registered.set(False)
        self.filter_status_single.set(False)
        self.filter_status_married.set(False)
        self.filter_status_widowed.set(False)
        self.filter_status_separated.set(False)
        self.filter_blood_unknown.set(False)
        self.filter_blood_A_plus.set(False)
        self.filter_blood_A_minus.set(False)
        self.filter_blood_B_plus.set(False)
        self.filter_blood_B_minus.set(False)
        self.filter_blood_AB_plus.set(False)
        self.filter_blood_AB_minus.set(False)
        self.filter_blood_O_plus.set(False)
        self.filter_blood_O_minus.set(False)
        self.filter_education_no_grade.set(False)
        self.filter_education_early_educ.set(False)
        self.filter_education_elementary.set(False)
        self.filter_education_elementary_grad.set(False)
        self.filter_education_high.set(False)
        self.filter_education_high_grad.set(False)
        self.filter_education_college.set(False)
        self.filter_education_college_grad.set(False)
        self.filter_education_bacca.set(False)
        self.filter_philsys_registered.set(False)
        self.filter_philsys_not_registered.set(False)
        self.filter_membership_pwd.set(False)
        self.filter_membership_senior.set(False)
        self.filter_membership_solo.set(False)
        self.filter_membership_four.set(False)
        self.filter_membership_fa.set(False)
        self.filter_membership_rsbsa.set(False)
        self.filter_status_active.set(True)
        self.filter_status_transferred.set(False)
        self.filter_status_deceased.set(False)
        self.filter_status_transient.set(False)

        self.populate_residentsTree()
        self.filters_window.grab_release()
        self.filters_window.destroy()

    def selected_form_action(self, check_value):
        if check_value == 'unlocked':
            self.unlock_form()
        if check_value == 'locked':
            self.lock_form()

    def lock_form(self):
        self.entry_residentPurok.configure(state='disabled')
        self.entry_residentLastName.configure(state='disabled')
        self.entry_residentFirstName.configure(state='disabled')
        self.entry_residentMiddleName.configure(state='disabled')
        self.entry_residentSuffix.configure(state='disabled')
        self.entry_residentAge.configure(state='disabled')
        self.entry_residentSex.configure(state='disabled')
        self.entry_residentStatus.configure(state='disabled')
        self.entry_residentBlood.configure(state='disabled')
        self.entry_residentDateOfBirth.configure(state='disabled')
        self.entry_residentPlaceOfBirth.configure(state='disabled')
        self.entry_residentOccupation.configure(state='disabled')
        self.entry_residentReligion.configure(state='disabled')
        self.entry_residentTribeEthnicity.configure(state='disabled')
        self.entry_residentEducation.configure(state='disabled')
        self.entry_residentComelec.configure(state='disabled')
        self.entry_residentPhilsys.configure(state='disabled')
        self.entry_residentPwd.configure(state='disabled')
        self.entry_residentDisability.configure(state='disabled')
        self.entry_residentSenior.configure(state='disabled')
        self.entry_residentSoloParent.configure(state='disabled')
        self.entry_residentKasambahay.configure(state='disabled')
        self.entry_resident4ps.configure(state='disabled')
        self.entry_residentSalt.configure(state='disabled')
        self.entry_residentGarbage.configure(state='disabled')
        self.entry_residentAnimals.configure(state='disabled')
        self.entry_residentFarmer_FirstOrg.configure(state='disabled')
        self.entry_residentFarmer_LastOrg.configure(state='disabled')
        self.entry_residentWater.configure(state='disabled')
        self.entry_residentFamilyPlan.configure(state='disabled')
        self.entry_residentCR.configure(state='disabled')
        self.entry_status.configure(state='disabled')

    def unlock_form(self):
        self.entry_residentPurok.configure(state='readonly')
        self.entry_residentLastName.configure(state='normal')
        self.entry_residentFirstName.configure(state='normal')
        self.entry_residentMiddleName.configure(state='normal')
        self.entry_residentSuffix.configure(state='normal')
        self.entry_residentAge.configure(state='normal')
        self.entry_residentSex.configure(state='readonly')
        self.entry_residentStatus.configure(state='readonly')
        self.entry_residentBlood.configure(state='readonly')
        self.entry_residentDateOfBirth.configure(state='normal')
        self.entry_residentPlaceOfBirth.configure(state='normal')
        self.entry_residentOccupation.configure(state='normal')
        self.entry_residentReligion.configure(state='normal')
        self.entry_residentTribeEthnicity.configure(state='normal')
        self.entry_residentEducation.configure(state='readonly')
        self.entry_residentComelec.configure(state='readonly')
        self.entry_residentPhilsys.configure(state='readonly')
        self.entry_residentPwd.configure(state='readonly')
        if self.entry_residentPwd.get().upper() == 'YES':
            self.entry_residentDisability.configure(state='normal')
        self.entry_residentSenior.configure(state='readonly')
        self.entry_residentSoloParent.configure(state='readonly')
        self.entry_residentKasambahay.configure(state='normal')
        self.entry_resident4ps.configure(state='readonly')
        self.entry_residentSalt.configure(state='normal')
        self.entry_residentGarbage.configure(state='normal')
        self.entry_residentAnimals.configure(state='normal')
        self.entry_residentFarmer_FirstOrg.configure(state='readonly')
        self.entry_residentFarmer_LastOrg.configure(state='readonly')
        self.entry_residentWater.configure(state='normal')
        self.entry_residentFamilyPlan.configure(state='normal')
        self.entry_residentCR.configure(state='normal')
        self.entry_status.configure(state='readonly')

    # Select the Document to Generate
    def select_document(self):
        # Check if resident record selected
        if not self.check_residentSelected():
            messagebox.showwarning('Empty Data', 'There is no Resident Selected!')
            return

        if self.check_residentStatus() == 'Transferred':
            if not messagebox.askyesno("Confirmation", "This individual has already transferred residence,\nDo you want to proceed?"):
                return
            
        if self.check_residentStatus() == 'Deceased':
            messagebox.showwarning('Error', 'Cannot generate document for deceased individual!')
            return

        self.select_doc_window = CTkToplevel(self)
        self.select_doc_window.title('Select Document')
        self.select_doc_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.select_doc_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.select_doc_window.after(200, lambda: self.select_doc_window.iconbitmap(self.iconPath))
        width = 300
        height = 480
        x_axis, y_axis = self._center_window(width, height)
        self.select_doc_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))
        self.select_doc_window.transient(self)
        self.select_doc_window.grab_set()

        self.select_doc_window.configure(
            fg_color=self.RESIDENTS_CONTENT_BG
        )

        # CREATE WIDGETS
        btn_lowIncome = CTkButton(
            self.select_doc_window,
            text='Certificate of Low Income',
            width=self.DOC_WIDTH,
            height=self.DOC_HEIGHT,
            font=self.DOC_FONT,
            command=self.generate_lowIncome
        )
        btn_goodMoral = CTkButton(
            self.select_doc_window,
            text='Certificate of\nGood Moral Character',
            width=self.DOC_WIDTH,
            height=self.DOC_HEIGHT,
            font=self.DOC_FONT,
            command=self.generate_goodMoral
        )
        btn_barangayClearance = CTkButton(
            self.select_doc_window,
            text='Barangay Clearance',
            width=self.DOC_WIDTH,
            height=self.DOC_HEIGHT,
            font=self.DOC_FONT,
            command=self.generate_barangayClearance,
        )
        btn_barangayResidency = CTkButton(
            self.select_doc_window,
            text='Barangay Residency',
            width=self.DOC_WIDTH,
            height=self.DOC_HEIGHT,
            font=self.DOC_FONT,
            command=self.generate_barangayResidency,
        )
        btn_jobSeeker = CTkButton(
            self.select_doc_window,
            text='Barangay Certification:\nFirst Time Job Seeker',
            width=self.DOC_WIDTH,
            height=self.DOC_HEIGHT,
            font=self.DOC_FONT,
            command=self.generate_jobSeeker
        )

        # CREATE LAYOUT
        btn_lowIncome.pack(anchor='center', pady=(20, 10))
        btn_goodMoral.pack(anchor='center', pady=(10, 10))
        btn_barangayClearance.pack(anchor='center', pady=(10, 10))
        btn_barangayResidency.pack(anchor='center', pady=(10, 10))
        btn_jobSeeker.pack(anchor='center', pady=(10, 20))

    # Center Window for Document Selection TopLevel
    def _center_window(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        return x_axis, y_axis

    # Check if there is a resident selected
    def check_residentSelected(self):
        resident_ID = self.entry_residentID.get()
        if resident_ID:
            return True
        else:
            return False
        
    def check_residentStatus(self):
        resident_ID = self.entry_residentID.get()
        return verify_residential_status(resident_ID)

    # Generate Low Income
    def generate_lowIncome(self):
        if not check_officials():
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return

        resident_data = self.get_residentData()
        if resident_data[0] == '':
            messagebox.showwarning(
                'Empty Data', 'There is no Resident Selected!')
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return
        resident_fullName = residentFullName(
            'name', resident_data[3], resident_data[4], resident_data[2], resident_data[5]
        )
        resident_purok = resident_data[1]
        resident_sex = resident_data[7]
        barangayCaptain = get_barangay_captain('name')

        self.lowIncome_window = CTkToplevel(self)
        self.lowIncome_window.title('Certificate of Low Income')
        self.lowIncome_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.lowIncome_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.lowIncome_window.after(200, lambda: self.lowIncome_window.iconbitmap(self.iconPath))
        width = 400
        height = 250
        x_axis, y_axis = self._center_window(width, height)
        self.lowIncome_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))
        self.lowIncome_window.transient(self)
        self.lowIncome_window.grab_set()
        
        self.lowIncome_window.configure(
            fg_color=self.RESIDENTS_CONTENT_BG
        )

        # CREATE WIDGET
        frame_lowIncome = CTkFrame(
            self.lowIncome_window,
            fg_color=self.RESIDENTS_CONTENT_BG,
        )
        label_reason = CTkLabel(
            frame_lowIncome,
            text='Request Reason',
            font=CONTENT_FONT,
        )
        entry_reason = CTkEntry(
            frame_lowIncome,
            width=300,
            font=CONTENT_FONT,
        )
        label_officer = CTkLabel(
            frame_lowIncome,
            text='Officer of the Day',
            font=CONTENT_FONT,
        )
        officer_list = ["None"]
        for item in get_barangay_kagawad():
            officer_list.append(item)
        entry_officer = CTkComboBox(
            frame_lowIncome,
            width=300,
            font=CONTENT_FONT,
            values=officer_list,
            state='readonly',
        )
        entry_officer.set(officer_list[0])
        submit_button = CTkButton(
            frame_lowIncome,
            text='CONFIRM',
            font=CONTENT_FONT,
            width=100,
            height=40,
            command=lambda: self.finalize_lowIncome(
                resident_fullName,
                resident_purok,
                resident_sex,
                entry_reason.get(),
                barangayCaptain,
                entry_officer.get()
            )
        )

        # CREATE LAYOUT
        frame_lowIncome.pack(anchor='center')
        label_reason.pack(anchor='nw', pady=(15, 5))
        entry_reason.pack(anchor='nw', pady=(5, 5))
        label_officer.pack(anchor='nw', pady=(15, 5))
        entry_officer.pack(anchor='nw', pady=(5, 15))
        submit_button.pack(anchor='center')

    # Finalize Low Income Parameters and Values
    def finalize_lowIncome(self, fullname, purok, sex, reason, captain, officer):
        if not reason or reason == '':
            messagebox.showwarning('Empty Data', 'Reason cannot be Empty!')
            return

        if not messagebox.askokcancel("Confirmation", f"Are you sure you want to confirm with,\nReason:'{reason}'\nOfficer:'{officer}'"):
            return

        self.select_doc_window.grab_release()
        self.select_doc_window.destroy()
        self.lowIncome_window.grab_release()
        self.lowIncome_window.destroy()

        messagebox.showinfo('Processing', 'Generating Document, Please wait...')

        if officer == 'None':
            process = multiprocessing.Process(
                target=do_certificateLowIncome,
                args=(fullname, purok, sex, reason, captain)
            )
            process.start()
        else:
            process = multiprocessing.Process(
                target=do_certificateLowIncome_on_duty,
                args=(fullname, purok, sex, reason, captain, officer)
            )
            process.start()
        log_generate_residents_doc(ACTIVE_USERNAME, "Certificate of Low Income", get_formatted_datetime(),
                                   fullname)

    # Generate Good Moral
    def generate_goodMoral(self):
        if not check_officials():
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return

        resident_data = self.get_residentData()
        if resident_data[0] == '':
            messagebox.showwarning(
                'Empty Data', 'There is no Resident Selected!')
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return
        resident_fullName = residentFullName(
            'name', resident_data[3], resident_data[4], resident_data[2], resident_data[5]
        )
        resident_purok = resident_data[1]
        resident_sex = resident_data[7]
        resident_status = resident_data[8]
        barangayCaptain = get_barangay_captain('name')

        self.goodMoral_window = CTkToplevel(self)
        self.goodMoral_window.title('Certificate of Good Moral Character')
        self.goodMoral_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.goodMoral_window.after(200, lambda: self.goodMoral_window.iconbitmap(self.iconPath))
        width = 400
        height = 305
        x_axis, y_axis = self._center_window(width, height)
        self.goodMoral_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))
        self.goodMoral_window.transient(self)
        self.goodMoral_window.grab_set()

        self.goodMoral_window.configure(
            fg_color=self.RESIDENTS_CONTENT_BG
        )

        # CREATE WIDGET
        frame_goodMoral = CTkFrame(
            self.goodMoral_window,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        label_reason = CTkLabel(
            frame_goodMoral,
            text='Request Reason',
            font=CONTENT_FONT,
        )
        entry_reason = CTkEntry(
            frame_goodMoral,
            width=300,
            font=CONTENT_FONT,
        )
        label_ctc = CTkLabel(
            frame_goodMoral,
            text='Community Tax Cert No.',
            font=CONTENT_FONT,
        )
        entry_ctc = CTkEntry(
            frame_goodMoral,
            width=300,
            font=CONTENT_FONT,
        )
        label_ctc_date = CTkLabel(
            frame_goodMoral,
            text='Date Issued',
            font=CONTENT_FONT,
        )
        entry_ctc_date = CTkEntry(
            frame_goodMoral,
            width=300,
            font=CONTENT_FONT,
        )
        submit_button = CTkButton(
            frame_goodMoral,
            text='CONFIRM',
            font=CONTENT_FONT,
            width=100,
            height=40,
            command=lambda: self.finalize_goodMoral(
                resident_fullName,
                resident_purok,
                resident_sex,
                resident_status,
                entry_reason.get(),
                entry_ctc.get(),
                entry_ctc_date.get(),
                barangayCaptain
            )
        )

        # CREATE LAYOUT
        frame_goodMoral.pack(anchor='center')
        label_reason.pack(anchor='nw', pady=(15, 5))
        entry_reason.pack(anchor='nw', pady=(2, 5))
        label_ctc.pack(anchor='nw', pady=(10, 5))
        entry_ctc.pack(anchor='nw', pady=(2, 5))
        label_ctc_date.pack(anchor='nw', pady=(10, 5))
        entry_ctc_date.pack(anchor='nw', pady=(2, 10))
        submit_button.pack(anchor='center')

    # Finalize Good Moral Parameters and Values
    def finalize_goodMoral(self, fullname, purok, sex, resident_status, reason, ctc, ctc_date, captain):
        if not reason or reason == '':
            messagebox.showwarning('Empty Data', 'Reason cannot be Empty!')
            return
        if not ctc or ctc == '':
            messagebox.showwarning('Empty Data', 'Community Tax Cert No. cannot be Empty!')
            return
        if not ctc_date or ctc_date == '':
            messagebox.showwarning('Empty Data', 'Date Issued cannot be Empty!')
            return

        if not messagebox.askokcancel(
            "Confirmation", 
            f"Are you sure you want to confirm with,\nReason:'{reason}'\nCTC:'{ctc}'\nDate Issued:'{ctc_date}'"
            ):
            return

        self.select_doc_window.grab_release()
        self.select_doc_window.destroy()
        self.goodMoral_window.grab_release()
        self.goodMoral_window.destroy()

        messagebox.showinfo('Processing', 'Generating Document, Please wait...')
        process = multiprocessing.Process(
            target=do_certificateOfGoodMoral,
            args=(fullname, purok, sex, resident_status, reason, ctc, ctc_date, captain)
        )
        process.start()
        log_generate_residents_doc(ACTIVE_USERNAME, "Certificate of Good Moral Character",
                                   get_formatted_datetime(), fullname)

    # Generate First Time Job Seekers
    def generate_jobSeeker(self):
        if not check_officials():
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return

        resident_data = self.get_residentData()
        if resident_data[0] == '':
            messagebox.showwarning(
                'Empty Data', 'There is no Resident Selected!')
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return
        resident_fullName_first = residentFullName(
            'fullName', resident_data[3], resident_data[4], resident_data[2], resident_data[5]
        )
        resident_fullName_second = residentFullName(
            'name', resident_data[3], resident_data[4], resident_data[2], resident_data[5]
        )
        resident_purok = resident_data[1]
        resident_age = resident_data[6]
        resident_sex = resident_data[7]
        barangayCaptain = get_barangay_captain('name')

        self.jobSeeker_window = CTkToplevel(self)
        self.jobSeeker_window.title('Barangay Certification: First Time Job Seekers Act')
        self.jobSeeker_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.jobSeeker_window.after(200, lambda: self.jobSeeker_window.iconbitmap(self.iconPath))
        width = 400
        height = 160
        x_axis, y_axis = self._center_window(width, height)
        self.jobSeeker_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))
        self.jobSeeker_window.transient(self)
        self.jobSeeker_window.grab_set()
        
        self.jobSeeker_window.configure(
            fg_color=self.RESIDENTS_CONTENT_BG
        )

        # CREATE WIDGET
        frame_jobSeeker = CTkFrame(
            self.jobSeeker_window,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        label_witness = CTkLabel(
            frame_jobSeeker,
            text='Kagawad Witness',
            font=CONTENT_FONT,
        )
        kagawad_list = get_barangay_kagawad()
        entry_witness = CTkComboBox(
            frame_jobSeeker,
            width=300,
            font=CONTENT_FONT,
            values=kagawad_list,
            state='readonly'
        )
        entry_witness.set(kagawad_list[0])
        submit_button = CTkButton(
            frame_jobSeeker,
            text='CONFIRM',
            font=CONTENT_FONT,
            width=100,
            height=40,
            command=lambda: self.finalize_jobSeeker(
                resident_fullName_first,
                resident_fullName_second,
                resident_purok,
                resident_age,
                resident_sex,
                entry_witness.get(),
                barangayCaptain
            )
        )

        # CREATE LAYOUT
        frame_jobSeeker.pack(anchor='center')
        label_witness.pack(anchor='nw', pady=(15, 5))
        entry_witness.pack(anchor='nw', pady=(2, 5))
        submit_button.pack(anchor='center')

    # Finalize First Time Job Seekers Parameters and Values
    def finalize_jobSeeker(self, fullname_first, fullname_second, purok, age, sex, witness, captain):
        if not witness or witness == '':
            messagebox.showwarning('Empty Data', 'Reason cannot be Empty!')
            return

        if not messagebox.askokcancel("Confirmation", f"Are you sure you want to confirm with,\nWitness:'{witness}'"):
            return

        self.select_doc_window.grab_release()
        self.select_doc_window.destroy()
        self.jobSeeker_window.grab_release()
        self.jobSeeker_window.destroy()

        messagebox.showinfo('Processing', 'Generating Document, Please wait...')
        process = multiprocessing.Process(
            target=do_jobSeeker,
            args=(
                fullname_first,
                fullname_second,
                purok,
                age,
                sex,
                witness,
                captain
            )
        )
        process.start()
        log_generate_residents_doc(ACTIVE_USERNAME, "Barangay Certification: First Time Job Seeker",
                                   get_formatted_datetime(), fullname_second)

    # Generate Barangay Clearance
    def generate_barangayClearance(self):
        if not check_officials():
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return

        resident_data = self.get_residentData()
        if resident_data[0] == '':
            messagebox.showwarning(
                'Empty Data', 'There is no Resident Selected!')
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return
        resident_fullName = residentFullName(
            'fullName', resident_data[3], resident_data[4], resident_data[2], resident_data[5]
        )
        resident_purok = resident_data[1]
        resident_sex = resident_data[7]

        self.barangayClearance_window = CTkToplevel(self)
        self.barangayClearance_window.title('Barangay Clearance')
        self.barangayClearance_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.barangayClearance_window.after(200, lambda: self.barangayClearance_window.iconbitmap(self.iconPath))
        width = 400
        height = 390
        x_axis, y_axis = self._center_window(width, height)
        self.barangayClearance_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))
        self.barangayClearance_window.transient(self)
        self.barangayClearance_window.grab_set()
        
        self.barangayClearance_window.configure(
            fg_color=self.RESIDENTS_CONTENT_BG
        )

        # CREATE WIDGET
        frame_barangayClearance = CTkFrame(
            self.barangayClearance_window,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        label_reason = CTkLabel(
            frame_barangayClearance,
            text='Request Reason',
            font=CONTENT_FONT,
        )
        entry_reason = CTkEntry(
            frame_barangayClearance,
            width=300,
            font=CONTENT_FONT,
        )
        label_ctc = CTkLabel(
            frame_barangayClearance,
            text='Community Tax Cert No.',
            font=CONTENT_FONT,
        )
        entry_ctc = CTkEntry(
            frame_barangayClearance,
            width=300,
            font=CONTENT_FONT,
        )
        label_ctc_date = CTkLabel(
            frame_barangayClearance,
            text='Date Issued',
            font=CONTENT_FONT,
        )
        entry_ctc_date = CTkEntry(
            frame_barangayClearance,
            width=300,
            font=CONTENT_FONT,
        )
        label_officer = CTkLabel(
            frame_barangayClearance,
            text='Officer of the Day',
            font=CONTENT_FONT,
        )
        officer_list = ["None"]
        for item in get_barangay_kagawad():
            officer_list.append(item)
        entry_officer = CTkComboBox(
            frame_barangayClearance,
            width=300,
            font=CONTENT_FONT,
            values=officer_list,
            state='readonly',
        )
        entry_officer.set(officer_list[0])
        submit_button = CTkButton(
            frame_barangayClearance,
            text='CONFIRM',
            font=CONTENT_FONT,
            width=100,
            height=40,
            command=lambda: self.finalize_barangayClearance(
                resident_fullName,
                resident_purok,
                resident_sex,
                entry_reason.get(),
                entry_ctc.get(),
                entry_ctc_date.get(),
                entry_officer.get()
            )
        )

        # CREATE LAYOUT
        frame_barangayClearance.pack(anchor='center')
        label_reason.pack(anchor='nw', pady=(15, 5))
        entry_reason.pack(anchor='nw', pady=(2, 5))
        label_ctc.pack(anchor='nw', pady=(10, 5))
        entry_ctc.pack(anchor='nw', pady=(2, 5))
        label_ctc_date.pack(anchor='nw', pady=(10, 5))
        entry_ctc_date.pack(anchor='nw', pady=(2, 5))
        label_officer.pack(anchor='nw', pady=(10, 5))
        entry_officer.pack(anchor='nw', pady=(2, 10))
        submit_button.pack(anchor='center')

    def finalize_barangayClearance(self, fullname, purok, sex, reason, ctc, ctc_date, officer):
        if not reason or reason == '':
            messagebox.showwarning('Empty Data', 'Reason cannot be Empty!')
            return
        if not ctc or ctc == '':
            messagebox.showwarning('Empty Data', 'Community Tax Cert No. cannot be Empty!')
            return
        if not ctc_date or ctc_date == '':
            messagebox.showwarning('Empty Data', 'Date Issued cannot be Empty!')
            return

        if not messagebox.askokcancel(
            "Confirmation", 
            f"Are you sure you want to confirm with,\nReason:'{reason}'\nCTC:'{ctc}'\nOfficer:'{officer}'\nDate Issued:'{ctc_date}'"
            ):
            return

        self.select_doc_window.grab_release()
        self.select_doc_window.destroy()
        self.barangayClearance_window.grab_release()
        self.barangayClearance_window.destroy()

        if officer == 'None':
            messagebox.showinfo('Processing', 'Generating Document, Please wait...')
            process = multiprocessing.Process(
                target=do_barangayClearance,
                args=(
                    fullname,
                    purok,
                    sex,
                    reason,
                    ctc,
                    ctc_date
                )
            )
            process.start()
        else:   
            messagebox.showinfo('Processing', 'Generating Document, Please wait...')
            process = multiprocessing.Process(
                target=do_barangayClearance_on_duty,
                args=(
                    fullname,
                    purok,
                    sex,
                    reason,
                    ctc,
                    ctc_date,
                    officer
                )
            )
            process.start()
        log_generate_residents_doc(ACTIVE_USERNAME, "Barangay Clearance", get_formatted_datetime(), fullname)

    def generate_barangayResidency(self):
        if not check_officials():
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return

        resident_data = self.get_residentData()
        if resident_data[0] == '':
            messagebox.showwarning(
                'Empty Data', 'There is no Resident Selected!')
            self.select_doc_window.grab_release()
            self.select_doc_window.destroy()
            return
        resident_fullName = residentFullName(
            'fullName', resident_data[3], resident_data[4], resident_data[2], resident_data[5]
        )
        resident_purok = resident_data[1]
        resident_sex = resident_data[7]

        self.barangayResidency_window = CTkToplevel(self)
        self.barangayResidency_window.title('Barangay Residency')
        self.barangayResidency_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.barangayResidency_window.after(200, lambda: self.barangayResidency_window.iconbitmap(self.iconPath))
        width = 400
        height = 250
        x_axis, y_axis = self._center_window(width, height)
        self.barangayResidency_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))
        self.barangayResidency_window.transient(self)
        self.barangayResidency_window.grab_set()
        
        self.barangayResidency_window.configure(
            fg_color=self.RESIDENTS_CONTENT_BG
        )

        # CREATE WIDGET
        frame_barangayResidency = CTkFrame(
            self.barangayResidency_window,
            fg_color=self.RESIDENTS_CONTENT_BG
        )
        label_reason = CTkLabel(
            frame_barangayResidency,
            text='Request Reason',
            font=CONTENT_FONT,
        )
        entry_reason = CTkEntry(
            frame_barangayResidency,
            width=300,
            font=CONTENT_FONT,
        )
        label_ctc = CTkLabel(
            frame_barangayResidency,
            text='Community Tax Cert No.',
            font=CONTENT_FONT,
        )
        entry_ctc = CTkEntry(
            frame_barangayResidency,
            width=300,
            font=CONTENT_FONT,
        )
        label_officer = CTkLabel(
            frame_barangayResidency,
            text='Officer of the Day',
            font=CONTENT_FONT,
        )
        officer_list = ["None"]
        for item in get_barangay_kagawad():
            officer_list.append(item)
        entry_officer = CTkComboBox(
            frame_barangayResidency,
            width=300,
            font=CONTENT_FONT,
            values=officer_list,
            state='readonly',
        )
        entry_officer.set(officer_list[0])
        submit_button = CTkButton(
            frame_barangayResidency,
            text='CONFIRM',
            font=CONTENT_FONT,
            width=100,
            height=40,
            command=lambda: self.finalize_barangayResidency(
                resident_fullName,
                resident_purok,
                resident_sex,
                entry_reason.get(),
                entry_officer.get(),
            )
        )

        # CREATE LAYOUT
        frame_barangayResidency.pack(anchor='center')
        label_reason.pack(anchor='nw', pady=(15, 5))
        entry_reason.pack(anchor='nw', pady=(2, 5))
        label_officer.pack(anchor='nw', pady=(15, 5))
        entry_officer.pack(anchor='nw', pady=(2, 10))
        submit_button.pack(anchor='center')

    def finalize_barangayResidency(self, fullname, purok, sex, reason, officer):
        if not reason or reason == '':
            messagebox.showwarning('Empty Data', 'Reason cannot be Empty!')
            return

        if not messagebox.askokcancel("Confirmation", f"Are you sure you want to confirm with,\nReason:'{reason}'\nOfficer:'{officer}'"):
            return

        self.select_doc_window.grab_release()
        self.select_doc_window.destroy()
        self.barangayResidency_window.grab_release()
        self.barangayResidency_window.destroy()

        if officer == 'None':
            messagebox.showinfo('Processing', 'Generating Document, Please wait...')
            process = multiprocessing.Process(
                target=do_barangayResidency,
                args=(
                    fullname,
                    purok,
                    sex,
                    reason
                )
            )
            process.start()
        else:
            messagebox.showinfo('Processing', 'Generating Document, Please wait...')
            process = multiprocessing.Process(
                target=do_barangayResidency_on_duty,
                args=(
                    fullname,
                    purok,
                    sex,
                    reason,
                    officer
                )
            )
            process.start()
        log_generate_residents_doc(ACTIVE_USERNAME, "Barangay Residency", get_formatted_datetime(), fullname)

    # Get all the data from the Form
    def get_residentData(self):
        # Name and Religion not capitalized due to different naming conventions
        temp_residentID = self.entry_residentID.get()
        temp_residentPurok = self.entry_residentPurok.get()
        temp_residentLastName = self.entry_residentLastName.get()
        temp_residentFirstName = self.entry_residentFirstName.get()
        temp_residentMiddleName = self.entry_residentMiddleName.get()
        temp_residentSuffix = self.entry_residentSuffix.get()
        temp_residentAge = self.entry_residentAge.get()
        temp_residentSex = self.entry_residentSex.get()
        temp_residentStatus = self.entry_residentStatus.get()
        temp_residentBlood = self.entry_residentBlood.get()
        temp_residentDateOfBirth = self.entry_residentDateOfBirth.get()
        temp_residentPlaceOfBirth = capitalize_sentence(self.entry_residentPlaceOfBirth.get())
        temp_residentOccupation = capitalize_sentence(self.entry_residentOccupation.get())
        temp_residentReligion = self.entry_residentReligion.get()
        temp_residentTribeEthnicity = capitalize_sentence(self.entry_residentTribeEthnicity.get())
        temp_residentEducation = capitalize_sentence(self.entry_residentEducation.get())
        temp_residentComelec = self.entry_residentComelec.get()
        temp_residentPhilsys = self.entry_residentPhilsys.get()
        temp_residentPWD = self.entry_residentPwd.get()
        temp_residentDisability = capitalize_sentence(self.entry_residentDisability.get())
        temp_residentSenior = self.entry_residentSenior.get()
        temp_residentSoloParent = self.entry_residentSoloParent.get()
        temp_residentKasambahay = self.entry_residentKasambahay.get()
        temp_resident4ps = self.entry_resident4ps.get()
        temp_residentSalt = capitalize_sentence(self.entry_residentSalt.get())
        temp_residentGarbage = capitalize_sentence(self.entry_residentGarbage.get())
        temp_residentAnimals = clean_sentence(self.entry_residentAnimals.get('1.0', END))
        temp_residentFarmer1stOrg = self.entry_residentFarmer_FirstOrg.get()
        temp_residentFarmer2ndOrg = self.entry_residentFarmer_LastOrg.get()
        temp_residentWater = capitalize_sentence(self.entry_residentWater.get())
        temp_residentFamily = capitalize_sentence(self.entry_residentFamilyPlan.get())
        temp_residentCR = capitalize_sentence(self.entry_residentCR.get())
        temp_residentResiStatus = capitalize_sentence(self.entry_status.get())

        temp_residentData = [
            temp_residentID, temp_residentPurok, temp_residentLastName, temp_residentFirstName, temp_residentMiddleName,
            temp_residentSuffix, temp_residentAge, temp_residentSex, temp_residentStatus, temp_residentBlood,
            temp_residentDateOfBirth, temp_residentPlaceOfBirth, temp_residentOccupation, temp_residentReligion, 
            temp_residentTribeEthnicity, temp_residentEducation, temp_residentComelec,
            temp_residentPhilsys, temp_residentPWD, temp_residentDisability, temp_residentSenior,
            temp_residentSoloParent, temp_residentKasambahay, temp_resident4ps, temp_residentSalt, temp_residentGarbage,
            temp_residentAnimals, temp_residentFarmer1stOrg, temp_residentFarmer2ndOrg, temp_residentWater,
            temp_residentFamily, temp_residentCR, temp_residentResiStatus
        ]

        return temp_residentData

    # Add Resident Button Function
    def save_resident(self):
        # Get all Data
        resident_data = self.get_residentData()

        # Check if Purok is empty
        if not resident_data[1]:
            messagebox.showwarning('Empty Field', 'Purok field is empty!')
            return
        # Check if Last Name is empty
        if not resident_data[2]:
            messagebox.showwarning('Empty Field', 'Last Name field is empty!')
            return
        # Check if First Name is empty
        if not resident_data[3]:
            messagebox.showwarning('Empty Field', 'First Name field is empty!')
            return
        # Check if Middle Name is empty
        if not resident_data[4]:
            messagebox.showwarning('Empty Field', 'Middle Name field is empty!')
            return
        # Check if Age is not Empty and within range of 0-150
        if not resident_data[6]:
            messagebox.showwarning('Empty Field', 'Age field is empty!')
            return
        if self.action_checkAge(resident_data[6]):
            return
        if 150 <= int(resident_data[6]) >= 0:
            messagebox.showwarning('Invalid Age', 'Age must be between 0 and 150!')
            return
        # Check if Sex is empty
        if not resident_data[7]:
            messagebox.showwarning("Invalid Entry", "Sex field is empty!")
            return
        # Check if Civil Status is empty
        if not resident_data[8]:
            messagebox.showwarning("Invalid Entry", "Civil Status field is empty!")
            return
        # Check if Blood Type is empty
        if not resident_data[9]:
            messagebox.showwarning("Invalid Entry", "Blood Type field is empty!")
            return
        # Check if Educational Level is empty
        if not resident_data[15]:
            messagebox.showwarning("Invalid Entry", "Educational Level field is empty!")
            return
        # Check if Comelec is empty
        if not resident_data[16]:
            messagebox.showwarning("Invalid Entry", "Comelec field is empty!")
            return
        # Check if Philsys is empty
        if not resident_data[17]:
            messagebox.showwarning("Invalid Entry", "Philsys field is empty!")
            return
        # Check if PWD is empty
        if not resident_data[18]:
            messagebox.showwarning("Invalid Entry", "PWD field is empty!")
            return
        # Check if Senior Member is empty
        if not resident_data[20]:
            messagebox.showwarning("Invalid Entry", "Senior Member field is empty!")
            return
        # Check if Solo Parent is empty
        if not resident_data[21]:
            messagebox.showwarning("Invalid Entry", "Solo Parent field is empty!")
            return
        # Check if 4PS is empty
        if not resident_data[23]:
            messagebox.showwarning("Invalid Entry", "4PS field is empty!")
            return
        # Check if Farmers: FA is empty
        if not resident_data[27]:
            messagebox.showwarning("Invalid Entry", "Farmers: FA field is empty!")
            return
        # Check if Farmers: RSBSA is empty
        if not resident_data[28]:
            messagebox.showwarning("Invalid Entry", "Farmers: RSBSA field is empty!")
            return
        # Check if Status is set
        if not resident_data[32]:
            messagebox.showwarning("Invalid Entry", "Resident status is empty!")
            return
        
        resident_name = get_resident_fullname(resident_data[3], resident_data[4], resident_data[2], resident_data[5])

        if check_name_exists(
                resident_data[2],
                resident_data[4],
                resident_data[3],
                resident_data[5],
        ):
            if not messagebox.askokcancel("Confirmation", "A record with the same name already exists.\nDo you wish to continue?"):
                return

        # Ask to finalize resident addition
        if messagebox.askokcancel("Add Resident", "Are you sure you want to add this Resident?"):
            insert_data(resident_data)

            log_profiling(get_formatted_datetime(), "SAVE", resident_name, "New Resident Saved", ACTIVE_USERNAME)

            messagebox.showinfo("Success", "Resident added successfully.")

            self.remove_treeSelected()
            self.clear_residentForm()
            self.populate_residentsTree()
        else:
            return

    def action_checkAge(self, age):
        try:
            int_variable = int(age)
        except ValueError:
            self.entry_residentAge.delete(0, END)
            messagebox.showwarning("Input Error", "Please enter a valid age!")
            return True

    # Update Resident Button Function
    def update_resident(self):
        # Get all Data
        resident_data = self.get_residentData()

        if not resident_data[0]:
            messagebox.showwarning('Empty Field', 'No Resident Selected!')
            return
        # Check if Purok is empty
        if not resident_data[1]:
            messagebox.showwarning('Empty Field', 'Purok field is empty!')
            return
        # Check if Last Name is empty
        if not resident_data[2]:
            messagebox.showwarning('Empty Field', 'Last Name field is empty!')
            return
        # Check if First Name is empty
        if not resident_data[3]:
            messagebox.showwarning('Empty Field', 'First Name field is empty!')
            return
        # Check if Middle Name is empty
        if not resident_data[4]:
            messagebox.showwarning('Empty Field', 'Middle Name field is empty!')
            return
        # Check if Age is not Empty and within range of 0-150
        if not resident_data[6]:
            messagebox.showwarning('Empty Field', 'Age field is empty!')
            return
        if self.action_checkAge(resident_data[6]):
            return
        if 150 <= int(resident_data[6]) >= 0:
            messagebox.showwarning('Invalid Age', 'Age must be between 0 and 150!')
            return
        # Check if Sex is empty
        if not resident_data[7]:
            messagebox.showwarning("Invalid Entry", "Sex field is empty!")
            return
        
        resident_name = get_resident_fullname(resident_data[3], resident_data[4], resident_data[2], resident_data[5])
        database_resident_data = get_resident_data(resident_data[0])

        if resident_data == database_resident_data:
            messagebox.showinfo("Update Failed", "No Changes in the information Detected")
            return

        attributes = ["resident_id", "purok", "lastname", "firstname", "middlename", "suffix", "age", "sex", "civil_status", "blood_type", "dob", "place_of_birth", "occupation", "religion", "tribe_and_ethnicity", "educational_status", "comelec", "philsys",  "pwd_member", "pwd_disability", "senior_member", "solo_parent_member", "kasambahay_salary", "four_ps", "salt_used", "garbage_disposal", "animals", "farmers_membership_FA", "farmers_membership_RSBSA", "source_of_water", "family_planning_used", "types_of_cr", "resident_status"]
        proper_attributes = ["Resident ID", "Purok", "Last Name", "First Name", "Middle Name", "Suffix", "Age", "Sex", "Civil Status", "Blood Type", "Date of Birth", "Place of Birth", "Occupation", "Religion", "Tribe and Ethnicity", "Educational Status", "COMELEC", "PHILSYS",  "PWD Member", "PWD Disability", "Senior Member", "Solo Parent Member", "Kasambahay Salary", "4ps", "Salt Used", "Garbage Disposal", "Animals", "Farmers Membership: FA", "Farmers Membership: RSBSA", "Source of Water", "Family Planning Used", "Types of CR", "Resident Status"]

        attributes_changed = []
        proper_attributes_changed = []

        for i in range(len(attributes)):
            if resident_data[i]!= database_resident_data[i]:
                attributes_changed.append(attributes[i])
                proper_attributes_changed.append(proper_attributes[i])

        attributes_changed = ", ".join(map(str, attributes_changed))
        proper_attributes_changed = ", ".join(map(str, proper_attributes_changed))

        if messagebox.askokcancel(
                "Update Resident",
                f"Are you sure you want to make changes on this Resident?\nChanges: {proper_attributes_changed}"
        ):
            update_data(resident_data)
            self.remove_treeSelected()
            self.clear_residentForm()
            self.hide_edit_form()

            messagebox.showinfo("Update Success", "Resident information has been updated.")
            log_profiling(get_formatted_datetime(), "UPDATE", resident_name, attributes_changed, ACTIVE_USERNAME)

            search_data = self.entry_searchBar.get()
            if search_data == "":
                self.populate_residentsTree()
                return

            self.update_tree_residentsData(search_data)
        else:
            return
        
    # Center Top Level Windows
    def _center_screen(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        return x_axis, y_axis

    # Populate or Refresh Treeview
    def populate_residentsTree(self):
        for item in self.tree_residentsData.get_children():
            self.tree_residentsData.delete(item)

        global count
        count = 0
        for record in get_residentsData(
            self.get_selected_purok(),
            self.filter_age_from.get(),
            self.filter_age_to.get(),
            self.filter_gender_male.get(),
            self.filter_gender_female.get(),
            self.filter_comelec_registered.get(),
            self.filter_comelec_not_registered.get(),
            self.filter_status_single.get(),
            self.filter_status_married.get(),
            self.filter_status_widowed.get(),
            self.filter_status_separated.get(),
            self.filter_blood_A_plus.get(),
            self.filter_blood_A_minus.get(),
            self.filter_blood_B_plus.get(),
            self.filter_blood_B_minus.get(),
            self.filter_blood_AB_plus.get(),
            self.filter_blood_AB_minus.get(),
            self.filter_blood_O_plus.get(),
            self.filter_blood_O_minus.get(),
            self.filter_blood_unknown.get(),
            self.filter_education_no_grade.get(),
            self.filter_education_early_educ.get(),
            self.filter_education_elementary.get(),
            self.filter_education_elementary_grad.get(),
            self.filter_education_high.get(),
            self.filter_education_high_grad.get(),
            self.filter_education_college.get(),
            self.filter_education_college_grad.get(),
            self.filter_education_bacca.get(),
            self.filter_philsys_registered.get(),
            self.filter_philsys_not_registered.get(),
            self.filter_membership_pwd.get(),
            self.filter_membership_senior.get(),
            self.filter_membership_solo.get(),
            self.filter_membership_four.get(),
            self.filter_membership_fa.get(),
            self.filter_membership_rsbsa.get(),
            self.filter_status_active.get(),
            self.filter_status_transferred.get(),
            self.filter_status_deceased.get(),
            self.filter_status_transient.get()
            ):
            self.tree_residentsData.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8],
                    record[9], record[10], record[11],record[12], record[13], record[14], record[15], record[16], 
                    record[17], record[18], record[19], record[20], record[21], record[22], record[23], record[24], 
                    record[25], record[26], record[27], record[28], record[29], record[30], record[31], record[32],
                )
            )
            count += 1

    # Display in Form the selected data in the Treeview
    def select_record(self, e):
        self.unlock_form()
        self.clear_residentForm()
        selected = self.tree_residentsData.focus()
        values = self.tree_residentsData.item(selected, 'values')

        if not values:
            return

        self.entry_residentDateOfBirth.delete(0, END)
        self.entry_residentDateOfBirth.insert(0, values[8])

        self.var_selected_record.set(f"{residentFullName('fullName', values[4], values[3], values[2], values[5])}")

        self.entry_residentID.insert(0, values[0])
        self.entry_residentPurok.set(values[1])
        self.entry_residentLastName.insert(0, values[2])
        self.entry_residentMiddleName.insert(0, values[3])
        self.entry_residentFirstName.insert(0, values[4])
        self.entry_residentSuffix.insert(0, values[5])
        self.entry_residentAge.delete(0, END)
        self.entry_residentAge.insert(0, values[6])
        self.entry_residentSex.set(values[7])
        self.entry_residentStatus.set(values[8])
        self.entry_residentBlood.set(values[9])
        self.entry_residentDateOfBirth.set_date(values[10])
        self.entry_residentPlaceOfBirth.insert(0, values[11])
        self.entry_residentOccupation.insert(0, values[12])
        self.entry_residentReligion.insert(0, values[13])
        self.entry_residentTribeEthnicity.insert(0, values[14])
        self.entry_residentEducation.set(values[15])
        self.entry_residentComelec.set(values[16])
        self.entry_residentPhilsys.set(values[17])
        self.entry_residentPwd.set(values[18])
        if values[18].lower() == "yes":
            self.entry_residentDisability.configure(state='normal')
            self.disability_placeholder.set(values[19])
        self.entry_residentSenior.set(values[20])
        self.entry_residentSoloParent.set(values[21])
        self.entry_residentKasambahay.insert(0, values[22])
        self.entry_resident4ps.set(values[23])
        self.entry_residentSalt.insert(0, values[24])
        self.entry_residentGarbage.insert(0, values[25])
        self.entry_residentAnimals.insert('1.0', values[26])
        self.entry_residentFarmer_FirstOrg.set(values[27])
        self.entry_residentFarmer_LastOrg.set(values[28])
        self.entry_residentWater.insert(0, values[29])
        self.entry_residentFamilyPlan.insert(0, values[30])
        self.entry_residentCR.insert(0, values[31])
        self.entry_status.set(values[32])

        self.hide_edit_form()
        self.show_edit_form()
        self.lock_form()

    def show_edit_form(self):
        self.check_edit_form.grid(
            row=0, column=1, sticky='e', padx=(0, 10)
        )

    def hide_edit_form(self):
        self.check_edit_form_var.set('locked')
        self.check_edit_form.grid_remove()

    # Search the Residents Data Treeview
    def on_search(self, e):
        search_data = self.search_data.get()
        self.update_tree_residentsData(search_data)

    def update_tree_residentsData(self, search_data):
        for item in self.tree_residentsData.get_children():
            self.tree_residentsData.delete(item)

        search_filter = self.filter_search.get()

        for item in get_residentsData(
            self.get_selected_purok(),
            self.filter_age_from.get(),
            self.filter_age_to.get(),
            self.filter_gender_male.get(),
            self.filter_gender_female.get(),
            self.filter_comelec_registered.get(),
            self.filter_comelec_not_registered.get(),
            self.filter_status_single.get(),
            self.filter_status_married.get(),
            self.filter_status_widowed.get(),
            self.filter_status_separated.get(),
            self.filter_blood_A_plus.get(),
            self.filter_blood_A_minus.get(),
            self.filter_blood_B_plus.get(),
            self.filter_blood_B_minus.get(),
            self.filter_blood_AB_plus.get(),
            self.filter_blood_AB_minus.get(),
            self.filter_blood_O_plus.get(),
            self.filter_blood_O_minus.get(),
            self.filter_blood_unknown.get(),
            self.filter_education_no_grade.get(),
            self.filter_education_early_educ.get(),
            self.filter_education_elementary.get(),
            self.filter_education_elementary_grad.get(),
            self.filter_education_high.get(),
            self.filter_education_high_grad.get(),
            self.filter_education_college.get(),
            self.filter_education_college_grad.get(),
            self.filter_education_bacca.get(),
            self.filter_philsys_registered.get(),
            self.filter_philsys_not_registered.get(),
            self.filter_membership_pwd.get(),
            self.filter_membership_senior.get(),
            self.filter_membership_solo.get(),
            self.filter_membership_four.get(),
            self.filter_membership_fa.get(),
            self.filter_membership_rsbsa.get(),
            self.filter_status_active.get(),
            self.filter_status_transferred.get(),
            self.filter_status_deceased.get(),
            self.filter_status_transient.get(),
        ):
            if search_filter == "Default":
                if (search_data.lower() in item[1].lower() or
                    search_data.lower() in item[2].lower() or
                    search_data.lower() in item[3].lower() or
                    search_data.lower() in item[4].lower() or
                    search_data.lower() in item[5].lower() or
                    search_data.lower() in item[7].lower() or
                    search_data.lower() in item[8].lower() or
                    search_data.lower() in item[9].lower() or
                    search_data.lower() in item[10].lower() or
                    search_data.lower() in item[11].lower() or
                    search_data.lower() in item[12].lower() or
                    search_data.lower() in item[13].lower() or
                    search_data.lower() in item[14].lower() or
                    search_data.lower() in item[15].lower() or
                    search_data.lower() in item[16].lower() or
                    search_data.lower() in item[17].lower() or
                    search_data.lower() in item[18].lower() or
                    search_data.lower() in item[19].lower() or
                    search_data.lower() in item[20].lower() or
                    search_data.lower() in item[21].lower() or
                    search_data.lower() in item[22].lower() or
                    search_data.lower() in item[23].lower() or
                    search_data.lower() in item[24].lower() or
                    search_data.lower() in item[25].lower() or
                    search_data.lower() in item[26].lower() or
                    search_data.lower() in item[27].lower() or
                    search_data.lower() in item[28].lower() or
                    search_data.lower() in item[29].lower() or
                    search_data.lower() in item[30].lower() or
                    search_data.lower() in item[31].lower() or
                    search_data.lower() in item[32].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Last Name":
                if (search_data.lower() in item[2].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Middle Name":
                if (search_data.lower() in item[3].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "First Name":
                if (search_data.lower() in item[4].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Suffix":
                if (search_data.lower() in item[5].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Date of Birth":
                if (search_data.lower() in item[10].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Place of Birth":
                if (search_data.lower() in item[11].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Occupation":
                if (search_data.lower() in item[12].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Religion":
                if (search_data.lower() in item[13].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Tribe and Ethnicity":
                if (search_data.lower() in item[14].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "PWD Disability":
                if (search_data.lower() in item[19].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Kasambahay":
                if (search_data.lower() in item[22].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Salt Used":
                if (search_data.lower() in item[24].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Garbage Disposal":
                if (search_data.lower() in item[25].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Animals":
                if (search_data.lower() in item[26].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Source of Water":
                if (search_data.lower() in item[29].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Family Planning":
                if (search_data.lower() in item[30].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)
            elif search_filter == "Types of CR":
                if (search_data.lower() in item[31].lower()):
                    self.tree_residentsData.insert('', 'end', values=item)

    # Deselect the selected record in the Treeview
    def remove_treeSelected(self):
        tree_selectedItem = self.tree_residentsData.selection()
        if tree_selectedItem:
            self.tree_residentsData.selection_remove(tree_selectedItem)

    # Clear Form combined function
    def clear_residentFormBtn(self, invoked):
        form_values = self.get_residentData()
        form_values = [value for value in form_values if value != ""]

        if len(form_values) <= 1:
            messagebox.showwarning("Empty Form", "There's nothing to clear!")
            return

        if invoked == 'clearBtn':
            response = messagebox.askokcancel(
                "Clear Form", "Are you sure you want to clear the form?"
            )
            if not response:
                return

            self.remove_treeSelected()
            self.unlock_form()
            self.clear_residentForm()
            self.hide_edit_form()

    # Clear Resident Form Button
    def clear_residentForm(self):
        self.var_selected_record.set("")
        self.entry_residentID.delete(0, END)
        self.entry_residentPurok.set("")
        self.entry_residentLastName.delete(0, END)
        self.entry_residentFirstName.delete(0, END)
        self.entry_residentMiddleName.delete(0, END)
        self.entry_residentSuffix.delete(0, END)
        self.entry_residentAge.delete(0, END)
        self.entry_residentSex.set("")
        self.entry_residentStatus.set("")
        self.entry_residentBlood.set("")
        self.entry_residentDateOfBirth.set_date(get_date_today())
        self.entry_residentPlaceOfBirth.delete(0, END)
        self.entry_residentOccupation.delete(0, END)
        self.entry_residentReligion.delete(0, END)
        self.entry_residentTribeEthnicity.delete(0, END)
        self.entry_residentEducation.set("")
        self.entry_residentComelec.set("")
        self.entry_residentPhilsys.set("")
        self.entry_residentPwd.set("")
        self.disability_placeholder.set("")
        self.entry_residentDisability.configure(state='disabled')
        self.entry_residentSenior.set("")
        self.entry_residentSoloParent.set("")
        self.entry_residentKasambahay.delete(0, END)
        self.entry_resident4ps.set("")
        self.entry_residentSalt.delete(0, END)
        self.entry_residentGarbage.delete(0, END)
        self.entry_residentAnimals.delete('1.0', END)
        self.entry_residentFarmer_FirstOrg.set("")
        self.entry_residentFarmer_LastOrg.set("")
        self.entry_residentWater.delete(0, END)
        self.entry_residentFamilyPlan.delete(0, END)
        self.entry_residentCR.delete(0, END)
        self.entry_status.set("")

    # Check if Age entered is a number
    def check_Age(self, e):
        variable = self.entry_residentAge.get()
        if variable == '':
            return
        try:
            int_variable = int(variable)
        except ValueError:
            self.entry_residentAge.delete(0, END)
            messagebox.showinfo("Input Error", "Please input a valid age.")
            self.entry_residentAge.focus()
            return

    # Check the PWD Membership
    def on_pwd_select(self, choice):
        if choice == 'YES':
            self.entry_residentDisability.configure(state='normal')
        else:
            self.disability_placeholder.set("")
            self.entry_residentDisability.configure(state='disabled')

    def check_birthDate(self, e):
        selected_date = self.entry_residentDateOfBirth.get_date()
        today = datetime.today()

        age = today.year - selected_date.year - ((today.month, today.day) < (selected_date.month, selected_date.day))
        
        if self.entry_residentAge.get() == "" or int(age) != int(self.entry_residentAge.get()):
            self.entry_residentAge.delete(0, END)
            self.entry_residentAge.insert(0, str(age))

        if not validate_birthDate(self.entry_residentDateOfBirth.get()):
            messagebox.showinfo("Input Error", "Date cannot be greater than today!")
            self.entry_residentDateOfBirth.set_date(get_date_today())
            return

    def view_statistics(self):
        self.toplevel_window = StatisticsPage(self)  # create window if its None or destroyed


class StatisticsPage(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_main_window()
        self.create_constants()
        self.create_widgets()
        self.create_layout()
        self.on_active_page = None
        self.combined_action('Purok')

    def _setup_main_window(self):
        self.title('Statistics')
        self.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(self.iconPath))
        self._center_screen(1000, 700)
        self.grab_set()
        self.focus()

    def _center_screen(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        self.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))

    def create_constants(self):
        # Dashboard Buttons
        self.BTN_INACTIVE = '#CED4DA'
        self.BTN_ACTIVE = '#495057'
        self.TEXT_INACTIVE = '#000'
        self.TEXT_ACTIVE = '#FAFAFA'
        self.BTN_HOVER = '#495057'
        self.BTN_WIDTH = 100
        self.BTN_HEIGHT = 50

        # Pie Chart Title
        self.title_font = {'fontsize': 22, 'fontweight': 'bold', 'fontname': 'Arial'}

    def create_widgets(self):
        self.frame_dashboard = CTkFrame(self)
        self.frame_content = CTkFrame(self)
        self.frame_content.configure(fg_color='#FFF')
        self.btn_purok = CTkButton(
            self.frame_dashboard,
            text='PUROK',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('Purok')
        )
        self.btn_sex = CTkButton(
            self.frame_dashboard,
            text='SEX',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('Sex')
        )
        self.btn_age = CTkButton(
            self.frame_dashboard,
            text='AGE',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('Age')
        )
        self.btn_education = CTkButton(
            self.frame_dashboard,
            text='EDUCATIONAL\nLEVEL',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('Educational')
        )
        self.btn_comelec = CTkButton(
            self.frame_dashboard,
            text='COMELEC',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('Comelec')
        )
        self.btn_philsys = CTkButton(
            self.frame_dashboard,
            text='PHILSYS',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('Philsys')
        )
        self.btn_pwd = CTkButton(
            self.frame_dashboard,
            text='PWD',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('Pwd')
        )
        self.btn_senior = CTkButton(
            self.frame_dashboard,
            text='SENIOR\nCITIZEN',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('Senior')
        )
        self.btn_soloParent = CTkButton(
            self.frame_dashboard,
            text='SOLO PARENT',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('SoloParent')
        )
        self.btn_4Ps = CTkButton(
            self.frame_dashboard,
            text='4Ps',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('4Ps')
        )
        self.btn_farmers = CTkButton(
            self.frame_dashboard,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            text='FARMERS\nMEMBERSHIP',
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
            command=lambda: self.combined_action('Farmers')
        )

    def create_layout(self):
        self.frame_dashboard.pack(side='left', fill='y', padx=10, pady=5)
        self.frame_content.pack(side='left', expand='true', fill='both', padx=(0, 5), pady=5)
        self.btn_purok.pack(anchor='w', pady=5)
        self.btn_sex.pack(anchor='w', pady=5)
        self.btn_age.pack(anchor='w', pady=5)
        self.btn_education.pack(anchor='w', pady=5)
        self.btn_comelec.pack(anchor='w', pady=5)
        self.btn_philsys.pack(anchor='w', pady=5)
        self.btn_pwd.pack(anchor='w', pady=5)
        self.btn_senior.pack(anchor='w', pady=5)
        self.btn_soloParent.pack(anchor='w', pady=5)
        self.btn_4Ps.pack(anchor='w', pady=5)
        self.btn_farmers.pack(anchor='w', pady=5)

    def combined_action(self, btn):
        if self.on_active_page == btn:
            return
        self.on_active_page = btn
        self.set_active(btn)
        self.update_content(btn)

    def set_active(self, btn):
        # Reset all buttons to inactive
        self.set_inactive()
        # Set clicked button to active state
        if btn == "Purok":
            self.btn_purok.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Sex":
            self.btn_sex.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Age":
            self.btn_age.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Educational":
            self.btn_education.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Comelec":
            self.btn_comelec.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Philsys":
            self.btn_philsys.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Pwd":
            self.btn_pwd.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Senior":
            self.btn_senior.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "SoloParent":
            self.btn_soloParent.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "4Ps":
            self.btn_4Ps.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )
        if btn == "Farmers":
            self.btn_farmers.configure(
                fg_color=self.BTN_ACTIVE,
                text_color=self.TEXT_ACTIVE,
                hover_color=self.BTN_HOVER,
            )

    def set_inactive(self):
        self.btn_purok.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_sex.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_age.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_education.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_comelec.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_philsys.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_pwd.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_senior.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_soloParent.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_4Ps.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )
        self.btn_farmers.configure(
            fg_color=self.BTN_INACTIVE,
            text_color=self.TEXT_INACTIVE,
            hover_color=self.BTN_HOVER,
        )

    def update_content(self, btn):
        for widget in self.frame_content.winfo_children():
            widget.destroy()
        if btn == "Purok":
            self.display_purok()
        elif btn == "Sex":
            self.display_sex()
        elif btn == "Age":
            self.display_age()
        elif btn == "Educational":
            self.display_educational()
        elif btn == "Comelec":
            self.display_comelec()
        elif btn == "Philsys":
            self.display_philsys()
        elif btn == "Pwd":
            self.display_pwd()
        elif btn == "Senior":
            self.display_senior()
        elif btn == "SoloParent":
            self.display_soloParent()
        elif btn == "4Ps":
            self.display_4Ps()
        elif btn == "Farmers":
            self.display_farmers()

    def display_purok(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content)
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        purok_data = {
            "labels": [
                "Vanda", "Walingwaling", "Bougainvillea", "Mercury", "Daisy",
                "Orchid", "Chrysanthemum", "Santan", "Rosas", "Sampaguita"
            ],
            "values": [],
            "count": []
        }
        for i in range(len(purok_data["labels"])):
            purok_data["values"].append(data["purok"][purok_data["labels"][i]]["percentage"])
            purok_data["count"].append(data["purok"][purok_data["labels"][i]]["count"])

        purok_data_frame = pd.DataFrame(purok_data)

        purok_data_frame = purok_data_frame[purok_data_frame["values"] != 0.00]

        purok_figure = plt.Figure(figsize=(6, 6), dpi=100)
        purok_ax = purok_figure.add_subplot(111)
        purok_ax.pie(
            purok_data_frame["values"],
            labels=purok_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99', '#ffd97d', '#8d99ae',
                    '#d9cab3', '#b0d0d3', '#dec0f1', '#f79d65', '#7e6c6c']
        )
        purok_ax.set_title("PERCENTAGE OF RESIDENTS PER PUROK", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(purok_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(frame_info, text='Specific Number of Residents per Purok', font=SEARCHBAR_FONT)
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        purok_vanda_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][0]} Population Count: {purok_data["count"][0]}',
            font=CONTENT_FONT
        )
        purok_walingwaling_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][1]} Population Count: {purok_data["count"][1]}',
            font=CONTENT_FONT
        )
        purok_bougainvillea_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][2]} Population Count: {purok_data["count"][2]}',
            font=CONTENT_FONT
        )
        purok_mercury_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][3]} Population Count: {purok_data["count"][3]}',
            font=CONTENT_FONT
        )
        purok_daisy_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][4]} Population Count: {purok_data["count"][4]}',
            font=CONTENT_FONT
        )
        purok_orchid_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][5]} Population Count: {purok_data["count"][5]}',
            font=CONTENT_FONT
        )
        purok_chrysanthenum_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][6]} Population Count: {purok_data["count"][6]}',
            font=CONTENT_FONT
        )
        purok_santan_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][7]} Population Count: {purok_data["count"][7]}',
            font=CONTENT_FONT
        )
        purok_rosas_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][8]} Population Count: {purok_data["count"][8]}',
            font=CONTENT_FONT
        )
        purok_sampaguita_info = CTkLabel(
            frame_info_content,
            text=f'Purok {purok_data["labels"][9]} Population Count: {purok_data["count"][9]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true')
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        purok_vanda_info.pack(anchor='nw', pady=(10, 10))
        purok_walingwaling_info.pack(anchor='nw', pady=(10, 10))
        purok_bougainvillea_info.pack(anchor='nw', pady=(10, 10))
        purok_mercury_info.pack(anchor='nw', pady=(10, 10))
        purok_daisy_info.pack(anchor='nw', pady=(10, 10))
        purok_orchid_info.pack(anchor='nw', pady=(10, 10))
        purok_chrysanthenum_info.pack(anchor='nw', pady=(10, 10))
        purok_santan_info.pack(anchor='nw', pady=(10, 10))
        purok_rosas_info.pack(anchor='nw', pady=(10, 10))
        purok_sampaguita_info.pack(anchor='nw', pady=(10, 20))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_sex(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content)
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        sex_data = {
            "labels": [
                "Male", "Female"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(sex_data["labels"])):
            sex_data["values"].append(data["sex"][0][sex_data["labels"][i].lower()]["percentage"])
            sex_data["count"].append(data["sex"][0][sex_data["labels"][i].lower()]["count"])

        sex_data_frame = pd.DataFrame(sex_data)

        sex_data_frame = sex_data_frame[sex_data_frame["values"] != 0.00]

        sex_figure = plt.Figure(figsize=(6, 6), dpi=100)
        sex_ax = sex_figure.add_subplot(111)
        sex_ax.pie(
            sex_data_frame["values"],
            labels=sex_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99']
        )
        sex_ax.set_title("PERCENTAGE OF RESIDENTS SEX", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(sex_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(frame_info, text='Specific Number of Residents per Sex', font=SEARCHBAR_FONT)
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        sex_male_info = CTkLabel(
            frame_info_content,
            text=f'{sex_data["labels"][0]} Population Count: {sex_data["count"][0]}',
            font=CONTENT_FONT
        )
        sex_female_info = CTkLabel(
            frame_info_content,
            text=f'{sex_data["labels"][1]} Population Count: {sex_data["count"][1]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true')
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        sex_male_info.pack(anchor='nw', pady=(10, 10))
        sex_female_info.pack(anchor='nw', pady=(10, 20))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_age(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content)
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        age_data = {
            "labels": [
                "Senior", "Legal", "Children", "New Born"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(age_data["labels"])):
            age_data["values"].append(data['age'][i][age_data["labels"][i]]['percentage'])
            age_data["count"].append(data['age'][i][age_data["labels"][i]]['count'])

        age_data_frame = pd.DataFrame(age_data)

        age_data_frame = age_data_frame[age_data_frame["values"] != 0.00]

        age_figure = plt.Figure(figsize=(6, 6), dpi=100)
        age_ax = age_figure.add_subplot(111)
        age_ax.pie(
            age_data_frame["values"],
            labels=age_data_frame["labels"],
            autopct='%1.2f%%',  # Corrected format string for percentages
            colors=['#a4ac86', '#a68a64', '#e7ad99']
        )
        age_ax.set_title("PERCENTAGE OF RESIDENTS AGE", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(age_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(frame_info, text='Specific Number of Residents per Age', font=SEARCHBAR_FONT)
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        age_senior_info = CTkLabel(
            frame_info_content,
            text=f'{age_data["labels"][0]} Population Count: {age_data["count"][0]}',
            font=CONTENT_FONT
        )
        age_legal_info = CTkLabel(
            frame_info_content,
            text=f'{age_data["labels"][1]} Population Count: {age_data["count"][1]}',
            font=CONTENT_FONT
        )
        age_minor_info = CTkLabel(
            frame_info_content,
            text=f'{age_data["labels"][2]} Population Count: {age_data["count"][2]}',
            font=CONTENT_FONT
        )
        age_baby_info = CTkLabel(
            frame_info_content,
            text=f'{age_data["labels"][3]} Population Count: {age_data["count"][3]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true')
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        age_senior_info.pack(anchor='nw', pady=(10, 10))
        age_legal_info.pack(anchor='nw', pady=(10, 10))
        age_minor_info.pack(anchor='nw', pady=(10, 10))
        age_baby_info.pack(anchor='nw', pady=(10, 20))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_educational(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content)
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        education_data = {
            "labels": [
                "Post Baccalaureate",
                "College Graduate",
                "College Level",
                "High School Graduate",
                "High School Level",
                "Elementary Graduate",
                "Elementary Level",
                "Early Childhood Education",
                "No Grade Reported"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(education_data["labels"])):
            education_data["values"].append(data['education'][i][education_data["labels"][i]]['percentage'])
            education_data["count"].append(data['education'][i][education_data["labels"][i]]['count'])

        education_data_frame = pd.DataFrame(education_data)

        education_data_frame = education_data_frame[education_data_frame["values"] != 0.00]

        education_figure = plt.Figure(figsize=(6, 6), dpi=100)
        education_ax = education_figure.add_subplot(111)
        education_ax.pie(
            education_data_frame["values"],
            labels=education_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99', '#ffd97d', '#8d99ae',
                    '#d9cab3', '#b0d0d3', '#dec0f1', '#f79d65', '#7e6c6c']
        )
        education_ax.set_title("PERCENTAGE OF RESIDENTS EDUCATIONAL LEVEL", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(education_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(
            frame_info,
            text='Specific Number of Residents per EDUCATIONAL LEVEL',
            font=SEARCHBAR_FONT
        )
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        education_postBaccalaureate_info = CTkLabel(
            frame_info_content,
            text=f'{education_data["labels"][0]} Population Count: {education_data["count"][0]}',
            font=CONTENT_FONT
        )
        education_collegeGrad_info = CTkLabel(
            frame_info_content,
            text=f'{education_data["labels"][1]} Population Count: {education_data["count"][1]}',
            font=CONTENT_FONT
        )
        education_collegeLevel_info = CTkLabel(
            frame_info_content,
            text=f'{education_data["labels"][2]} Population Count: {education_data["count"][2]}',
            font=CONTENT_FONT
        )
        education_highSchoolGrad_info = CTkLabel(
            frame_info_content,
            text=f'{education_data["labels"][3]} Population Count: {education_data["count"][3]}',
            font=CONTENT_FONT
        )
        education_highSchoolLevel_info = CTkLabel(
            frame_info_content,
            text=f'{education_data["labels"][4]} Population Count: {education_data["count"][4]}',
            font=CONTENT_FONT
        )
        education_elementaryGrad_info = CTkLabel(
            frame_info_content,
            text=f'{education_data["labels"][5]} Population Count: {education_data["count"][5]}',
            font=CONTENT_FONT
        )
        education_elementaryLevel_info = CTkLabel(
            frame_info_content,
            text=f'{education_data["labels"][6]} Population Count: {education_data["count"][6]}',
            font=CONTENT_FONT
        )
        education_earlyChildhood_info = CTkLabel(
            frame_info_content,
            text=f'{education_data["labels"][7]} Population Count: {education_data["count"][7]}',
            font=CONTENT_FONT
        )
        education_noGradeReported_info = CTkLabel(
            frame_info_content,
            text=f'{education_data["labels"][8]} Population Count: {education_data["count"][8]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true')
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        education_postBaccalaureate_info.pack(anchor='nw', pady=(10, 10))
        education_collegeGrad_info.pack(anchor='nw', pady=(10, 10))
        education_collegeLevel_info.pack(anchor='nw', pady=(10, 10))
        education_highSchoolGrad_info.pack(anchor='nw', pady=(10, 10))
        education_highSchoolLevel_info.pack(anchor='nw', pady=(10, 10))
        education_elementaryGrad_info.pack(anchor='nw', pady=(10, 10))
        education_elementaryLevel_info.pack(anchor='nw', pady=(10, 10))
        education_earlyChildhood_info.pack(anchor='nw', pady=(10, 10))
        education_noGradeReported_info.pack(anchor='nw', pady=(10, 20))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_comelec(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content)
        frame_info = CTkFrame(frame_content)
        frame_gender_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        comelec_data = {
            "labels": [
                "Registered", "Not Registered"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(comelec_data["labels"])):
            comelec_data["values"].append(data['comelec'][i][comelec_data["labels"][i]]['percentage'])
            comelec_data["count"].append(data['comelec'][i][comelec_data["labels"][i]]['count'])

        comelec_data_frame = pd.DataFrame(comelec_data)

        comelec_data_frame = comelec_data_frame[comelec_data_frame["values"] != 0.00]

        comelec_figure = plt.Figure(figsize=(6, 6), dpi=100)
        comelec_ax = comelec_figure.add_subplot(111)
        comelec_ax.pie(
            comelec_data_frame["values"],
            labels=comelec_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99', '#ffd97d', '#8d99ae',
                    '#d9cab3', '#b0d0d3', '#dec0f1', '#f79d65', '#7e6c6c']
        )
        comelec_ax.set_title("PERCENTAGE OF RESIDENTS COMELEC REGISTERED", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(comelec_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(
            frame_info,
            text='Specific Number of Residents per Comelec Registration',
            font=SEARCHBAR_FONT
        )
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        comelec_registered_info = CTkLabel(
            frame_info_content,
            text=f'{comelec_data["labels"][0]} Population Count: {comelec_data["count"][0]}',
            font=CONTENT_FONT
        )
        comelec_notRegistered_info = CTkLabel(
            frame_info_content,
            text=f'{comelec_data["labels"][1]} Population Count: {comelec_data["count"][1]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        # -- FRAME GENDER INFO
        comelec_gender_count = count_comelec_gender()
        frame_gender_info_content = CTkFrame(frame_gender_info, fg_color=CONTENT_BG)
        label_gender_info = CTkLabel(
            frame_gender_info_content,
            text='Comelec Registered Count based on Gender',
            font=SEARCHBAR_FONT
        )
        total_male_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'MALE Registered Count: {comelec_gender_count[0]}',
            font=CONTENT_FONT
        )
        total_female_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'FEMALE Registered Count: {comelec_gender_count[1]}',
            font=CONTENT_FONT
        )
        total_male_unregistered_info = CTkLabel(
            frame_gender_info_content,
            text=f'MALE Not Registered Count: {comelec_gender_count[2]}',
            font=CONTENT_FONT
        )
        total_female_unregistered_info = CTkLabel(
            frame_gender_info_content,
            text=f'FEMALE Not Registered Count: {comelec_gender_count[3]}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        frame_gender_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true')
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        frame_gender_info_content.pack(anchor='center')
        comelec_registered_info.pack(anchor='nw', pady=(10, 10))
        comelec_notRegistered_info.pack(anchor='nw', pady=(10, 20))
        label_gender_info.pack(anchor='center', fill='y', pady=(30, 10))
        total_male_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_female_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_male_unregistered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_female_unregistered_info.pack(anchor='nw', pady=(10, 20), padx=(100, 0))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_philsys(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content)
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        philsys_data = {
            "labels": [
                "Registered", "Not Registered"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(philsys_data["labels"])):
            philsys_data["values"].append(data['philsys'][i][philsys_data["labels"][i]]['percentage'])
            philsys_data["count"].append(data['philsys'][i][philsys_data["labels"][i]]['count'])

        philsys_data_frame = pd.DataFrame(philsys_data)

        philsys_data_frame = philsys_data_frame[philsys_data_frame["values"] != 0.00]

        philsys_figure = plt.Figure(figsize=(6, 6), dpi=100)
        philsys_ax = philsys_figure.add_subplot(111)
        philsys_ax.pie(
            philsys_data_frame["values"],
            labels=philsys_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99', '#ffd97d', '#8d99ae',
                    '#d9cab3', '#b0d0d3', '#dec0f1', '#f79d65', '#7e6c6c']
        )
        philsys_ax.set_title("PERCENTAGE OF RESIDENTS COMELEC REGISTERED", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(philsys_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(
            frame_info,
            text='Specific Number of Residents per Comelec Registration',
            font=SEARCHBAR_FONT
        )
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        philsys_registered_info = CTkLabel(
            frame_info_content,
            text=f'{philsys_data["labels"][0]} Population Count: {philsys_data["count"][0]}',
            font=CONTENT_FONT
        )
        philsys_notRegistered_info = CTkLabel(
            frame_info_content,
            text=f'{philsys_data["labels"][1]} Population Count: {philsys_data["count"][1]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        # -- FRAME GENDER INFO
        frame_gender_info = CTkFrame(frame_content)
        comelec_gender_count = count_philsys_gender()
        frame_gender_info_content = CTkFrame(frame_gender_info, fg_color=CONTENT_BG)
        label_gender_info = CTkLabel(
            frame_gender_info_content,
            text='Philsys Registered Count based on Gender',
            font=SEARCHBAR_FONT
        )
        total_male_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'MALE Registered Count: {comelec_gender_count[0]}',
            font=CONTENT_FONT
        )
        total_female_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'FEMALE Registered Count: {comelec_gender_count[1]}',
            font=CONTENT_FONT
        )
        total_male_unregistered_info = CTkLabel(
            frame_gender_info_content,
            text=f'MALE Not Registered Count: {comelec_gender_count[2]}',
            font=CONTENT_FONT
        )
        total_female_unregistered_info = CTkLabel(
            frame_gender_info_content,
            text=f'FEMALE Not Registered Count: {comelec_gender_count[3]}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true')
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        philsys_registered_info.pack(anchor='nw', pady=(10, 10))
        philsys_notRegistered_info.pack(anchor='nw', pady=(10, 20))

        frame_gender_info.pack(anchor='center', expand='true', fill='both')
        frame_gender_info_content.pack(anchor='center')
        label_gender_info.pack(anchor='center', fill='y', pady=(30, 10))
        total_male_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_female_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_male_unregistered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_female_unregistered_info.pack(anchor='nw', pady=(10, 20), padx=(100, 0))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_pwd(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content)
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        pwd_data = {
            "labels": [
                "YES", "NO"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(pwd_data["labels"])):
            pwd_data["values"].append(data['pwd'][i][pwd_data["labels"][i]]['percentage'])
            pwd_data["count"].append(data['pwd'][i][pwd_data["labels"][i]]['count'])

        pwd_data_frame = pd.DataFrame(pwd_data)

        pwd_data_frame = pwd_data_frame[pwd_data_frame["values"] != 0.00]

        pwd_figure = plt.Figure(figsize=(6, 6), dpi=100)
        pwd_ax = pwd_figure.add_subplot(111)
        pwd_ax.pie(
            pwd_data_frame["values"],
            labels=pwd_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99', '#ffd97d', '#8d99ae',
                    '#d9cab3', '#b0d0d3', '#dec0f1', '#f79d65', '#7e6c6c']
        )
        pwd_ax.set_title("PERCENTAGE OF RESIDENTS PWD MEMBERS", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(pwd_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(
            frame_info,
            text='Specific Number of Residents per PWD Members',
            font=SEARCHBAR_FONT
        )
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        pwd_member_info = CTkLabel(
            frame_info_content,
            text=f'PWD Members Population Count: {pwd_data["count"][0]}',
            font=CONTENT_FONT
        )
        pwd_nonMember_info = CTkLabel(
            frame_info_content,
            text=f'Non-PWD Members Population Count: {pwd_data["count"][1]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        frame_gender_info = CTkFrame(frame_content)
        comelec_gender_count = count_pwd_gender()
        frame_gender_info_content = CTkFrame(frame_gender_info, fg_color=CONTENT_BG)
        label_gender_info = CTkLabel(
            frame_gender_info_content,
            text='PWD Member Count based on Gender',
            font=SEARCHBAR_FONT
        )
        total_male_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'MALE Registered Count: {comelec_gender_count[0]}',
            font=CONTENT_FONT
        )
        total_female_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'FEMALE Registered Count: {comelec_gender_count[1]}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true')
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        pwd_member_info.pack(anchor='nw', pady=(10, 10))
        pwd_nonMember_info.pack(anchor='nw', pady=(10, 20))

        frame_gender_info.pack(anchor='center', expand='true', fill='both')
        frame_gender_info_content.pack(anchor='center')
        label_gender_info.pack(anchor='center', fill='y', pady=(30, 10))
        total_male_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_female_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_senior(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content, fg_color='#FFF')
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        senior_data = {
            "labels": [
                "YES", "NO"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(senior_data["labels"])):
            senior_data["values"].append(data['senior'][i][senior_data["labels"][i]]['percentage'])
            senior_data["count"].append(data['senior'][i][senior_data["labels"][i]]['count'])

        senior_data_frame = pd.DataFrame(senior_data)

        senior_data_frame = senior_data_frame[senior_data_frame["values"] != 0.00]

        senior_figure = plt.Figure(figsize=(6, 6), dpi=100)
        senior_ax = senior_figure.add_subplot(111)
        senior_ax.pie(
            senior_data_frame["values"],
            labels=senior_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99', '#ffd97d', '#8d99ae',
                    '#d9cab3', '#b0d0d3', '#dec0f1', '#f79d65', '#7e6c6c']
        )
        senior_ax.set_title("PERCENTAGE OF RESIDENTS\nSENIOR CITIZEN MEMBERS", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(senior_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(
            frame_info,
            text='Specific Number of Residents per Senior Citizen Membership',
            font=SEARCHBAR_FONT
        )
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        senior_member_info = CTkLabel(
            frame_info_content,
            text=f'Senior Citizen Members Population Count: {senior_data["count"][0]}',
            font=CONTENT_FONT
        )
        senior_nonMember_info = CTkLabel(
            frame_info_content,
            text=f'Non-Senior Citizen Members Population Count: {senior_data["count"][1]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        frame_gender_info = CTkFrame(frame_content)
        comelec_gender_count = count_senior_gender()
        frame_gender_info_content = CTkFrame(frame_gender_info, fg_color=CONTENT_BG)
        label_gender_info = CTkLabel(
            frame_gender_info_content,
            text='Senior Member Count based on Gender',
            font=SEARCHBAR_FONT
        )
        total_male_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'MALE Registered Count: {comelec_gender_count[0]}',
            font=CONTENT_FONT
        )
        total_female_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'FEMALE Registered Count: {comelec_gender_count[1]}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true', pady=(20, 0))
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        senior_member_info.pack(anchor='nw', pady=(10, 10))
        senior_nonMember_info.pack(anchor='nw', pady=(10, 30))

        frame_gender_info.pack(anchor='center', expand='true', fill='both')
        frame_gender_info_content.pack(anchor='center')
        label_gender_info.pack(anchor='center', fill='y', pady=(30, 10))
        total_male_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_female_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_soloParent(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content, fg_color='#FFF')
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        soloParent_data = {
            "labels": [
                "YES", "NO"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(soloParent_data["labels"])):
            soloParent_data["values"].append(data['solo_parent'][i][soloParent_data["labels"][i]]['percentage'])
            soloParent_data["count"].append(data['solo_parent'][i][soloParent_data["labels"][i]]['count'])

        soloParent_data_frame = pd.DataFrame(soloParent_data)

        soloParent_data_frame = soloParent_data_frame[soloParent_data_frame["values"] != 0.00]

        soloParent_figure = plt.Figure(figsize=(6, 6), dpi=100)
        soloParent_ax = soloParent_figure.add_subplot(111)
        soloParent_ax.pie(
            soloParent_data_frame["values"],
            labels=soloParent_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99', '#ffd97d', '#8d99ae',
                    '#d9cab3', '#b0d0d3', '#dec0f1', '#f79d65', '#7e6c6c']
        )
        soloParent_ax.set_title("PERCENTAGE OF RESIDENTS\nSOLO PARENT MEMBERS", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(soloParent_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(
            frame_info,
            text='Specific Number of Residents per Solo Parent Membership',
            font=SEARCHBAR_FONT
        )
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        soloParent_member_info = CTkLabel(
            frame_info_content,
            text=f'Solo Parent Members Population Count: {soloParent_data["count"][0]}',
            font=CONTENT_FONT
        )
        soloParent_nonMember_info = CTkLabel(
            frame_info_content,
            text=f'Non-Solo Parent Members Population Count: {soloParent_data["count"][1]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        frame_gender_info = CTkFrame(frame_content)
        comelec_gender_count = count_solo_parent_gender()
        frame_gender_info_content = CTkFrame(frame_gender_info, fg_color=CONTENT_BG)
        label_gender_info = CTkLabel(
            frame_gender_info_content,
            text='Solo Parents Count based on Gender',
            font=SEARCHBAR_FONT
        )
        total_male_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'MALE Registered Count: {comelec_gender_count[0]}',
            font=CONTENT_FONT
        )
        total_female_registered_info = CTkLabel(
            frame_gender_info_content,
            text=f'FEMALE Registered Count: {comelec_gender_count[1]}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true', pady=(20, 0))
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        soloParent_member_info.pack(anchor='nw', pady=(10, 10))
        soloParent_nonMember_info.pack(anchor='nw', pady=(10, 20))

        frame_gender_info.pack(anchor='center', expand='true', fill='both')
        frame_gender_info_content.pack(anchor='center')
        label_gender_info.pack(anchor='center', fill='y', pady=(30, 10))
        total_male_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_female_registered_info.pack(anchor='nw', pady=(10, 10), padx=(100, 0))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_4Ps(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content, fg_color='#FFF')
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        _4Ps_data = {
            "labels": [
                "YES", "NO"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(_4Ps_data["labels"])):
            _4Ps_data["values"].append(data['4Ps'][i][_4Ps_data["labels"][i]]['percentage'])
            _4Ps_data["count"].append(data['4Ps'][i][_4Ps_data["labels"][i]]['count'])

        _4Ps_data_frame = pd.DataFrame(_4Ps_data)

        _4Ps_data_frame = _4Ps_data_frame[_4Ps_data_frame["values"] != 0.00]

        _4Ps_figure = plt.Figure(figsize=(6, 6), dpi=100)
        _4Ps_ax = _4Ps_figure.add_subplot(111)
        _4Ps_ax.pie(
            _4Ps_data_frame["values"],
            labels=_4Ps_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99', '#ffd97d', '#8d99ae',
                    '#d9cab3', '#b0d0d3', '#dec0f1', '#f79d65', '#7e6c6c']
        )
        _4Ps_ax.set_title("PERCENTAGE OF RESIDENTS 4Ps MEMBERS", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(_4Ps_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(
            frame_info,
            text='Specific Number of Residents per 4Ps Membership',
            font=SEARCHBAR_FONT
        )
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        _4Ps_member_info = CTkLabel(
            frame_info_content,
            text=f'4Ps Members Population Count: {_4Ps_data["count"][0]}',
            font=CONTENT_FONT
        )
        _4Ps_nonMember_info = CTkLabel(
            frame_info_content,
            text=f'Non-4Ps Members Population Count: {_4Ps_data["count"][1]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true')
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        _4Ps_member_info.pack(anchor='nw', pady=(10, 10))
        _4Ps_nonMember_info.pack(anchor='nw', pady=(10, 20))
        total_count_info.pack(anchor='nw', pady=(10, 30))

    def display_farmers(self):
        # CREATE WIDGET
        frame_content = CTkScrollableFrame(self.frame_content)
        frame_content.configure(bg_color=CONTENT_BG, fg_color='#FFF')
        frame_graph = CTkFrame(frame_content, fg_color='#FFF')
        frame_info = CTkFrame(frame_content)

        data = get_statistics_data()
        total_count = get_residents_count()

        # -- FRAME GRAPH
        residents_count = data['residents_count']
        farmers_data = {
            "labels": [
                "FA", "RSBSA", "NONE"
            ],
            "values": [],
            "count": []
        }

        for i in range(len(farmers_data["labels"])):
            farmers_data["values"].append(data['farmers'][i][farmers_data["labels"][i]]['percentage'])
            farmers_data["count"].append(data['farmers'][i][farmers_data["labels"][i]]['count'])

        farmers_data_frame = pd.DataFrame(farmers_data)

        farmers_data_frame = farmers_data_frame[farmers_data_frame["values"] != 0.00]

        farmers_figure = plt.Figure(figsize=(6, 6), dpi=100)
        farmers_ax = farmers_figure.add_subplot(111)
        farmers_ax.pie(
            farmers_data_frame["values"],
            labels=farmers_data_frame["labels"],
            autopct='%1.2f%%',
            colors=['#a4ac86', '#a68a64', '#e7ad99', '#ffd97d', '#8d99ae',
                    '#d9cab3', '#b0d0d3', '#dec0f1', '#f79d65', '#7e6c6c']
        )
        farmers_ax.set_title("PERCENTAGE OF RESIDENTS FARMERS MEMBERS", fontdict=self.title_font)
        purok_pie = FigureCanvasTkAgg(farmers_figure, frame_graph)

        # -- FRAME INFO
        label_info = CTkLabel(
            frame_info,
            text='Specific Number of Residents per 4Ps Membership',
            font=SEARCHBAR_FONT
        )
        frame_info_content = CTkFrame(frame_info, fg_color=CONTENT_BG)
        fa_member_info = CTkLabel(
            frame_info_content,
            text=f'Farmers FA Population Count: {farmers_data["count"][0]}',
            font=CONTENT_FONT
        )
        rsbsa_member_info = CTkLabel(
            frame_info_content,
            text=f'Farmers RSBSA Population Count: {farmers_data["count"][1]}',
            font=CONTENT_FONT
        )
        none_member_info = CTkLabel(
            frame_info_content,
            text=f'Non-Farmers Members Population Count: {farmers_data["count"][2]}',
            font=CONTENT_FONT
        )
        total_count_info = CTkLabel(
            frame_info_content,
            text=f'Total Count: {total_count['residents_count']}',
            font=CONTENT_FONT
        )

        # CREATE LAYOUT
        frame_content.pack(side='left', expand='true', fill='both')
        frame_graph.pack(anchor='center', expand='true', fill='both')
        frame_info.pack(anchor='center', expand='true', fill='both')
        purok_pie.get_tk_widget().pack(side='left', fill='both', expand='true')
        label_info.pack(anchor='center', fill='y', pady=(30, 10))
        frame_info_content.pack(anchor='center')
        fa_member_info.pack(anchor='nw', pady=(10, 10))
        rsbsa_member_info.pack(anchor='nw', pady=(10, 10))
        none_member_info.pack(anchor='nw', pady=(10, 20))
        total_count_info.pack(anchor='nw', pady=(10, 30))


class BlotterPage(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            fg_color=CONTENT_BG,
        )
        self.create_constants()
        self.create_widgets()
        self.create_layout()

    def create_constants(self):
        # Search Bar
        self.SEARCH_FONT = ('Bahnschrift SemiBold', 30, 'normal')
        # Search Bar Entry size
        self.ENTRY_WIDTH = 600
        # Buttons size
        self.BTN_WIDTH = 150
        self.BTN_HEIGHT = 40
        # Buttons Colors
        self.TEXT_COLOR = "#fafafa"
        self.BTN_GREEN = "#656D4A"
        self.BTN_HOVER_GREEN = "#A4AC86"
        self.BTN_BROWN = "#936639"
        self.BTN_HOVER_BROWN = "#A68A64"

        self.blotter_label_font = ('Bahnschrift SemiBold', 26, 'normal')
        self.blotter_entry_font = ('Bahnschrift SemiBold', 16, 'normal')
        self.blotter_date_entry_font = ('Bahnschrift SemiBold', 12, 'normal')
        self.blotter_instructions = ('Bahnschrift SemiBold', 12, 'normal')

        self.record_case_no_font = ('Bahnschrift SemiBold', 24, 'normal')
        self.record_content_font = ('Bahnschrift SemiBold', 20, 'normal')
        self.record_names_font = ('Bahnschrift SemiBold', 16, 'normal')

        self.BLOTTER_CONTENT_BG = "#dad7cd"

        # View Record Information Color
        self.ENTRY_COLOR = '#000'

        self.TREE_HEADING_COLOR = "#344e41"
        self.TREE_SELECTED_COLOR = "#344e41"
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", font=("Bahnschrift SemiBold", 12, "normal"), rowheight=30)
        self.tree_style.configure("Treeview.Heading", font=("Bahnschrift SemiBold", 16, "bold"),padding=(0, 5), foreground=self.TREE_HEADING_COLOR)
        self.tree_style.map("Treeview",
                            background=[("selected", self.TREE_SELECTED_COLOR)],
                            foreground=[("selected", self.TEXT_COLOR)]
                            )

    def create_widgets(self):
        # Blotter Page Label
        self.label_blotter = CTkLabel(
            self,
            font=LABELFRAME_FONT,
            text='Blotter Information'
        )
        # First Level Container
        self.frame_firstLevel = CTkFrame(self)
        # Second Level Container
        self.frame_secondLevel = CTkFrame(self, border_width=5)

        # - First Level Content
        self.label_searchBar = CTkLabel(
            self.frame_firstLevel,
            text='Search',
            font=SEARCHBAR_FONT,
        )
        self.search_data = StringVar()
        self.entry_searchBar = CTkEntry(
            self.frame_firstLevel,
            width=self.ENTRY_WIDTH,
            font=self.SEARCH_FONT,
            placeholder_text="Search here...",
            textvariable=self.search_data
        )
        self.entry_searchBar.bind("<KeyRelease>", self.on_search)
        self.btn_addRecord = CTkButton(
            self.frame_firstLevel,
            text='Add a Record',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
            font=CONTENT_FONT,
            command=self.add_record,
        )
        self.btn_viewRecord = CTkButton(
            self.frame_firstLevel,
            text='View Record',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            fg_color=self.BTN_BROWN,
            hover_color=self.BTN_HOVER_BROWN,
            font=CONTENT_FONT,
            command=self.view_record
        )

        # - Second Level Content
        self.test = CTkLabel(self.frame_secondLevel, text='test')

        self.tree_blotterData = ttk.Treeview(self.frame_secondLevel)
        self.tree_blotterData.configure()
        self.tree_blotterData["columns"] = (
            "Record ID", "Date Filed", "Barangay Case No.", "Complainant/s", "Respondent/s", "Reason"
        )
        self.tree_blotterData.heading("#0", text="", anchor='w')
        self.tree_blotterData.column("#0", width=0, stretch=NO)
        self.tree_blotterData.heading("Record ID", text="", anchor='w')
        self.tree_blotterData.column("Record ID", width=0, stretch=NO)
        for column in self.tree_blotterData["columns"][1:]:
            self.tree_blotterData.heading(column, text=column)
            self.tree_blotterData.column(column, anchor='w')
        self.tree_blotterData_scroll = ttk.Scrollbar(
            self.frame_secondLevel,
            orient='vertical',
            command=self.tree_blotterData.yview
        )
        self.tree_blotterData.configure(
            yscrollcommand=self.tree_blotterData_scroll.set
        )
        self.populate_blotter_tree()

    def create_layout(self):
        # Blotter Page Label
        self.label_blotter.pack(anchor='nw', pady=10, padx=20)
        # First Level Container
        self.frame_firstLevel.pack(side='top', fill='y', pady=(5, 20))
        # Second Level Container
        self.frame_secondLevel.pack(side='top', fill='both', expand='true', pady=(0, 20), padx=20)

        # - First Level Content
        self.label_blotter.pack()
        self.label_searchBar.pack(side='left', padx=(0, 10))
        self.entry_searchBar.pack(side='left', padx=(0, 30))
        self.btn_addRecord.pack(side='left', padx=(0, 10))
        self.btn_viewRecord.pack(side='left')
        # - Second Level Content
        self.tree_blotterData.pack(side='left', fill='both', expand='true')
        self.tree_blotterData_scroll.pack(side='right', fill='y')

    def on_search(self, e):
        search_data = self.search_data.get()
        self.update_tree_blotterData(search_data)

    def update_tree_blotterData(self, search_data):
        for item in self.tree_blotterData.get_children():
            self.tree_blotterData.delete(item)

        for item in get_blotterData():
            temp_respondents_names = get_respondents_names(item[2])
            temp_complainants_names = get_complainants_names(item[2])
            respondents_names = []
            complainants_names = []
            for i in range(len(temp_respondents_names)):
                respondents_names.append(
                    get_resident_name(
                        temp_respondents_names[i][2],
                        temp_respondents_names[i][3],
                        temp_respondents_names[i][4],
                        temp_respondents_names[i][5]
                        )
                )
            for j in range(len(temp_complainants_names)):
                complainants_names.append(
                    get_resident_name(
                        temp_complainants_names[j][2],
                        temp_complainants_names[j][3],
                        temp_complainants_names[j][4],
                        temp_complainants_names[j][5]
                        )
                )
            final_respondents_names = concatenate_names(respondents_names)
            final_complainants_names = concatenate_names(complainants_names)
            if (search_data.lower() in item[2].lower() or
                search_data.lower() in final_complainants_names.lower() or
                search_data.lower() in final_respondents_names.lower()):
                self.tree_blotterData.insert('', 'end', values=(
                    item[0],
                    item[1],
                    item[2],
                    final_complainants_names,
                    final_respondents_names,
                    item[3]
                ))

    def view_record(self):
        values = self.check_selected_record()
        if len(values) == 0:
            messagebox.showwarning("No Record Selected", "There is no Record Selected.")
            return

        self.view_record_window = CTkToplevel(self)
        window_width = 1500
        window_height = 700
        x_axis, y_axis = self._center_screen(window_width, window_height)
        self.view_record_window.title('View Record')
        self.view_record_window.resizable(False, False)
        self.view_record_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.after(200, lambda: self.view_record_window.iconbitmap(self.view_record_window.iconPath))
        self.view_record_window.geometry("{}x{}+{}+{}".format(
            window_width, window_height, x_axis, y_axis
        ))
        self.view_record_window.transient(self)
        self.view_record_window.grab_set()
        self.view_record_window.focus()

        temp_complainants = get_complainants_names(values[2])
        temp_respondents = get_respondents_names(values[2])
        temp_complainants_address = get_complainants_address(values[2])
        temp_respondents_address = get_respondents_address(values[2])

        # CREATE WIDGETS
        self.frame_window = CTkScrollableFrame(
            self.view_record_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.btn_generate_documents = CTkButton(
            self.frame_window,
            text='Generate Documents',
            font=self.record_names_font,
            width=200,
            height=50,
            command=lambda: self.blotter_select_documents(
                values,
                temp_complainants,
                temp_respondents,
                temp_complainants_address,
                temp_respondents_address
                )
        )
        self.label_view_record_window = CTkLabel(
            self.frame_window,
            font=self.blotter_label_font,
            text='Record Information'
        )
        self.frame_record_information = CTkFrame(
            self.frame_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.frame_record_case_date = CTkFrame(
            self.frame_record_information,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        # - Case No.
        self.label_record_case_no = CTkLabel(
            self.frame_record_case_date,
            font=self.record_case_no_font,
            text='BARANGAY CASE NO.: '
        )
        self.entry_record_case_no = CTkLabel(
            self.frame_record_case_date,
            font=self.record_case_no_font,
            text_color=self.ENTRY_COLOR,
            text=values[2]
        )
        # - Date Filed
        self.label_record_date_filed = CTkLabel(
            self.frame_record_case_date,
            font=self.record_content_font,
            text='DATE FILED: '
        )
        self.entry_record_date_filed = CTkLabel(
            self.frame_record_case_date,
            font=self.record_content_font,
            text_color=self.ENTRY_COLOR,
            text=values[1]
        )
        # - Record Complainants and Respondents
        self.frame_record_complainants_respondents = CTkFrame(
            self.frame_record_information,
            fg_color=self.BLOTTER_CONTENT_BG,
            border_width=5
        )
        # -- Complainants Container
        self.frame_record_complainants = CTkFrame(
            self.frame_record_complainants_respondents,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        # -- Respondents Container
        self.frame_record_respondents = CTkFrame(
            self.frame_record_complainants_respondents,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        # -- Complainants Name
        self.label_record_complaints = CTkLabel(
            self.frame_record_complainants,
            font=self.record_content_font,
            text='COMPLAINANT/S:',
            anchor="nw"
        )
        # -- Respondents Name
        self.label_record_respondents = CTkLabel(
            self.frame_record_respondents,
            font=self.record_content_font,
            text='RESPONDENT/S:',
            anchor="nw"
        )
        # - Address
        self.frame_record_address = CTkFrame(
            self.frame_record_information,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_record_address = CTkLabel(
            self.frame_record_address,
            font=self.record_content_font,
            text='ADDRESS:',
            anchor="nw"
        )
        self.frame_addresses_container = CTkFrame(
            self.frame_record_address,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        complainants_address = f"{temp_complainants_address[2]}, {temp_complainants_address[3]},\n{temp_complainants_address[4]}, {temp_complainants_address[5]}"
        respondents_address = f"{temp_respondents_address[2]}, {temp_respondents_address[3]},\n{temp_respondents_address[4]}, {temp_respondents_address[5]}"
        self.entry_complainants_address = CTkLabel(
            self.frame_addresses_container,
            font=self.record_content_font,
            text_color=self.ENTRY_COLOR,
            text=complainants_address,
        )
        self.entry_respondents_address = CTkLabel(
            self.frame_addresses_container,
            font=self.record_content_font,
            text_color=self.ENTRY_COLOR,
            text=respondents_address,
        )
        # - Reason
        self.frame_record_reason = CTkFrame(
            self.frame_record_information,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_record_reason = CTkLabel(
            self.frame_record_reason,
            font=self.record_content_font,
            text='REASON:',
            anchor="nw"
        )
        self.entry_record_reason = CTkTextbox(
            self.frame_record_reason,
            font=self.record_content_font,
            text_color=self.ENTRY_COLOR,
            width=1000,
        )
        self.entry_record_reason.insert('1.0', values[5])
        self.entry_record_reason.configure(state='disabled')
        # - Note
        self.frame_record_note = CTkFrame(
            self.frame_record_information,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_record_note = CTkLabel(
            self.frame_record_note,
            font=self.record_content_font,
            text='NOTE:',
            anchor="nw"
        )
        self.entry_record_note = CTkTextbox(
            self.frame_record_note,
            font=self.record_content_font,
            text_color=self.ENTRY_COLOR,
            width=1000,
        )
        self.entry_record_note.insert('1.0', get_record_note(values[0]))
        self.entry_record_note.configure(state='disabled')

        # self.frame_generated_documents = CTkFrame(
        #     self.frame_window,
        #     fg_color=self.BLOTTER_CONTENT_BG
        # )
        # self.label_generated_documents = CTkLabel(
        #     self.frame_generated_documents,
        #     font=self.record_content_font,
        #     text='BLOTTER CASE ACTIVITY:',
        #     anchor="nw"
        # )

        # CREATE LAYOUT
        self.frame_window.pack(anchor='nw', fill='both', expand='true')
        self.btn_generate_documents.pack(anchor='ne', pady=10, padx=200)
        self.label_view_record_window.pack(anchor='center', pady=20)
        self.frame_record_information.pack(anchor='center', padx=200, fill='x')
        self.frame_record_case_date.pack(anchor='nw', fill='x')
        self.label_record_case_no.pack(side='left')
        self.entry_record_case_no.pack(side='left')
        self.entry_record_date_filed.pack(side='right')
        self.label_record_date_filed.pack(side='right')
        self.frame_record_complainants_respondents.pack(fill="x", pady=(10, 0))
        self.frame_record_complainants.pack(side="left", fill="both", expand='true')
        self.frame_record_respondents.pack(side="right", fill="both", expand='true')
        self.label_record_complaints.pack(anchor="nw")
        self.label_record_respondents.pack(anchor="nw", fill='x')

        self.frame_record_address.pack(anchor="nw", fill="both", expand='true')
        self.label_record_address.pack(anchor='nw')
        self.frame_addresses_container.pack(anchor='center')
        self.entry_complainants_address.pack(side='left', padx=(0, 100))
        self.entry_respondents_address.pack(side='right', padx=(100, 0))

        self.frame_record_reason.pack(anchor='nw', fill='x')
        self.label_record_reason.pack(anchor='nw')
        self.entry_record_reason.pack(anchor='center', pady=(10, 50))
        self.frame_record_note.pack(anchor='nw', fill='x')
        self.label_record_note.pack(anchor='nw')
        self.entry_record_note.pack(anchor='center', pady=(10, 50))

        # self.frame_generated_documents.pack(anchor='nw', pady=(10, 80), padx=(200, 0))
        # self.label_generated_documents.pack(anchor='nw')

        # data_generated_documents = get_generated_documents(values[2])
        # data_final_generated_documents = []
        # for i in range(len(data_generated_documents)):
        #     data_final_generated_documents.append(
        #         f"{data_generated_documents[i][0]} - {data_generated_documents[i][1]}"
        #     )
        
        # for record in data_final_generated_documents:
        #     label = CTkLabel(
        #         self.frame_generated_documents,
        #         text=record,
        #         font=self.record_names_font,
        #     )
        #     label.pack(anchor='nw', padx=(100, 0))

        # DYNAMIC WIDGETS AND LAYOUTS
        names = split_names(values[3])
        for i, text in enumerate(names):
            label = CTkLabel(
                self.frame_record_complainants,
                text=text.upper(),
                font=self.record_names_font,
                text_color=self.ENTRY_COLOR
            )
            label.pack(anchor='n', fill='x')

        names = split_names(values[4])
        for i, text in enumerate(names):
            label = CTkLabel(
                self.frame_record_respondents,
                text=text.upper(),
                font=self.record_names_font,
                text_color=self.ENTRY_COLOR
            )
            label.pack(anchor='n', fill='x')

    def blotter_select_documents(self, values, complainants, respondents, complainants_address, respondents_address):
        self.select_documents_window = CTkToplevel()
        window_width = 1100
        window_height = 450
        x_axis, y_axis = self._center_screen(window_width, window_height)
        self.select_documents_window.title("Document Selection")
        self.select_documents_window.resizable(False, False)
        self.select_documents_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.after(200, lambda: self.select_documents_window.iconbitmap(self.select_documents_window.iconPath))
        self.select_documents_window.geometry("{}x{}+{}+{}".format(
            window_width, window_height, x_axis, y_axis
        ))
        self.select_documents_window.transient(self)
        self.select_documents_window.grab_set()
        self.select_documents_window.focus()

        self.select_documents_window.protocol("WM_DELETE_WINDOW", self.on_closing_select_doc)

        # CONSTANTS
        btn_width = 325
        btn_height = 80

        self.select_documents_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        # CREATE WIDGETS
        self.frame_first_level = CTkFrame(
            self.select_documents_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.frame_second_level = CTkFrame(
            self.select_documents_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.frame_third_level = CTkFrame(
            self.select_documents_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.frame_fourth_level = CTkFrame(
            self.select_documents_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        # - First Level
        self.btn_KPFormNo7 = CTkButton(
            self.frame_first_level,
            text='KP Form No. 7\nOFFICE OF THE LUPONG TAGAPAMAYAPA\nCOMPLAINT',
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_1(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )
        self.btn_KPFormNo9 = CTkButton(
            self.frame_first_level,
            text="KP Form No. 9\nOFFICE OF THE LUPONG TAGAPAMAYAPA\nSUMMONS AND OFFICER'S RETURN FORM",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_2(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )
        self.btn_KPFormNo12_1 = CTkButton(
            self.frame_first_level,
            text="KP Form No. 12\nOFFICE OF THE LUPONG TAGAPAMAYAPA\nNOTICE OF HEARING (MEDIATION PROCESS)",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_4(
                values,
                complainants,
                respondents,
                complainants_address
            )
        )
        # - Second Level
        self.btn_KPFormNo12_2 = CTkButton(
            self.frame_second_level,
            text="KP Form No. 12\nOFFICE OF THE LUPONG TAGAPAMAYAPA\nNOTICE OF HEARING (RE: FAILURE TO APPEAR)",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_5(
                values,
                respondents,
                respondents_address,
                complainants
            )
        )
        self.btn_KPFormNo16 = CTkButton(
            self.frame_second_level,
            text="KP Form No. 16\nOFFICE OF THE LUPONG TAGAPAMAYAPA\nAMICABLE SETTLEMENT",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_6(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )
        self.btn_KPFormNo17 = CTkButton(
            self.frame_second_level,
            text="KP Form No. 17\nOFFICE OF THE LUPONG TAGAPAMAYAPA\nREPUDIATION",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_7(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )
        # - Third Level
        self.btn_KPFormNo13 = CTkButton(
            self.frame_third_level,
            text="KP Form No. 13\nOFFICE OF THE PANGKAT TAGAPAGKASUNDO\nNOTICE OF HEARING (CONCILIATION PROCEEDINGS)",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_8(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )
        self.btn_certificate_to_action = CTkButton(
            self.frame_third_level,
            text="CERTIFICATE TO FILE ACTION",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_9(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )
        self.btn_subpoena = CTkButton(
            self.frame_third_level,
            text="SUBPOENA",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_10(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )
        # - Fourth Level
        self.btn_chosen_pangkat = CTkButton(
            self.frame_fourth_level,
            text="OFFICE OF THE LUPONG TAGAPAMAYAPA\nNOTICE TO CHOSEN PANGKAT MEMBER",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_11(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )
        self.btn_KPFormNo22 = CTkButton(
            self.frame_fourth_level,
            text="KP Form No. 22\nOFFICE OF THE LUPONG TAGAPAMAYAPA\nCERTIFICATION TO BAR COUNTERCLAIM",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_12(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )
        self.btn_KPFormNo21 = CTkButton(
            self.frame_fourth_level,
            text="KP Form No. 21\nOFFICE OF THE PANGKAT TAGAPAGKASUNDO\nCERTIFICATION TO BAR ACTION",
            width=btn_width,
            height=btn_height,
            command=lambda: self.generate_form_13(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address
            )
        )

        # CREATE LAYOUT
        self.frame_first_level.pack(anchor='center', pady=(45, 5))
        self.frame_second_level.pack(anchor='center', pady=5)
        self.frame_third_level.pack(anchor='center', pady=5)
        self.frame_fourth_level.pack(anchor='center', pady=(5, 40))
        self.btn_KPFormNo7.pack(side='left')
        self.btn_KPFormNo9.pack(side='left', padx=10)
        self.btn_KPFormNo12_1.pack(side='left')
        self.btn_KPFormNo12_2.pack(side='left')
        self.btn_KPFormNo16.pack(side='left', padx=10)
        self.btn_KPFormNo17.pack(side='left')
        self.btn_KPFormNo13.pack(side='left')
        self.btn_certificate_to_action.pack(side='left', padx=10)
        self.btn_subpoena.pack(side='left')
        self.btn_chosen_pangkat.pack(side='left')
        self.btn_KPFormNo22.pack(side='left', padx=10)
        self.btn_KPFormNo21.pack(side='left')

    def on_closing_select_doc(self):
        self.select_documents_window.grab_release()
        self.select_documents_window.destroy()
        self.view_record_window.grab_set()

    def check_selected_record(self):
        selected = self.tree_blotterData.focus()
        values = self.tree_blotterData.item(selected, 'values')
        return values

    def populate_blotter_tree(self):
        for item in self.tree_blotterData.get_children():
            self.tree_blotterData.delete(item)
        global count
        count = 0
        for record in get_blotterData():
            temp_respondents_names = get_respondents_names(record[2])
            temp_complainants_names = get_complainants_names(record[2])
            respondents_names = []
            complainants_names = []
            for i in range(len(temp_respondents_names)):
                respondents_names.append(
                    get_resident_name(
                        temp_respondents_names[i][2],
                        temp_respondents_names[i][3],
                        temp_respondents_names[i][4],
                        temp_respondents_names[i][5]
                        )
                )
            for j in range(len(temp_complainants_names)):
                complainants_names.append(
                    get_resident_name(
                        temp_complainants_names[j][2],
                        temp_complainants_names[j][3],
                        temp_complainants_names[j][4],
                        temp_complainants_names[j][5]
                        )
                )
            final_respondents_names = concatenate_names(respondents_names)
            final_complainants_names = concatenate_names(complainants_names)

            self.tree_blotterData.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0],
                    record[1],
                    record[2],
                    final_complainants_names,
                    final_respondents_names,
                    record[3]
                )
            )
            count += 1

    def add_record(self):
        self.add_record_window = CTkToplevel(self)
        window_width = 1000
        window_height = 700
        x_axis, y_axis = self._center_screen(window_width, window_height)
        self.add_record_window.title('Add Record')
        self.add_record_window.resizable(False, False)
        self.add_record_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.after(200, lambda: self.add_record_window.iconbitmap(self.add_record_window.iconPath))
        self.add_record_window.geometry("{}x{}+{}+{}".format(
            window_width, window_height, x_axis, y_axis
        ))
        self.add_record_window.transient(self)
        self.add_record_window.grab_set()
        self.add_record_window.focus()

        year_today = str(get_year_today())[2:]
        case_no = ""

        last_blotter_case_no = get_last_blotter_case()

        if last_blotter_case_no == None:
            case_no = "01"
        else:
            last_blotter_case_no = last_blotter_case_no.split('-')

            if int(year_today) > int(last_blotter_case_no[0]):
                case_no = "01"
            else:
                temp_case_no = int(last_blotter_case_no[1]) + 1
                if temp_case_no < 10:
                    temp_case_no = f"0{str(temp_case_no)}"
                case_no = str(temp_case_no)

        blotter_case_no = '-'.join([str(year_today), str(case_no)])

        self.respondents_purok = []

        self.complainants_display_list = []
        self.respondents_display_list = []
        self.complainants_list = []
        self.respondents_list = []

        self.current_button = ""

        self.add_record_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        # CREATE WIDGETS
        self.frame_add_record_window_container = CTkScrollableFrame(
            self.add_record_window,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_add_record = CTkLabel(
            self.frame_add_record_window_container,
            text='ADD BLOTTER RECORD',
            font=self.blotter_label_font
        )
        self.frame_entry_container = CTkFrame(
            self.frame_add_record_window_container,
            fg_color=self.BLOTTER_CONTENT_BG,
            width=300,
        )
        # - Date Filed
        self.frame_date_filed = CTkFrame(
            self.frame_entry_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_date_filed = CTkLabel(
            self.frame_date_filed,
            font=self.blotter_entry_font,
            text='Date Filed: '
        )
        style = ttk.Style(self)
        style.configure('CustomDateEntry.TEntry',
                        foreground='gray14',
                        background=self.BLOTTER_CONTENT_BG,
                        font=self.blotter_date_entry_font,
                        padding=(5, 2, 0, 3), )
        self.entry_date_filed = DateEntry(
            self.frame_date_filed,
            style='CustomDateEntry.TEntry',
            width=24,
            font=self.blotter_date_entry_font,
            pady=10,
            date_pattern='dd-mm-yyyy'
        )
        self.entry_date_filed.bind("<<DateEntrySelected>>", self.check_date)
        # - Barangay Case No.
        self.frame_case_no = CTkFrame(
            self.frame_entry_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_case_no = CTkLabel(
            self.frame_case_no,
            font=self.blotter_entry_font,
            text='Barangay Case No.: '
        )
        self.entry_case_no = CTkEntry(
            self.frame_case_no,
            font=self.blotter_entry_font,
            width=227
        )
        self.entry_case_no.insert(0, blotter_case_no)
        # - Complainants
        self.frame_complainants = CTkFrame(
            self.frame_entry_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.frame_complainants_label = CTkFrame(
            self.frame_complainants,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_complainants = CTkLabel(
            self.frame_complainants_label,
            font=self.blotter_entry_font,
            text='Complainant/s: '
        )
        self.btn_add_complainants = CTkButton(
            self.frame_complainants_label,
            text='Add Complainant/s',
            command=lambda: self.modify_individual('Complainant')
        )
        self.entry_complainants = CTkTextbox(
            self.frame_complainants,
            font=self.blotter_entry_font,
            width=390,
            height=100,
            state='disabled'
        )
        # - Complainants Address
        self.frame_complainants_address = CTkFrame(
            self.frame_entry_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_complainants_address = CTkLabel(
            self.frame_complainants_address,
            font=self.blotter_entry_font,
            text="Complainant's Address: "
        )
        self.frame_purok_address = CTkFrame(
            self.frame_complainants_address,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_purok_address = CTkLabel(
            self.frame_purok_address,
            font=self.blotter_entry_font,
            text="Purok/Zone/Street: "
        )
        self.entry_purok_address = CTkEntry(
            self.frame_purok_address,
            font=self.blotter_entry_font,
            width=237
        )
        self.frame_barangay_address = CTkFrame(
            self.frame_complainants_address,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_barangay_address = CTkLabel(
            self.frame_barangay_address,
            font=self.blotter_entry_font,
            text="Barangay: "
        )
        self.entry_barangay_address = CTkEntry(
            self.frame_barangay_address,
            font=self.blotter_entry_font,
            width=237
        )
        self.frame_city_address = CTkFrame(
            self.frame_complainants_address,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_city_address = CTkLabel(
            self.frame_city_address,
            font=self.blotter_entry_font,
            text="City/Municipality: "
        )
        self.entry_city_address = CTkEntry(
            self.frame_city_address,
            font=self.blotter_entry_font,
            width=237
        )
        self.frame_province_address = CTkFrame(
            self.frame_complainants_address,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_province_address = CTkLabel(
            self.frame_province_address,
            font=self.blotter_entry_font,
            text="Province: "
        )
        self.entry_province_address = CTkEntry(
            self.frame_province_address,
            font=self.blotter_entry_font,
            width=237
        )
        # - Respondents
        self.frame_respondents = CTkFrame(
            self.frame_entry_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.frame_respondents_label = CTkFrame(
            self.frame_respondents,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_respondents = CTkLabel(
            self.frame_respondents_label,
            font=self.blotter_entry_font,
            text='Respondent/s: '
        )
        self.btn_add_respondents = CTkButton(
            self.frame_respondents_label,
            text='Add Respondent/s',
            command=lambda: self.combined_add_respondents_prompt('Respondent'),
            # command=lambda: self.modify_respondents()
        )
        self.entry_respondents = CTkTextbox(
            self.frame_respondents,
            font=self.blotter_entry_font,
            width=390,
            height=100,
            state='disabled'
        )
        # - Respondents Address
        self.frame_respondents_address = CTkFrame(
            self.frame_entry_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_respondents_address = CTkLabel(
            self.frame_respondents_address,
            font=self.blotter_entry_font,
            text="Respondent's Address: "
        )
        self.frame_resp_purok_address = CTkFrame(
            self.frame_respondents_address,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        # self.label_resp_purok_address = CTkLabel(
        #     self.frame_resp_purok_address,
        #     font=self.blotter_entry_font,
        #     text="Purok: "
        # )
        # purok_list = [
        # "Vanda", "Walingwaling", "Bougainvillea", "Mercury", "Daisy",
        # "Orchid", "Chrysanthenum", "Santan", "Rosas", "Sampaguita"
        # ]
        # self.entry_resp_purok_address = CTkComboBox(
        #     self.frame_resp_purok_address,
        #     font=self.blotter_entry_font,
        #     width=237,
        #     values=purok_list,
        #     state='readonly'
        # )
        self.label_resp_purok_address = CTkLabel(
            self.frame_resp_purok_address,
            font=self.blotter_entry_font,
            text="Purok/Zone/Street: "
        )
        self.entry_resp_purok_address = CTkEntry(
            self.frame_resp_purok_address,
            font=self.blotter_entry_font,
            width=237
        )
        self.frame_resp_barangay_address = CTkFrame(
            self.frame_respondents_address,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_resp_barangay_address = CTkLabel(
            self.frame_resp_barangay_address,
            font=self.blotter_entry_font,
            text="Barangay: "
        )
        self.entry_resp_barangay_address = CTkEntry(
            self.frame_resp_barangay_address,
            font=self.blotter_entry_font,
            width=237
        )
        self.frame_resp_city_address = CTkFrame(
            self.frame_respondents_address,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_resp_city_address = CTkLabel(
            self.frame_resp_city_address,
            font=self.blotter_entry_font,
            text="City/Municipality: "
        )
        self.entry_resp_city_address = CTkEntry(
            self.frame_resp_city_address,
            font=self.blotter_entry_font,
            width=237
        )
        self.frame_resp_province_address = CTkFrame(
            self.frame_respondents_address,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_resp_province_address = CTkLabel(
            self.frame_resp_province_address,
            font=self.blotter_entry_font,
            text="Province: "
        )
        self.entry_resp_province_address = CTkEntry(
            self.frame_resp_province_address,
            font=self.blotter_entry_font,
            width=237
        )
        # - Reason
        self.frame_reason = CTkFrame(
            self.frame_entry_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_reason = CTkLabel(
            self.frame_reason,
            font=self.blotter_entry_font,
            text='Reason (Short Description only): '
        )
        self.entry_reason = CTkTextbox(
            self.frame_reason,
            font=self.blotter_entry_font,
            width=390,
            height=100,
        )
        # - Note
        self.frame_note = CTkFrame(
            self.frame_entry_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        self.label_note = CTkLabel(
            self.frame_note,
            font=self.blotter_entry_font,
            text='Note: '
        )
        self.entry_note = CTkTextbox(
            self.frame_note,
            font=self.blotter_entry_font,
            width=390,
            height=100,
        )

        # - Save Record Button
        self.btn_save_record = CTkButton(
            self.frame_entry_container,
            font=self.blotter_entry_font,
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
            text='SAVE RECORD',
            command=self.save_record
        )

        # CREATE LAYOUT
        self.frame_add_record_window_container.pack(side='top', expand='true', fill='both')
        self.label_add_record.pack(side='top', fill='y', pady=10)
        self.frame_entry_container.pack(side='top')
        self.frame_date_filed.pack(anchor='nw', pady=(0, 5))
        self.label_date_filed.pack(side='left')
        self.entry_date_filed.pack(side='left', padx=(80, 0))
        self.frame_case_no.pack(anchor='nw', pady=(0, 5))
        self.label_case_no.pack(side='left')
        self.entry_case_no.pack(side='left', padx=(15, 0))

        self.frame_complainants.pack(anchor='nw', pady=(15, 5))
        self.frame_complainants_label.pack(anchor='nw', fill='x')
        self.label_complainants.pack(side='left')
        self.btn_add_complainants.pack(side='right', pady=(0, 5))
        self.entry_complainants.pack(anchor='nw')

        self.frame_complainants_address.pack(anchor='nw', pady=(0, 5))
        self.label_complainants_address.pack(anchor='nw')
        self.frame_purok_address.pack(anchor='nw', pady=(0, 5))
        self.label_purok_address.pack(side='left', padx=(0, 10))
        self.entry_purok_address.pack(side='left')
        self.frame_barangay_address.pack(anchor='nw', pady=(0, 5))
        self.label_barangay_address.pack(side='left', padx=(0, 75))
        self.entry_barangay_address.pack(side='left')
        self.frame_city_address.pack(anchor='nw', pady=(0, 5))
        self.label_city_address.pack(side='left', padx=(0, 26))
        self.entry_city_address.pack(side='left')
        self.frame_province_address.pack(anchor='nw', pady=(0, 5))
        self.label_province_address.pack(side='left', padx=(0, 81))
        self.entry_province_address.pack(side='left')

        self.frame_respondents.pack(anchor='nw', pady=(15, 5))
        self.frame_respondents_label.pack(anchor='nw', fill='x')
        self.label_respondents.pack(side='left')
        self.btn_add_respondents.pack(side='right', pady=(0, 5))
        self.entry_respondents.pack(anchor='nw')
        self.frame_respondents_address.pack(anchor='nw', pady=(0, 5))
        self.label_respondents_address.pack(anchor='nw')
        self.frame_resp_purok_address.pack(anchor='nw', pady=(0, 5))
        # self.label_resp_purok_address.pack(side='left', padx=(0, 100))
        # self.entry_resp_purok_address.pack(side='left')
        self.label_resp_purok_address.pack(side='left', padx=(0, 10))
        self.entry_resp_purok_address.pack(side='left')
        self.frame_resp_barangay_address.pack(anchor='nw', pady=(0, 5))
        self.label_resp_barangay_address.pack(side='left', padx=(0, 75))
        self.entry_resp_barangay_address.pack(side='left')
        self.frame_resp_city_address.pack(anchor='nw', pady=(0, 5))
        self.label_resp_city_address.pack(side='left', padx=(0, 26))
        self.entry_resp_city_address.pack(side='left')
        self.frame_resp_province_address.pack(anchor='nw', pady=(0, 5))
        self.label_resp_province_address.pack(side='left', padx=(0, 81))
        self.entry_resp_province_address.pack(side='left')

        self.frame_reason.pack(anchor='nw', pady=(15, 5))
        self.label_reason.pack(anchor='nw')
        self.entry_reason.pack(anchor='nw', pady=(0, 5))

        self.frame_note.pack(anchor='nw', pady=(15, 5))
        self.label_note.pack(anchor='nw')
        self.entry_note.pack(anchor='nw', pady=(0, 5))

        self.btn_save_record.pack(anchor='center', pady=10)

    def combined_add_respondents_prompt(self, btn):
        result = messagebox.askyesnocancel("Confirmation", "Do you want to select respondents from profiled residents?\nYes - Select from profiled residents\nNo - Manually enter name\nCancel - Go back")

        if result is None:
            return
        
        if result:
            self.modify_respondents()
        if not result:
            self.modify_individual('Respondent')

    def save_record(self):
        blotter_date_filed = self.entry_date_filed.get()
        blotter_case_no = self.entry_case_no.get()
        temp_complainants_names = self.complainants_list
        temp_complainants_purok = capitalize_sentence(self.entry_purok_address.get())
        temp_complainants_barangay = capitalize_sentence(self.entry_barangay_address.get())
        temp_complainants_city = capitalize_sentence(self.entry_city_address.get())
        temp_complainants_province = capitalize_sentence(self.entry_province_address.get())
        temp_respondents_names = self.respondents_list
        temp_respondents_purok = capitalize_sentence(self.entry_resp_purok_address.get())
        temp_respondents_barangay = capitalize_sentence(self.entry_resp_barangay_address.get())
        temp_respondents_city = capitalize_sentence(self.entry_resp_city_address.get())
        temp_respondents_province = capitalize_sentence(self.entry_resp_province_address.get())
        blotter_reason = clean_sentence(self.entry_reason.get('1.0', END))
        blotter_note = clean_sentence(self.entry_note.get('1.0', END))
        
        if check_blotter_case_no(blotter_case_no):
            messagebox.showwarning('Duplicate Data', 'There is an existing record for this Case No.!')
            return

        if blotter_date_filed == '':
            messagebox.showwarning('Empty Data', 'No Date Selected!')
            return
        if blotter_case_no == '':
            messagebox.showwarning('Empty Data', 'Empty barangay Case No!')
            return
        if len(temp_complainants_names) == 0:
            messagebox.showwarning('Empty Data', 'Empty Complainants Name!')
            return
        if len(temp_respondents_names) == 0:
            messagebox.showwarning('Empty Data', 'Empty Respondents Name!')
            return
        if blotter_reason == '':
            messagebox.showwarning('Empty Data', 'Empty Reason!')
            return
        if (
            not temp_complainants_purok or
            not temp_complainants_barangay or
            not temp_complainants_city or
            not temp_complainants_province or
            not temp_respondents_purok or
            not temp_respondents_barangay or
            not temp_respondents_city or
            not temp_respondents_province
            ):
            messagebox.showwarning('Empty Data', 'Addresses cannot be empty!')
            return

        if not messagebox.askokcancel("Confirmation", "Are you sure you want to confirm?"):
            return

        save_blotter_record(
            blotter_date_filed,
            blotter_case_no,
            blotter_reason,
            blotter_note
        )
        for i in range(len(self.respondents_list)):
            save_blotter_respondents(
                blotter_case_no,
                self.respondents_list[i][0],
                self.respondents_list[i][1],
                self.respondents_list[i][2],
                self.respondents_list[i][3]
            )
        for i in range(len(self.complainants_list)):
            save_blotter_complainants(
                blotter_case_no,
                self.complainants_list[i][0],
                self.complainants_list[i][1],
                self.complainants_list[i][2],
                self.complainants_list[i][3]
            )
        add_complainants_address(
            blotter_case_no,
            temp_complainants_purok,
            temp_complainants_barangay,
            temp_complainants_city,
            temp_complainants_province
        )
        add_respondents_address(
            blotter_case_no,
            temp_respondents_purok,
            temp_respondents_barangay,
            temp_respondents_city,
            temp_respondents_province
        )
        log_blotter(
            get_formatted_datetime(),
            blotter_case_no,
            "RECORD CREATED",
            ACTIVE_USERNAME
        )

        self.populate_blotter_tree()
        self.add_record_window.grab_release()
        self.add_record_window.destroy()

    def modify_respondents(self):
        self.modify_modify_respondents_window = CTkToplevel(self)
        window_width = 400
        window_height = 600
        x_axis, y_axis = self._center_screen(window_width, window_height)
        self.modify_modify_respondents_window.title(f'Add Respondents')
        self.modify_modify_respondents_window.resizable(False, False)
        self.modify_modify_respondents_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.after(200, lambda: self.modify_modify_respondents_window.iconbitmap(self.modify_modify_respondents_window.iconPath))
        self.modify_modify_respondents_window.geometry("{}x{}+{}+{}".format(
            window_width, window_height, x_axis, y_axis
        ))
        self.modify_modify_respondents_window.transient(self)
        self.modify_modify_respondents_window.grab_set()
        self.modify_modify_respondents_window.focus()

        self.modify_modify_respondents_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        # CREATE WIDGETS
        self.label_window = CTkLabel(
            self.modify_modify_respondents_window,
            text=f'Add Respondent',
            font=self.blotter_entry_font
        )
        self.btn_add_name = CTkButton(
            self.modify_modify_respondents_window,
            text='ADD',
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
            text_color=self.TEXT_COLOR,
            command=self.select_respondent
        )
        self.btn_remove_name = CTkButton(
            self.modify_modify_respondents_window,
            text='REMOVE',
            fg_color=self.BTN_BROWN,
            hover_color=self.BTN_HOVER_BROWN,
            text_color=self.TEXT_COLOR,
            command=lambda: self.remove_name('Respondent')
        )
        self.list_name = tk.Listbox(
            self.modify_modify_respondents_window,
            font=self.blotter_entry_font,
            height=17,
            width=60
        )

        # CREATE LAYOUT
        self.label_window.pack(side='top', pady=(20, 10))

        self.btn_add_name.pack(anchor='center', pady=(10, 5))
        self.btn_remove_name.pack(anchor='center', pady=5)

        self.list_name.pack(anchor='center', pady=(10, 15), padx=10)

        self.refresh_listbox('Respondent')

        self.modify_modify_respondents_window.protocol("WM_DELETE_WINDOW", self.on_closing_modify_respondents)


    def select_respondent(self):
        self.select_respondent_window = CTkToplevel(self)
        window_width = 1200
        window_height = 550
        x_axis, y_axis = self._center_screen(window_width, window_height)
        self.select_respondent_window.title(f'Select Respondent')
        self.select_respondent_window.resizable(False, False)
        self.select_respondent_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.after(200, lambda: self.select_respondent_window.iconbitmap(self.select_respondent_window.iconPath))
        self.select_respondent_window.geometry("{}x{}+{}+{}".format(
            window_width, window_height, x_axis, y_axis
        ))
        self.select_respondent_window.transient(self)
        self.select_respondent_window.grab_set()
        self.select_respondent_window.focus()

        self.select_respondent_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.label_window = CTkLabel(
            self.select_respondent_window,
            text=f'Select Respondent',
            font=self.blotter_entry_font
        )

        self.respondents_search_data = StringVar()
        self.entry_respondents_searchbar = CTkEntry(
            self.select_respondent_window,
            font=CONTENT_FONT,
            width=400,
            height=40,
            textvariable=self.respondents_search_data
        )
        self.entry_respondents_searchbar.bind("<KeyRelease>", self.on_respondents_search)

        self.frame_respondents_list = CTkFrame(
            self.select_respondent_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.tree_respondents_list = ttk.Treeview(self.frame_respondents_list)
        self.tree_respondents_list.configure()
        self.tree_respondents_list["columns"] = (
            "Resident ID", "Purok", "Last Name", "First Name", "Middle Name", "Suffix"
        )
        self.tree_respondents_list.heading("#0", text="", anchor='w')
        self.tree_respondents_list.column("#0", width=0, stretch=NO)
        self.tree_respondents_list.heading("Resident ID", text="", anchor='w')
        self.tree_respondents_list.column("Resident ID", width=0, stretch=NO)
        for column in self.tree_respondents_list["columns"][1:]:
            self.tree_respondents_list.heading(column, text=column)
            self.tree_respondents_list.column(column, stretch=YES)
        self.tree_respondents_list_scrollY = ttk.Scrollbar(
            self.frame_respondents_list,
            orient=VERTICAL,
            command=self.tree_respondents_list.yview
        )
        self.tree_respondents_list.configure(
            yscrollcommand=self.tree_respondents_list_scrollY.set
        )

        self.btn_add_respondent = CTkButton(
            self.select_respondent_window,
            text='ADD RESPONDENT',
            command=self.add_selected_respondents
        )

        self.label_window.pack(side='top', pady=(20, 10))
        self.entry_respondents_searchbar.pack(anchor='center')
        self.frame_respondents_list.pack(anchor='center', pady=(10, 20), padx=20, expand='true', fill='both')
        self.tree_respondents_list.pack(anchor='nw', fill='both')
        self.btn_add_respondent.pack(anchor='center', pady=(0, 20))

        respondents_data = get_respondents_list()

        for item in self.tree_respondents_list.get_children():
            self.tree_respondents_list.delete(item)

        global count
        count = 0
        for record in respondents_data:
            self.tree_respondents_list.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    record[4],
                    record[5]
                )
            )
            count += 1

        self.select_respondent_window.protocol("WM_DELETE_WINDOW", self.on_closing_select_respondents)

    def on_respondents_search(self, e):
        search_data = self.respondents_search_data.get()
        self.update_tree_respondents_data(search_data)

    def update_tree_respondents_data(self, search_data):
        for item in self.tree_respondents_list.get_children():
            self.tree_respondents_list.delete(item)

        respondents_data = get_respondents_list()

        for item in respondents_data:
            if (
                search_data.lower() in item[2].lower() or
                search_data.lower() in item[3].lower() or
                search_data.lower() in item[4].lower() 
            ):
                self.tree_respondents_list.insert('', 'end', values=item)

    def add_selected_respondents(self):
        selected = self.tree_respondents_list.focus()
        values = self.tree_respondents_list.item(selected, 'values')

        if not values:
            messagebox.showerror("Error", "There is no individual selected!")
            return

        self.selected_respondent_id = values[0]
        self.selected_respondent_purok = values[1]
        self.selected_respondent_last_name = values[2]
        self.selected_respondent_first_name = values[3]
        self.selected_respondent_middle_name = values[4]
        self.selected_respondent_suffix = values[5]

        if (
           not self.selected_respondent_id or
           not self.selected_respondent_purok or
           not self.selected_respondent_last_name or
           not self.selected_respondent_first_name or
           not self.selected_respondent_middle_name
        ):
            messagebox.showerror("Error", "Incomplete data selected!")
            return
        
        temp_name = (
            self.selected_respondent_first_name,
            self.selected_respondent_middle_name,
            self.selected_respondent_last_name,
            self.selected_respondent_suffix
        )

        temp_display_name = get_resident_name(
            self.selected_respondent_first_name,
            self.selected_respondent_middle_name,
            self.selected_respondent_last_name,
            self.selected_respondent_suffix
        )
        

        self.respondents_display_list.append(temp_display_name)
        self.respondents_list.append(temp_name)

        self.select_respondent_window.grab_release()
        self.select_respondent_window.destroy()

        self.refresh_listbox('Respondent')
        self.display_name('Respondent')

    def modify_individual(self, btn_type):
        self.modify_individual_window = CTkToplevel(self)
        window_width = 400
        window_height = 600
        x_axis, y_axis = self._center_screen(window_width, window_height)
        self.modify_individual_window.title(f'Add {btn_type}')
        self.modify_individual_window.resizable(False, False)
        self.modify_individual_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.after(200, lambda: self.modify_individual_window.iconbitmap(self.modify_individual_window.iconPath))
        self.modify_individual_window.geometry("{}x{}+{}+{}".format(
            window_width, window_height, x_axis, y_axis
        ))
        self.modify_individual_window.transient(self)
        self.modify_individual_window.grab_set()
        self.modify_individual_window.focus()

        self.modify_individual_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.current_button = btn_type

        # CREATE CONSTANTS
        entry_width = 250

        # CREATE WIDGETS
        self.label_window = CTkLabel(
            self.modify_individual_window,
            text=f'Add {btn_type}',
            font=self.blotter_entry_font
        )
        # First Name
        self.frame_first_name_container = CTkFrame(
            self.modify_individual_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_first_name = CTkLabel(
            self.frame_first_name_container,
            font=self.blotter_entry_font,
            text="First Name: "
        )
        self.entry_first_name = CTkEntry(
            self.frame_first_name_container,
            font=self.blotter_entry_font,
            width=entry_width
        )
        # Middle Name
        self.frame_middle_name_container = CTkFrame(
            self.modify_individual_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_middle_name = CTkLabel(
            self.frame_middle_name_container,
            font=self.blotter_entry_font,
            text="Middle Name: "
        )
        self.entry_middle_name = CTkEntry(
            self.frame_middle_name_container,
            font=self.blotter_entry_font,
            width=entry_width
        )
        # Last Name
        self.frame_last_name_container = CTkFrame(
            self.modify_individual_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_last_name = CTkLabel(
            self.frame_last_name_container,
            font=self.blotter_entry_font,
            text="Last Name: "
        )
        self.entry_last_name = CTkEntry(
            self.frame_last_name_container,
            font=self.blotter_entry_font,
            width=entry_width
        )
        # Suffix
        self.frame_suffix_name_container = CTkFrame(
            self.modify_individual_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_suffix_name = CTkLabel(
            self.frame_suffix_name_container,
            font=self.blotter_entry_font,
            text="Suffix: "
        )
        self.entry_suffix_name = CTkEntry(
            self.frame_suffix_name_container,
            font=self.blotter_entry_font,
            width=entry_width
        )
        self.btn_add_name = CTkButton(
            self.modify_individual_window,
            text='ADD',
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
            text_color=self.TEXT_COLOR,
            command=lambda: self.add_name(btn_type)
        )
        self.btn_remove_name = CTkButton(
            self.modify_individual_window,
            text='REMOVE',
            fg_color=self.BTN_BROWN,
            hover_color=self.BTN_HOVER_BROWN,
            text_color=self.TEXT_COLOR,
            command=lambda: self.remove_name(btn_type)
        )
        self.list_name = tk.Listbox(
            self.modify_individual_window,
            font=self.blotter_entry_font,
            height=17,
            width=60
        )

        # CREATE LAYOUT
        self.label_window.pack(side='top', pady=(20, 10))

        self.frame_first_name_container.pack(anchor='w', pady=5, padx=(20, 0))
        self.label_first_name.pack(side='left', padx=(0, 25))
        self.entry_first_name.pack(side='left')

        self.frame_middle_name_container.pack(anchor='w', pady=5, padx=(20, 0))
        self.label_middle_name.pack(side='left', padx=(0, 10))
        self.entry_middle_name.pack(side='left')

        self.frame_last_name_container.pack(anchor='w', pady=5, padx=(20, 0))
        self.label_last_name.pack(side='left', padx=(0, 28))
        self.entry_last_name.pack(side='left')

        self.frame_suffix_name_container.pack(anchor='w', pady=5, padx=(20, 0))
        self.label_suffix_name.pack(side='left', padx=(0, 65))
        self.entry_suffix_name.pack(side='left')

        self.btn_add_name.pack(anchor='center', pady=(10, 5))
        self.btn_remove_name.pack(anchor='center', pady=5)

        self.list_name.pack(anchor='center', pady=(10, 15), padx=10)

        self.refresh_listbox(btn_type)

        self.modify_individual_window.protocol("WM_DELETE_WINDOW", self.on_closing_modify_individual_window)


    def add_name(self, btn_type):
        if (not self.entry_first_name.get() or 
            not self.entry_middle_name.get() or 
            not self.entry_last_name.get()):
            messagebox.showerror("Empty Field", "First, Middle, and Last Name cannot be empty!")
            return
        temp_name = [self.entry_first_name.get(), 
                     self.entry_middle_name.get(), 
                     self.entry_last_name.get(),
                     self.entry_suffix_name.get()]
        temp_display_name = get_resident_name(self.entry_first_name.get(), 
                                              self.entry_middle_name.get(), 
                                              self.entry_last_name.get(),
                                              self.entry_suffix_name.get())
        if btn_type == 'Respondent':
            self.respondents_display_list.append(temp_display_name)
            self.respondents_list.append(temp_name)
        if btn_type == 'Complainant':
            self.complainants_display_list.append(temp_display_name)
            self.complainants_list.append(temp_name)

        self.refresh_listbox(btn_type)
        self.clear_name_entries()
        self.display_name(btn_type)

    def remove_name(self, btn_type):
        selected_current_list = []
        selected_current_display_list = []
        if btn_type == 'Respondent':
            selected_current_display_list = self.respondents_display_list
            selected_current_list = self.respondents_list
        if btn_type == 'Complainant':
            selected_current_display_list = self.complainants_display_list
            selected_current_list = self.complainants_list

        try:
            selected_index = self.list_name.curselection()[0]
            selected_current_list.pop(selected_index)
            selected_current_display_list.pop(selected_index)

            if btn_type == 'Respondent':
                self.respondents_display_list = selected_current_display_list
                self.respondents_list = selected_current_list
            if btn_type == 'Complainant':
                self.complainants_display_list = selected_current_display_list
                self.complainants_list = selected_current_list

            self.refresh_listbox(btn_type)
            self.display_name(btn_type)
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a name to remove.")
        
    def display_name(self, btn_type):
        names = ""
        if btn_type == 'Respondent':
            names = concatenate_names(self.current_list_view)
            self.entry_respondents.configure(state='normal')
            self.entry_respondents.delete('1.0', END)
            self.entry_respondents.insert('1.0', names)
            self.entry_respondents.configure(state='disabled')
        if btn_type == 'Complainant':
            names = concatenate_names(self.current_list_view)
            self.entry_complainants.configure(state='normal')
            self.entry_complainants.delete('1.0', END)
            self.entry_complainants.insert('1.0', names)
            self.entry_complainants.configure(state='disabled')

    def clear_name_entries(self):
        self.entry_first_name.delete(0, tk.END)
        self.entry_middle_name.delete(0, tk.END)
        self.entry_last_name.delete(0, tk.END)
        self.entry_suffix_name.delete(0, tk.END)

    def refresh_listbox(self, btn_type):
        if btn_type == 'Respondent':
            self.current_list_view = self.respondents_display_list
        elif btn_type == 'Complainant':
            self.current_list_view = self.complainants_display_list

        # Clear the Listbox
        self.list_name.delete(0, tk.END)
        for item in self.current_list_view:
            self.list_name.insert(tk.END, item)

    def _center_screen(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        return x_axis, y_axis
    
    def check_date(self, e):
        if not validate_birthDate(self.entry_date_filed.get()):
            messagebox.showinfo("Input Error", "Date cannot be greater than today!")
            self.entry_date_filed.set_date(get_date_today())
            return

    def generate_form_12(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return

        if check_document_exist(values[2], "Form12"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return
        
        self.form_12_window = CTkToplevel(self)
        self.form_12_window.title("KP Form No. 22 - Certification to Bar Counterclaim")
        self.form_12_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_12_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_12_window.after(200, lambda: self.form_12_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 255
        x, y = self._center_screen(window_width, window_height)
        self.form_12_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_12_window.transient(self)
        self.form_12_window.grab_set()

        self.form_12_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.frame_form_12_container = CTkFrame(
            self.form_12_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.in_charge_list = get_form_9_data()

        self.secretary_var = StringVar(value=self.in_charge_list[1])
        self.chairman_var = StringVar(value=self.in_charge_list[2])

        self.label_secretary_name = CTkLabel(
            self.frame_form_12_container,
            font=self.blotter_entry_font,
            text="Pangkat Secretary: "
        )

        self.entry_secretary_name = CTkOptionMenu(
            self.frame_form_12_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.secretary_var
        )

        self.label_chairman_name = CTkLabel(
            self.frame_form_12_container,
            font=self.blotter_entry_font,
            text="Pangkat Chairman: "
        )

        self.entry_chairman_name = CTkOptionMenu(
            self.frame_form_12_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.chairman_var
        )
        
        self.btn_confirm = CTkButton(
            self.frame_form_12_container,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_12(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.secretary_var.get(),
                self.chairman_var.get()
                )
        )
        
        self.frame_form_12_container.pack(anchor='center')
        self.label_secretary_name.pack(anchor='w', pady=(30, 5))
        self.entry_secretary_name.pack(anchor='center')
        self.label_chairman_name.pack(anchor='w', pady=(10, 5))
        self.entry_chairman_name.pack(anchor='center')

        self.btn_confirm.pack(anchor='center', pady=(20, 0))

        self.form_12_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form12"))

    def finalize_form_12(
            self, 
            values,
            cmplnts, 
            rspndnts, 
            comp_add, 
            res_add, 
            secretary,
            chairman
            ):
        if not secretary or not chairman:
            messagebox.showwarning("Empty Data", "Please fill in all fields.")
            return

        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected Pangkat,\nSecretary: {secretary}\nChairman: {chairman}"):
            return
        
        process = multiprocessing.Process(
            target=do_form_12,
            args=(
                values,
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add, 
                secretary,
                chairman
            )
        )
        process.start()

        messagebox.showinfo(
            "Success", "Generating KP Form No. 22 - Certification to Bar Counterclaim.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED KP Form No. 22 - Certification to Bar Counterclaim",
            ACTIVE_USERNAME
            )
        self.close_windows("Form12")

    def generate_form_13(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return
        
        if check_document_exist(values[2], "Form13"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return
        
        self.form_13_window = CTkToplevel(self)
        self.form_13_window.title("KP Form No. 22 - Certification to Bar Action")
        self.form_13_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_13_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_13_window.after(200, lambda: self.form_13_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 325
        x, y = self._center_screen(window_width, window_height)
        self.form_13_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_13_window.transient(self)
        self.form_13_window.grab_set()
        
        self.form_13_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.frame_form_13_container = CTkFrame(
            self.form_13_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.in_charge_list = get_form_9_data()

        self.member_var = StringVar(value=self.in_charge_list[0])
        self.secretary_var = StringVar(value=self.in_charge_list[1])
        self.chairman_var = StringVar(value=self.in_charge_list[2])

        self.label_member_name = CTkLabel(
            self.frame_form_13_container,
            font=self.blotter_entry_font,
            text="Pangkat Member: "
        )

        self.entry_member_name = CTkOptionMenu(
            self.frame_form_13_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.member_var
        )

        self.label_secretary_name = CTkLabel(
            self.frame_form_13_container,
            font=self.blotter_entry_font,
            text="Pangkat Secretary: "
        )

        self.entry_secretary_name = CTkOptionMenu(
            self.frame_form_13_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.secretary_var
        )

        self.label_chairman_name = CTkLabel(
            self.frame_form_13_container,
            font=self.blotter_entry_font,
            text="Pangkat Chairman: "
        )

        self.entry_chairman_name = CTkOptionMenu(
            self.frame_form_13_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.chairman_var
        )
        
        self.btn_confirm = CTkButton(
            self.frame_form_13_container,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_13(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.secretary_var.get(),
                self.member_var.get(),
                self.chairman_var.get()
                )
        )
        
        self.frame_form_13_container.pack(anchor='center')
        self.label_member_name.pack(anchor='w', pady=(30, 5))
        self.entry_member_name.pack(anchor='center')
        self.label_secretary_name.pack(anchor='w', pady=(10, 5))
        self.entry_secretary_name.pack(anchor='center')
        self.label_chairman_name.pack(anchor='w', pady=(10, 5))
        self.entry_chairman_name.pack(anchor='center')
        self.entry_chairman_name.pack(anchor='nw')

        self.btn_confirm.pack(anchor='center', pady=(20, 0))

        self.form_13_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form13"))

    def finalize_form_13(
            self, 
            values,
            cmplnts, 
            rspndnts, 
            comp_add, 
            res_add, 
            secretary,
            member,
            chairman
            ):
        if not secretary or not member or not chairman:
            messagebox.showwarning("Empty Data", "Please fill in all fields.")
            return

        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected Pangkat,\nMember: {member}\nSecretary: {secretary}\nChairman: {chairman}"):
            return
        
        process = multiprocessing.Process(
            target=do_form_13,
            args=(
                values,
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add, 
                secretary,
                member,
                chairman
            )
        )
        process.start()

        messagebox.showinfo(
            "Success", "Generating KP Form No. 21 - Certification to Bar Action.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED KP Form No. 21 - Certification to Bar Action",
            ACTIVE_USERNAME
            )
        self.close_windows("Form13")

    def generate_form_11(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return
        
        if check_document_exist(values[2], "Form11"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return
        
        self.form_11_window = CTkToplevel(self)
        self.form_11_window.title("Notice to Chosen Pangkat Member")
        self.form_11_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_11_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_11_window.after(200, lambda: self.form_11_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 615
        x, y = self._center_screen(window_width, window_height)
        self.form_11_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_11_window.transient(self)
        self.form_11_window.grab_set()
        
        self.form_11_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.frame_form_11_container = CTkFrame(
            self.form_11_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_summon_date = CTkLabel(
            self.frame_form_11_container,
            font=self.blotter_entry_font,
            text='Invitation Date: '
        )
        self.frame_summon_date = CTkFrame(
            self.frame_form_11_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        style = ttk.Style(self)
        style.configure('CustomDateEntry.TEntry',
                        foreground='gray14',
                        background=CONTENT_BG,
                        font=TK_CONTENT_FONT,
                        padding=(5, 2, 0, 3), )
        self.entry_summon_date = DateEntry(
            self.frame_summon_date,
            style='CustomDateEntry.TEntry',
            width=27,
            font=TK_CONTENT_FONT,
            pady=10,
            date_pattern='dd-mm-yyyy'
        )
        self.label_summon_time = CTkLabel(
            self.frame_form_11_container,
            font=self.blotter_entry_font,
            text='Invitation Time: '
        )
        self.frame_summon_time = CTkFrame(
            self.frame_form_11_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.entry_summon_time = CTkEntry(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=160,
            placeholder_text="HH:MM"
        )
        period_value = ["AM", "PM"]
        self.time_period_var = StringVar(value=period_value[0])
        self.entry_summon_time_period = CTkOptionMenu(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=80,
            fg_color='#FAFAFA',
            text_color="#000",
            values=period_value,
            variable=self.time_period_var
        )

        self.pangkat_list = get_barangay_pangkat_member()
        self.first_pangkat_var = StringVar(value=self.pangkat_list[0])
        self.second_pangkat_var = StringVar(value=self.pangkat_list[1])
        self.third_pangkat_var = StringVar(value=self.pangkat_list[2])

        self.purok_list = [
            "Vanda", "Walingwaling", "Bougainvillea", "Mercury", "Daisy",
            "Orchid", "Chrysanthemum", "Santan", "Rosas", "Sampaguita"
        ]
        self.first_pangkat_purok_var = StringVar(value=self.purok_list[0])
        self.second_pangkat_purok_var = StringVar(value=self.purok_list[1])
        self.third_pangkat_purok_var = StringVar(value=self.purok_list[2])

        self.label_chosen_pangkat = CTkLabel(
            self.frame_form_11_container,
            font=self.blotter_entry_font,
            text='CHOSEN PANGKAT: '
            )
        
        self.label_first_pangkat_name = CTkLabel(
            self.frame_form_11_container,
            font=self.blotter_entry_font,
            text='First Pangkat: '
        )
        self.entry_first_pangkat_name = CTkOptionMenu(
            self.frame_form_11_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color='#FAFAFA',
            text_color="#000",
            values=self.pangkat_list,
            variable=self.first_pangkat_var
        )
        self.frame_first_pangkat_purok = CTkFrame(
            self.frame_form_11_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_first_pangkat_purok = CTkLabel(
            self.frame_first_pangkat_purok,
            font=self.blotter_entry_font,
            text='Purok: '
        )
        self.entry_first_pangkat_purok = CTkOptionMenu(
            self.frame_first_pangkat_purok,
            font=self.blotter_entry_font,
            width=180,
            fg_color='#FAFAFA',
            text_color="#000",
            values=self.purok_list,
            variable=self.first_pangkat_purok_var
        )

        self.label_second_pangkat_name = CTkLabel(
            self.frame_form_11_container,
            font=self.blotter_entry_font,
            text='Second Pangkat: '
        )
        self.entry_second_pangkat_name = CTkOptionMenu(
            self.frame_form_11_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color='#FAFAFA',
            text_color="#000",
            values=self.pangkat_list,
            variable=self.second_pangkat_var
        )
        self.frame_second_pangkat_purok = CTkFrame(
            self.frame_form_11_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_second_pangkat_purok = CTkLabel(
            self.frame_second_pangkat_purok,
            font=self.blotter_entry_font,
            text='Purok: '
        )
        self.entry_second_pangkat_purok = CTkOptionMenu(
            self.frame_second_pangkat_purok,
            font=self.blotter_entry_font,
            width=180,
            fg_color='#FAFAFA',
            text_color="#000",
            values=self.purok_list,
            variable=self.second_pangkat_purok_var
        )

        self.label_third_pangkat_name = CTkLabel(
            self.frame_form_11_container,
            font=self.blotter_entry_font,
            text='Third Pangkat: '
        )
        self.entry_third_pangkat_name = CTkOptionMenu(
            self.frame_form_11_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color='#FAFAFA',
            text_color="#000",
            values=self.pangkat_list,
            variable=self.third_pangkat_var
        )
        self.frame_third_pangkat_purok = CTkFrame(
            self.frame_form_11_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_third_pangkat_purok = CTkLabel(
            self.frame_third_pangkat_purok,
            font=self.blotter_entry_font,
            text='Purok: '
        )
        self.entry_third_pangkat_purok = CTkOptionMenu(
            self.frame_third_pangkat_purok,
            font=self.blotter_entry_font,
            width=180,
            fg_color='#FAFAFA',
            text_color="#000",
            values=self.purok_list,
            variable=self.third_pangkat_purok_var
        )

        self.btn_confirm = CTkButton(
            self.frame_form_11_container,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_11(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.entry_summon_date.get_date(),
                self.entry_summon_time.get(),
                self.time_period_var.get(),
                self.first_pangkat_var.get(),
                self.second_pangkat_var.get(),
                self.third_pangkat_var.get(),
                self.first_pangkat_purok_var.get(),
                self.second_pangkat_purok_var.get(),
                self.third_pangkat_purok_var.get()
                )
        )
        
        self.frame_form_11_container.pack(anchor='center')
        self.label_summon_date.pack(anchor='w', pady=(30, 5))
        self.frame_summon_date.pack(anchor='center')
        self.entry_summon_date.pack(anchor='nw')
        self.label_summon_time.pack(anchor='w', pady=(10, 5))
        self.frame_summon_time.pack(anchor='center')
        self.entry_summon_time.pack(side='left')
        self.entry_summon_time_period.pack(side='left')

        self.label_chosen_pangkat.pack(anchor='w', pady=(30, 5))
        self.label_first_pangkat_name.pack(anchor='nw')
        self.entry_first_pangkat_name.pack(anchor='center')
        self.frame_first_pangkat_purok.pack(anchor='nw', pady=(5, 10))
        self.label_first_pangkat_purok.pack(side='left', padx=(0, 10))
        self.entry_first_pangkat_purok.pack(side='left')

        self.label_second_pangkat_name.pack(anchor='nw')
        self.entry_second_pangkat_name.pack(anchor='center')
        self.frame_second_pangkat_purok.pack(anchor='nw', pady=(5, 10))
        self.label_second_pangkat_purok.pack(side='left', padx=(0, 10))
        self.entry_second_pangkat_purok.pack(side='left')

        self.label_third_pangkat_name.pack(anchor='nw')
        self.entry_third_pangkat_name.pack(anchor='center')
        self.frame_third_pangkat_purok.pack(anchor='nw', pady=(5, 10))
        self.label_third_pangkat_purok.pack(side='left', padx=(0, 10))
        self.entry_third_pangkat_purok.pack(side='left')

        self.btn_confirm.pack(anchor='center', pady=(20, 0))

        self.form_11_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form11"))

    def finalize_form_11(
            self, 
            values,
            cmplnts, 
            rspndnts, 
            comp_add, 
            res_add, 
            date, 
            time, 
            period,
            first_pangkat,
            second_pangkat,
            third_pangkat,
            first_purok,
            second_purok,
            third_purok
            ):
        if not date or not time or not period:
            messagebox.showwarning("Empty Data", "Please fill in both time and date sections.")
            return

        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nDate: {date}\nTime: {time} {period}\nPangkat: {first_pangkat} from {first_purok}\nPangkat: {second_pangkat} from {second_purok}\nPangkat: {third_pangkat} from {third_purok}"):
            return
        
        process = multiprocessing.Process(
            target=do_form_11,
            args=(
                values,
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add, 
                date, 
                time, 
                period,
                first_pangkat,
                second_pangkat,
                third_pangkat,
                first_purok,
                second_purok,
                third_purok
            )
        )
        process.start()

        messagebox.showinfo(
            "Success", "Generating Certificate to Chosen Pangkat Member.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED Certificate to Chosen Pangkat Member",
            ACTIVE_USERNAME
            )
        self.close_windows("Form11")

    def generate_form_10(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return
        
        if check_document_exist(values[2], "Form10"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return
        
        self.form_10_window = CTkToplevel(self)
        self.form_10_window.title("Subpoena")
        self.form_10_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_10_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_10_window.after(200, lambda: self.form_10_window.iconbitmap(self.iconPath))
        window_width = 500
        window_height = 545
        x, y = self._center_screen(window_width, window_height)
        self.form_10_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_10_window.transient(self)
        self.form_10_window.grab_set()
        
        self.form_10_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.frame_form_10_container = CTkFrame(
            self.form_10_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_summon_name = CTkLabel(
            self.frame_form_10_container,
            font=self.blotter_entry_font,
            text='Name: '
        )
        self.entry_summon_name = CTkEntry(
            self.frame_form_10_container,
            font=self.blotter_entry_font,
            width=300,
            placeholder_text="Ex. Juan D. Dela Cruz Sr."
        )

        self.label_summon_address = CTkLabel(
            self.frame_form_10_container,
            font=self.blotter_entry_font,
            text='Address: '
        )

        self.frame_summon_address_purok = CTkFrame(
            self.frame_form_10_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_summon_address_purok = CTkLabel(
            self.frame_summon_address_purok,
            font=self.blotter_entry_font,
            text='Purok/Zone/Street: '
        )
        self.entry_summon_address_purok = CTkEntry(
            self.frame_summon_address_purok,
            font=self.blotter_entry_font,
            width=180
        )

        self.frame_summon_address_barangay = CTkFrame(
            self.frame_form_10_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_summon_address_barangay = CTkLabel(
            self.frame_summon_address_barangay,
            font=self.blotter_entry_font,
            text='Barangay: '
        )
        self.entry_summon_address_barangay = CTkEntry(
            self.frame_summon_address_barangay,
            font=self.blotter_entry_font,
            width=180
        )

        self.frame_summon_address_city = CTkFrame(
            self.frame_form_10_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_summon_address_city = CTkLabel(
            self.frame_summon_address_city,
            font=self.blotter_entry_font,
            text='City/Municipality: '
        )
        self.entry_summon_address_city = CTkEntry(
            self.frame_summon_address_city,
            font=self.blotter_entry_font,
            width=180
        )

        self.frame_summon_address_province = CTkFrame(
            self.frame_form_10_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_summon_address_province = CTkLabel(
            self.frame_summon_address_province,
            font=self.blotter_entry_font,
            text='Province: '
        )
        self.entry_summon_address_province = CTkEntry(
            self.frame_summon_address_province,
            font=self.blotter_entry_font,
            width=180
        )

        self.label_summon_date = CTkLabel(
            self.frame_form_10_container,
            font=self.blotter_entry_font,
            text='Invitation Date: '
        )
        self.frame_summon_date = CTkFrame(
            self.frame_form_10_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        style = ttk.Style(self)
        style.configure('CustomDateEntry.TEntry',
                        foreground='gray14',
                        background=CONTENT_BG,
                        font=TK_CONTENT_FONT,
                        padding=(5, 2, 0, 3), )
        self.entry_summon_date = DateEntry(
            self.frame_summon_date,
            style='CustomDateEntry.TEntry',
            width=27,
            font=TK_CONTENT_FONT,
            pady=10,
            date_pattern='dd-mm-yyyy'
        )
        self.label_summon_time = CTkLabel(
            self.frame_form_10_container,
            font=self.blotter_entry_font,
            text='Invitation Time: '
        )
        self.frame_summon_time = CTkFrame(
            self.frame_form_10_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.entry_summon_time = CTkEntry(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=160,
            placeholder_text="HH:MM"
        )
        period_value = ["AM", "PM"]
        self.time_period_var = StringVar(value=period_value[0])
        self.entry_summon_time_period = CTkOptionMenu(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=80,
            fg_color='#FAFAFA',
            text_color="#000",
            values=period_value,
            variable=self.time_period_var
        )

        self.label_in_charge_name = CTkLabel(
            self.frame_form_10_container,
            font=self.blotter_entry_font,
            text="Facilitating Official (Barangay/Pangkat Chairman): "
        )
        self.in_charge_list = get_form_5_in_charge()
        self.in_charge_var = StringVar(value=self.in_charge_list[0])
        self.entry_in_charge_name = CTkOptionMenu(
            self.frame_form_10_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.in_charge_var,
            command=self.form_5_on_change
        )
        self.entry_in_charge_role = "Punong Barangay"

        self.btn_confirm = CTkButton(
            self.frame_form_10_container,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_10(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.entry_summon_name.get(),
                self.entry_summon_address_purok.get(),
                self.entry_summon_address_barangay.get(),
                self.entry_summon_address_city.get(),
                self.entry_summon_address_province.get(),
                self.entry_summon_date.get_date(),
                self.entry_summon_time.get(),
                self.time_period_var.get(),
                self.in_charge_var.get(),
                self.entry_in_charge_role
                )
        )
        
        self.frame_form_10_container.pack(anchor='center')
        self.label_summon_name.pack(anchor='nw', pady=(30, 0))
        self.entry_summon_name.pack(anchor='center', pady=(0, 10))

        self.label_summon_address.pack(anchor='nw', pady=(0, 5))
        self.frame_summon_address_purok.pack(anchor='nw', pady=(0, 5))
        self.label_summon_address_purok.pack(side='left')
        self.entry_summon_address_purok.pack(side='left', padx=(8, 0))
        self.frame_summon_address_barangay.pack(anchor='nw', pady=(0, 5))
        self.label_summon_address_barangay.pack(side='left')
        self.entry_summon_address_barangay.pack(side='left', padx=(73, 0))
        self.frame_summon_address_city.pack(anchor='nw', pady=(0, 5))
        self.label_summon_address_city.pack(side='left')
        self.entry_summon_address_city.pack(side='left', padx=(24, 0))
        self.frame_summon_address_province.pack(anchor='nw', pady=(0, 10))
        self.label_summon_address_province.pack(side='left')
        self.entry_summon_address_province.pack(side='left', padx=(79, 0))

        self.label_summon_date.pack(anchor='nw')
        self.frame_summon_date.pack(anchor='center', pady=(0, 10))
        self.entry_summon_date.pack(anchor='nw')
        self.label_summon_time.pack(anchor='nw')
        self.frame_summon_time.pack(anchor='center', pady=(0, 10))
        self.entry_summon_time.pack(side='left')
        self.entry_summon_time_period.pack(side='left')

        self.label_in_charge_name.pack(anchor="nw")
        self.entry_in_charge_name.pack(anchor='center', pady=(0, 20))

        self.btn_confirm.pack(anchor='center')

        self.form_10_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form10"))

    def finalize_form_10(
            self, 
            values,
            complainants,
            respondents,
            complainants_address,
            respondents_address,
            summon_name,
            summon_purok,
            summon_barangay,
            summon_city,
            summon_province,
            summon_date,
            summon_time,
            summon_time_period,
            in_charge_name,
            in_charge_role
            ):
        if (not date or 
            not summon_name or 
            not summon_purok or 
            not summon_barangay or 
            not summon_city or 
            not summon_province or 
            not summon_date or 
            not summon_time or 
            not summon_time_period or 
            not in_charge_name or
            not in_charge_role):
            messagebox.showwarning("Empty Data", "Please fill in fields.")
            return
        
        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nSummon name: {summon_name}\nPurok: {summon_purok}\nBarangay: {summon_barangay}\nCity: {summon_city}\nProvince: {summon_province}\nDate: {summon_date}\nTime: {summon_time} {summon_time_period}\nOfficial In-charge: {in_charge_name}\nIn-charge role: {in_charge_role}"):
            return
        
        process = multiprocessing.Process(
            target=do_form_10,
            args=(
                values,
                complainants,
                respondents,
                complainants_address,
                respondents_address,
                summon_name,
                summon_purok,
                summon_barangay,
                summon_city,
                summon_province,
                summon_date,
                summon_time,
                summon_time_period,
                in_charge_name,
                in_charge_role
            )
        )
        process.start()

        messagebox.showinfo(
            "Success", "Generating Subpoena.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED Subpoena",
            ACTIVE_USERNAME
            )
        self.close_windows("Form10")

    def generate_form_9(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return
        
        if check_document_exist(values[2], "Form9"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return
        
        self.form_9_window = CTkToplevel(self)
        self.form_9_window.title("Certificate to File Action")
        self.form_9_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_9_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_9_window.after(200, lambda: self.form_9_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 325
        x, y = self._center_screen(window_width, window_height)
        self.form_9_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_9_window.transient(self)
        self.form_9_window.grab_set()
        
        self.form_9_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )
        
        self.in_charge_list = get_form_9_data()

        self.member_var = StringVar(value=self.in_charge_list[0])
        self.secretary_var = StringVar(value=self.in_charge_list[1])
        self.chairman_var = StringVar(value=self.in_charge_list[2])

        self.label_member_name = CTkLabel(
            self.form_9_window,
            font=self.blotter_entry_font,
            text="Pangkat Member: "
        )

        self.entry_member_name = CTkOptionMenu(
            self.form_9_window,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.member_var
        )

        self.label_secretary_name = CTkLabel(
            self.form_9_window,
            font=self.blotter_entry_font,
            text="Pangkat Secretary: "
        )

        self.entry_secretary_name = CTkOptionMenu(
            self.form_9_window,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.secretary_var
        )

        self.label_chairman_name = CTkLabel(
            self.form_9_window,
            font=self.blotter_entry_font,
            text="Pangkat Chairman: "
        )

        self.entry_chairman_name = CTkOptionMenu(
            self.form_9_window,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.chairman_var
        )

        self.btn_confirm = CTkButton(
            self.form_9_window,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_9(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.member_var.get(),
                self.secretary_var.get(),
                self.chairman_var.get()
                )
        )
        
        self.label_member_name.pack(anchor='w', pady=(30, 5), padx=(50, 0))
        self.entry_member_name.pack(anchor='center')
        self.label_secretary_name.pack(anchor='w', pady=(10, 5), padx=(50, 0))
        self.entry_secretary_name.pack(anchor='center')
        self.label_chairman_name.pack(anchor='w', pady=(10, 5), padx=(50, 0))
        self.entry_chairman_name.pack(anchor='center')
        self.btn_confirm.pack(anchor='center', pady=(20, 0))
        
        self.form_9_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form9"))

    def finalize_form_9(self, values, cmplnts, rspndnts, comp_add, res_add, member, secretary, chairman):
        if not member and not secretary and not chairman:
            messagebox.showwarning("Empty Data", "Please select the individuals.")
            return
        
        if (
            member == secretary or 
            member == chairman or 
            secretary == chairman
            ):
            messagebox.showwarning("Duplicate Selection", "Please select unique individuals.")
            return
        
        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected Pangkat,\nMember: {member}\nSecretary: {secretary}\nChairman: {chairman}"):
            return
        
        process = multiprocessing.Process(
            target=do_form_9,
            args=(
                values,
                cmplnts,
                rspndnts,
                comp_add,
                res_add,
                member,
                secretary,
                chairman
            )
        )
        process.start()
        messagebox.showinfo(
            "Success", "Generating Certificate to File Action.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED Certificate to File Action",
            ACTIVE_USERNAME
            )
        self.close_windows("Form9")

    def generate_form_8(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return
        
        if check_document_exist(values[2], "Form8"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return
        
        self.form_8_window = CTkToplevel(self)
        self.form_8_window.title("KP Form No. 13 - Notice of Hearing (Conciliation Proceedings)")
        self.form_8_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_8_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_8_window.after(200, lambda: self.form_8_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 255
        x, y = self._center_screen(window_width, window_height)
        self.form_8_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_8_window.transient(self)
        self.form_8_window.grab_set()
        
        self.form_8_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.frame_form_8_container = CTkFrame(
            self.form_8_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_summon_date = CTkLabel(
            self.frame_form_8_container,
            font=self.blotter_entry_font,
            text='Invitation Date: '
        )
        self.frame_summon_date = CTkFrame(
            self.frame_form_8_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        style = ttk.Style(self)
        style.configure('CustomDateEntry.TEntry',
                        foreground='gray14',
                        background=CONTENT_BG,
                        font=TK_CONTENT_FONT,
                        padding=(5, 2, 0, 3), )
        self.entry_summon_date = DateEntry(
            self.frame_summon_date,
            style='CustomDateEntry.TEntry',
            width=27,
            font=TK_CONTENT_FONT,
            pady=10,
            date_pattern='dd-mm-yyyy'
        )
        self.label_summon_time = CTkLabel(
            self.frame_form_8_container,
            font=self.blotter_entry_font,
            text='Invitation Time: '
        )
        self.frame_summon_time = CTkFrame(
            self.frame_form_8_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.entry_summon_time = CTkEntry(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=160,
            placeholder_text="HH:MM"
        )
        period_value = ["AM", "PM"]
        self.time_period_var = StringVar(value=period_value[0])
        self.entry_summon_time_period = CTkOptionMenu(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=80,
            fg_color='#FAFAFA',
            text_color="#000",
            values=period_value,
            variable=self.time_period_var
        )
        self.btn_confirm = CTkButton(
            self.frame_form_8_container,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_8(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.entry_summon_date.get_date(),
                self.entry_summon_time.get(),
                self.time_period_var.get()
                )
        )
        
        self.frame_form_8_container.pack(anchor='center')
        self.label_summon_date.pack(anchor='w', pady=(30, 5))
        self.frame_summon_date.pack(anchor='center')
        self.entry_summon_date.pack(anchor='nw')
        self.label_summon_time.pack(anchor='w', pady=(10, 5))
        self.frame_summon_time.pack(anchor='center')
        self.entry_summon_time.pack(side='left')
        self.entry_summon_time_period.pack(side='left')
        self.btn_confirm.pack(anchor='center', pady=(20, 0))

        self.form_8_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form8"))

    def finalize_form_8(self, values, cmplnts, rspndnts, comp_add, res_add, date, time, period):
        if not date or not time or not period:
            messagebox.showwarning("Empty Data", "Please fill in both time and date sections.")
            return
        
        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nDate: {date}\nTime: {time} {period}"):
            return

        process = multiprocessing.Process(
            target=do_form_8,
            args=(
                values,
                cmplnts,
                rspndnts,
                comp_add,
                res_add,
                date,
                time,
                period
            )
        )
        process.start()

        messagebox.showinfo(
            "Success", "Generating KP Form No. 13 - Notice of Hearing.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED KP Form No. 13 - Notice of Hearing",
            ACTIVE_USERNAME
            )
        self.close_windows("Form8")

    def generate_form_7(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return
        
        if check_document_exist(values[2], "Form7"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return

        self.form_7_window = CTkToplevel(self)
        self.form_7_window.title("KP FORM No. 17 - Repudiation")
        self.form_7_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_7_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_7_window.after(200, lambda: self.form_7_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 685
        x, y = self._center_screen(window_width, window_height)
        self.form_7_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_7_window.transient(self)
        self.form_7_window.grab_set()

        self.form_7_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.label_fraud = CTkLabel(
            self.form_7_window,
            font=self.blotter_entry_font,
            text='Fraud: '
        )
        self.entry_fraud = CTkTextbox(
            self.form_7_window,
            font=self.blotter_entry_font,
            width=300,
            height=100
        )
        self.label_violence = CTkLabel(
            self.form_7_window,
            font=self.blotter_entry_font,
            text='Violence: '
        )
        self.entry_violence = CTkTextbox(
            self.form_7_window,
            font=self.blotter_entry_font,
            width=300,
            height=100
        )
        self.label_intimidation = CTkLabel(
            self.form_7_window,
            font=self.blotter_entry_font,
            text='Intimidation: '
        )
        self.entry_intimidation = CTkTextbox(
            self.form_7_window,
            font=self.blotter_entry_font,
            width=300,
            height=100
        )
        self.label_in_charge_name = CTkLabel(
            self.form_7_window,
            font=self.blotter_entry_font,
            text="Facilitating Official: "
        )
        self.in_charge_list = get_form_5_in_charge()
        self.in_charge_var = StringVar(value=self.in_charge_list[0])
        self.entry_in_charge_name = CTkOptionMenu(
            self.form_7_window,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.in_charge_var,
            command=self.form_5_on_change
        )
        self.label_in_charge_role = CTkLabel(
            self.form_7_window,
            font=self.blotter_entry_font,
            text="Official Role: "
        )
        self.in_charge_role_list = [
            "Punong Barangay",
            "Pangkat Chairman",
            "Pangkat Member"
        ]
        self.in_charge_role_var = StringVar(value=self.in_charge_role_list[0])
        self.entry_in_charge_role = CTkOptionMenu(
            self.form_7_window,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_role_list,
            variable=self.in_charge_role_var,
        )

        self.btn_confirm = CTkButton(
            self.form_7_window,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_7(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.entry_fraud.get('1.0', 'end-1c'),
                self.entry_violence.get('1.0', 'end-1c'),
                self.entry_intimidation.get('1.0', 'end-1c'),
                self.in_charge_var.get(),
                self.in_charge_role_var.get()
                )
        )

        self.label_fraud.pack(anchor='w', pady=(30, 5), padx=(50, 0))
        self.entry_fraud.pack(anchor='center')
        self.label_violence.pack(anchor='w', pady=(10, 5), padx=(50, 0))
        self.entry_violence.pack(anchor='center')
        self.label_intimidation.pack(anchor='w', pady=(10, 5), padx=(50, 0))
        self.entry_intimidation.pack(anchor='center')
        self.label_in_charge_name.pack(anchor='w', pady=(10, 5), padx=(50, 0))
        self.entry_in_charge_name.pack(anchor='center')
        self.label_in_charge_role.pack(anchor='w', pady=(10, 5), padx=(50, 0))
        self.entry_in_charge_role.pack(anchor='center')
        self.btn_confirm.pack(anchor='center', pady=(20, 0))
        
        self.form_7_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form7"))

    def finalize_form_7(self, values, cmplnts, rspndnts, comp_add, res_add, fraud, violence, intimidation, charge_name, charge_role):
        if not fraud and not violence and not intimidation:
            messagebox.showwarning("Empty Data", "Please fill in one of the following.")
            return
        
        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nFraud: {fraud}\nViolence: {violence}\nIntimidation: {intimidation}\nOfficer In-Charge: {charge_name}\nIn-Charge Role: {charge_role}"):
            return
        
        process = multiprocessing.Process(
            target=do_form_7,
            args=(
                values,
                cmplnts,
                rspndnts,
                comp_add,
                res_add,
                fraud,
                violence,
                intimidation,
                charge_name,
                charge_role
            )
        )
        process.start()
        messagebox.showinfo(
            "Success", "Generating KP Form No. 17 - Repudiation.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED KP Form No. 17 - Repudiation",
            ACTIVE_USERNAME
            )
        self.close_windows("Form7")
        
    def generate_form_6(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return
        
        if check_document_exist(values[2], "Form6"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return

        self.form_6_window = CTkToplevel(self)
        self.form_6_window.title("KP FORM No. 16 - Amicable Settlement")
        self.form_6_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_6_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_6_window.after(200, lambda: self.form_6_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 255
        x, y = self._center_screen(window_width, window_height)
        self.form_6_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_6_window.transient(self)
        self.form_6_window.grab_set()

        self.form_6_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.label_settlement = CTkLabel(
            self.form_6_window,
            font=self.blotter_entry_font,
            text='Settle Dispute through: '
        )
        self.entry_settlement = CTkTextbox(
            self.form_6_window,
            font=self.blotter_entry_font,
            width=300,
            height=100
        )
        self.btn_confirm = CTkButton(
            self.form_6_window,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_6(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.entry_settlement.get('1.0', 'end-1c')
                )
        )

        self.label_settlement.pack(anchor='w', pady=(30, 5), padx=(50, 0))
        self.entry_settlement.pack(anchor='center')
        self.btn_confirm.pack(anchor='center', pady=(20, 5))
        
        self.form_6_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form6"))

    def finalize_form_6(self, values, cmplnts, rspndnts, comp_add, res_add, statement):
        if not statement:
            messagebox.showwarning("Empty Data", "Please fill in statement.")
            return
        
        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nSettlement: {statement}"):
            return
        
        process = multiprocessing.Process(
            target=do_form_6,
            args=(
                values,
                cmplnts,
                rspndnts,
                comp_add,
                res_add,
                statement
            )
        )
        process.start()
        messagebox.showinfo(
            "Success", "Generating KP Form No. 16 - Amicable Settlement.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED KP Form No. 16 - Amicable Settlement",
            ACTIVE_USERNAME
            )
        self.close_windows("Form6")
        
    def generate_form_5(self, values, rspndnts, resp_add, cmplnts):
        if not check_officials():
            return
        
        if check_document_exist(values[2], "Form5"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return
        
        self.form_5_window = CTkToplevel(self)
        self.form_5_window.title("KP FORM No. 12 - Notice of Hearing (Re:Failure to Appear)")
        self.form_5_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_5_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_5_window.after(200, lambda: self.form_5_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 405
        x, y = self._center_screen(window_width, window_height)
        self.form_5_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_5_window.transient(self)
        self.form_5_window.grab_set()
        
        self.form_5_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.frame_form_5_container = CTkFrame(
            self.form_5_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_hear_date = CTkLabel(
            self.frame_form_5_container,
            font=self.blotter_entry_font,
            text='Hearing Date: '
        )
        self.frame_hear_date = CTkFrame(
            self.frame_form_5_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        style = ttk.Style(self)
        style.configure('CustomDateEntry.TEntry',
                        foreground='gray14',
                        background=CONTENT_BG,
                        font=TK_CONTENT_FONT,
                        padding=(5, 2, 0, 3), )
        self.entry_hear_date = DateEntry(
            self.frame_hear_date,
            style='CustomDateEntry.TEntry',
            width=27,
            font=TK_CONTENT_FONT,
            pady=10,
            date_pattern='dd-mm-yyyy'
        )
        self.label_hear_time = CTkLabel(
            self.frame_form_5_container,
            font=self.blotter_entry_font,
            text='Hearing Time: '
        )
        self.frame_hear_time = CTkFrame(
            self.frame_form_5_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.entry_hear_time = CTkEntry(
            self.frame_hear_time,
            font=self.blotter_entry_font,
            width=160,
            placeholder_text="HH:MM"
        )
        period_value = ["AM", "PM"]
        self.time_period_var = StringVar(value=period_value[0])
        self.entry_hear_time_period = CTkOptionMenu(
            self.frame_hear_time,
            font=self.blotter_entry_font,
            width=80,
            fg_color='#FAFAFA',
            text_color="#000",
            values=period_value,
            variable=self.time_period_var
        )
        self.label_prev_hear_date = CTkLabel(
            self.frame_form_5_container,
            font=self.blotter_entry_font,
            text='Previous Scheduled Hearing Date: '
        )
        style = ttk.Style(self)
        style.configure('CustomDateEntry.TEntry',
                        foreground='gray14',
                        background=CONTENT_BG,
                        font=TK_CONTENT_FONT,
                        padding=(5, 2, 0, 3), )
        self.entry_prev_hear_date = DateEntry(
            self.frame_form_5_container,
            style='CustomDateEntry.TEntry',
            width=27,
            font=TK_CONTENT_FONT,
            pady=10,
            date_pattern='dd-mm-yyyy'
        )
        self.label_in_charge_name = CTkLabel(
            self.frame_form_5_container,
            font=self.blotter_entry_font,
            text="Facilitating Official\n(Barangay/Pangkat Chairman): ",
            anchor='w'
        )
        self.in_charge_list = get_form_5_in_charge()
        self.in_charge_var = StringVar(value=self.in_charge_list[0])
        self.entry_in_charge_name = CTkOptionMenu(
            self.frame_form_5_container,
            font=self.blotter_entry_font,
            width=240,
            fg_color="#FAFAFA",
            text_color="#000",
            values=self.in_charge_list,
            variable=self.in_charge_var,
            command=self.form_5_on_change
        )
        self.entry_in_charge_role = "Punong Barangay"
        self.btn_confirm = CTkButton(
            self.frame_form_5_container,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_5(
                values,
                rspndnts,
                resp_add,
                self.entry_hear_date.get_date(),
                self.entry_hear_time.get(),
                self.entry_hear_time_period.get(),
                self.entry_prev_hear_date.get_date(),
                self.in_charge_var.get(),
                self.entry_in_charge_role,
                cmplnts
            )
        )
        
        self.frame_form_5_container.pack(anchor='center')
        self.label_hear_date.pack(anchor='w', pady=(30, 5))
        self.frame_hear_date.pack(anchor='center')
        self.entry_hear_date.pack(anchor='nw')
        self.label_hear_time.pack(anchor='w', pady=(10, 5))
        self.frame_hear_time.pack(anchor='center')
        self.entry_hear_time.pack(side='left')
        self.entry_hear_time_period.pack(side='left')
        self.label_prev_hear_date.pack(anchor='w', pady=(10, 5))
        self.entry_prev_hear_date.pack(anchor='center')
        self.label_in_charge_name.pack(anchor='w', pady=(10, 5))
        self.entry_in_charge_name.pack(anchor='center')
        self.btn_confirm.pack(anchor='center', pady=(20, 5))

        self.form_5_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form5"))

    def form_5_on_change(self, e):
        self.entry_in_charge_role = ""
        if self.in_charge_var.get() == self.in_charge_list[0]:
            self.entry_in_charge_role = "Punong Barangay"
        else:
            self.entry_in_charge_role = "Pangkat Chairman"

    def finalize_form_5(self, values, rspndnts, resp_add, date, time, period, prev_date, per_charge, per_role, cmplnts):
        if not date or not time or not period or not prev_date or not per_charge or not per_role:
            messagebox.showwarning("Empty Data", "Please fill in all the fields.")
            return
        
        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nDate: {date}\nTime: {time} {period}\nPrevious Date: {prev_date}\nOfficer In-Charge: {per_charge}\nIn-Charge Role: {per_role}"):
            return
        
        process = multiprocessing.Process(
            target=do_form_5,
            args=(
                values, 
                rspndnts, 
                resp_add, 
                date, 
                time, 
                period, 
                prev_date, 
                per_charge, 
                per_role,
                cmplnts
            )
        )
        process.start()

        messagebox.showinfo(
            "Success", "Generating KP Form No. 12 - Notice of Hearing (Re: Failure to Appear).\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED KP Form No. 12 - Notice of Hearing (Re: Failure to Appear)",
            ACTIVE_USERNAME
            )
        self.close_windows("Form5")

    def generate_form_4(self, values, cmplnts, rspndnts, comp_add):
        if not check_officials():
            return
        
        if check_document_exist(values[2], "Form4"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return
        
        self.form_4_window = CTkToplevel(self)
        self.form_4_window.title("KP FORM No. 12 - Notice of Hearing (Mediation Process).")
        self.form_4_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_4_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_4_window.after(200, lambda: self.form_4_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 255
        x, y = self._center_screen(window_width, window_height)
        self.form_4_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_4_window.transient(self)
        self.form_4_window.grab_set()
        
        self.form_4_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.frame_form_4_container = CTkFrame(
            self.form_4_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_summon_date = CTkLabel(
            self.frame_form_4_container,
            font=self.blotter_entry_font,
            text='Hearing Date: '
        )
        self.frame_summon_date = CTkFrame(
            self.frame_form_4_container,
            fg_color=self.BLOTTER_CONTENT_BG,
        )
        style = ttk.Style(self)
        style.configure('CustomDateEntry.TEntry',
                        foreground='gray14',
                        background=CONTENT_BG,
                        font=TK_CONTENT_FONT,
                        padding=(5, 2, 0, 3), )
        self.entry_summon_date = DateEntry(
            self.frame_summon_date,
            style='CustomDateEntry.TEntry',
            width=27,
            font=TK_CONTENT_FONT,
            pady=10,
            date_pattern='dd-mm-yyyy'
        )
        self.label_summon_time = CTkLabel(
            self.frame_form_4_container,
            font=self.blotter_entry_font,
            text='Hearing Time: '
        )
        self.frame_summon_time = CTkFrame(
            self.frame_form_4_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.entry_summon_time = CTkEntry(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=160,
            placeholder_text="HH:MM"
        )
        period_value = ["AM", "PM"]
        self.time_period_var = StringVar(value=period_value[0])
        self.entry_summon_time_period = CTkOptionMenu(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=80,
            fg_color='#FAFAFA',
            text_color="#000",
            values=period_value,
            variable=self.time_period_var
        )
        self.btn_confirm = CTkButton(
            self.frame_form_4_container,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_4(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add,
                self.entry_summon_date.get_date(),
                self.entry_summon_time.get(),
                self.time_period_var.get()
                )
        )
        
        self.frame_form_4_container.pack(anchor='center')
        self.label_summon_date.pack(anchor='w', pady=(30, 5))
        self.frame_summon_date.pack(anchor='center')
        self.entry_summon_date.pack(anchor='nw')
        self.label_summon_time.pack(anchor='w', pady=(10, 5))
        self.frame_summon_time.pack(anchor='center')
        self.entry_summon_time.pack(side='left')
        self.entry_summon_time_period.pack(side='left')
        self.btn_confirm.pack(anchor='center', pady=(20, 0))

        self.form_4_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form4"))

    def finalize_form_4(self, values, cmplnts, rspndnts, comp_add, date, time, period):
        if not date or not time or not period:
            messagebox.showwarning("Empty Data", "Please fill in both time and date sections.")
            return
        
        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nDate: {date}\nTime: {time} {period}"):
            return

        process = multiprocessing.Process(
            target=do_form_4,
            args=(
                values,
                cmplnts,
                rspndnts,
                comp_add,
                date,
                time,
                period
            )
        )
        process.start()

        messagebox.showinfo(
            "Success", "Generating KP Form No. 12 - Notice of Hearing.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED KP Form No. 12 - Notice of Hearing",
            ACTIVE_USERNAME
            )
        self.close_windows("Form4")

    def generate_form_2(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return
        

        if check_document_exist(values[2], "Form2"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return
        
        self.form_2_window = CTkToplevel(self)
        self.form_2_window.title("KP FORM No. 9 - Summons and Officer's Return")
        self.form_2_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.form_2_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.form_2_window.after(200, lambda: self.form_2_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 325
        x, y = self._center_screen(window_width, window_height)
        self.form_2_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.form_2_window.transient(self)
        self.form_2_window.grab_set()

        self.form_2_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.frame_form_2_container = CTkFrame(
            self.form_2_window,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.label_summon_date = CTkLabel(
            self.frame_form_2_container,
            font=self.blotter_entry_font,
            text='Summon Date: '
        )
        self.frame_summon_date = CTkFrame(
            self.frame_form_2_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        style = ttk.Style(self)
        style.configure('CustomDateEntry.TEntry',
                        foreground='gray14',
                        background=CONTENT_BG,
                        font=TK_CONTENT_FONT,
                        padding=(5, 2, 0, 3), )
        self.entry_summon_date = DateEntry(
            self.frame_summon_date,
            style='CustomDateEntry.TEntry',
            width=27,
            font=TK_CONTENT_FONT,
            pady=10,
            date_pattern='dd-mm-yyyy'
        )
        self.label_summon_time = CTkLabel(
            self.frame_form_2_container,
            font=self.blotter_entry_font,
            text='Summon Time: '
        )
        self.frame_summon_time = CTkFrame(
            self.frame_form_2_container,
            fg_color=self.BLOTTER_CONTENT_BG
        )
        self.entry_summon_time = CTkEntry(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=160,
            placeholder_text="HH:MM"
        )
        period_value = ["AM", "PM"]
        self.time_period_var = StringVar(value=period_value[0])
        self.entry_summon_time_period = CTkOptionMenu(
            self.frame_summon_time,
            font=self.blotter_entry_font,
            width=80,
            fg_color='#FAFAFA',
            text_color="#000",
            values=period_value,
            variable=self.time_period_var
        )
        self.label_officer_name = CTkLabel(
            self.frame_form_2_container,
            font=self.blotter_entry_font,
            text="Officer's Name: "
        )
        self.entry_officer_name = CTkEntry(
            self.frame_form_2_container,
            font=self.blotter_entry_font,
            width=240,
        )
        self.btn_confirm = CTkButton(
            self.frame_form_2_container,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_2(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.entry_summon_date.get_date(),
                self.entry_summon_time.get(),
                self.time_period_var.get(),
                self.entry_officer_name.get()
                )
        )
        
        self.frame_form_2_container.pack(anchor='center')
        self.label_summon_date.pack(anchor='w', pady=(30, 5))
        self.frame_summon_date.pack(anchor='center')
        self.entry_summon_date.pack(anchor='nw')
        self.label_summon_time.pack(anchor='w', pady=(10, 5))
        self.frame_summon_time.pack(anchor='center')
        self.entry_summon_time.pack(side='left')
        self.entry_summon_time_period.pack(side='left')
        self.label_officer_name.pack(anchor='w', pady=(10, 5))
        self.entry_officer_name.pack(anchor='center')
        self.btn_confirm.pack(anchor='center', pady=(20, 5))

        self.form_2_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form2"))

    def finalize_form_2(self, values, cmplnts, rspndnts, comp_add, res_add, date, time, period, officer):
        if not date or not time or not period:
            messagebox.showwarning("Empty Data", "Please fill in both time, date, and officer's name sections.")
            return
        
        if not officer:
            if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nDate: {date}\nTime: {time} {period}"):
                return
        else:
            if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nDate: {date}\nTime: {time} {period}\nOfficer: {officer}"):
                return
        
        process = multiprocessing.Process(
            target=do_form_2,
            args=(
                values,
                cmplnts,
                rspndnts,
                comp_add,
                res_add,
                date,
                time,
                period
            )
        )
        process.start()
        process = multiprocessing.Process(
            target=do_form_3,
            args=(
                values,
                cmplnts,
                rspndnts,
                officer
            )
        )
        process.start()

        messagebox.showinfo(
            "Success", "Generating KP Form No. 9 - Summons.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED KP Form No. 9 - Summons",
            ACTIVE_USERNAME
            )
        self.close_windows("Form2")

    def generate_form_1(self, values, cmplnts, rspndnts, comp_add, res_add):
        if not check_officials():
            return

        if check_document_exist(values[2], "Form1"):
            # messagebox.showwarning(
            #     "Alert", "This document already exists in the directory."
            # )
            # return
            if not messagebox.askokcancel("Confirmation", "This document already exists in the directory, would you like to create a new one?"):
                return
        else:
            if not messagebox.askokcancel("Confirmation", "Do you want to generate this document?"):
                return

        self.complaints_window = CTkToplevel(self)
        self.complaints_window.title("KP Form No. 7 - Complaints")
        self.complaints_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.complaints_window.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.complaints_window.after(200, lambda: self.complaints_window.iconbitmap(self.iconPath))
        window_width = 400
        window_height = 405
        x, y = self._center_screen(window_width, window_height)
        self.complaints_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.complaints_window.transient(self)
        self.complaints_window.grab_set()

        self.complaints_window.configure(
            fg_color=self.BLOTTER_CONTENT_BG
        )

        self.label_complaint = CTkLabel(
            self.complaints_window,
            font=self.blotter_entry_font,
            text='Complaint: '
        )
        self.entry_complaint = CTkTextbox(
            self.complaints_window,
            font=self.blotter_entry_font,
            width=300,
            height=100
        )
        self.label_relief = CTkLabel(
            self.complaints_window,
            font=self.blotter_entry_font,
            text='Relief: '
        )
        self.entry_relief = CTkTextbox(
            self.complaints_window,
            font=self.blotter_entry_font,
            width=300,
            height=100
        )
        self.btn_confirm = CTkButton(
            self.complaints_window,
            text='Confirm',
            font=self.blotter_entry_font,
            command=lambda: self.finalize_form_1(
                values, 
                cmplnts, 
                rspndnts, 
                comp_add, 
                res_add,
                self.entry_complaint.get('1.0', 'end-1c'),
                self.entry_relief.get('1.0', 'end-1c')
                )
        )

        self.label_complaint.pack(anchor='w', pady=(30, 5), padx=50)
        self.entry_complaint.pack(anchor='center')
        self.label_relief.pack(anchor='w', pady=(10, 5), padx=50)
        self.entry_relief.pack(anchor='center')
        self.btn_confirm.pack(anchor='center', pady=(20))
        
        self.complaints_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_info_tab("Form1"))

    def finalize_form_1(self, values, cmplnts, rspndnts, comp_add, res_add, reason, relief):
        if not reason or not relief:
            messagebox.showwarning("Empty Data", "Please fill in both complaint and relief sections.")
            return
        
        if not messagebox.askyesno("Confirmation", f"Are you sure of the selected,\nReason: {reason}\nRelief: {relief}"):
            return
        
        process = multiprocessing.Process(
            target=do_form_1,
            args=(
                values,
                cmplnts,
                rspndnts,
                comp_add,
                res_add,
                reason,
                relief
            )
        )
        process.start()
        messagebox.showinfo(
            "Success", "Generating KP Form No. 7 - Complaints.\nPlease wait..."
        )
        log_blotter(
            get_formatted_datetime(),
            values[2],
            "GENERATED KP Form No. 7 - Complaints",
            ACTIVE_USERNAME
            )
        self.close_windows("Form1")

    # For closing the Add Complainants Window
    def on_closing_modify_individual_window(self):
        self.modify_individual_window.grab_release()
        self.modify_individual_window.destroy()
        self.add_record_window.grab_set()

    # For closing the Add Respondents Window
    def on_closing_modify_respondents(self):
        self.modify_modify_respondents_window.grab_release()
        self.modify_modify_respondents_window.destroy()
        self.add_record_window.grab_set()

    # For closing the Select Respondents Window
    def on_closing_select_respondents(self):
        self.select_respondent_window.grab_release()
        self.select_respondent_window.destroy()
        self.modify_modify_respondents_window.grab_set()

    def on_closing_info_tab(self, btn):
        if btn == "Form1":
            self.complaints_window.grab_release()
            self.complaints_window.destroy()
        if btn == "Form2":
            self.form_2_window.grab_release()
            self.form_2_window.destroy()
        if btn == "Form4":
            self.form_4_window.grab_release()
            self.form_4_window.destroy()
        if btn == "Form5":
            self.form_5_window.grab_release()
            self.form_5_window.destroy()
        if btn == "Form6":
            self.form_6_window.grab_release()
            self.form_6_window.destroy()
        if btn == "Form7":
            self.form_7_window.grab_release()
            self.form_7_window.destroy()
        if btn == "Form8":
            self.form_8_window.grab_release()
            self.form_8_window.destroy()
        if btn == "Form9":
            self.form_9_window.grab_release()
            self.form_9_window.destroy()
        if btn == "Form10":
            self.form_10_window.grab_release()
            self.form_10_window.destroy()
        if btn == "Form11":
            self.form_11_window.grab_release()
            self.form_11_window.destroy()
        if btn == "Form12":
            self.form_12_window.grab_release()
            self.form_12_window.destroy()
        if btn == "Form13":
            self.form_13_window.grab_release()
            self.form_13_window.destroy()
        if btn == "Form14":
            self.form_14_window.grab_release()
            self.form_14_window.destroy()
        self.select_documents_window.grab_set()

    def close_windows(self, btn):
        self.select_documents_window.grab_release()
        self.select_documents_window.destroy()
        
        if btn == "Form1":
            self.complaints_window.grab_release()
            self.complaints_window.destroy()

        if btn == "Form2":
            self.form_2_window.grab_release()
            self.form_2_window.destroy()

        if btn == "Form4":
            self.form_4_window.grab_release()
            self.form_4_window.destroy()

        if btn == "Form5":
            self.form_5_window.grab_release()
            self.form_5_window.destroy()

        if btn == "Form6":
            self.form_6_window.grab_release()
            self.form_6_window.destroy()

        if btn == "Form7":
            self.form_7_window.grab_release()
            self.form_7_window.destroy()
            
        if btn == "Form8":
            self.form_8_window.grab_release()
            self.form_8_window.destroy()

        if btn == "Form9":
            self.form_9_window.grab_release()
            self.form_9_window.destroy()

        if btn == "Form10":
            self.form_10_window.grab_release()
            self.form_10_window.destroy()

        if btn == "Form11":
            self.form_11_window.grab_release()
            self.form_11_window.destroy()

        if btn == "Form12":
            self.form_12_window.grab_release()
            self.form_12_window.destroy()

        if btn == "Form13":
            self.form_13_window.grab_release()
            self.form_13_window.destroy()

        if btn == "Form14":
            self.form_14_window.grab_release()
            self.form_14_window.destroy()

        self.view_record_window.grab_set()
        self.view_record_window.focus()


class OfficialsPage(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            fg_color=CONTENT_BG
        )
        self.constants()
        self.create_widgets()
        self.create_layout()
        self.set_officials()

    def constants(self):
        self.POBLACION_NAME = ('Bahnschrift SemiBold', 50, 'normal')
        self.OFFICIAL_SECTION = ('Bahnschrift SemiBold', 35, 'normal')
        self.OFFICIAL_NAME = ('Bahnschrift SemiBold', 22, 'normal')
        self.OFFICIAL_POSITION = ('Bahnschrift SemiBold', 16, 'normal')

        # Get poblacion logo
        self.IMAGE_PATH = resources_path('assets/images/Poblacion8Seal.png')
        self.IMAGE_WIDTH = 200
        self.IMAGE_HEIGHT = 200
        self.POBLACION_LOGO = CTkImage(
            light_image=Image.open(self.IMAGE_PATH), size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        )
        self.empty_name = 'N/A'
        self.BTN_WIDTH = 150
        self.BTN_HEIGHT = 50
        self.BTN_FONT = ('Bahnschrift SemiBold', 16, 'normal')

        # Modify Officials Window
        self.HEADER_FONT = ('Bahnschrift SemiBold', 24, 'normal')
        self.CONTENT_FONT = ('Bahnschrift SemiBold', 16, 'normal')
        self.ENTRY_WIDTH = 300
        self.LABEL_LEFT = 105
        self.BG_COLOR = '#CED4DA'
        self.TEXT_COLOR = "#fafafa"
        self.BTN_GREEN = "#656D4A"
        self.BTN_HOVER_GREEN = "#A4AC86"
        self.BTN_BROWN = "#936639"
        self.BTN_HOVER_BROWN = "#A68A64"
        self.BTN_BLUE = "#023e8a"
        self.BTN_HOVER_BLUE = "#0077b6"

        self.TREE_HEADING_COLOR = "#344e41"
        self.TREE_SELECTED_COLOR = "#344e41"
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview", font=("Bahnschrift SemiBold", 12, "normal"), rowheight=30)
        self.tree_style.configure("Treeview.Heading", font=("Bahnschrift SemiBold", 16, "bold"),padding=(0, 5), foreground=self.TREE_HEADING_COLOR)
        self.tree_style.map("Treeview",
                            background=[("selected", self.TREE_SELECTED_COLOR)],
                            foreground=[("selected", self.TEXT_COLOR)]
                            )
        
        self.FONT_AUTHENTICATION =  ('Bahnschrift SemiBold', 20, 'normal')
        self.BTN_LOGOUT = '#9d0208'
        self.BTN_LOGOUT_HOVER = '#e5383b'

        self.OFFICIALS_CONTENT_BG = "#dad7cd"

    def create_widgets(self):
        self.officials_container = CTkScrollableFrame(
            self, 1610, 850,
        )
        self.buttons_container = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG
        )
        self.btn_modify_officials = CTkButton(
            self.buttons_container,
            text='Modify officials',
            anchor='center',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            font=self.BTN_FONT,
            command=self.user_authentication,
        )
        self.btn_print_officials = CTkButton(
            self.buttons_container,
            text='Print officials',
            anchor='center',
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            font=self.BTN_FONT,
            fg_color="#495057",
            hover_color="#6c757d",
            command=self.print_officials,
        )
        self.poblacion_logo = CTkLabel(
            self.officials_container,
            image=self.POBLACION_LOGO,
            text='',
            anchor='center',
        )
        self.barangay_name = CTkLabel(
            self.officials_container,
            font=self.POBLACION_NAME,
            anchor='center',
            text='BARANGAY POBLACION 8',
        )
        self.barangay_section = CTkLabel(
            self.officials_container,
            font=self.OFFICIAL_SECTION,
            anchor='center',
            text='SANGGUNIANG BARANGAY',
        )

        # BARANGAY OFFICIALS
        self.barangay_captain = CTkLabel(
            self.officials_container,
            font=self.OFFICIAL_NAME,
            anchor='center',
            text=self.empty_name,
        )
        self.barangay_captain_position = CTkLabel(
            self.officials_container,
            font=self.OFFICIAL_POSITION,
            anchor='center',
            text='BARANGAY CAPTAIN (PUNONG BARANGAY)',
        )
        self.first_kagawad_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.first_kagawad_container = CTkFrame(
            self.first_kagawad_row,
            fg_color=CONTENT_BG
        )
        self.second_kagawad_container = CTkFrame(
            self.first_kagawad_row,
            fg_color=CONTENT_BG
        )
        self.first_kagawad = CTkLabel(
            self.first_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.first_kagawad_position = CTkLabel(
            self.first_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='BARANGAY COUNCILOR (KAGAWAD)',
        )
        self.second_kagawad = CTkLabel(
            self.second_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.second_kagawad_position = CTkLabel(
            self.second_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='BARANGAY COUNCILOR (KAGAWAD)',
        )
        self.second_kagawad_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.third_kagawad_container = CTkFrame(
            self.second_kagawad_row,
            fg_color=CONTENT_BG
        )
        self.fourth_kagawad_container = CTkFrame(
            self.second_kagawad_row,
            fg_color=CONTENT_BG
        )
        self.third_kagawad = CTkLabel(
            self.third_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.third_kagawad_position = CTkLabel(
            self.third_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='BARANGAY COUNCILOR (KAGAWAD)',
        )
        self.fourth_kagawad = CTkLabel(
            self.fourth_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.fourth_kagawad_position = CTkLabel(
            self.fourth_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='BARANGAY COUNCILOR (KAGAWAD)',
        )
        self.third_kagawad_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.fifth_kagawad_container = CTkFrame(
            self.third_kagawad_row,
            fg_color=CONTENT_BG
        )
        self.sixth_kagawad_container = CTkFrame(
            self.third_kagawad_row,
            fg_color=CONTENT_BG
        )
        self.fifth_kagawad = CTkLabel(
            self.fifth_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.fifth_kagawad_position = CTkLabel(
            self.fifth_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='BARANGAY COUNCILOR (KAGAWAD)',
        )
        self.sixth_kagawad = CTkLabel(
            self.sixth_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.sixth_kagawad_position = CTkLabel(
            self.sixth_kagawad_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='BARANGAY COUNCILOR (KAGAWAD)',
        )
        self.fourth_kagawad_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.seventh_kagawad = CTkLabel(
            self.fourth_kagawad_row,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.seventh_kagawad_position = CTkLabel(
            self.fourth_kagawad_row,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='BARANGAY COUNCILOR (KAGAWAD)',
        )
        self.fifth_kagawad_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.secretary_container = CTkFrame(
            self.fifth_kagawad_row,
            fg_color=CONTENT_BG
        )
        self.treasurer_container = CTkFrame(
            self.fifth_kagawad_row,
            fg_color=CONTENT_BG
        )
        self.secretary_name = CTkLabel(
            self.secretary_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.secretary_position = CTkLabel(
            self.secretary_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='BARANGAY SECRETARY',
        )
        self.treasurer_name = CTkLabel(
            self.treasurer_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.treasurer_position = CTkLabel(
            self.treasurer_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='BARANGAY TREASURER',
        )
        self.sixth_kagawad_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.sk_chairman_name = CTkLabel(
            self.sixth_kagawad_row,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.sk_chairman_position = CTkLabel(
            self.sixth_kagawad_row,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='SANGGUNIANG KABATAAN CHAIRMAN',
        )

        # PANGKAT TAGAPAGKASUNDO
        self.pangkat_section = CTkLabel(
            self.officials_container,
            font=self.OFFICIAL_SECTION,
            anchor='center',
            text='LUPON TAGAPAGPAMAYAPA',
        )
        self.first_pangkat_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.first_pangkat_container = CTkFrame(
            self.first_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.second_pangkat_container = CTkFrame(
            self.first_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.first_pangkat_name = CTkLabel(
            self.first_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.first_pangkat_position = CTkLabel(
            self.first_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )
        self.second_pangkat_name = CTkLabel(
            self.second_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.second_pangkat_position = CTkLabel(
            self.second_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )
        self.second_pangkat_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.third_pangkat_container = CTkFrame(
            self.second_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.fourth_pangkat_container = CTkFrame(
            self.second_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.third_pangkat_name = CTkLabel(
            self.third_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.third_pangkat_position = CTkLabel(
            self.third_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )
        self.fourth_pangkat_name = CTkLabel(
            self.fourth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.fourth_pangkat_position = CTkLabel(
            self.fourth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )
        self.third_pangkat_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.fifth_pangkat_container = CTkFrame(
            self.third_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.sixth_pangkat_container = CTkFrame(
            self.third_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.fifth_pangkat_name = CTkLabel(
            self.fifth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.fifth_pangkat_position = CTkLabel(
            self.fifth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )
        self.sixth_pangkat_name = CTkLabel(
            self.sixth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.sixth_pangkat_position = CTkLabel(
            self.sixth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )
        self.fourth_pangkat_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.seventh_pangkat_container = CTkFrame(
            self.fourth_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.eight_pangkat_container = CTkFrame(
            self.fourth_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.seventh_pangkat_name = CTkLabel(
            self.seventh_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.seventh_pangkat_position = CTkLabel(
            self.seventh_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )
        self.eight_pangkat_name = CTkLabel(
            self.eight_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.eight_pangkat_position = CTkLabel(
            self.eight_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )
        self.fifth_pangkat_row = CTkFrame(
            self.officials_container,
            fg_color=CONTENT_BG,
        )
        self.ninth_pangkat_container = CTkFrame(
            self.fifth_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.tenth_pangkat_container = CTkFrame(
            self.fifth_pangkat_row,
            fg_color=CONTENT_BG
        )
        self.ninth_pangkat_name = CTkLabel(
            self.ninth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.ninth_pangkat_position = CTkLabel(
            self.ninth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )
        self.tenth_pangkat_name = CTkLabel(
            self.tenth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_NAME,
            text=self.empty_name
        )
        self.tenth_pangkat_position = CTkLabel(
            self.tenth_pangkat_container,
            anchor='center',
            font=self.OFFICIAL_POSITION,
            text='LUPON MEMBER',
        )

    def create_layout(self):
        self.officials_container.pack(anchor='center', fill='x')
        self.buttons_container.pack(anchor='w', pady=(20, 10), padx=20)
        self.btn_modify_officials.pack(side='left', padx=(0, 10))
        self.btn_print_officials.pack(side='left')
        self.poblacion_logo.pack(anchor='center', fill='x', pady=(10, 0))
        self.barangay_name.pack(anchor='center', fill='x')

        self.barangay_section.pack(anchor='center', fill='x', pady=(50, 30))
        self.barangay_captain.pack(anchor='center', fill='x')
        self.barangay_captain_position.pack(anchor='center', fill='x', pady=(0, 20))

        self.first_kagawad_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.first_kagawad_container.pack(side='left', expand='true', fill='x')
        self.second_kagawad_container.pack(side='left', expand='true', fill='x')
        self.first_kagawad.pack(anchor='center')
        self.second_kagawad.pack(anchor='center')
        self.first_kagawad_position.pack(anchor='center')
        self.second_kagawad_position.pack(anchor='center')

        self.second_kagawad_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.third_kagawad_container.pack(side='left', expand='true', fill='x')
        self.fourth_kagawad_container.pack(side='left', expand='true', fill='x')
        self.third_kagawad.pack(anchor='center', expand='true', fill='x')
        self.fourth_kagawad.pack(anchor='center', expand='true', fill='x')
        self.third_kagawad_position.pack(anchor='center', expand='true', fill='x')
        self.fourth_kagawad_position.pack(anchor='center', expand='true', fill='x')

        self.third_kagawad_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.fifth_kagawad_container.pack(side='left', expand='true', fill='x')
        self.sixth_kagawad_container.pack(side='left', expand='true', fill='x')
        self.fifth_kagawad.pack(anchor='center', expand='true', fill='x')
        self.fifth_kagawad_position.pack(anchor='center', expand='true', fill='x')
        self.sixth_kagawad.pack(anchor='center', expand='true', fill='x')
        self.sixth_kagawad_position.pack(anchor='center', expand='true', fill='x')

        self.fourth_kagawad_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.seventh_kagawad.pack(anchor='center', expand='true', fill='x')
        self.seventh_kagawad_position.pack(anchor='center', expand='true', fill='x')

        self.fifth_kagawad_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.secretary_container.pack(side='left', expand='true', fill='x')
        self.treasurer_container.pack(side='left', expand='true', fill='x')
        self.secretary_name.pack(anchor='center', expand='true', fill='x')
        self.secretary_position.pack(anchor='center', expand='true', fill='x')
        self.treasurer_name.pack(anchor='center', expand='true', fill='x')
        self.treasurer_position.pack(anchor='center', expand='true', fill='x')

        self.sixth_kagawad_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.sk_chairman_name.pack(anchor='center', expand='true', fill='x')
        self.sk_chairman_position.pack(anchor='center', expand='true', fill='x')

        self.pangkat_section.pack(anchor='center', fill='x', pady=(50, 30))

        self.first_pangkat_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.first_pangkat_container.pack(side='left', expand='true', fill='x')
        self.second_pangkat_container.pack(side='left', expand='true', fill='x')
        self.first_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.first_pangkat_position.pack(anchor='center', expand='true', fill='x')
        self.second_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.second_pangkat_position.pack(anchor='center', expand='true', fill='x')

        self.second_pangkat_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.third_pangkat_container.pack(side='left', expand='true', fill='x')
        self.fourth_pangkat_container.pack(side='left', expand='true', fill='x')
        self.third_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.third_pangkat_position.pack(anchor='center', expand='true', fill='x')
        self.fourth_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.fourth_pangkat_position.pack(anchor='center', expand='true', fill='x')

        self.third_pangkat_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.fifth_pangkat_container.pack(side='left', expand='true', fill='x')
        self.sixth_pangkat_container.pack(side='left', expand='true', fill='x')
        self.fifth_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.fifth_pangkat_position.pack(anchor='center', expand='true', fill='x')
        self.sixth_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.sixth_pangkat_position.pack(anchor='center', expand='true', fill='x')

        self.fourth_pangkat_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.seventh_pangkat_container.pack(side='left', expand='true', fill='x')
        self.eight_pangkat_container.pack(side='left', expand='true', fill='x')
        self.seventh_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.seventh_pangkat_position.pack(anchor='center', expand='true', fill='x')
        self.eight_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.eight_pangkat_position.pack(anchor='center', expand='true', fill='x')

        self.fifth_pangkat_row.pack(anchor='center', expand='true', fill='x', pady=(0, 20))
        self.ninth_pangkat_container.pack(side='left', expand='true', fill='x')
        self.tenth_pangkat_container.pack(side='left', expand='true', fill='x')
        self.ninth_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.ninth_pangkat_position.pack(anchor='center', expand='true', fill='x')
        self.tenth_pangkat_name.pack(anchor='center', expand='true', fill='x')
        self.tenth_pangkat_position.pack(anchor='center', expand='true', fill='x')

    def set_officials(self):
        barangayCaptain = check_barangayCaptain()
        barangayKagawad = check_barangayKagawad()
        barangaySecretary = check_secretary()
        barangayTreasurer = check_treasurer()
        barangaySK = check_sk_chairman()
        barangayPangkatMembers = check_pangkat()

        self.barangay_captain.configure(text=f'HON. {barangayCaptain.upper()}')
        self.first_kagawad.configure(text=f'HON. {barangayKagawad[0].upper()}')
        self.second_kagawad.configure(text=f'HON. {barangayKagawad[1].upper()}')
        self.third_kagawad.configure(text=f'HON. {barangayKagawad[2].upper()}')
        self.fourth_kagawad.configure(text=f'HON. {barangayKagawad[3].upper()}')
        self.fifth_kagawad.configure(text=f'HON. {barangayKagawad[4].upper()}')
        self.sixth_kagawad.configure(text=f'HON. {barangayKagawad[5].upper()}')
        self.seventh_kagawad.configure(text=f'HON. {barangayKagawad[6].upper()}')
        self.secretary_name.configure(text=barangaySecretary.upper())
        self.treasurer_name.configure(text=barangayTreasurer.upper())
        self.sk_chairman_name.configure(text=barangaySK.upper())

        self.first_pangkat_name.configure(text=barangayPangkatMembers[0].upper())
        self.second_pangkat_name.configure(text=barangayPangkatMembers[1].upper())
        self.third_pangkat_name.configure(text=barangayPangkatMembers[2].upper())
        self.fourth_pangkat_name.configure(text=barangayPangkatMembers[3].upper())
        self.fifth_pangkat_name.configure(text=barangayPangkatMembers[4].upper())
        self.sixth_pangkat_name.configure(text=barangayPangkatMembers[5].upper())
        self.seventh_pangkat_name.configure(text=barangayPangkatMembers[6].upper())
        self.eight_pangkat_name.configure(text=barangayPangkatMembers[7].upper())
        self.ninth_pangkat_name.configure(text=barangayPangkatMembers[8].upper())
        self.tenth_pangkat_name.configure(text=barangayPangkatMembers[9].upper())

    def print_officials(self):
        if not count_officials():
            messagebox.showwarning("Error", "Cannot print incomplete list of Barangay Officials and Lupon Members!")
            return

        if not messagebox.askokcancel("Confirmation", "Are you sure you want to generate the list of Barangay Officials and Lupon Members?"):
            return
        
        process = multiprocessing.Process(
            target=do_barangay_officials_list
        )
        process.start()

    def user_authentication(self):
        self.authentication_window = CTkToplevel(self)
        self._center_screen(400, 200)
        self.authentication_window.title("User Authentication")
        self.authentication_window.transient(self)
        self.authentication_window.grab_set()
        self.authentication_window.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.authentication_window.iconbitmap(default=self.authentication_window.iconPath)
        if platform.startswith("win"):
            self.after(200, lambda: self.authentication_window.iconbitmap(self.authentication_window.iconPath))

        # CREATE WIDGETS
        label_authentication = CTkLabel(
            self.authentication_window,
            text="Enter current users password:",
            font=self.FONT_AUTHENTICATION,
        )
        entry_password = CTkEntry(
            self.authentication_window,
            show="•",
            font=self.FONT_AUTHENTICATION,
            width=200
        )
        btn_confirm_password = CTkButton(
            self.authentication_window,
            text="Confirm",
            font=self.FONT_AUTHENTICATION,
            command=lambda: self.modify_officials(entry_password.get()),
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
        )
        btn_cancel = CTkButton(
            self.authentication_window,
            text="Cancel",
            font=self.FONT_AUTHENTICATION,
            command=self.close_user_authentication_window,
            fg_color=self.BTN_LOGOUT,
            hover_color=self.BTN_LOGOUT_HOVER
        )

        # CREATE LAYOUT
        label_authentication.pack(pady=(20, 0))
        entry_password.pack(anchor='center')
        btn_confirm_password.pack(anchor='center', pady=10)
        btn_cancel.pack(anchor='center')
        
    def close_user_authentication_window(self):
        self.authentication_window.grab_release()
        self.authentication_window.destroy()

    def _center_screen(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        self.authentication_window.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))

    def modify_officials(self, password):
        if not verify_user(ACTIVE_USERNAME, password):
            messagebox.showerror("Authentication Error", "Incorrect password!")
            return
        
        log_user_activity(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime(), f"ACCESSED MODIFY OFFICIALS")
        self.close_user_authentication_window()
        
        self.modify_window = CTkToplevel(self)
        self.modify_window.title('Modify Officials')
        self.modify_window.resizable(False, False)
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        if platform.startswith("win"):
            self.modify_window.after(200, lambda: self.modify_window.iconbitmap(self.iconPath))
        self.modify_window.transient(self)
        self.modify_window.grab_set()

        self.modify_window.configure(
            fg_color=self.OFFICIALS_CONTENT_BG
        )

        window_width = 800
        window_height = 500

        x_axis, y_axis = self._center_screen_(window_width, window_height)
        self.modify_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_axis, y_axis))

        # CREATE WIDGETS
        self.label_indiv_info = CTkLabel(
            self.modify_window,
            text='Barangay Official/Personnel/Lupon Individual Information',
            font=self.HEADER_FONT
        )
        self.container = CTkFrame(
            self.modify_window,
            fg_color=self.OFFICIALS_CONTENT_BG
        )
        # ENTRY CONTAINER
        self.frame_entryLabel = CTkFrame(
            self.container,
            fg_color=self.OFFICIALS_CONTENT_BG
        )
        # ID - HIDDEN
        self.entry_ID = CTkEntry(
            self.frame_entryLabel,
        )
        # FIRST NAME
        self.frame_firstName = CTkFrame(
            self.frame_entryLabel,
            fg_color=self.OFFICIALS_CONTENT_BG
        )
        self.label_firstName = CTkLabel(
            self.frame_firstName,
            text='First Name: ',
            font=self.CONTENT_FONT
        )
        self.entry_firstName = CTkEntry(
            self.frame_firstName,
            width=self.ENTRY_WIDTH,
            font=self.CONTENT_FONT
        )
        # MIDDLE NAME
        self.frame_middleName = CTkFrame(
            self.frame_entryLabel,
            fg_color=self.OFFICIALS_CONTENT_BG
        )
        self.label_middleName = CTkLabel(
            self.frame_middleName,
            text='Middle Name: ',
            font=self.CONTENT_FONT,
        )
        self.entry_middleName = CTkEntry(
            self.frame_middleName,
            width=self.ENTRY_WIDTH,
            font=self.CONTENT_FONT
        )
        # LAST NAME
        self.frame_lastName = CTkFrame(
            self.frame_entryLabel,
            fg_color=self.OFFICIALS_CONTENT_BG
        )
        self.label_lastName = CTkLabel(
            self.frame_lastName,
            text='Last Name: ',
            font=self.CONTENT_FONT,
        )
        self.entry_lastName = CTkEntry(
            self.frame_lastName,
            width=self.ENTRY_WIDTH,
            font=self.CONTENT_FONT
        )
        # SUFFIX
        self.frame_suffix = CTkFrame(
            self.frame_entryLabel,
            fg_color=self.OFFICIALS_CONTENT_BG
        )
        self.label_suffix = CTkLabel(
            self.frame_suffix,
            text='Suffix: ',
            font=self.CONTENT_FONT,
        )
        self.entry_suffix = CTkEntry(
            self.frame_suffix,
            width=self.ENTRY_WIDTH,
            font=self.CONTENT_FONT
        )
        # POSITION
        self.frame_position = CTkFrame(
            self.frame_entryLabel,
            fg_color=self.OFFICIALS_CONTENT_BG
        )
        self.label_position = CTkLabel(
            self.frame_position,
            text='Position: ',
            font=self.CONTENT_FONT,
        )
        positions_list = ['Punong Barangay',
                          'Kagawad',
                          'Treasurer',
                          'Secretary',
                          'SK Chairman',
                          'Lupon'
                          ]
        self.entry_position = CTkComboBox(
            self.frame_position,
            width=self.ENTRY_WIDTH,
            font=self.CONTENT_FONT,
            values=positions_list,
            state="readonly"
        )

        # BUTTONS CONTAINER
        self.frame_buttons = CTkFrame(
            self.container,
            fg_color=self.OFFICIALS_CONTENT_BG
        )
        self.btn_clear_form = CTkButton(
            self.frame_buttons,
            text='CLEAR FORM',
            text_color=self.TEXT_COLOR,
            fg_color=self.BTN_BLUE,
            hover_color=self.BTN_HOVER_BLUE,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            command=self.clear_entries
        )
        self.btn_add = CTkButton(
            self.frame_buttons,
            text='ADD INDIVIDUAL',
            text_color=self.TEXT_COLOR,
            fg_color=self.BTN_GREEN,
            hover_color=self.BTN_HOVER_GREEN,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            command=self.add_individual
        )
        self.btn_update = CTkButton(
            self.frame_buttons,
            text='UPDATE INDIVIDUAL',
            text_color=self.TEXT_COLOR,
            fg_color=self.BTN_BROWN,
            hover_color=self.BTN_HOVER_BROWN,
            width=self.BTN_WIDTH,
            height=self.BTN_HEIGHT,
            command=self.update_individual
        )

        # DISPLAY OFFICIALS CONTAINER
        self.frame_displayData = CTkFrame(
            self.modify_window,
            fg_color=self.OFFICIALS_CONTENT_BG
        )
        officials_column = ["Officials ID", "First Name", "Middle Name", "Last Name", "Suffix", "Official Position"]
        self.tree_officials = ttk.Treeview(
            self.frame_displayData,
            columns=officials_column,
            show="headings",
            height=10,
        )
        self.tree_officials.heading('#0', text='', anchor='w')
        self.tree_officials.column('#0', width=0, stretch=NO)
        self.tree_officials.heading('Officials ID', text='', anchor='w')
        self.tree_officials.column('Officials ID', width=0, stretch=NO)
        for column in officials_column[1:]:
            self.tree_officials.heading(column, text=column)
            self.tree_officials.column(column, width=150, anchor='n')
        scrollbar = ttk.Scrollbar(
            self.frame_displayData,
            orient=VERTICAL,
            command=self.tree_officials.yview
        )
        self.tree_officials.configure(yscrollcommand=scrollbar.set)

        self.populate_officialsTree()

        self.tree_officials.bind("<ButtonRelease-1>", self.selected_official)

        # CREATE LAYOUT
        self.label_indiv_info.pack(anchor='center', fill='x', pady=(20, 0))

        self.container.pack(anchor='nw', fill='x')

        self.frame_entryLabel.pack(side='left', padx=(self.LABEL_LEFT, 0))

        self.frame_firstName.pack(anchor='nw', pady=(20, 0))
        self.label_firstName.pack(side='left', )
        self.entry_firstName.pack(side='left', padx=(25, 0))

        self.frame_middleName.pack(anchor='nw', pady=(5, 0))
        self.label_middleName.pack(side='left')
        self.entry_middleName.pack(side='left', padx=(10, 0))

        self.frame_lastName.pack(anchor='nw', pady=(5, 0))
        self.label_lastName.pack(side='left')
        self.entry_lastName.pack(side='left', padx=(26, 0))

        self.frame_suffix.pack(anchor='nw', pady=(5, 0))
        self.label_suffix.pack(side='left')
        self.entry_suffix.pack(side='left', padx=(64, 0))

        self.frame_position.pack(anchor='nw', pady=(5, 0))
        self.label_position.pack(side='left')
        self.entry_position.pack(side='left', padx=(47, 0))

        self.frame_buttons.pack(side='left', padx=(20, 0))
        self.btn_clear_form.pack(anchor='center', pady=(20, 5))
        self.btn_add.pack(anchor='center', pady=(0, 5))
        self.btn_update.pack(anchor='center', pady=(0, 0))

        self.frame_displayData.pack(anchor='center', pady=(20, 10))
        self.tree_officials.pack(anchor='nw')

    def add_individual(self):
        temp_firstName = capitalize_sentence(self.entry_firstName.get())
        temp_middleName = capitalize_sentence(self.entry_middleName.get())
        temp_lastName = capitalize_sentence(self.entry_lastName.get())
        temp_suffix = self.entry_suffix.get()
        temp_position = self.entry_position.get()

        if (not temp_firstName or
                not temp_middleName or
                not temp_lastName or
                not temp_position):
            messagebox.showwarning("Empty Data", "Please Fill out all the fields.")
            return

        if check_officials_exists(temp_firstName, temp_middleName, temp_lastName, temp_suffix):
            messagebox.showwarning("Name Exists", "Name already exists.")
            return

        max_counts = {
            "Punong Barangay": 1,
            "Kagawad": 7,
            "Secretary": 1,
            "Treasurer": 1,
            "Lupon": 10,
            "SK Chairman": 1
        }

        if temp_position in max_counts:
            if get_officials_count(temp_position) < max_counts[temp_position]:

                response = messagebox.askokcancel(
                    "Add Individual", f"Confirm adding this individual as {temp_position}?"
                )
                if not response:
                    return

                insert_official(
                    temp_firstName,
                    temp_middleName,
                    temp_lastName,
                    temp_suffix,
                    temp_position,
                )
                self.populate_officialsTree()
                self.clear_entries()
                self.set_officials()
                log_user_activity(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime(), f"ADDED {temp_position.upper()}")
                messagebox.showinfo("Success", f"A {temp_position} has been added!")
            else:
                messagebox.showwarning("Error", f"{temp_position} is already at maximum!")
        else:
            messagebox.showwarning("Error", "Invalid Official Position!")

    def update_individual(self):
        temp_id = self.entry_ID.get()
        temp_firstName = capitalize_sentence(self.entry_firstName.get())
        temp_middleName = capitalize_sentence(self.entry_middleName.get())
        temp_lastName = capitalize_sentence(self.entry_lastName.get())
        temp_suffix = self.entry_suffix.get().upper()
        temp_position = capitalize_sentence(self.entry_position.get())

        if temp_id == "":
            messagebox.showwarning("Empty Data", "There is no record selected!")
            return

        if (not temp_firstName or
                not temp_middleName or
                not temp_lastName or
                not temp_position):
            messagebox.showwarning("Empty Data", "Please Fill out all the fields.")
            return

        response = messagebox.askokcancel(
            "Update Individual", f"Confirm updating this individual?"
        )
        if not response:
            return

        update_official(
            temp_id,
            temp_firstName,
            temp_middleName,
            temp_lastName,
            temp_suffix,
            temp_position
        )

        self.populate_officialsTree()
        self.clear_entries()
        self.set_officials()
        log_user_activity(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime(), f"UPDATED {temp_position.upper()}")
        messagebox.showinfo("Success", "Information Updated!")

    def clear_officialsTree(self):
        for item in self.tree_officials.get_children():
            self.tree_officials.delete(item)

    def populate_officialsTree(self):
        self.clear_officialsTree()
        global count
        count = 0
        for record in get_officials():
            self.tree_officials.insert(
                '',
                'end',
                iid=count,
                text='',
                values=(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    record[4],
                    record[5],
                )
            )
            count += 1

    def selected_official(self, e):
        self.clear_entries()
        selected = self.tree_officials.focus()
        values = self.tree_officials.item(selected, 'values')

        if not values:
            return

        self.entry_ID.insert(0, values[0])
        self.entry_firstName.insert(0, values[1])
        self.entry_middleName.insert(0, values[2])
        self.entry_lastName.insert(0, values[3])
        self.entry_suffix.insert(0, values[4])
        self.entry_position.set(values[5])

    def clear_entries(self):
        self.entry_ID.delete(0, 'end')
        self.entry_firstName.delete(0, 'end')
        self.entry_middleName.delete(0, 'end')
        self.entry_lastName.delete(0, 'end')
        self.entry_suffix.delete(0, 'end')
        self.entry_position.set("")

    def _center_screen_(self, appWidth, appHeight):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (appWidth / 2))
        y_axis = int((sysHeight / 2) - (appHeight / 2)) - int(sysHeight * 0.015)
        return x_axis, y_axis


class AboutPage(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            fg_color=CONTENT_BG
        )
        self.constants()
        self.create_widgets()
        self.create_layout()

    def constants(self):
        self.IMAGE_POBLACION_SEAL = resources_path('assets/images/Poblacion8Seal.png')
        self.IMAGE_NDMC_SEAL = resources_path('assets/images/NDMCSeal.png')
        self.IMAGE_CITE_SEAL = resources_path('assets/images/CITESeal.png')
        self.IMAGE_TEKNOW_SEAL = resources_path('assets/images/TeKnowLogo.png')
        self.IMAGE_CSE_SEAL = resources_path('assets/images/NDMCCMS.png')

        self.IMAGE_CREATOR_1 = resources_path('assets/images/creator_1.png')
        self.IMAGE_CREATOR_2 = resources_path('assets/images/creator_2.png')
        self.IMAGE_CREATOR_3 = resources_path('assets/images/creator_3.png')

        self.IMAGE_WIDTH = 100
        self.IMAGE_HEIGHT = 100
        
        self.teknow_seal = CTkImage(
            light_image=Image.open(self.IMAGE_TEKNOW_SEAL), size=(877, 220)
        )
        self.poblacion_seal = CTkImage(
            light_image=Image.open(self.IMAGE_POBLACION_SEAL), size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        )
        self.ndmc_seal = CTkImage(
            light_image=Image.open(self.IMAGE_NDMC_SEAL), size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        )
        self.cite_seal = CTkImage(
            light_image=Image.open(self.IMAGE_CITE_SEAL), size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        )
        self.extension_seal = CTkImage(
            light_image=Image.open(self.IMAGE_CSE_SEAL), size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        )

        self.creator_1 = CTkImage(
            light_image=Image.open(self.IMAGE_CREATOR_1), size=(160, 160)
        )
        self.creator_2 = CTkImage(
            light_image=Image.open(self.IMAGE_CREATOR_2), size=(160, 160)
        )
        self.creator_3 = CTkImage(
            light_image=Image.open(self.IMAGE_CREATOR_3), size=(160, 160)
        )

    def create_widgets(self):
        self.frame_about_container = CTkScrollableFrame(
            self,
            bg_color=CONTENT_BG
        )
        self.label_project = CTkLabel(
            self.frame_about_container,
            text="THIS COMPUTERIZED SYSTEM IS UNDER THE PROJECT NAMED:",
            font=('', 17, 'bold')
        )
        self.img_teknow_logo = CTkLabel(
            self.frame_about_container,
            image=self.teknow_seal,
            text='',
        )
        self.label_teknow_title = CTkLabel(
            self.frame_about_container,
            text="SA BARYO",
            font=('', 40, 'bold')
        )
        self.textbox_teknow_description_1 = CTkTextbox(
            self.frame_about_container,
            width=700,
            height=160,
            corner_radius=0,
            wrap='word',
            fg_color=CONTENT_BG,
            font=('', 15, 'bold'),
            border_width=0
        )
        self.textbox_teknow_description_2 = CTkTextbox(
            self.frame_about_container,
            width=700, 
            corner_radius=0,
            wrap='word',
            fg_color=CONTENT_BG,
            font=('', 15, 'bold'),
            border_width=0
        )

        self.textbox_teknow_description_1._textbox.tag_configure("center", justify='left') # first, justify text position using tag_configure
        self.textbox_teknow_description_1.insert("0.0", 'The "TeKnow sa Baryo" project, as a community extension service of the College of Information Technology and Engineering, aims to bring about significant change in the barangays especially in Midsayap through digital transformation. Hence, "TeKnow" is derived from the words Technology and Knowledge. By digitizing barangay processes, developing innovative systems, and providing computer literacy to residents, students, and workers, the project aims to elevate technical skills and expedite community services. This project will also strengthen the connection between Notre Dame of Midsayap College and the community, leading to more effective collaboration and improved services for all.')
        self.textbox_teknow_description_1._textbox.tag_add("center", "1.0", "end")

        self.textbox_teknow_description_2._textbox.tag_configure("text", justify='left') # first, justify text position using tag_configure
        self.textbox_teknow_description_2.insert("0.0", 'Further, one of our missions as an academic and Catholic institution is to embody the daring missionary spirit passed on to us by the Oblates of Mary Immaculate. Thus, we are here not only to provide quality education but also to offer services to the community and reach those we can.')
        self.textbox_teknow_description_2._textbox.tag_add("text", "0.0", "end")

        self.textbox_teknow_description_1.configure(state='disabled')
        self.textbox_teknow_description_2.configure(state='disabled')
        
        self.label_entities = CTkLabel(
            self.frame_about_container,
            text="THE ORGANIZATIONS INVOLVED IN THIS PROJECT:",
            font=('', 17, 'bold')
        )
        self.frame_entities_first_level = CTkFrame(
            self.frame_about_container,
            bg_color=CONTENT_BG
        )
        self.img_ndmc = CTkLabel(
            self.frame_entities_first_level,
            image=self.ndmc_seal,
            text='',
        )
        self.label_ndmc = CTkLabel(
            self.frame_entities_first_level,
            text="NOTRE DAME OF MIDSAYAP COLLEGE",
            font=('', 25, 'bold')
        )
        self.frame_entities_second_level = CTkFrame(
            self.frame_about_container,
            bg_color=CONTENT_BG
        )
        self.img_cite = CTkLabel(
            self.frame_entities_second_level,
            image=self.cite_seal,
            text='',
        )
        self.label_cite = CTkLabel(
            self.frame_entities_second_level,
            text="COLLEGE OF INFORMATION TECHNOLOGY AND ENGINEERING",
            font=('', 25, 'bold')
        )
        self.frame_entities_third_level = CTkFrame(
            self.frame_about_container,
            bg_color=CONTENT_BG
        )
        self.img_extension = CTkLabel(
            self.frame_entities_third_level,
            image=self.extension_seal,
            text='',
        )
        self.label_extension = CTkLabel(
            self.frame_entities_third_level,
            text="COMMUNITY EXTENSION SERVICES",
            font=('', 25, 'bold')
        )
        self.frame_entities_fourth_level = CTkFrame(
            self.frame_about_container,
            bg_color=CONTENT_BG
        )
        self.img_poblacion = CTkLabel(
            self.frame_entities_fourth_level,
            image=self.poblacion_seal,
            text='',
        )
        self.label_poblacion = CTkLabel(
            self.frame_entities_fourth_level,
            text="BARANGAY POBLACION 8",
            font=('', 25, 'bold')
        )

        # self.label_developers = CTkLabel(
        #     self.frame_about_container,
        #     text="MEET THE DEVELOPERS OF THIS PROJECT:",
        #     font=('', 17, 'bold')
        # )
        # self.frame_developer_1 = CTkFrame(
        #     self.frame_about_container,
        #     fg_color=CONTENT_BG
        # )
        # self.img_creator_1 = CTkLabel(
        #     self.frame_developer_1,
        #     image=self.creator_1,
        #     text='',
        # )
        # self.label_creator_1 = CTkLabel(
        #     self.frame_developer_1,
        #     text="ANGELO CAILANG BUENAVISTA",
        #     font=('', 20, 'bold')
        # )
        # self.frame_developer_2 = CTkFrame(
        #     self.frame_about_container,
        #     fg_color=CONTENT_BG
        # )
        # self.img_creator_2 = CTkLabel(
        #     self.frame_developer_2,
        #     image=self.creator_2,
        #     text='',
        # )
        # self.label_creator_2 = CTkLabel(
        #     self.frame_developer_2,
        #     text="LOWENSTEIN FABREGAR CABILOGAN",
        #     font=('', 20, 'bold')
        # )
        # self.frame_developer_3 = CTkFrame(
        #     self.frame_about_container,
        #     fg_color=CONTENT_BG
        # )
        # self.img_creator_3 = CTkLabel(
        #     self.frame_developer_3,
        #     image=self.creator_3,
        #     text='',
        # )
        # self.label_creator_3 = CTkLabel(
        #     self.frame_developer_3,
        #     text="JOHN WILMER DURANGPARANG DELA CERNA",
        #     font=('', 20, 'bold')
        # )

    def create_layout(self):
        self.frame_about_container.pack(anchor='nw', expand='true', fill='both')
        self.label_project.pack(anchor='w', pady=110, padx=50)
        self.img_teknow_logo.pack(anchor='center')
        self.label_teknow_title.pack(anchor='center')
        self.textbox_teknow_description_1.pack(anchor='center')
        self.textbox_teknow_description_2.pack(anchor='center')
        
        self.label_entities.pack(anchor='w', pady=(110, 40), padx=50)
        self.frame_entities_first_level.pack(anchor='w', pady=5, padx=(400, 0))
        self.frame_entities_second_level.pack(anchor='w', pady=5, padx=(400, 0))
        self.frame_entities_third_level.pack(anchor='w', pady=5, padx=(400, 0))
        self.frame_entities_fourth_level.pack(anchor='w', pady=(5, 180), padx=(400, 0))
        self.img_ndmc.pack(side='left')
        self.label_ndmc.pack(side='left', padx=(15, 0))
        self.img_cite.pack(side='left')
        self.label_cite.pack(side='left', padx=(15, 0))
        self.img_extension.pack(side='left')
        self.label_extension.pack(side='left', padx=(15, 0))
        self.img_poblacion.pack(side='left')
        self.label_poblacion.pack(side='left', padx=(15, 0))
        
        # self.label_developers.pack(anchor='w', pady=(160, 40), padx=50)
        # self.frame_developer_1.pack(anchor='w', padx=(480, 0))
        # self.img_creator_1.pack(side='left')
        # self.label_creator_1.pack(side='left')
        # self.frame_developer_2.pack(anchor='w', padx=(480, 0))
        # self.img_creator_2.pack(side='left')
        # self.label_creator_2.pack(side='left')
        # self.frame_developer_3.pack(anchor='w', padx=(480, 0), pady=(0, 100))
        # self.img_creator_3.pack(side='left')
        # self.label_creator_3.pack(side='left')


class LoginWindow(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.create_constants()
        self.create_widgets()
        self.create_layout()

    def create_constants(self):
        self.IMAGE_POBLACION_SEAL = resources_path('assets/images/Poblacion8Seal.png')
        self.IMAGE_WIDTH = 200
        self.IMAGE_HEIGHT = 200
        self.poblacion_seal = CTkImage(
            light_image=Image.open(self.IMAGE_POBLACION_SEAL), size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        )
        self.login_font = ('Bahnschrift SemiBold', 30, 'normal')
        temp_background_image = Image.open(resources_path("assets/images/LoginImage.png"))
        self.background_image = ImageTk.PhotoImage(temp_background_image)
        self.ENTRY_WIDTH = 300
        
        self.IMAGE_NDMC_PATH = resources_path('assets/images/NDMCSeal.png')
        self.IMAGE_CITE_PATH = resources_path('assets/images/CITESeal.png')
        self.IMAGE_CES_PATH = resources_path('assets/images/NDMCCMS.png')
        self.IMAGE_TEKNOW_PATH = resources_path('assets/images/TeKnowLogo.png')
        
        self.IMAGE_WIDTH = 500
        self.IMAGE_HEIGHT = 500
        self.IMAGE_DESC_WIDTH = 40
        self.IMAGE_DESC_HEIGHT = 40

        self.temp_img_ndmc = CTkImage(
            light_image=Image.open(self.IMAGE_NDMC_PATH), size=(self.IMAGE_DESC_WIDTH, self.IMAGE_DESC_HEIGHT)
        )
        self.temp_img_cite = CTkImage(
            light_image=Image.open(self.IMAGE_CITE_PATH), size=(self.IMAGE_DESC_WIDTH, self.IMAGE_DESC_HEIGHT)
        )
        self.temp_img_ces = CTkImage(
            light_image=Image.open(self.IMAGE_CES_PATH), size=(self.IMAGE_DESC_WIDTH, self.IMAGE_DESC_HEIGHT)
        )
        self.temp_img_teknow = CTkImage(
            light_image=Image.open(self.IMAGE_TEKNOW_PATH), size=(60, 17)
        )

    def create_widgets(self):
        # Background Image Container
        self.canvas_bg_image = CTkCanvas(self)
        self.canvas_bg_image.create_image(0, 0, image=self.background_image, anchor="nw")
        self.canvas_bg_image.image = self.background_image
        # - Window Container
        self.frame_login_window = CTkFrame(
            self,
            fg_color='#ced4da',
            corner_radius=20
        )
        # -- Image
        self.img_poblacion_seal = CTkLabel(
            self.frame_login_window,
            image=self.poblacion_seal,
            text='',
        )
        # -- Username Container
        self.frame_username_container = CTkFrame(
            self.frame_login_window,
            fg_color='#ced4da',
        )
        # -- Password Container
        self.frame_password_container = CTkFrame(
            self.frame_login_window,
            fg_color='#ced4da',
        )
        # --- Username Widgets
        self.label_username = CTkLabel(
            self.frame_username_container,
            font=self.login_font,
            text='USERNAME: '
        )
        self.entry_username = CTkEntry(
            self.frame_username_container,
            font=self.login_font,
            width=self.ENTRY_WIDTH
        )
        self.entry_username.focus()
        # --- Password Widgets
        self.label_password = CTkLabel(
            self.frame_password_container,
            font=self.login_font,
            text='PASSWORD: '
        )
        self.entry_password = CTkEntry(
            self.frame_password_container,
            font=self.login_font,
            show='•',
            width=self.ENTRY_WIDTH
        )
        # -- Login Button
        self.btn_login = CTkButton(
            self.frame_login_window,
            text='LOGIN',
            font=self.login_font,
            command=self.check_credentials
        )

        self.small_desc = CTkFrame(
            self,
            fg_color=CONTENT_BG,
        )
        self.img_ndmc = CTkLabel(
            self.small_desc,
            image=self.temp_img_ndmc,
            text='',
        )
        self.img_cite = CTkLabel(
            self.small_desc,
            image=self.temp_img_cite,
            text='',
        )
        self.img_ces = CTkLabel(
            self.small_desc,
            image=self.temp_img_ces,
            text='',
        )
        self.img_teknow = CTkLabel(
            self.small_desc,
            image=self.temp_img_teknow,
            text='',
        )
        self.label_desc = CTkLabel(
            self.small_desc,
            text="SA BARYO: A COMMUNITY EXTENSION PROGRAM OF NDMC COLLEGE OF INFORMATION TECHNOLOGY AND ENGINEERING",
            font=('', 13, 'bold')
        )

    def create_layout(self):
        self.canvas_bg_image.pack(fill="both", expand=True)

        self.frame_login_window.place(
            relx=0.5,  # Relative x position (0.5 for center)
            rely=0.5,  # Relative y position (0.5 for center)
            anchor='center'  # Anchor point for positioning
        )
        self.img_poblacion_seal.pack(
            anchor='center',
            pady=(60, 50)
        )
        self.frame_username_container.pack(
            anchor='center',
        )
        self.frame_password_container.pack(
            anchor='center',
            padx=100,
        )
        self.label_username.pack(side='left')
        self.entry_username.pack(side='left', pady=(0, 10))
        self.label_password.pack(side='left')
        self.entry_password.pack(side='left')
        self.btn_login.pack(
            anchor='center',
            pady=(20, 100)
        )

        self.small_desc.pack(anchor='sw', fill='x', pady=5, padx=20)
        self.img_ndmc.pack(side='left')
        self.img_cite.pack(side='left', padx=(10, 0))
        self.img_ces.pack(side='left', padx=(10, 0))
        self.img_teknow.pack(side='left', padx=(15, 0))
        self.label_desc.pack(side='left', padx=(5, 0))

    def check_credentials(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username:
            messagebox.showwarning("Login Error", "Username cannot be Empty!")
            return

        if verify_user(username, password):
            self.entry_password.delete(0, 'end')
            global ACTIVE_USER_ID
            global ACTIVE_USERNAME
            global ACTIVE_USER_ROLE
            global ACTIVE_USER_TYPE
            ACTIVE_USER_INFO = get_user_info(username)

            ACTIVE_USER_ID = ACTIVE_USER_INFO[0][0]
            ACTIVE_USERNAME = ACTIVE_USER_INFO[0][3]
            ACTIVE_USER_ROLE = ACTIVE_USER_INFO[0][2]
            ACTIVE_USER_TYPE = ACTIVE_USER_INFO[0][1]

            log_login(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime())

            set_logged_out_false()
            update_birthdays()
            do_requirements()
            self.parent.show_dashboard()
        else:
            messagebox.showwarning("Login Error", "Incorrect username or password!")

    def check_credentials_event(self, e):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username:
            messagebox.showwarning("Login Error", "Username cannot be Empty!")
            return

        if verify_user(username, password):
            self.entry_password.delete(0, 'end')
            global ACTIVE_USER_ID
            global ACTIVE_USERNAME
            global ACTIVE_USER_ROLE
            global ACTIVE_USER_TYPE
            ACTIVE_USER_INFO = get_user_info(username)

            ACTIVE_USER_ID = ACTIVE_USER_INFO[0][0]
            ACTIVE_USERNAME = ACTIVE_USER_INFO[0][3]
            ACTIVE_USER_ROLE = ACTIVE_USER_INFO[0][2]
            ACTIVE_USER_TYPE = ACTIVE_USER_INFO[0][1]

            log_login(ACTIVE_USERNAME, ACTIVE_USER_ROLE, get_formatted_datetime())

            set_logged_out_false()
            update_birthdays()
            do_requirements()
            self.parent.show_dashboard()
        else:
            messagebox.showwarning("Login Error", "Incorrect username or password!")


class MainApplication(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_main_window()
        initialize_database()

        self.login_window = LoginWindow(self)
        self.login_window.pack(anchor='nw', fill='both', expand='true')
        self.dashboard = None

    def show_dashboard(self):
        self.login_window.pack_forget()
        self.dashboard = Dashboard(self)
        self.dashboard.pack(fill='both', expand='true')

    def show_login(self):
        if self.dashboard:
            self.dashboard.pack_forget()
        self.login_window.pack(anchor='nw', fill='both', expand='true')

    def _setup_main_window(self):
        self.title(MAIN_APP_NAME)
        self.resizable(True, True)
        set_default_color_theme(
            resources_path("assets/theme/custom_theme.json"))
        set_appearance_mode('light')
        self.iconPath = resources_path('assets/images/Poblacion8Seal.ico')
        self.iconbitmap(default=self.iconPath)
        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(self.iconPath))
        self._center_screen(1580, 880)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if not messagebox.askokcancel("Confirm Action", "You are about to exit the application."):
            return
        if not LOGGED_OUT:
            system_logout("ATYPICAL")
        clear_active_user_info()
        self.destroy()

    def _center_screen(self, width, height):
        sysWidth = self.winfo_screenwidth()
        sysHeight = self.winfo_screenheight()
        x_axis = int((sysWidth / 2) - (width / 2))
        y_axis = int((sysHeight / 2) - (height / 2)) - int(sysHeight * 0.015)
        self.geometry("{}x{}+{}+{}".format(width, height, x_axis, y_axis))


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = MainApplication()
    app.mainloop()
