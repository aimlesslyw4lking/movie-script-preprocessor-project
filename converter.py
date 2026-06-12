from pathlib import Path

MIN_COLUMNS = 10
POS_STOP_TAG = "PUNCT"

input_folder = Path("input_conllu")
output_folder = Path("output_antconc")

output_folder.mkdir(exist_ok=True)

for input_path in input_folder.glob("*.conllu"):
    subcorpus = input_path.stem
        
    antconc_tokens = []
        
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
                
            columns = line.split("\t")
                
            if len(columns) < MIN_COLUMNS or columns[3] == POS_STOP_TAG:
                continue
                
            word   = columns[1]
            lemma  = columns[2]
            pos    = columns[3]
            deprel = columns[7]
            
            antconc_tokens.append(
                f"{word}#{lemma}#{pos}#{deprel}#{subcorpus}"
                )

    if not antconc_tokens:
        print(f"Пропущен файл (токены не найдены): {input_path.name}")
        continue

    output_path = output_folder / f"{subcorpus}_ready.txt"
        
    output_path.write_text(" ".join(antconc_tokens), encoding="utf-8")
    print(f"Успешно обработан файл: {input_path.name} -> {output_path.name}")

print("\nВсе файлы готовы для загрузки в AntConc!")
