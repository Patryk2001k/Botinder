import os
import re
import tokenize
import io
import shutil
import datetime

# ==========================================
# KONFIGURACJA SKRYPTU
# ==========================================
TWORZ_KOPIE_ZAPASOWA = True

# Potężna lista ignorowanych folderów dla wielu ekosystemów IT
IGNORED_DIRS = {
    # Systemowe i kopie zapasowe skryptu
    "COPY",
    ".git",
    # Konfiguracje środowisk programistycznych (IDE)
    ".vscode",
    ".idea",
    ".vs",
    # Ecosytem Python
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".tox",
    # Ecosytem Frontend (Node.js, React, Angular, Vue, Next.js)
    "node_modules",
    "dist",
    "build",
    "out",
    ".next",
    ".nuxt",
    ".angular",
    "coverage",
    # Ecosytem Java (Maven, Gradle)
    "target",
    ".gradle",
    # Ecosytem C / C++
    "bin",
    "obj",
}


def zrob_pelen_backup(target_dir):
    """Tworzy pełną kopię zapasową całego katalogu przed rozpoczęciem czyszczenia."""
    if not TWORZ_KOPIE_ZAPASOWA:
        return

    # Generujemy unikalną nazwę dla folderu backupu (data + czas)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nazwa_celu = os.path.basename(os.path.normpath(target_dir))
    if not nazwa_celu:
        nazwa_celu = "projekt"

    backup_dir = os.path.join(target_dir, "COPY", f"backup_{nazwa_celu}_{timestamp}")

    print(f"📦 Tworzenie pełnej kopii zapasowej źródłowych plików...")

    # Funkcja copytree zignoruje wszystko co jest w IGNORED_DIRS (w tym sam folder COPY),
    # więc nie skopiujemy gigabajtów bibliotek, a jedynie czysty kod.
    shutil.copytree(
        target_dir, backup_dir, ignore=shutil.ignore_patterns(*IGNORED_DIRS)
    )

    print(f"✅ Zapisano pełną kopię w: {backup_dir}\n")


# ==========================================
# SILNIKI CZYSZCZĄCE DLA RÓŻNYCH JĘZYKÓW
# ==========================================


def clean_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Krok 1: Usunięcie Docstringów (""" komentarz """) wiszących w powietrzu
    docstring_pattern = r'(?m)^[ \t]*("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')[ \t]*\n?'
    code = re.sub(docstring_pattern, "", code)

    # Krok 2: Usunięcie klasycznych komentarzy '#'
    hash_pattern = r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(#.*)'

    def replace_hash(match):
        if match.group(2):
            return ""
        return match.group(0)

    clean_code = re.sub(hash_pattern, replace_hash, code)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(clean_code)


def clean_c_style_file(file_path):
    """Czyści: JS, TS, JSX, TSX, Java, C, C++, CS, CSS, SCSS"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    pattern = r'("(?:\\.|[^"\\])*")|(\'(?:\\.|[^\'\\])*\')|(`(?:\\.|[^`\\])*`)|(/\*[\s\S]*?\*/|//.*)'

    def replace_logic(match):
        if match.group(4):
            return ""
        return match.group(0)

    clean_code = re.sub(pattern, replace_logic, code)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(clean_code)


def clean_lua_file(file_path):
    """Czyści: Lua, GLua"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    pattern = r'("(?:\\.|[^"\\])*")|(\'(?:\\.|[^\'\\])*\')|(--\[\[[\s\S]*?\]\]|--.*)'

    def replace_logic(match):
        if match.group(3):
            return ""
        return match.group(0)

    clean_code = re.sub(pattern, replace_logic, code)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(clean_code)


def clean_html_file(file_path):
    """Czyści: HTML, HTM"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    pattern = r""
    clean_code = re.sub(pattern, "", code)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(clean_code)


# MAPOWANIE ROZSZERZEŃ NA SILNIKI CZYSZCZĄCE
EXTENSION_MAP = {
    # Backend
    ".py": clean_python_file,
    ".java": clean_c_style_file,
    ".c": clean_c_style_file,
    ".cpp": clean_c_style_file,
    ".h": clean_c_style_file,
    ".hpp": clean_c_style_file,
    ".cs": clean_c_style_file,
    ".lua": clean_lua_file,
    # Frontend
    ".js": clean_c_style_file,
    ".ts": clean_c_style_file,
    ".jsx": clean_c_style_file,
    ".tsx": clean_c_style_file,
    ".css": clean_c_style_file,
    ".scss": clean_c_style_file,
    ".html": clean_html_file,
    ".htm": clean_html_file,
}

# ==========================================
# GŁÓWNA LOGIKA SKANOWANIA
# ==========================================


def process_project(target_dir):
    print(f"\nRozpoczynam skanowanie katalogu: {target_dir}")

    # Tworzymy JEDNĄ pełną kopię przed wejściem w pętlę modyfikującą pliki
    zrob_pelen_backup(target_dir)

    counter = 0
    for root, dirs, files in os.walk(target_dir):
        # Usuwamy ignorowane foldery z listy przeszukiwań (żeby w nie nie wchodzić)
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            # Skrypt blokuje modyfikację samego siebie
            if file == os.path.basename(__file__):
                continue

            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            if ext in EXTENSION_MAP:
                EXTENSION_MAP[ext](file_path)
                counter += 1

    print(f"==================================================")
    print(f"✅ Operacja zakończona sukcesem. Wyczyszczono plików: {counter}")
    print(f"==================================================")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    print("--- UNIWERSALNY STRIPPER KOMENTARZY (MULTI-LANGUAGE) ---")
    print("1 - Wyczyść WSZYSTKO w obecnym folderze i podfolderach")
    print("2 - Wyczyść tylko wewnątrz konkretnego podfolderu")

    wybor = input("\nWybierz tryb (1 lub 2): ").strip()

    if wybor == "1":
        process_project(current_dir)
    elif wybor == "2":
        folder_name = input("Podaj nazwę folderu (np. frontend): ").strip()
        target_path = (
            os.path.join(current_dir, folder_name)
            if not os.path.isabs(folder_name)
            else folder_name
        )

        if os.path.exists(target_path) and os.path.isdir(target_path):
            process_project(target_path)
        else:
            print(
                f"❌ Błąd: Nie znaleziono folderu '{folder_name}' w lokalizacji {current_dir}"
            )
    else:
        print("❌ Błąd: Nieprawidłowy wybór.")
