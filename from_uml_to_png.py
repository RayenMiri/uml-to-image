import os
import sys
import zlib
import base64
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: The 'requests' library is required. Install it with 'pip install requests'.")
    sys.exit(1)

def encode_plantuml(text):
    """
    Encode PlantUML text to the special format used in PlantUML server URLs.
    
    This function compresses the PlantUML text using the DEFLATE algorithm,
    encodes it in base64, and then translates it to the PlantUML-specific encoding.
    
    Args:
        text (str): The PlantUML diagram code as string
        
    Returns:
        str: Encoded string ready to be used in PlantUML server URLs
    """
    # Compress using DEFLATE algorithm with maximum compression (UTF-8 encoded)
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed = compressor.compress(text.encode('utf-8')) + compressor.flush()
    
    # Base64 encode and translate to PlantUML format
    b64 = base64.b64encode(compressed).decode('utf-8')
    std_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    plantuml_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    translated = b64.translate(str.maketrans(std_chars, plantuml_chars))
    return translated

def process_file(file_path, output_dir):
    """
    Process a single .puml file and save the PNG output.
    
    This function reads a PlantUML file, encodes its content, sends it to the
    PlantUML server for rendering, and saves the resulting PNG image.
    
    Args:
        file_path (Path): Path to the .puml file
        output_dir (Path): Directory where the PNG should be saved
        
    Returns:
        None
    """
    # Explicitly read with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as f:
        plantuml_code = f.read()
    
    encoded = encode_plantuml(plantuml_code)
    url = f'https://www.plantuml.com/plantuml/png/{encoded}'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            output_path = output_dir / f'{file_path.stem}.png'
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f'Fichier créé avec succès: {output_path}')
        else:
            print(f'Erreur avec {file_path.name}: Code d\'état {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Erreur de connexion pour {file_path.name}: {str(e)}')

def main():
    """
    Main function to process PlantUML files in a directory.
    
    This function finds all .puml files in the specified directory (or current
    working directory if none is provided), processes them, and saves the
    resulting PNG files in a 'sortie_png' subdirectory.
    
    Command line usage:
        python from_uml_to_png.py [input_directory]
    """
    # Set up directories
    input_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    output_dir = input_dir / 'sortie_png'
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Find all .puml files
    puml_files = list(input_dir.glob('*.puml'))
    
    if not puml_files:
        print(f'Aucun fichier .puml trouvé dans {input_dir}')
        return
    
    # Process each file
    for puml_file in puml_files:
        print(f'Traitement de {puml_file.name}...')
        process_file(puml_file, output_dir)

if __name__ == '__main__':
    main()