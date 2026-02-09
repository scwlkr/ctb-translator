# CTB Translator - Technical Documentation

This document provides a comprehensive technical overview of the CTB Translator project, covering the architecture, build system, and a deep dive into the binary parsing logic.

## 1. Project Overview

The **CTB Translator** is a web-based utility that parses AutoCAD Color-Dependent Plot Style (`.ctb`) files and extracts their internal settings (Lineweight, Screen, Color, etc.) into a readable HTML table.

### Architecture
- **Frontend**: HTML5, CSS3 (Vanilla).
- **Runtime**: PyScript (WebAssembly) to execute Python logic in the browser.
- **Logic**: Python 3 (Pure, no external dependencies like Pandas).
- **Development Server**: Bun (or Python `http.server`).

---

## 2. File Structure

```
ctb-translator/
├── index.html              # Main application entry point (UI)
├── style.css               # Styling (Drafting & Print layouts)
├── ctb-translator-web.py   # Core parsing logic (Python)
├── pyscript.json          # PyScript configuration
├── README.md               # Quick start guide
└── DOCUMENTATION.md        # Technical documentation (This file)
```

---

## 3. Build & Development

The project is designed to be **static** and **serverless**. It does not require a backend build step (like Webpack or Vite), although one can be added if the project grows.

### Prerequisites
- **Bun** (Recommended for local serving) OR **Python 3**.

### Running Locally
To serve the application locally:

**Using Bun:**
```bash
bun x http-server .
# OR
bun run --hot index.html
```

**Using Python:**
```bash
python -m http.server 8000
```

Access the app at `http://localhost:3000` (Bun) or `http://localhost:8000` (Python).

### Deployment
This project is optimized for **GitHub Pages**. Only the `main` branch needs to be deployed. No build artifacts are required.

---

## 4. Deep Dive: Parsing Logic (`ctb-translator-web.py`)

The core of the application is a Python script that manually parses the binary structure of a `.ctb` file.

### 4.1. File Format Overview
A `.ctb` file is essentially a **Zlib-compressed** file containing text-based definitions of plot styles. It is NOT a standard text file and must be decompressed first.

### 4.2. Decompression Step
When a file is uploaded:
1.  **Read Bytes**: The browser (`index.html`) reads the file as an `ArrayBuffer` and passes a `Uint8Array` to the Python function `process_file_content`.
2.  **Signature Search**: The script scans the byte stream for the Zlib header signature `0x78` followed by a specific compression level byte (`0xDA`, `0x9C`, etc.).
3.  **Decompression**: Once the offset is found, `zlib.decompress` inflates the data into a readable string.

```python
# Code Snippet: Finding the Zlib stream
start_offset = -1
for i in range(len(data) - 1):
    if data[i] == 0x78 and data[i+1] in [0xDA, 0x9C, ...]:
        start_offset = i
        break
```

### 4.3. Data Structure Parsing
The decompressed text follows a pseudo-JSON/Struct format. The parser iterates through lines to identify two main sections:

#### A. Custom Lineweight Table (`custom_lineweight_table`)
Contains the mapping of index-based lineweights to physical millimeters.
- **Format**: `index = value` inside curly braces.
- **Logic**: These values are stored in a dictionary `lineweight_map` to resolve "Index" based lineweights later.

#### B. Plot Styles (Colors 1-255)
Each color is defined as a numbered object (e.g., `1{ ... }`).
- **Key Properties Extracted**:
    - `color`: The internal raw color value.
    - `screen`: Ink intensity (0-100).
    - `lineweight`: An integer index.
        - `0`: "Specify" (User corrections applied here).
        - `-1`: "Use object lineweight".
        - `>0`: References the `custom_lineweight_table`.
    - `description`, `linetype`, `end_style`, `join_style`, `fill_style`.

### 4.4. Post-Processing Logic
After extraction, usage logic is applied to make the data human-readable:

1.  **Hex Mapping**:
    - A standard `ACI_HEX_LIST` maps AutoCAD Color Indices (1-255) to web-safe Hex codes for visual display.
    
2.  **"Plots Same As" Grouping**:
    - This feature identifies redundant styles.
    - **Logic**:
        - Create a unique key for each color based on: `(Plot Color, Screen, Line Weight)`.
        - Group all colors sharing this key.
        - If a group has multiple members, the "Plots Same As" column lists the *other* colors in that group.
        - **Exception**: Colors with "Specify" lineweight are excluded from grouping as they are unique override styles.

### 4.5. Rendering
The final data structure is a list of dictionaries. The Python script interacts directly with the DOM to render the HTML Table, leveraging PyScript's `document` API.

---

## 5. Extensibility
To add new features:
1.  **New Column**: Add extraction logic in `parse_ctb_bytes` inside the `lines` loop, then update `render_table` to create the `td` element.
2.  **New Calculations**: Modify `process_data` to implement new business logic (e.g., cost estimation based on ink usage).
