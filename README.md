# CTB to Excel Converter

A robust tool to convert AutoCAD `.ctb` plot style files into a visually formatted Excel spreadsheet.

## Features
- **100% Accurate**: Reads internal lineweight tables directly from the file.
- **Visual Formatting**:
    - **Screen Color**: Cells are filled with the actual color hex code.
    - **Formatting**: Headers and borders are applied for readability.
- **Smart Logic**:
    - **Plot Color**: Automatically detects if a color plots as "Black" or uses the object's color.
    - **Plots Same As**: Groups colors that share identical plot settings, reducing redundancy. (Excludes "Specify" lineweights).
- **Safe Execution**: Never overwrites existing files. Automatically creates copies (e.g., `filename-copy.xlsx`).
- **CLI Support**: Supports dragging and dropping files or running via command line.

## Requirements
- Python 3.6+
- Libraries: `pandas`, `xlsxwriter`

To install dependencies:
```bash
pip install pandas xlsxwriter
```

## How to Use
### Method 1: Interactive
1.  Run the script:
    ```bash
    python ctb-translator.py
    ```
2.  Paste the full path to your `.ctb` file when prompted.
    - Example: `C:\Path\To\file.ctb`

### Method 2: Command Line / Drag & Drop
Pass the file path as an argument:
```bash
python ctb-translator.py "C:\Path\To\file.ctb"
```

## Output
The script generates an Excel file in the **same folder** as the input file.
- **Columns**: Color, Screen Color, Plot Line, Plot Color, Screen, Line Weight, Plots Same As.

## Troubleshooting
- **File Not Found**: Ensure the path is correct and surrounded by quotes if it contains spaces (the script handles quote removal automatically).
