from pathlib import Path
# import pymorphy3
from spacy.lang.ru import Russian



class ScriptNotFoundError(Exception):
   """Raised when the .txt file containing a script was not found in the destinated folder """

class ScriptCompilationError(Exception):
    """Raised when an error occurs during tokenization and parsing into a dictionary """

class ScriptPreprocessingError(Exception):
    """Raised when an error occurs during the lemmatization and stopword extraction """

class CleanScriptNotWrittenError(Exception):
    """Raised when the cleaned .txt corpus file fails to be written """

def find_scripts():
    """
    Finds the path containing .txt script files.
    """
    pathlist = Path("./raw_scripts").rglob('*.txt')
    return (path for path in pathlist)

    
def tokenize_and_compile(find_scripts) -> dict[str, list[str]]:
    """
    Tokenizes a .txt file in the script folder according to the format.
    Compiles each character found in the script and their
    respective tokenized lines into key-value pairs.

    Args: find_scripts - scripts in the folder

    Returns: dict[str, list[str]]
    """
    char_lines = {}
    
    for path in find_scripts:
        for line in path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            
            if line.startswith('[') and ']' in line:
                parts = line.split("]", 1)
                
                name = parts[0].replace('[', '').strip().lower().replace('ё', 'е')
                speech = parts[1]
                
                clean_tokens = []
                for word in speech.lower().split():
                    cleaned = ''.join(char for char in word if char.isalnum())
                    if cleaned:
                        clean_tokens.append(cleaned)
                
                if name not in char_lines:
                    char_lines[name] = []
                
                char_lines[name].extend(clean_tokens)
                
    return char_lines

def lemmatize_and_clean(char_lines: dict) -> dict[str, int]:
    """
    Lemmatizes and cleans the compiled dictionary of character lines.
    
    Args: char_lines: dict[str, int] - Key-value pairs of the character
    and their tokenized lines

    Returns: char_lines_clean: dict[str, int] - Key-value pairs of the character
    and their lines that are tokenized and cleaned from some of the most popular stopwords
    """
    
    # morph = pymorphy3.MorphAnalyzer()
    stopwords = Russian().Defaults.stop_words

    char_lines_clean = {}
    
    # for name in char_lines:
    #     char_lines[name] = [
    #         morph.parse(token)[0].normal_form
    #         for token in char_lines[name]
    #     ]

    for name in char_lines:
        char_lines_clean[name] = [word for word in char_lines[name]
            if word not in stopwords
            ]

    return char_lines_clean

def write_cleaned_file(char_lines_clean: dict[str, int]) -> bool:
    """ 
    Creates a corpus-ready .txt file. 
    
    Args: char_lines_clean: dict[str, int] 

    Returns: a corpus-ready file for you to enjoy!!! (or suffer bc of projects!)
    
    """
    try:
        output_dir = Path("./cleaned_scripts")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for name, tokens in char_lines_clean.items():
            no_space_name = name.replace(" ", "_")
            file_path = output_dir / f'{no_space_name}_corpus.txt'
            
            file_words = " ".join(tokens)
        
            file_path.write_text(file_words, encoding='utf-8')
            print(f"Saved one! - {file_path}!")

        print('Your files are good to go now :3')
        return True
        
    except CleanScriptNotWrittenError:
        return False
