# CTB Translator

A powerful tool to convert AutoCAD `.ctb` plot style files into human-readable reports.

## Web Application (New!)
This project now features a fully client-side **Web Application** that runs entirely in your browser using PyScript.

👉 **[Launch Web App](index.html)** (Run locally)

### Features
- **Drag & Drop**: Simply drop your `.ctb` file to parse.
- **Instant Preview**: See tables immediately without installing Python.
- **Print Ready**: Generates professional, clean reports via the "Print" button.
- **Privacy Focused**: Files are processed locally in your browser memory; nothing is uploaded to a server.

### Technical Documentation
For a deep dive into how the parsing works and how to build the project, see **[DOCUMENTATION.md](DOCUMENTATION.md)**.

---

## Legacy Python Script
The original command-line script is still available for batch processing or terminal usage.

### Features
- **Excel Export**: Generates formatted `.xlsx` files.
- **100% Accurate**: Reads internal lineweight tables.

### Usage
```bash
python ctb-translator.py "path/to/file.ctb"
```

## Requirements
- **Web App**: A modern web browser (Chrome, Edge, Firefox).
- **Legacy Script**: Python 3.6+ and `pandas`, `xlsxwriter`.
