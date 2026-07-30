from pathlib import Path

PROJECT_NAME = "data-cleaning-project"

folders = [
    "data/raw",
    "data/processed",
    "notebooks",
    "src",
    "reports/figures",
    "tests"
]


files = [
    "README.md",
    "requirements.txt",
    ".gitignore",
    "src/main.py",
    "src/data_loader.py",
    "src/cleaning.py",
    "src/excel_manager.py",
    "src/reports.py",
    "src/utils.py",
    "reports/cleaning_report.txt",
    "notebooks/01_data_quality_analysis.ipynb"
]


project_path = Path(PROJECT_NAME)

project_path.mkdir(exist_ok=True)

# Criar pastas
for folder in folders:
    (project_path / folder).mkdir(parents=True, exist_ok=True)

# Criar arquivos vazios
for file in files:
    (project_path / file).touch(exist_ok=True)

print("=" * 50)
print("✅ Estrutura do projeto criada com sucesso!")
print("=" * 50)
print(f"Projeto criado em:\n{project_path.resolve()}")