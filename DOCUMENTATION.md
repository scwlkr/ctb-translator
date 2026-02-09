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

**Mapping Logic (Crucial):**
The internal raw lineweight index in the Color Definition is **1-based** relative to the **0-based** Custom Table.
- **Formula**: `Actual Lineweight = Table[Raw_Index - 1]`
- **Exceptions**:
  - `0`: Mapped to "Specify" (or "Use Object").
  - `-1`: "Use object lineweight".
  - `-2`: "ByBlock".
  - `-3`: "Default".

### 4. Hex Color Generation
The script adds a `Hex` column corresponding to the AutoCAD Color Index (ACI).
- **Alignment**: Color 1 (Red) is correctly mapped to `#FF0000`.

## Output
The script generates an Excel file in the same directory as the input file, replacing the `.ctb` extension with `.xlsx`.
- **Columns**: Color, Description, Hex, Dither, Grayscale, Pen No, Virtual Pen, Screen, Linetype, Adaptive, Line Weight, Line End Style, Line Join Style, Fill Style.

## Dependencies
- `python` (3.6+)
- `pandas`
- `openpyxl` (for Excel export)
- `zlib` (Built-in)
