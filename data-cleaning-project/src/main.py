import os
from pathlib import Path

import pandas as pd

df = pd.read_csv("data-cleaning-transformation-python/data-cleaning-project/data/raw/netflix_titles.csv")

# ==========================================================
# PATHS
# ==========================================================

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "netflix_titles.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "netflix_titles_clean.csv"


# ==========================================================
# GENERAL FUNCTIONS
# ==========================================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to return to the menu...")


# ==========================================================
# MENU
# ==========================================================

def display_menu():

    print("=" * 70)
    print("        DATA CLEANING AND TRANSFORMATION SYSTEM")
    print("=" * 70)

    print("\nWelcome to the Data Cleaning System!")
    print("No changes will be made automatically.")
    print("You must review each problem and decide what action to take.")

    print("\n1 — View dataset information")
    print("2 — Analyze missing values")
    print("3 — Analyze duplicate rows")
    print("4 — Handle duplicate rows")
    print("5 — Standardize text columns")
    print("6 — Clean and convert numeric columns")
    print("7 — View cleaning report")
    print("8 — Save cleaned dataset")
    print("0 — Exit")

    print("\n" + "=" * 70)


# ==========================================================
# OPTION 1
# ==========================================================

def display_dataset_info(df):

    print("=" * 70)
    print("DATASET INFORMATION")
    print("=" * 70)

    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}\n")

    df.info()


# ==========================================================
# OPTION 2
# ==========================================================

def analyze_missing_values(df):

    print("=" * 70)
    print("MISSING VALUES ANALYSIS")
    print("=" * 70)

    print("\nMissing Values by Column\n")

    df.info()

    missing_values = df.isnull().sum()

    missing_percentage = df.isnull().mean() * 100

    missing_summary = pd.DataFrame({
        "Missing Values": missing_values,
        "Missing Percentage (%)": missing_percentage.round(2)
    })

    missing_columns = missing_summary[
    missing_summary["Missing Values"] > 0
]

    print("\nSummary:\n")
    print(f"{missing_columns}\n")

    # ==========================================================

""" 
    opc = int(input("Enter the column you wish to change. "))

    if opc == 1: """
        

analyze_missing_values(df)

# ==========================================================
# OPTION 3
# ==========================================================

def analyze_duplicates(df):

    print("=" * 70)
    print("DUPLICATE ROWS ANALYSIS")
    print("=" * 70)

    print("\nThis option has not been implemented yet.")


# ==========================================================
# OPTION 4
# ==========================================================

def remove_duplicates(df):

    print("=" * 70)
    print("HANDLE DUPLICATE ROWS")
    print("=" * 70)

    print("\nThis option has not been implemented yet.")

    return df


# ==========================================================
# OPTION 5
# ==========================================================

def standardize_text(df):

    print("=" * 70)
    print("STANDARDIZE TEXT COLUMNS")
    print("=" * 70)

    print("\nThis option has not been implemented yet.")

    return df


# ==========================================================
# OPTION 6
# ==========================================================

def convert_numeric_columns(df):

    print("=" * 70)
    print("CLEAN AND CONVERT NUMERIC COLUMNS")
    print("=" * 70)

    print("\nThis option has not been implemented yet.")

    return df


# ==========================================================
# OPTION 7
# ==========================================================

def display_cleaning_report(cleaning_report):

    print("=" * 70)
    print("CLEANING REPORT")
    print("=" * 70)

    if len(cleaning_report) == 0:

        print("\nNo cleaning actions have been performed yet.")

    else:

        print()

        for index, action in enumerate(cleaning_report, start=1):
            print(f"{index} — {action}")


# ==========================================================
# OPTION 8
# ==========================================================

def save_clean_dataset(df):

    # Save the cleaned DataFrame as a CSV file
    df.to_csv(OUTPUT_PATH, index=False)

    print("=" * 70)
    print("SAVE CLEANED DATASET")
    print("=" * 70)

    print("\nDataset saved successfully!")

    # Display the location where the file was saved
    print(f"\nSaved to:\n{OUTPUT_PATH}")

# ==========================================================
# MAIN
# ==========================================================

def cleaning(df):

    cleaning_report = []

    while True:

        clear_screen()
        display_menu()

        try:
            op = int(input("Choose an option: "))

        except ValueError:

            print("\nInvalid option. Please enter a number.")
            pause()
            continue

        if op == 1:

            clear_screen()

            display_dataset_info(df)

            pause()

        elif op == 2:

            clear_screen()

            analyze_missing_values(df)

            pause()

        elif op == 3:

            clear_screen()

            pause()

        elif op == 4:

            clear_screen()

            analyze_duplicates(df)

            pause()

        elif op == 5:

            clear_screen()

            df = remove_duplicates(df)

            pause()

        elif op == 6:

            clear_screen()

            df = standardize_text(df)

            pause()

        elif op == 7:

            clear_screen()

            df = convert_numeric_columns(df)

            pause()

        elif op == 8:

            clear_screen()

            display_cleaning_report(cleaning_report)

            pause()

        elif op == 9:

            clear_screen()

            save_clean_dataset(df)

            pause()

        elif op == 0:

            clear_screen()

            print("Program closed.")
            break

        else:

            print("\nInvalid option. Choose a number from 0 to 9.")
            pause()


