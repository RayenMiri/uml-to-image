# uml-to-image

A simple Python utility to convert PlantUML (.puml) files to PNG images using the public PlantUML server.

## Overview

This tool allows you to batch convert PlantUML diagram files to PNG images without requiring a local PlantUML installation. It works by:

1. Reading your .puml files
2. Encoding them in the format required by the PlantUML server
3. Requesting the rendered PNG images from the server
4. Saving the images to a local directory

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Clone this repository or download the `from_uml_to_png.py` script.

2. Install the required dependency:
   ```bash
   pip install requests
   ```

## Usage

### Basic Usage

Run the script in a directory containing .puml files:

```bash
python from_uml_to_png.py
```

By default, the script will:
- Look for .puml files in the current directory
- Create a subdirectory called "sortie_png"
- Save the generated PNG files in the subdirectory

### Specify an Input Directory

You can also specify a directory containing the .puml files:

```bash
python from_uml_to_png.py /path/to/your/uml/files
```

### Output

The script will create PNG files with the same base names as your .puml files in the "sortie_png" subdirectory.

## How It Works

1. **Encoding**: The script uses the DEFLATE compression algorithm and a special base64 variant to encode the PlantUML text into a format that the PlantUML server can process via URL.

2. **Remote Rendering**: The encoded diagram is sent to the public PlantUML server at plantuml.com, which renders it and returns a PNG image.

3. **Local Saving**: The returned PNG image is saved to your local filesystem.

## Limitations

- Requires an internet connection to access the PlantUML server
- Subject to the limitations and availability of the public PlantUML server
- Large or complex diagrams might time out or fail to render
