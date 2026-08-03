# 🎬 Netflix Data Cleaning and Management System

> Python project for exploring, cleaning, transforming, visualising, and managing the Netflix Titles dataset through a terminal application and a Streamlit web interface.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualisation-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20Application-FF4B4B?logo=streamlit)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel%20Files-217346)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)

---

## 📖 Overview

This project was developed as part of the **Data Analyst Programme** at **CESAE Digital**.

It uses the Netflix Titles dataset to demonstrate fundamental Python concepts and data-analysis operations, including functions, conditions, loops, lists, dictionaries, file handling, Pandas DataFrames, charts, and interactive menus.

The project provides two ways to work with the data:

- A **terminal application** built with Python.
- A **web interface** built with Streamlit.

The cleaning process is user-controlled. The application analyses the data and presents available actions, but the user decides which changes should be applied.

---

## 🎯 Objectives

- Explore and understand the Netflix Titles dataset.
- Inspect columns, data types, and dataset dimensions.
- Detect and handle missing values.
- Detect and remove duplicate rows.
- Standardise text values.
- Extract numbers and convert column types.
- Search and browse the Netflix catalogue.
- Create histograms and boxplots for numeric columns.
- Add, edit, and remove catalogue records.
- Preserve `show_id` as a unique identifier.
- Keep a history of changes and allow the last operation to be undone.
- Restore the original dataset.
- Generate a cleaning report.
- Export the cleaned dataset to CSV and Excel.
- Provide the same main operations through a Streamlit interface.

---

## 🏗️ Project Structure

```text
project_Andreza_Ilana_Bruno/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── raw/
│   │   ├── netflix_titles.csv
│   │   ├── netflix_titles.xlsx
│   │   ├── netflix_titles_original.csv
│   │   └── netflix_titles_original.xlsx
│   │
│   └── processed/
│       ├── netflix_template.xlsx
│       ├── netflix_titles_cleaned.csv
│       └── cleaning_report.txt          # Generated when the report is saved
│
├── notebook/
│   ├── netflix_notebook_.ipynb
│   └── streamlit_notebook_apenas_streamlit.ipynb
│
└── src/
    ├── netflix.py
    └── netflix_streamlit_app.py
```

---

## 🚀 Project Workflow

```text
Raw Netflix Dataset
         │
         ▼
Data Exploration and Quality Assessment
         │
         ▼
User-selected Cleaning and Transformation
         │
         ▼
Catalogue Management
         │
         ▼
Cleaning Report and Processed Dataset
         │
         ├──────────────► Terminal Interface
         │
         └──────────────► Streamlit Web Interface
```

---

## 🔍 Module 1 — Data Exploration and Quality Assessment

This module focuses on understanding the dataset before applying changes.

### Main activities

- Load the Netflix dataset.
- Show the number of rows and columns.
- Inspect column names and data types.
- Count missing values by column.
- Count unique values.
- Detect completely duplicated rows.
- Browse the full catalogue.
- Search titles without case sensitivity.
- Inspect a row by index.
- Inspect a value by row and column.
- Identify numeric columns.
- Generate a histogram or boxplot.

The analysis is also documented in:

```text
notebook/netflix_notebook_.ipynb
```

---

## 🧹 Module 2 — Data Cleaning and Transformation

This module improves data consistency through operations selected by the user.

### Missing values

- Show columns containing missing values.
- Show the number and percentage of missing values.
- Display examples of existing and missing records.
- Remove rows with missing values.
- Fill missing values with a fixed value.
- Fill numeric values with the mean or median.

### Duplicate rows

- Count completely duplicated rows.
- Display all repeated rows.
- Remove duplicates after user confirmation.

### Text standardisation

- Convert text to uppercase.
- Convert text to lowercase.
- Remove leading and trailing spaces.
- Remove repeated spaces between words.
- Replace selected text.

### Cleaning and conversion

- Extract numbers from text.
- Convert a column to integer.
- Convert a column to decimal.
- Identify values that cannot be converted.

---

## 📑 Module 3 — Catalogue and Excel Management

The terminal and Streamlit applications allow the user to manage individual records.

### Main features

- Add a new title.
- Require `show_id` and `title` when adding records.
- Prevent duplicated `show_id` values.
- Edit an existing value by row and column.
- Prevent an edited `show_id` from duplicating another record.
- Remove a record after confirmation.
- Create an empty Excel fill-in template.
- Validate the template columns before importing.
- Reject empty or duplicated `show_id` values during import.
- Import completed template rows into the current dataset.

---

## ↩️ History, Restore, and Report

Before modifying the DataFrame, the program stores a copy in `history`. This allows the last operation to be undone during the current session.

The project also keeps:

- `original_df` — original data used by the restore operation.
- `cleaning_report` — descriptions of completed operations.
- `has_unsaved_changes` — indicates whether the current data still needs to be saved.

The cleaning report can be saved to:

```text
data/processed/cleaning_report.txt
```

The report contains the operations performed and the final number of rows and columns.

---

## 💾 Generated Files

When the user saves the dataset, the application generates or updates:

```text
data/processed/netflix_titles_cleaned.csv
data/raw/netflix_titles.xlsx
```

The original files are preserved separately and can be used to restore the dataset.

---

## 🌐 Streamlit Web Application

The Streamlit application provides a visual interface for the project.

### Interface features

- Sidebar navigation.
- Custom Netflix-inspired HTML and CSS.
- Session data stored with `st.session_state`.
- Dataset metrics and interactive DataFrames.
- Missing-value and duplicate analysis.
- Text cleaning and column conversion controls.
- Catalogue search, addition, editing, and removal.
- Undo and restore buttons.
- Success, warning, information, and error messages.
- Cleaning report display and download.
- Dataset saving inside the project.
- CSV download through the browser.
- Side-by-side comparison of original and current datasets.

The Streamlit-specific components are documented in:

```text
notebook/streamlit_notebook_apenas_streamlit.ipynb
```

---

## 🛠️ Technologies

- Python 3.13
- Pandas
- Matplotlib
- Streamlit
- OpenPyXL
- Tabulate
- Jupyter Notebook
- Git and GitHub

---

## 💻 Installation

Clone the repository:

```bash
git clone <repository-url>
```

Enter the project directory:

```bash
cd project_Andreza_Ilana_Bruno
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment.

### macOS or Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

Run all commands from the project root.

### Terminal application

```bash
python3 src/netflix.py
```

The main menu contains:

1. Explore
2. Cleaning and Processing
3. Catalogue Management
4. Finalization
5. Utilities

### Streamlit application

```bash
streamlit run src/netflix_streamlit_app.py
```

Streamlit normally opens the application at:

```text
http://localhost:8501
```

### Notebooks

Open the following files in Jupyter Notebook or VS Code and select a Python kernel:

```text
notebook/netflix_notebook_.ipynb
notebook/streamlit_notebook_apenas_streamlit.ipynb
```

Run the notebook cells from top to bottom or use **Run All**.

---

## 📈 Expected Outputs

- Dataset quality summary.
- Missing-value analysis.
- Duplicate-row analysis.
- Histogram and boxplot.
- Cleaned Netflix dataset.
- Updated Excel dataset.
- Cleaning report in TXT format.
- Excel fill-in template.
- Interactive terminal application.
- Interactive Streamlit web application.

---

## 👥 Team

| Name | GitHub | Role |
|:---|:---|:---|
| Andreza Silva | — | Data Analyst |
| Ilana Freire | [@ilanafreire](https://github.com/ilanafreire) | Data Analyst |
| Bruno Moller | [@brunomoller](https://github.com/brunomoller) | Data Analyst |

---

## 📚 Skills Demonstrated

- Fundamental Python programming.
- Functions, parameters, conditions, and loops.
- Lists and dictionaries.
- File and path management.
- Pandas DataFrames.
- Data quality assessment.
- Data cleaning and transformation.
- Excel file management.
- Data visualisation.
- Streamlit interface development.
- Technical documentation.
- Version control with Git and GitHub.

---

## ⚠️ Project Notes

- Cleaning is not automatic; the user chooses and confirms each operation.
- Undo history exists only during the current application session.
- Unsaved changes may be lost when the program is closed.
- Saving a new TXT report replaces the previous `cleaning_report.txt`.
- The project detects structural issues, but column-specific semantic validation can be expanded in future versions.

---

## 📄 License

This repository was developed exclusively for educational purposes as part of the **Data Analyst Programme at CESAE Digital**.

---

## 📬 Contact

For questions or suggestions, contact the project contributors through GitHub.
