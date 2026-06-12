# movie-script-preprocessor-project

## Overview

**movie-script-preprocessor-project** is a Python-based text preprocessing tool designed for linguistic analysis of Russian-language dialogue scripts.

The program processes annotated dialogue files in the format:

```text
[character_name] dialogue text
```

and automatically:

* extracts character utterances
* tokenizes dialogue text
* normalizes words through lemmatization
* removes Russian stop words
* generates separate text corpora for each character

TThe resulting corpora can be used for linguistic analysis, including lexical analysis, stylistic comparison, frequency analysis, and the identification of distinctive speech patterns between characters.

---

## Table of contents

* [Overview](#overview)
* [Project goal](#project-goal)
* [Features](#features)
* [Project structure](#project-structure)
* [System requirements](#system-requirements)
* [Installation and setup](#installation-and-setup)
* [Input data format](#input-data-format)

  * [Supported file format](#supported-file-format)
  * [Dialogue format](#dialogue-format)
  * [Parsing rules](#parsing-rules)
  * [Input format examples](#input-format-examples)
* [Processing pipeline](#processing-pipeline)

  * [1. Script discovery](#1-script-discovery)
  * [2. Tokenization and dialogue compilation](#2-tokenization-and-dialogue-compilation)
  * [3. Lemmatization and stop word removal](#3-lemmatization-and-stop-word-removal)
  * [4. Corpus generation](#4-corpus-generation)
* [Running the program](#running-the-program)
* [Output](#output)
* [Processing behavior](#processing-behavior)
* [Implementation notes](#implementation-notes)
* [License](#license)

---

## Project goal

The preprocessing pipeline was developed to support linguistic research on Russian-language dialogue corpora.

The generated corpora can be used for:

* lexical analysis
* stylistic comparison between characters
* frequency analysis
* identification of idiolectal features
* linguistic profiling

---

## Features

The program performs the following operations:

1. Recursively searches for `.txt` dialogue files formatted as:
   ```text
   [character_name] dialogue text
   ```
2. Extracts character names and dialogue text.
3. Converts text to lowercase.
4. Tokenizes dialogue into words.
5. Removes punctuation and non-alphanumeric symbols.
6. Lemmatizes tokens to dictionary forms.
7. Removes Russian stop words.
8. Generates one corpus file per character.
9. Preserves the original word order within each character’s utterances.

---

## Project structure

```text
movie-script-preprocessor-project/
│
├── raw_scripts/                     # Folder containing unprocessed scripts
│   └── *.txt
│
├── cleaned_scripts/                 # Automatically created folder with character corpora
│   ├── ежик_corpus.txt
│   ├── крош_corpus.txt
│   ├── бараш_corpus.txt
│   └── ...
│
├── main.py                          # Program entry point
├── processor.py                    # Text preprocessing logic
├── requirements.txt                # Project dependencies
├── .gitignore                      # Ignored files and directories
├── LICENSE                         # MIT License
└── README.md                       # Project documentation
```

### Directory description

| Path               | Description                                      |
| ------------------ | ------------------------------------------------ |
| `raw_scripts/`     | Stores input `.txt` script files                 |
| `cleaned_scripts/` | Stores generated corpora (created automatically) |
| `main.py`          | Executes the preprocessing pipeline              |
| `processor.py`     | Contains text preprocessing functions            |
| `requirements.txt` | Lists required Python packages                   |

---

## System requirements

### Software requirements

* Python **3.8 or higher**
* `pip`

### Supported operating systems

The project is cross-platform and can run on:

* Windows
* Linux
* macOS

Any operating system capable of running Python **3.8+** should be compatible.

### Dependencies

The following Python packages are required:

```text
pymorphy3==2.0.6
spacy==3.8.14
```

No additional spaCy language model download is required.

The project uses the built-in Russian stop word list provided by:

```python
spacy.lang.ru.Russian().Defaults.stop_words
```

---

## Installation and setup

It is recommended to use a virtual environment.

### 1. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## Input data format

### Supported file format

The program processes:

```text
.txt
```

files encoded in:

```text
UTF-8
```

All input files must be placed inside:

```text
raw_scripts/
```

### Multi-file behavior

The program recursively searches for **all `.txt` files** inside `raw_scripts/`, including nested directories.

Implementation:

```python
Path("./raw_scripts").rglob("*.txt")
```

If multiple files are present:

* all files are processed
* all dialogue lines are read sequentially
* the content is combined into a single processing stream
* character corpora are compiled across all discovered files

Example:

```text
raw_scripts/
├── episode_1.txt
├── episode_2.txt
└── archive/
    └── special_episode.txt
```

In this case, dialogues from all files are merged into the same character corpora.

If isolated corpora are required per script, files should be processed separately.

### Dialogue format

The expected dialogue structure is:

```text
[character_name] dialogue text
```

Example:

```text
[крош] Здесь! Быстрей сюда!
[ежик] Бегу, бегу!
[бараш] Сегодня дождь обещали.
```

Each line should contain:

1. a character name enclosed in square brackets `[]`;
2. dialogue text following the closing bracket `]` on the same line.

### Parsing rules

#### Character name normalization

Character names are:

* extracted from square brackets
* converted to lowercase
* normalized by replacing `ё` with `е`

Example:

```text
[Ёжик] → ежик
```

This normalization ensures consistent character naming and token representation.

---

#### Dialogue preprocessing

Dialogue text is:

1. converted to lowercase;
2. split into tokens using whitespace;
3. stripped of any non-alphanumeric characters using `isalnum()`.

Example input:

```text
[Крош] Здесь! Быстрей сюда!
```

After tokenization:

```text
здесь быстрей сюда
```

Important behavior:

* punctuation marks are removed
* digits are preserved
* alphanumeric characters remain
* service annotations are cleaned as ordinary text
* token order is preserved

Example:

```text
[крош] У меня 3 яблока!
```

Becomes:

```text
у меня 3 яблока
```

Digits remain unchanged during lemmatization.

---

#### Service annotations

The program does not process service annotations specially.

Example:

```text
{неразбр}
```

After cleaning:

```text
неразбр
```

During token cleaning, only alphanumeric characters are preserved.

### Input format examples

The parser processes lines matching the expected dialogue structure:

```text
[character_name] dialogue text
```

Examples of accepted and ignored input formats:

| Input example    | Behavior                                                      |
| ---------------- | ------------------------------------------------------------- |
| `[крош] Привет!` | Processed                                                     |
| `[крош]`         | Character name is extracted, but no dialogue tokens are added |
| `крош Привет!`   | Ignored during preprocessing                                  |
| `[крош Привет!`  | Ignored during preprocessing                                  |
| `крош: Привет!`  | Ignored during preprocessing                                  |

Lines that do not match the expected dialogue format are ignored during preprocessing.

---

## Processing pipeline

The preprocessing pipeline consists of four stages.

### 1. Script discovery

Function:

```python
find_scripts()
```

The program recursively searches for `.txt` files inside:

```text
./raw_scripts
```

All discovered files are included in preprocessing.

---

### 2. Tokenization and dialogue compilation

Function:

```python
tokenize_and_compile()
```

This stage:

* extracts character names
* separates metadata from dialogue
* tokenizes dialogue text
* aggregates tokens by character

Output structure:

```python
dict[str, list[str]]
```

Example:

```python
{
    "крош": ["здесь", "быстрей", "сюда"],
    "ежик": ["бегу", "бегу"]
}
```

Character names are normalized to lowercase and `ё` is replaced with `е`.

The original word order is preserved.

---

### 3. Lemmatization and stop word removal

Function:

```python
lemmatize_and_clean()
```

Libraries used:

```text
pymorphy3
spaCy
```

#### Lemmatization

Words are normalized using:

```python
pymorphy3.MorphAnalyzer()
```

Examples:

```text
бегу → бежать
помогите → помочь
пилюли → пилюля
```

---

#### Stop word removal

The project uses the built-in Russian stop word list from spaCy:

```python
Russian().Defaults.stop_words
```

Examples of removed stop words:

```text
и, в, на, но, это, что, как
```

Stop words are removed after lemmatization.

Output structure:

```python
dict[str, list[str]]
```

---

### 4. Corpus generation

Function:

```python
write_cleaned_file()
```

The program automatically creates:

```text
cleaned_scripts/
```

if it does not already exist.

For each character, a separate corpus file is generated:

```text
<character_name>_corpus.txt
```

Examples:

```text
ежик_corpus.txt
крош_corpus.txt
бараш_corpus.txt
```

Each file contains:

* lemmatized tokens
* stop words removed
* whitespace-separated tokens
* preserved token order

Example output:

```text
солнце уходить прогреться думать хватить
```

---

## Running the program

Open a terminal in the project root directory and run:

```bash
python main.py
```

Example console output:

```text
Hi!! <3    Looking for your scripts now...
Scripts found! Let's compile them now <3
Your scripts have been compiled successfully! ^_^
Yay! The scripts are ready! Let's upload them to a folder now

Saved one! - cleaned_scripts/ежик_corpus.txt!
Saved one! - cleaned_scripts/крош_corpus.txt!
Saved one! - cleaned_scripts/бараш_corpus.txt!

Your files are good to go now :3
```

---

## Output

After successful execution, processed corpora are saved to:

```text
cleaned_scripts/
```

Each file represents the processed dialogue corpus of a single character.

Example:

```text
ежик_corpus.txt
```

Possible content:

```text
бежать прогреться солнце думать помочь
```

---

## Processing behavior

The preprocessing pipeline supports flexible processing of annotated dialogue scripts.

| Scenario | Behavior |
|---|---|
| `.txt` files in `raw_scripts/` | All discovered files are processed recursively |
| Valid dialogue entries | Character names and dialogue text are extracted and processed |
| Empty dialogue entries | Character names are preserved without dialogue tokens |
| Multiple input files | Character corpora are compiled across all discovered files |

Only dialogue lines matching the expected format are included in preprocessing.

---

## Implementation notes

* The original token order is preserved within each character corpus.
* Character names are normalized by replacing `ё` with `е`.
* Numeric tokens are preserved during preprocessing.
* Character corpora are compiled from all `.txt` files discovered in `raw_scripts/`.

---

## License

This project is distributed under the **MIT License**.

See the `LICENSE` file for complete license information.
