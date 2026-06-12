from pathlib import Path
from ufal.udpipe import Model, Pipeline


class ScriptNotFoundError(Exception):
   """Raised when the .txt file containing a script was not found in the destinated folder """

class ScriptCompilationError(Exception):
    """Raised when an error occurs during parsing into a dictionary """

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
                speech = parts[1].strip()

                if name not in char_lines:
                    char_lines[name] = []

                char_lines[name].append(speech)

    return char_lines


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
            
            file_words = "\n".join(tokens)
        
            file_path.write_text(file_words, encoding='utf-8')
            print(f"Saved one! - {file_path}!")

        print('Your files are good to go now :3')
        return True
        
    except CleanScriptNotWrittenError:
        return False

class UDPipeAnalyzer:
    """
    Converts character corpora into CoNLL-U format using UDPipe.
    """

    MODEL_PATH = Path("./assets/model/russian-syntagrus-ud-2.0-170801.udpipe")

    def __init__(self):

        self.model = Model.load(str(self.MODEL_PATH))

        if self.model is None:
            raise FileNotFoundError(
                f"UDPipe model not found: {self.MODEL_PATH}"
            )

        self.pipeline = Pipeline(
            self.model,
            "tokenize",
            Pipeline.DEFAULT,
            Pipeline.DEFAULT,
            "conllu"
        )

    def process_all(self) -> bool:
        """
        Processes scripts and .conllu files 
        """
        try:
            input_dir = Path("./cleaned_scripts")
            output_dir = Path("./input_conllu")

            output_dir.mkdir(parents=True, exist_ok=True)

            txt_files = list(input_dir.glob("*.txt"))

            if not txt_files:
                raise FileNotFoundError(
                    "No txt files found in ./cleaned_scripts"
                )

            for txt_file in txt_files:

                text = txt_file.read_text(
                    encoding="utf-8"
                ).strip()

                if not text:
                    continue

                conllu = self.pipeline.process(text)

                output_file = (
                    output_dir /
                    f"{txt_file.stem.replace('_corpus', '')}.conllu"
                )

                output_file.write_text(
                    conllu,
                    encoding="utf-8"
                )

                print(f"Created {output_file}")

            return True

        except ScriptPreprocessingError("Yuck! Something went wrong while annotating!"):

            return False