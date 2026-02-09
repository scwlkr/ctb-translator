# CTB to Excel Converter - Technical Documentation

## Overview
This tool converts AutoCAD Plot Style (`.ctb`) files into human-readable Excel (`.xlsx`) spreadsheets. It uses a robust, generalized approach to ensure 100% accuracy by reading the internal definition tables directly from the file rather than relying on standard lookup tables that may vary between environments.

## How It Works

### 1. Decompression
`.ctb` files are standard Zlib-compressed archives. The script first scans the binary file for the Zlib signature (`0x78`) and decompresses the content into raw text.

### 2. Table Parsing (The "Dynamic" Logic)
The most critical feature of this converter is its ability to handle custom lineweight definitions using a **Dynamic Lookup** strategy.

**The Problem:**
AutoCAD stores lineweights as an *index* (integer), not a value (mm). Standard mappings (e.g., Index 8 = 0.30mm) are not universal and can be overridden by the file itself.

**The Solution:**
The script searches the file for the `custom_lineweight_table` block.
```text
custom_lineweight_table{
 0=0.0
 1=0.05
 ...
 17=0.7
 ...
}
```
It builds a dictionary from this table: `{Index: Value_mm}`.

### 3. Color Definition Parsing
The script iterates through every color definition (indices 0-254 for Colors 1-255). It extracts properties like:
- `lineweight`: The raw index into the custom table.
- `screen`: The ink density (0-100).
- `linetype`, `end_style`, etc.

**New Logic Features:**
- **Plot Color Determination**:
  - Checks the internal `color` value.
  - `-1023410176`: Mapped to "Black".
  - `-1006632961` (and others): Mapped to "Color" (Use Object Color).
- **Smart Grouping ("Plots Same As")**:
  - Groups colors that have identical `Plot Color`, `Screen`, and `Line Weight` settings.
  - **Exclusion**: Colors with `Line Weight` set to "Specify" are excluded from these groups to prevent clutter.

### 4. Hex Color Generation
The script adds a `Screen Color` column corresponding to the AutoCAD Color Index (ACI).
- **Alignment**: Color 1 (Red) is correctly mapped to `#FF0000`.

## Output
The script generates an Excel file in the same directory as the input file, replacing the `.ctb` extension with `.xlsx`.
If the file already exists, it appends `-copy` or `-copy(n)` to avoid overwriting.

**Columns:**
1.  **Color**: The ACI Color Name (e.g., Color 1).
2.  **Screen Color**: Hex code (Cell background filled with color).
3.  **Plot Line**: Displays the Line Weight.
4.  **Plot Color**: "Black" or "Color".
5.  **Screen**: Screening percentage (0-100).
6.  **Line Weight**: Lineweight in mm or special value (e.g., Specify).
7.  **Plots Same As**: List of other colors sharing the same plot settings.

## Dependencies
- `python` (3.6+)
- `pandas`
- `xlsxwriter` (for Excel formatting)
- `zlib` (Built-in)
