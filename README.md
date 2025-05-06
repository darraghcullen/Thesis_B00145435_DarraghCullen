# FileChecker

**FileChecker** is a CLI-based Android integrity and tamper detection tool built for digital forensic investigations. It automates snapshot extraction from Android devices over ADB, compares forensically hashed files, and generates structured forensic reports.

---

## 🔍 Features

- 📱 ADB-based file extraction from Android devices
- 🧮 SHA-256 hash snapshot generation with metadata
- 🔎 Tamper detection: new, deleted, modified, metadata-changed files
- 📑 Generates detailed `.csv` and `.txt` forensic reports
- 🧰 Modular Python CLI architecture
- 🧾 Forensic chain-of-custody integrity built-in

---

## 🚀 Installation

```bash
git clone https://github.com/darraghcullen/file_checker.git
cd file_checker
pip install -r requirements.txt
