from collections import Counter
from pathlib import Path
import re
import sys

DEFAULT_FILE = "cipher1.txt"

# Isi mapping cipherteks -> plaintext sedikit demi sedikit dari hasil analisis.
MAPPING = {
    "m": "s",
    "j": "u",
    "y": "b",
    "u": "t",
    "z": "i",
    "k": "o",
    "d": "n",
    "w": "c",
    "n": "p",
    "s": "h",
    "g": "e",
    "a": "r",
    "x": "a",
    "q": "l",
    "b": "m",  # mebykq→memory, ckab→word
    "c": "f",  # caghjgdwzgm→frequencies
    "e": "y",  # mzbzqxaqe→similarly
    "f": "j",  # fjqzjm→julius
    "h": "q",  # caghjgdwzgm→frequencies
    "i": "d",  # rkai→word, izozmzkdm→divisions
    "l": "z",  # agwktdzlgi→recognized
    "o": "v",  # igozmgi→devised, izozmzkdm→divisions
    "p": "k",  # pgerkai→keyword, bxpg→make
    "r": "w",  # rkai→word, rakdt→wrong
    "t": "g",  # rakdt→wrong, bgmmxtg→message
    "v": "x",  # gvxbnqg→example, wkbnqgv→complex
}


def read_ciphertext(filename):
    return Path(filename).read_text(encoding="utf-8")


def show_frequency(text):
    letters = [char for char in text.lower() if char.isalpha()]
    counts = Counter(letters)

    print("=== FREKUENSI HURUF ===")
    for letter, count in counts.most_common():
        print(f"{letter}: {count}")


def word_pattern(word):
    labels = {}
    next_label = 0
    pattern = []

    for char in word.lower():
        if char not in labels:
            labels[char] = next_label
            next_label += 1
        pattern.append(labels[char])

    return tuple(pattern)


def show_repeated_words(text):
    words = re.findall(r"[A-Za-z]+", text.lower())
    counts = Counter(words)

    print("\n=== KATA YANG SERING MUNCUL ===")
    for word, count in counts.most_common(20):
        print(f"{word:20} {count:>3} kali | pola {word_pattern(word)}")


def decrypt_with_mapping(text):
    result = []

    for char in text:
        lower = char.lower()
        plain = MAPPING.get(lower)

        if plain is None:
            result.append("_" if char.isalpha() else char)
        else:
            result.append(plain.upper() if char.isupper() else plain)

    return "".join(result)


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE

    try:
        ciphertext = read_ciphertext(filename)
    except FileNotFoundError:
        print(f"File tidak ditemukan: {filename}")
        print(f"Letakkan cipher1.txt di folder proyek atau jalankan:")
        print(f"python cryptanalysis.py path/ke/cipher1.txt")
        raise SystemExit(1)

    show_frequency(ciphertext)
    show_repeated_words(ciphertext)

    print("\n=== HASIL DEKRIPSI SEMENTARA ===")
    print(decrypt_with_mapping(ciphertext))


if __name__ == "__main__":
    main()
