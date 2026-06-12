from pathlib import Path


class ConverterError(Exception):
    """
    Base exception class for all converter-related errors.
    """


class SourceFolderNotFoundError(ConverterError):
    """
    Raised when the specified input folder does not exist.
    """


class NoConlluFilesFoundError(ConverterError):
    """
    Raised when no CoNLL-U files are found in the source directory.
    """


class EmptyFileError(ConverterError):
    """
    Raised when a file contains no valid tokens to process.
    """


class Converter:
    """
    Handles bulk conversion of CoNLL-U files into linear text format for AntConc.
    """

    MIN_COLUMNS: int = 10
    POS_STOP_TAG: str = "PUNCT"
    STOP_POS: set[str] = {
    "ADP",      # предлоги
    "CCONJ",    # сочинительные союзы
    "SCONJ",    # подчинительные союзы
    "PART",     # частицы
    "INTJ"      # междометия
    }

    STOP_LEMMAS: set[str] = {
        "и", "а", "но",
        "в", "во",
        "на",
        "с", "со",
        "к", "ко",
        "по",
        "у",
        "из",
        "за",
        "что",
        "это",
        "как",
        "же",
        "ли",
        "бы",
        "не",
        "ни"
    }
    DEFAULT_INPUT_DIR: Path = Path("input_conllu")
    DEFAULT_OUTPUT_DIR: Path = Path("output_antconc")

    def __init__(self, input_folder: str | Path | None = None, output_folder: str | Path | None = None):
        """
        Initializes the converter with custom paths or uses standard defaults.
        """
        self.input_folder = Path(input_folder) if input_folder else self.DEFAULT_INPUT_DIR
        self.output_folder = Path(output_folder) if output_folder else self.DEFAULT_OUTPUT_DIR

    def _parse_line(self, line: str, subcorpus: str) -> str | None:
        """
        Parses a single CoNLL-U line and formats it into a custom token string.
        """
        if line.startswith("#") or not line.strip():
            return None
            
        columns = line.split("\t")

        if len(columns) < self.MIN_COLUMNS:
            return None

        word   = columns[1]
        lemma  = columns[2]
        pos    = columns[3]
        deprel = columns[7]

        if pos == self.POS_STOP_TAG:
            return None

        if pos in self.STOP_POS:
            return None

        if lemma.lower() in self.STOP_LEMMAS:
            return None
        
        return f"{word}#{lemma}#{pos}#{deprel}#{subcorpus}"
    
    def convert_single_file(self, input_path: Path) -> Path:
        """
        Processes a single CoNLL-U file and writes the extracted tokens to a text file.
        """
        subcorpus = input_path.stem
        antconc_tokens = []
        
        with input_path.open("r", encoding="utf-8") as f:
            for line in f:
                token = self._parse_line(line, subcorpus)
                if token:
                    antconc_tokens.append(token)

        if not antconc_tokens:
            raise EmptyFileError(f"File {input_path.name} contains no valid tokens for processing.")

        output_path = self.output_folder / f"{subcorpus}_ready.txt"
        output_path.write_text(" ".join(antconc_tokens), encoding="utf-8")
        return output_path
    
    def convert_all(self) -> list[Path]:
        """
        Discovers, validates, and converts all CoNLL-U files in the input directory.
        """
        if not self.input_folder.exists():
            raise SourceFolderNotFoundError(f"Source folder not found: {self.input_folder}")

        conllu_files = list(self.input_folder.glob("*.conllu"))
        if not conllu_files:
            raise NoConlluFilesFoundError(f"No *.conllu files found in folder: {self.input_folder}")

        self.output_folder.mkdir(exist_ok=True)
        processed_files = []

        for input_path in conllu_files:
            try:
                output_path = self.convert_single_file(input_path)
                processed_files.append(output_path)
            except EmptyFileError:
                raise

        return processed_files
