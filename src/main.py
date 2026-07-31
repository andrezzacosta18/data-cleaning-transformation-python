import os
from pathlib import Path
from IPython.display import display 
import pandas as pd


# ==========================================================
# PATHS
# ==========================================================
df = pd.read_csv("data/raw/netflix_titles.csv")


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
    print("2 — Analyze and Handle missing values")
    print("3 — Analyze and Handle duplicate rows")
    print("4 — Standardize text columns")
    print("5 — Clean and convert numeric columns")
    print("6 — View cleaning report")
    print("7 — Undo last operation")
    print("8— Restore original dataset")
    print("9 — Save cleaned dataset")
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

def handle_missing_values(df):

    backup_df = df.copy()
    print("=" * 70)
    print("MISSING VALUES ANALYSIS")
    print("=" * 70)

    missing_values = df.isnull().sum()
    missing_percentage = df.isnull().mean() * 100

    missing_summary = pd.DataFrame({
        "Missing Values": missing_values,
        "Missing Percentage (%)": missing_percentage.round(2)
    })

    missing_columns = missing_summary[
        missing_summary["Missing Values"] > 0
    ]

    if missing_columns.empty:
        print("\nThere are no missing values in the dataset.")
        return df

    columns = list(missing_columns.index)

    print("\nColumns with missing values:\n")

    for index, column in enumerate(columns, start=1):

        missing_count = missing_summary.loc[
            column,
            "Missing Values"
        ]

        missing_percent = missing_summary.loc[
            column,
            "Missing Percentage (%)"
        ]

        print(
            f"{index} - {column} "
            f"({missing_count} missing | {missing_percent:.2f}%)"
        )

    print("0 - Return")

    try:
        column_option = int(input("\nChoose a column: "))

    except ValueError:
        print("\nInvalid option. Please enter a number.")
        return df

    if column_option == 0:
        return df

    if column_option < 1 or column_option > len(columns):
        print("\nInvalid column option.")
        return df

    selected_column = columns[column_option - 1]

    missing_count = missing_summary.loc[
        selected_column,
        "Missing Values"
    ]

    missing_percent = missing_summary.loc[
        selected_column,
        "Missing Percentage (%)"
    ]

    print("\n" + "=" * 70)
    print(f"COLUMN: {selected_column}")
    print("=" * 70)

    print(
        f"\nThe column '{selected_column}' has "
        f"{missing_count} missing values "
        f"({missing_percent:.2f}%)."
    )

    print("\nWhat would you like to do?\n")

    print("1 - Remove rows")
    print("2 - Fill with a fixed value")
    print("3 - Leave as it is")
    print("0 - Return")

    valid_options = [0, 1, 2, 3]

    while True:

        try:
            action = int(input("\nChoose an option: "))

            if action in valid_options:
                break

            print("\nInvalid option. Please choose a valid option.")

        except ValueError:
            print("\nInvalid option. Please enter a number.")


    if action == 0:
        return df

    if action == 1:

        rows_before = len(df)

        print(f"The dataset has {rows_before} rows and {missing_count} missing values.")
        confirm = input(
        "\nAre you sure you want to remove these rows? (y/n): "
        ).lower()

        if confirm == "y":

            df = df.dropna(subset=[selected_column])
            print("\nRows removed successfully.")
            return df

        else:

            print("\nOperation cancelled.")


    elif action == 2:

        fixed_value = input("\nEnter the value to use: ")

        df[selected_column] = df[selected_column].fillna(fixed_value)

        print(
            f"\nMissing values in '{selected_column}' "
            f"were filled with '{fixed_value}'."
        )

    elif action == 3:

        print(
            f"\nThe column '{selected_column}' "
            f"was left unchanged."
        )

    else:
        print("\nInvalid option.")

    return df


# ==========================================================
# OPTION 3
# ==========================================================

def handle_duplicates(df):

    print("=" * 70)
    print("DUPLICATE ROWS ANALYSIS")
    print("=" * 70)

    duplicated_rows = df.duplicated().sum()

    if duplicated_rows == 0:
        print("\nThere are no duplicate rows in the dataset.")
        return

    print(f"\nNumber of duplicate rows: {duplicated_rows}")

    print("\nWhat would you like to do?\n")

    print("1 - Remove duplicates")
    print("2 - Leave as it is")
    print("0 - Return")

    valid_options = [0, 1, 2]

    while True:

        try:
            action = int(input("\nChoose an option: "))

            if action in valid_options:
                break

            print("\nInvalid option. Please choose a valid option.")

        except ValueError:
            print("\nInvalid option. Please enter a number.")

        if action == 0:
            return df
        
    if action == 1:
        duplicate_rows = df.duplicated().sum()

        if duplicate_rows > 0:
            duplicate_data = df[ 
                df.duplicated()
                ] 
            display(duplicate_data)
        else:
            print("No duplicate rows found.")

            print(df[df.duplicated(keep=False)])



# ==========================================================
# OPTION 4
# ==========================================================
def standardize_text(df):

    print("=" * 70)
    print("STANDARDIZE TEXT COLUMNS")
    print("=" * 70)

    text_columns = list(
    df.select_dtypes(
        include=["object", "string"]
    ).columns
)
    
    print("\nChoose the standardization you want to apply:\n")

    print("1 - Convert to UPPERCASE")
    print("2 - Convert to lowercase")
    print("3 - Convert to Title Case")
    print("4 - Remove leading and trailing spaces")
    print("5 - Remove extra spaces")
    print("6 - Replace text")
    print("0 - Return")

    valid_options = [0, 1, 2 ,3, 4, 5, 6]

    while True:

        try:
            action = int(input("\nChoose an option: "))

            if action in valid_options:
                break

            print("\nInvalid option. Please choose a valid option.")

        except ValueError:
            print("\nInvalid option. Please enter a number.")



# ==========================================================
# OPTION 5
# ==========================================================



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

  
    print("=" * 70)
    print("SAVE CLEANED DATASET")
    print("=" * 70)

    print("\nDataset saved successfully!")
    print(f"\nSaved to:\n{OUTPUT_PATH}")


# ==========================================================
# MAIN
# ==========================================================

def cleaning(df):

    cleaning_report = []

    backup_df = df.copy()

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
            df = handle_missing_values(df)
            pause()

        elif op == 3:

            clear_screen()
            handle_duplicates(df)
            pause()

        elif op == 4:

            clear_screen()
            df = handle_duplicates(df)
            pause()

        elif op == 5:

            clear_screen()
            df = standardize_text(df)
            pause()

        elif op == 6:

            clear_screen()
            df = convert_numeric_columns(df)
            pause()

        
        elif op == 7:

            clear_screen()
            df = backup_df.copy()
            print("\nLast operation undone successfully.")
            pause()

        elif op == 8:

            clear_screen()

            confirm = input(
                "\nRestore the original dataset? "
                "All unsaved changes will be lost. (y/n): "
            ).lower()

            if confirm == "y":

                df = pd.read_csv("data/raw/netflix_titles.csv")

                print("\nOriginal dataset restored successfully.")

            else:

                print("\nOperation cancelled.")

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

            print("\nInvalid option. Choose a number from 0 to 8.")
            pause()


try:
    df = pd.read_csv("data/raw/netflix_titles.csv")
    cleaning(df)

except FileNotFoundError:
    print("Dataset not found.")
    print(f"Expected path:\n{"data/raw/netflix_titles.csv"}")