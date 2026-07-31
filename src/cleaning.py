import os
from pathlib import Path

import pandas as pd


# ==========================================================
# PATHS
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "raw" / "netflix_titles.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "netflix_titles_cleaned.csv"


# ==========================================================
# GENERAL FUNCTIONS
# ==========================================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to return to the menu...")


def display_columns(columns, title="AVAILABLE COLUMNS"):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    for index, column in enumerate(columns, start=1):
        print(f"{index} - {column}")

    print("0 - Return")


def choose_column(columns):
    while True:
        try:
            column_option = int(input("\nChoose a column: "))

            if column_option == 0:
                return None

            if 1 <= column_option <= len(columns):
                return columns[column_option - 1]

            print("\nInvalid option. Choose a column from the list.")

        except ValueError:
            print("\nInvalid option. Please enter a number.")


def display_column_analysis(df, selected_column):
    print("\n" + "=" * 70)
    print(f"COLUMN ANALYSIS: {selected_column}")
    print("=" * 70)

    print(f"\nData type: {df[selected_column].dtype}")
    print(f"Missing values: {df[selected_column].isnull().sum()}")
    print(f"Unique values: {df[selected_column].nunique(dropna=True)}")

    print("\nSample values:")
    print(df[selected_column].dropna().head(10).to_string(index=False))

    print("\nMost frequent values:")
    print(df[selected_column].value_counts(dropna=False).head(10))


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

    print("\n1 - View dataset information")
    print("2 - Analyze and handle missing values")
    print("3 - Analyze and handle duplicate rows")
    print("4 - Standardize text columns")
    print("5 - Clean and convert numeric columns")
    print("6 - View cleaning report")
    print("7 - Undo last operation")
    print("8 - Restore original dataset")
    print("9 - Save cleaned dataset")
    print("0 - Exit")

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

    print("Column types and non-null values:\n")
    df.info()

    print("\nFirst five rows:\n")
    print(df.head())


# ==========================================================
# OPTION 2
# ==========================================================

def handle_missing_values(df):
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
        return df, None

    columns = list(missing_columns.index)

    print("\nColumns with missing values:\n")

    for index, column in enumerate(columns, start=1):
        missing_count = missing_summary.loc[column, "Missing Values"]
        missing_percent = missing_summary.loc[column, "Missing Percentage (%)"]

        print(
            f"{index} - {column} "
            f"({missing_count} missing | {missing_percent:.2f}%)"
        )

    print("0 - Return")

    selected_column = choose_column(columns)

    if selected_column is None:
        return df, None

    missing_count = missing_summary.loc[selected_column, "Missing Values"]
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
    print("3 - Fill with the mean or median")
    print("4 - Leave as it is")
    print("0 - Return")

    while True:
        try:
            action = int(input("\nChoose an option: "))

            if action in [0, 1, 2, 3, 4]:
                break

            print("\nInvalid option. Please choose a valid option.")

        except ValueError:
            print("\nInvalid option. Please enter a number.")

    if action == 0:
        return df, None

    if action == 1:
        print(
            f"\nThe dataset has {len(df)} rows and "
            f"{missing_count} missing values in '{selected_column}'."
        )

        confirm = input(
            "\nAre you sure you want to remove these rows? (y/n): "
        ).strip().lower()

        if confirm == "y":
            df = df.dropna(subset=[selected_column]).copy()
            print("\nRows removed successfully.")
            report = f"Removed rows with missing values from '{selected_column}'."
            return df, report

        print("\nOperation cancelled.")
        return df, None

    if action == 2:
        fixed_value = input("\nEnter the value to use: ")

        if pd.api.types.is_numeric_dtype(df[selected_column]):
            try:
                fixed_value = float(fixed_value)
            except ValueError:
                print("\nThis numeric column requires a numeric value.")
                return df, None

        df[selected_column] = df[selected_column].fillna(fixed_value)

        print(
            f"\nMissing values in '{selected_column}' "
            f"were filled with '{fixed_value}'."
        )

        report = (
            f"Filled missing values in '{selected_column}' "
            f"with '{fixed_value}'."
        )
        return df, report

    if action == 3:
        if not pd.api.types.is_numeric_dtype(df[selected_column]):
            print("\nThis is not a numeric column. Choose another method.")
            return df, None

        print("\nChoose a method:\n")
        print("1 - Mean")
        print("2 - Median")
        print("0 - Return")

        while True:
            try:
                method = int(input("\nChoose an option: "))

                if method in [0, 1, 2]:
                    break

                print("\nInvalid option. Please choose a valid option.")

            except ValueError:
                print("\nInvalid option. Please enter a number.")

        if method == 0:
            return df, None

        if method == 1:
            fill_value = df[selected_column].mean()
            method_name = "mean"
        else:
            fill_value = df[selected_column].median()
            method_name = "median"

        df[selected_column] = df[selected_column].fillna(fill_value)

        print(
            f"\nMissing values in '{selected_column}' were filled "
            f"with the {method_name}: {fill_value:.2f}."
        )

        report = (
            f"Filled missing values in '{selected_column}' "
            f"with the {method_name} ({fill_value:.2f})."
        )
        return df, report

    print(f"\nThe column '{selected_column}' was left unchanged.")
    return df, None


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
        return df, None

    print(f"\nNumber of duplicate rows: {duplicated_rows}")

    print("\nDuplicate rows:\n")
    print(df[df.duplicated(keep=False)].head(20))

    print("\nWhat would you like to do?\n")
    print("1 - Remove duplicates")
    print("2 - Leave as it is")
    print("0 - Return")

    while True:
        try:
            action = int(input("\nChoose an option: "))

            if action in [0, 1, 2]:
                break

            print("\nInvalid option. Please choose a valid option.")

        except ValueError:
            print("\nInvalid option. Please enter a number.")

    if action == 0 or action == 2:
        print("\nDuplicate rows were left unchanged.")
        return df, None

    confirm = input(
        f"\nRemove {duplicated_rows} duplicate rows? (y/n): "
    ).strip().lower()

    if confirm == "y":
        df = df.drop_duplicates().copy()
        print("\nDuplicate rows removed successfully.")
        report = f"Removed {duplicated_rows} duplicate rows."
        return df, report

    print("\nOperation cancelled.")
    return df, None


# ==========================================================
# OPTION 4
# ==========================================================

def standardize_text(df):
    print("=" * 70)
    print("STANDARDIZE TEXT COLUMNS")
    print("=" * 70)

    text_columns = list(
        df.select_dtypes(include=["object", "string"]).columns
    )

    if len(text_columns) == 0:
        print("\nThere are no text columns in the dataset.")
        return df, None

    display_columns(text_columns, "TEXT COLUMNS")

    selected_column = choose_column(text_columns)

    if selected_column is None:
        return df, None

    display_column_analysis(df, selected_column)

    print("\nChoose the standardization you want to apply:\n")
    print("1 - Convert to UPPERCASE")
    print("2 - Convert to lowercase")
    print("3 - Remove extra spaces")
    print("4 - Replace text")
    print("0 - Return")

    while True:
        try:
            action = int(input("\nChoose an option: "))

            if action in [0, 1, 2, 3, 4]:
                break

            print("\nInvalid option. Please choose a valid option.")

        except ValueError:
            print("\nInvalid option. Please enter a number.")

    if action == 0:
        return df, None

    if action == 1:
        df[selected_column] = df[selected_column].str.upper()
        print(f"\nColumn '{selected_column}' converted to uppercase.")
        report = f"Converted '{selected_column}' to uppercase."

    elif action == 2:
        df[selected_column] = df[selected_column].str.lower()
        print(f"\nColumn '{selected_column}' converted to lowercase.")
        report = f"Converted '{selected_column}' to lowercase."

    elif action == 3:
        df[selected_column] = (
            df[selected_column]
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )
        print(f"\nExtra spaces removed from '{selected_column}'.")
        report = f"Removed extra spaces from '{selected_column}'."

    else:
        old_text = input("\nWhat text would you like to replace? ")
        new_text = input("Replace with: ")

        df[selected_column] = df[selected_column].str.replace(
            old_text,
            new_text,
            regex=False
        )

        print(
            f"\n'{old_text}' was replaced with '{new_text}' "
            f"in '{selected_column}'."
        )
        report = (
            f"Replaced '{old_text}' with '{new_text}' "
            f"in '{selected_column}'."
        )

    return df, report


# ==========================================================
# OPTION 5
# ==========================================================

def clean_and_convert_numeric(df):
    print("=" * 70)
    print("CLEAN AND CONVERT NUMERIC COLUMNS")
    print("=" * 70)

    columns = list(df.columns)
    display_columns(columns)

    selected_column = choose_column(columns)

    if selected_column is None:
        return df, None

    display_column_analysis(df, selected_column)

    print("\nWhat would you like to do?\n")
    print("1 - Remove a symbol or text")
    print("2 - Remove thousand separators")
    print("3 - Replace decimal comma with decimal point")
    print("4 - Extract the first number from each value")
    print("5 - Convert to integer")
    print("6 - Convert to float")
    print("0 - Return")

    while True:
        try:
            action = int(input("\nChoose an option: "))

            if action in [0, 1, 2, 3, 4, 5, 6]:
                break

            print("\nInvalid option. Please choose a valid option.")

        except ValueError:
            print("\nInvalid option. Please enter a number.")

    if action == 0:
        return df, None

    if action == 1:
        text_to_remove = input("\nEnter the symbol or text to remove: ")

        df[selected_column] = (
            df[selected_column]
            .astype("string")
            .str.replace(text_to_remove, "", regex=False)
            .str.strip()
        )

        print(
            f"\n'{text_to_remove}' was removed from "
            f"'{selected_column}'."
        )
        report = f"Removed '{text_to_remove}' from '{selected_column}'."
        return df, report

    if action == 2:
        separator = input(
            "\nEnter the thousand separator to remove (example: . or ,): "
        )

        df[selected_column] = (
            df[selected_column]
            .astype("string")
            .str.replace(separator, "", regex=False)
            .str.strip()
        )

        print(
            f"\nThousand separator '{separator}' was removed "
            f"from '{selected_column}'."
        )
        report = (
            f"Removed thousand separator '{separator}' "
            f"from '{selected_column}'."
        )
        return df, report

    if action == 3:
        df[selected_column] = (
            df[selected_column]
            .astype("string")
            .str.replace(",", ".", regex=False)
            .str.strip()
        )

        print(
            f"\nDecimal commas were replaced with decimal points "
            f"in '{selected_column}'."
        )
        report = (
            f"Replaced decimal commas with decimal points "
            f"in '{selected_column}'."
        )
        return df, report

    if action == 4:
        extracted_numbers = (
            df[selected_column]
            .astype("string")
            .str.extract(r"([-+]?\d*[.,]?\d+)", expand=False)
            .str.replace(",", ".", regex=False)
        )

        df[selected_column] = pd.to_numeric(
            extracted_numbers,
            errors="coerce"
        )

        print(f"\nNumbers extracted from '{selected_column}'.")
        report = f"Extracted numeric values from '{selected_column}'."
        return df, report

    if action == 5:
        converted_values = pd.to_numeric(
            df[selected_column],
            errors="coerce"
        )

        invalid_values = (
            converted_values.isna() & df[selected_column].notna()
        ).sum()

        if invalid_values > 0:
            print(
                f"\nConversion was not completed. {invalid_values} values "
                "could not be converted to integers."
            )
            print("Clean the symbols or text first.")
            return df, None

        if converted_values.dropna().mod(1).ne(0).any():
            print(
                "\nConversion was not completed because the column "
                "contains decimal values."
            )
            return df, None

        if converted_values.isna().any():
            df[selected_column] = converted_values.astype("Int64")
        else:
            df[selected_column] = converted_values.astype("int64")

        print(f"\nColumn '{selected_column}' converted to integer.")
        report = f"Converted '{selected_column}' to integer."
        return df, report

    converted_values = pd.to_numeric(
        df[selected_column],
        errors="coerce"
    )

    invalid_values = (
        converted_values.isna() & df[selected_column].notna()
    ).sum()

    if invalid_values > 0:
        print(
            f"\nConversion was not completed. {invalid_values} values "
            "could not be converted to float."
        )
        print("Clean the symbols or text first.")
        return df, None

    df[selected_column] = converted_values.astype("float64")

    print(f"\nColumn '{selected_column}' converted to float.")
    report = f"Converted '{selected_column}' to float."
    return df, report


# ==========================================================
# OPTION 6
# ==========================================================

def display_cleaning_report(cleaning_report):
    print("=" * 70)
    print("CLEANING REPORT")
    print("=" * 70)

    if len(cleaning_report) == 0:
        print("\nNo cleaning actions have been performed yet.")
        return

    print()

    for index, action in enumerate(cleaning_report, start=1):
        print(f"{index} - {action}")


# ==========================================================
# OPTION 9
# ==========================================================

def save_clean_dataset(df):
    print("=" * 70)
    print("SAVE CLEANED DATASET")
    print("=" * 70)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nDataset saved successfully!")
    print(f"\nSaved to:\n{OUTPUT_PATH}")


# ==========================================================
# MAIN
# ==========================================================

def cleaning(df):
    cleaning_report = []
    undo_stack = []

    while True:
        clear_screen()
        display_menu()

        try:
            option = int(input("Choose an option: "))

        except ValueError:
            print("\nInvalid option. Please enter a number.")
            pause()
            continue

        if option == 1:
            clear_screen()
            display_dataset_info(df)
            pause()

        elif option == 2:
            clear_screen()
            previous_df = df.copy(deep=True)
            df, report = handle_missing_values(df)

            if report is not None:
                undo_stack.append(previous_df)
                cleaning_report.append(report)

            pause()

        elif option == 3:
            clear_screen()
            previous_df = df.copy(deep=True)
            df, report = handle_duplicates(df)

            if report is not None:
                undo_stack.append(previous_df)
                cleaning_report.append(report)

            pause()

        elif option == 4:
            clear_screen()
            previous_df = df.copy(deep=True)
            df, report = standardize_text(df)

            if report is not None:
                undo_stack.append(previous_df)
                cleaning_report.append(report)

            pause()

        elif option == 5:
            clear_screen()
            previous_df = df.copy(deep=True)
            df, report = clean_and_convert_numeric(df)

            if report is not None:
                undo_stack.append(previous_df)
                cleaning_report.append(report)

            pause()

        elif option == 6:
            clear_screen()
            display_cleaning_report(cleaning_report)
            pause()

        elif option == 7:
            clear_screen()

            if len(undo_stack) == 0:
                print("\nThere is no operation to undo.")
            else:
                df = undo_stack.pop()

                if len(cleaning_report) > 0:
                    removed_action = cleaning_report.pop()
                    print(f"\nOperation undone: {removed_action}")
                else:
                    print("\nLast operation undone successfully.")

            pause()

        elif option == 8:
            clear_screen()

            confirm = input(
                "\nRestore the original dataset? "
                "All unsaved changes will be lost. (y/n): "
            ).strip().lower()

            if confirm == "y":
                df = pd.read_csv(INPUT_PATH)
                undo_stack.clear()
                cleaning_report.clear()
                print("\nOriginal dataset restored successfully.")
            else:
                print("\nOperation cancelled.")

            pause()

        elif option == 9:
            clear_screen()
            save_clean_dataset(df)
            pause()

        elif option == 0:
            clear_screen()
            print("Program closed.")
            break

        else:
            print("\nInvalid option. Choose a number from 0 to 9.")
            pause()


if __name__ == "__main__":
    try:
        dataframe = pd.read_csv(INPUT_PATH)
        cleaning(dataframe)

    except FileNotFoundError:
        print("Dataset not found.")
        print(f"Expected path:\n{INPUT_PATH}")

    except pd.errors.EmptyDataError:
        print("The dataset is empty.")

    except pd.errors.ParserError:
        print("The dataset could not be read. Check the CSV format.")