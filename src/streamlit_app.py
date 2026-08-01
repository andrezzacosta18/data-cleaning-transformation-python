from pathlib import Path

import pandas as pd
import streamlit as st


# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "netflix_titles.csv"
ORIGINAL_PATH = PROJECT_ROOT / "data" / "raw" / "netflix_titles_original.csv"


# ==========================================================
# NAVIGATION — grouped by real workflow stage
# ==========================================================

CATEGORIES = {
    "Explore": ["Dataset information", "Consult catalog"],
    "Clean": [
        "Missing values",
        "Duplicate rows",
        "Standardize text",
        "Clean and convert",
    ],
    "Catalog": ["Add new movie", "Edit movie", "Remove movie"],
    "Wrap up": ["Cleaning report", "Save dataset"],
}


# ==========================================================
# PAGE CONFIGURATION & THEME
# ==========================================================

st.set_page_config(
    page_title="Netflix Data Cleaning System",
    page_icon="🎬",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    section[data-testid="stSidebar"] {
        background-color: #141414;
    }

    section[data-testid="stSidebar"] * {
        color: #F5F5F7 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #2A2A2A !important;
    }

    .brand {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.9rem;
        letter-spacing: 0.06em;
        color: #E50914 !important;
        margin: 0;
        line-height: 1.1;
    }

    .brand-sub {
        font-size: 0.78rem;
        color: #A3A3A3 !important;
        margin: 0 0 1.1rem 0;
    }

    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.5rem;
        letter-spacing: 0.02em;
        margin-bottom: 0.1rem;
    }

    .hero-sub {
        color: #6B6B6B;
        font-size: 0.95rem;
        margin-bottom: 1.3rem;
    }

    .stepper {
        display: flex;
        align-items: center;
        margin-bottom: 1.6rem;
    }

    .stepper .step {
        padding: 0.32rem 0.9rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #9A9AA0;
        background: #F0F0F2;
        white-space: nowrap;
    }

    .stepper .step.active {
        color: #FFFFFF;
        background: #E50914;
    }

    .stepper .divider {
        flex: 1;
        height: 1px;
        background: #E4E4E7;
        margin: 0 0.6rem;
        min-width: 12px;
    }

    div[data-testid="stMetric"] {
        background: #FAFAFA;
        border: 1px solid #ECECEE;
        border-radius: 12px;
        padding: 0.7rem 1rem 0.5rem 1rem;
    }

    section[data-testid="stSidebar"] div[data-testid="stMetric"] {
        background: #1F1F1F;
        border: 1px solid #2A2A2A;
    }

    section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: #1A1A1A;
        border: 1px solid #2A2A2A !important;
        border-radius: 12px;
    }

    section[data-testid="stSidebar"] button[kind="secondary"],
    section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
        background-color: #1F1F1F !important;
        border: 1px solid #2A2A2A !important;
        color: #F5F5F7 !important;
    }

    section[data-testid="stSidebar"] button[kind="secondary"]:hover,
    section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {
        border-color: #E50914 !important;
        color: #E50914 !important;
    }

    section[data-testid="stSidebar"] button[kind="secondary"]:disabled,
    section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:disabled {
        color: #5A5A5A !important;
        border-color: #232323 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# SESSION STATE
# ==========================================================

def load_dataset(path):
    return pd.read_csv(path)


if "df" not in st.session_state:

    try:
        st.session_state.df = load_dataset(RAW_PATH)

    except FileNotFoundError:
        st.error(
            f"Couldn't find the dataset at:\n{RAW_PATH}\n\n"
            "Check the file exists at that path, then reload the page."
        )
        st.stop()


if "original_df" not in st.session_state:

    if ORIGINAL_PATH.exists():
        st.session_state.original_df = load_dataset(ORIGINAL_PATH)

    else:
        st.session_state.original_df = st.session_state.df.copy()


if "history" not in st.session_state:
    st.session_state.history = []

if "cleaning_report" not in st.session_state:
    st.session_state.cleaning_report = []

if "confirm_restore" not in st.session_state:
    st.session_state.confirm_restore = False


def save_backup():
    st.session_state.history.append(st.session_state.df.copy())


def add_report(message):
    st.session_state.cleaning_report.append(message)


def flash(message, kind="success"):
    st.session_state["_flash"] = (kind, message)


def undo_last_operation():

    if len(st.session_state.history) == 0:
        flash("There is no operation to undo.", "warning")
        return

    st.session_state.df = st.session_state.history.pop()

    if len(st.session_state.cleaning_report) > 0:
        st.session_state.cleaning_report.pop()

    flash("Last operation undone.")


def restore_original_dataset():

    st.session_state.df = st.session_state.original_df.copy()
    st.session_state.history.clear()
    st.session_state.cleaning_report.clear()

    flash("Original dataset restored.")


df = st.session_state.df


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown(
    '<p class="brand">🎬 DATA STUDIO</p>'
    '<p class="brand-sub">Netflix cleaning &amp; catalog toolkit</p>',
    unsafe_allow_html=True,
)

category = st.sidebar.radio(
    "Section",
    list(CATEGORIES.keys()),
)

page = st.sidebar.radio(
    "Page",
    CATEGORIES[category],
    label_visibility="collapsed",
)

st.sidebar.divider()

with st.sidebar.container(border=True):

    st.markdown(
        f"**{df.shape[0]:,}** rows &nbsp;·&nbsp; "
        f"**{df.shape[1]}** cols &nbsp;·&nbsp; "
        f"**{int(df.isnull().sum().sum()):,}** missing",
        unsafe_allow_html=True,
    )

if st.session_state.history:
    st.sidebar.caption(
        f"{len(st.session_state.history)} change(s) can be undone."
    )
else:
    st.sidebar.caption("No changes yet this session.")

if st.sidebar.button(
    "↩ Undo last operation",
    use_container_width=True,
    disabled=len(st.session_state.history) == 0,
):
    undo_last_operation()
    st.rerun()

if st.session_state.confirm_restore:

    st.sidebar.warning("This discards every change made this session.")

    confirm_col1, confirm_col2 = st.sidebar.columns(2)

    if confirm_col1.button(
        "Yes, restore",
        use_container_width=True,
        type="primary",
    ):
        restore_original_dataset()
        st.session_state.confirm_restore = False
        st.rerun()

    if confirm_col2.button("Cancel", use_container_width=True):
        st.session_state.confirm_restore = False
        st.rerun()

else:

    if st.sidebar.button(
        "🔄 Restore original dataset",
        use_container_width=True,
    ):
        st.session_state.confirm_restore = True
        st.rerun()


# ==========================================================
# HEADER — stepper + flash message
# ==========================================================

order = list(CATEGORIES.keys())
current_index = order.index(category)

steps_html = '<div class="stepper">'

for index, step_name in enumerate(order):

    step_class = "step active" if index == current_index else "step"
    steps_html += f'<div class="{step_class}">{index + 1}. {step_name}</div>'

    if index < len(order) - 1:
        steps_html += '<div class="divider"></div>'

steps_html += "</div>"

st.markdown(steps_html, unsafe_allow_html=True)

st.markdown(
    '<p class="hero-title">🎬 Netflix Data Cleaning &amp; Catalog Studio</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="hero-sub">Review the dataset, choose an operation, '
    "and apply only the changes you consider necessary.</p>",
    unsafe_allow_html=True,
)

flash_data = st.session_state.pop("_flash", None)

if flash_data:
    flash_kind, flash_message = flash_data
    getattr(st, flash_kind)(flash_message)


# ==========================================================
# DATASET INFORMATION
# ==========================================================

if page == "Dataset information":

    st.header("Dataset information")

    with st.container(border=True):

        column1, column2, column3 = st.columns(3)
        column1.metric("Rows", df.shape[0])
        column2.metric("Columns", df.shape[1])
        column3.metric("Missing values", int(df.isnull().sum().sum()))

    st.subheader("Column summary")

    column_summary = pd.DataFrame({
        "Column": df.columns,
        "Data type": [str(data_type) for data_type in df.dtypes],
        "Missing values": df.isnull().sum().values,
        "Unique values": df.nunique().values,
    })

    st.dataframe(column_summary, use_container_width=True, hide_index=True)

    st.subheader("Dataset preview")

    st.dataframe(df.head(20), use_container_width=True)


# ==========================================================
# MISSING VALUES
# ==========================================================

elif page == "Missing values":

    st.header("Missing values")

    missing_summary = pd.DataFrame({
        "Column": df.columns,
        "Missing values": df.isnull().sum().values,
        "Missing percentage (%)": (
            df.isnull().mean().values * 100
        ).round(2),
    })

    missing_summary = missing_summary[
        missing_summary["Missing values"] > 0
    ]

    if missing_summary.empty:

        st.success("There are no missing values in the dataset.")

    else:

        try:
            styled_summary = missing_summary.style.background_gradient(
                subset=["Missing percentage (%)"],
                cmap="Reds",
            )
            st.dataframe(
                styled_summary,
                use_container_width=True,
                hide_index=True,
            )

        except ImportError:
            st.dataframe(
                missing_summary,
                use_container_width=True,
                hide_index=True,
            )

        selected_column = st.selectbox(
            "Choose a column",
            missing_summary["Column"].tolist(),
        )

        missing_count = int(df[selected_column].isnull().sum())
        missing_percentage = df[selected_column].isnull().mean() * 100

        st.info(
            f"The column '{selected_column}' has {missing_count} "
            f"missing values ({missing_percentage:.2f}%)."
        )

        if pd.api.types.is_numeric_dtype(df[selected_column]):

            actions = [
                "Leave as it is",
                "Remove rows",
                "Fill with a fixed value",
                "Fill with the mean",
                "Fill with the median",
            ]

        else:

            actions = [
                "Leave as it is",
                "Remove rows",
                "Fill with a fixed value",
            ]

        action = st.selectbox("Choose an action", actions)

        if action == "Remove rows":

            st.warning(f"{missing_count} rows will be removed.")

            if st.button("Remove rows", type="primary"):

                save_backup()

                st.session_state.df = df.dropna(
                    subset=[selected_column]
                )

                add_report(
                    f"Removed rows with missing values "
                    f"from '{selected_column}'."
                )
                flash("Rows removed.")
                st.rerun()

        elif action == "Fill with a fixed value":

            fixed_value = st.text_input("Enter the value to use")

            if st.button("Fill missing values", type="primary"):

                if fixed_value == "":

                    st.warning(
                        "Enter a value before applying the operation."
                    )

                elif pd.api.types.is_numeric_dtype(df[selected_column]):

                    try:
                        cast_value = (
                            float(fixed_value)
                            if "." in fixed_value
                            else int(fixed_value)
                        )

                    except ValueError:
                        st.error(
                            "That value doesn't match the column's "
                            "numeric type. Enter a number instead."
                        )
                        st.stop()

                    save_backup()

                    st.session_state.df.loc[:, selected_column] = (
                        df[selected_column].fillna(cast_value)
                    )

                    add_report(
                        f"Filled missing values in '{selected_column}' "
                        f"with '{cast_value}'."
                    )
                    flash("Missing values filled.")
                    st.rerun()

                else:

                    save_backup()

                    st.session_state.df.loc[:, selected_column] = (
                        df[selected_column].fillna(fixed_value)
                    )

                    add_report(
                        f"Filled missing values in '{selected_column}' "
                        f"with '{fixed_value}'."
                    )
                    flash("Missing values filled.")
                    st.rerun()

        elif action == "Fill with the mean":

            mean_value = df[selected_column].mean()
            st.write(f"Mean: {mean_value:.2f}")

            if st.button("Fill with mean", type="primary"):

                save_backup()

                st.session_state.df.loc[:, selected_column] = (
                    df[selected_column].fillna(mean_value)
                )

                add_report(
                    f"Filled missing values in '{selected_column}' "
                    "using the mean."
                )
                flash("Missing values filled with the mean.")
                st.rerun()

        elif action == "Fill with the median":

            median_value = df[selected_column].median()
            st.write(f"Median: {median_value:.2f}")

            if st.button("Fill with median", type="primary"):

                save_backup()

                st.session_state.df.loc[:, selected_column] = (
                    df[selected_column].fillna(median_value)
                )

                add_report(
                    f"Filled missing values in '{selected_column}' "
                    "using the median."
                )
                flash("Missing values filled with the median.")
                st.rerun()


# ==========================================================
# DUPLICATE ROWS
# ==========================================================

elif page == "Duplicate rows":

    st.header("Duplicate rows")

    duplicated_rows = int(df.duplicated().sum())

    with st.container(border=True):
        st.metric("Duplicate rows", duplicated_rows)

    if duplicated_rows == 0:

        st.success("There are no duplicate rows in the dataset.")

    else:

        duplicate_data = df[df.duplicated(keep=False)]
        st.dataframe(duplicate_data, use_container_width=True)

        if st.button("Remove duplicate rows", type="primary"):

            save_backup()
            st.session_state.df = df.drop_duplicates()
            add_report("Removed duplicate rows.")
            flash("Duplicate rows removed.")
            st.rerun()


# ==========================================================
# STANDARDIZE TEXT
# ==========================================================

elif page == "Standardize text":

    st.header("Standardize text columns")

    text_columns = list(
        df.select_dtypes(include=["object", "string"]).columns
    )

    if len(text_columns) == 0:

        st.warning("There are no text columns in the dataset.")

    else:

        selected_column = st.selectbox("Choose a text column", text_columns)

        st.subheader("Column preview")

        preview = df[selected_column].value_counts(dropna=False).head(15)
        st.dataframe(preview.rename("Count"), use_container_width=True)

        action = st.selectbox(
            "Choose a standardization",
            [
                "Convert to UPPERCASE",
                "Convert to lowercase",
                "Remove leading and trailing spaces",
                "Remove extra spaces between words",
                "Replace text",
            ],
        )

        if action == "Convert to UPPERCASE":

            if st.button("Apply uppercase", type="primary"):

                save_backup()
                st.session_state.df.loc[:, selected_column] = (
                    df[selected_column].str.upper()
                )
                add_report(f"Converted '{selected_column}' to uppercase.")
                flash("Column converted to uppercase.")
                st.rerun()

        elif action == "Convert to lowercase":

            if st.button("Apply lowercase", type="primary"):

                save_backup()
                st.session_state.df.loc[:, selected_column] = (
                    df[selected_column].str.lower()
                )
                add_report(f"Converted '{selected_column}' to lowercase.")
                flash("Column converted to lowercase.")
                st.rerun()

        elif action == "Remove leading and trailing spaces":

            if st.button("Remove spaces", type="primary"):

                save_backup()
                st.session_state.df.loc[:, selected_column] = (
                    df[selected_column].str.strip()
                )
                add_report(
                    f"Removed leading and trailing spaces "
                    f"from '{selected_column}'."
                )
                flash("Spaces removed.")
                st.rerun()

        elif action == "Remove extra spaces between words":

            if st.button("Remove extra spaces", type="primary"):

                save_backup()
                st.session_state.df.loc[:, selected_column] = (
                    df[selected_column]
                    .str.replace(r"\s+", " ", regex=True)
                    .str.strip()
                )
                add_report(
                    f"Removed extra spaces from '{selected_column}'."
                )
                flash("Extra spaces removed.")
                st.rerun()

        elif action == "Replace text":

            old_text = st.text_input("Text to replace")
            new_text = st.text_input("Replace with")

            if st.button("Replace text", type="primary"):

                if old_text == "":

                    st.warning("Enter the text you want to replace.")

                else:

                    save_backup()
                    st.session_state.df.loc[:, selected_column] = (
                        df[selected_column].str.replace(
                            old_text, new_text, regex=False
                        )
                    )
                    add_report(
                        f"Replaced '{old_text}' with '{new_text}' "
                        f"in '{selected_column}'."
                    )
                    flash("Text replaced.")
                    st.rerun()


# ==========================================================
# CLEAN AND CONVERT
# ==========================================================

elif page == "Clean and convert":

    st.header("Clean and convert columns")

    selected_column = st.selectbox("Choose a column", df.columns.tolist())

    with st.container(border=True):

        column1, column2, column3 = st.columns(3)
        column1.metric("Data type", str(df[selected_column].dtype))
        column2.metric(
            "Missing values", int(df[selected_column].isnull().sum())
        )
        column3.metric("Unique values", int(df[selected_column].nunique()))

    st.subheader("Sample values")

    st.dataframe(
        df[[selected_column]].dropna().head(15),
        use_container_width=True,
    )

    action = st.selectbox(
        "Choose an operation",
        [
            "Extract numbers from text",
            "Convert column to integer",
            "Convert column to float",
        ],
    )

    if action == "Extract numbers from text":

        if not pd.api.types.is_string_dtype(df[selected_column]):

            st.warning(
                "The selected column is already numeric "
                "or is not a text column."
            )

        elif st.button("Extract numbers", type="primary"):

            save_backup()
            st.session_state.df.loc[:, selected_column] = (
                df[selected_column].str.extract(
                    r"(\d+(?:\.\d+)?)", expand=False
                )
            )
            add_report(f"Extracted numbers from '{selected_column}'.")
            flash("Numbers extracted.")
            st.rerun()

    elif action == "Convert column to integer":

        if st.button("Convert to integer", type="primary"):

            numeric_values = pd.to_numeric(
                df[selected_column], errors="coerce"
            )

            invalid_count = int(
                numeric_values.isnull().sum()
                - df[selected_column].isnull().sum()
            )

            if invalid_count > 0:

                st.error(
                    f"{invalid_count} values couldn't be converted. "
                    "Clean the column first."
                )

            elif numeric_values.isnull().any():

                st.error(
                    "The column still has missing values. "
                    "Handle them before converting to integer."
                )

            else:

                save_backup()
                st.session_state.df.loc[:, selected_column] = (
                    numeric_values.astype("int64")
                )
                add_report(f"Converted '{selected_column}' to integer.")
                flash("Column converted to integer.")
                st.rerun()

    elif action == "Convert column to float":

        if st.button("Convert to float", type="primary"):

            numeric_values = pd.to_numeric(
                df[selected_column], errors="coerce"
            )

            invalid_count = int(
                numeric_values.isnull().sum()
                - df[selected_column].isnull().sum()
            )

            if invalid_count > 0:
                st.warning(
                    f"{invalid_count} values couldn't be converted "
                    "and will become missing values."
                )

            save_backup()
            st.session_state.df.loc[:, selected_column] = (
                numeric_values.astype("float64")
            )
            add_report(f"Converted '{selected_column}' to float.")
            flash("Column converted to float.")
            st.rerun()


# ==========================================================
# CONSULT CATALOG
# ==========================================================

elif page == "Consult catalog":

    st.header("Consult catalog")

    consultation = st.radio(
        "Choose a consultation",
        [
            "Search movie",
            "Consult index",
            "Consult index and column",
            "Show full catalog",
        ],
        horizontal=True,
    )

    if consultation == "Search movie":

        movie_name = st.text_input("Enter the movie name")

        if movie_name:

            result = df[
                df["title"].str.contains(movie_name, case=False, na=False)
            ]

            if result.empty:
                st.warning("Movie not found.")

            else:
                st.success(f"Movies found: {result.shape[0]}")
                st.dataframe(result, use_container_width=True)

    elif consultation == "Consult index":

        row_index = st.number_input(
            "Enter the index number", min_value=0, step=1
        )

        if st.button("Consult index"):

            if row_index in df.index:
                st.dataframe(df.loc[[row_index]], use_container_width=True)

            else:
                st.warning("Index not found.")

    elif consultation == "Consult index and column":

        row_index = st.number_input(
            "Enter the row index", min_value=0, step=1
        )
        selected_column = st.selectbox(
            "Choose a column", df.columns.tolist()
        )

        if st.button("Consult value"):

            if row_index not in df.index:
                st.warning("Index not found.")

            else:

                result = pd.DataFrame({
                    "ROW": [row_index],
                    "COLUMN": [selected_column],
                    "VALUE": [df.loc[row_index, selected_column]],
                })
                st.dataframe(
                    result, use_container_width=True, hide_index=True
                )

    elif consultation == "Show full catalog":

        st.write(f"Full table: {df.shape[0]} rows x {df.shape[1]} columns")
        st.dataframe(df, use_container_width=True)


# ==========================================================
# ADD NEW MOVIE
# ==========================================================

elif page == "Add new movie":

    st.header("Add new movie")

    new_row = {}

    with st.form("add_movie_form"):

        for column in df.columns:

            if column == "release_year":

                new_row[column] = st.number_input(
                    column, min_value=1900, max_value=2100, step=1
                )

            else:

                new_row[column] = st.text_input(column)

        submitted = st.form_submit_button("Add movie", type="primary")

    if submitted:

        if not str(new_row.get("title", "")).strip():

            st.warning("Enter a title before adding the movie.")

        else:

            save_backup()

            new_index = len(df)
            st.session_state.df.loc[new_index] = new_row

            title = new_row.get("title", f"row {new_index}")
            add_report(f"Added new movie: '{title}'.")
            flash(f"'{title}' added to the catalog.")
            st.rerun()


# ==========================================================
# EDIT MOVIE
# ==========================================================

elif page == "Edit movie":

    st.header("Edit movie")

    row_index = st.number_input("Index", min_value=0, step=1)
    selected_column = st.selectbox("Choose a column", df.columns.tolist())

    if row_index in df.index:

        current_value = df.loc[row_index, selected_column]
        st.write(f"Current value: {current_value}")

        new_value = st.text_input("Enter the new value")

        if st.button("Update value", type="primary"):

            save_backup()
            st.session_state.df.loc[row_index, selected_column] = new_value
            add_report(
                f"Edited row {row_index}, column '{selected_column}'."
            )
            flash("Value updated.")
            st.rerun()

    else:
        st.warning("Index not found.")


# ==========================================================
# REMOVE MOVIE
# ==========================================================

elif page == "Remove movie":

    st.header("Remove movie")

    row_index = st.number_input("Row to remove", min_value=0, step=1)

    if row_index in df.index:

        st.dataframe(df.loc[[row_index]], use_container_width=True)

        confirm_removal = st.checkbox(
            f"I confirm I want to remove row {row_index}"
        )

        if st.button("Remove movie", type="primary", disabled=not confirm_removal):

            save_backup()
            st.session_state.df = df.drop(row_index).reset_index(drop=True)
            add_report(f"Removed row {row_index}.")
            flash("Row removed.")
            st.rerun()

    else:
        st.warning("Index not found.")


# ==========================================================
# CLEANING REPORT
# ==========================================================

elif page == "Cleaning report":

    st.header("Cleaning report")

    if len(st.session_state.cleaning_report) == 0:

        st.info("No cleaning actions have been performed yet.")

    else:

        report_df = pd.DataFrame({
            "Step": range(1, len(st.session_state.cleaning_report) + 1),
            "Action": st.session_state.cleaning_report,
        })

        st.dataframe(report_df, use_container_width=True, hide_index=True)

        report_text = "\n".join(
            f"{index} - {action}"
            for index, action in enumerate(
                st.session_state.cleaning_report, start=1
            )
        )

        st.download_button(
            label="Download cleaning report",
            data=report_text,
            file_name="cleaning_report.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ==========================================================
# SAVE DATASET
# ==========================================================

elif page == "Save dataset":

    st.header("Save cleaned dataset")

    st.write(
        "Download the current version of the dataset "
        "with all changes applied."
    )

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download cleaned dataset",
        data=csv_data,
        file_name="netflix_titles_cleaned.csv",
        mime="text/csv",
        use_container_width=True,
        type="primary",
    )

    st.subheader("Current dataset preview")

    st.dataframe(df.head(20), use_container_width=True)