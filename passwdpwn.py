import itertools
import hashlib
import os
import random
import string

special_chars = ['@', '#', '$', '%', '^', '&', '*', '!', '?', '_', '-', '=', '+']
leet_map = {
    'a': ['a', '@', '4'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7']
}

def get_input_list(prompt):
    return [item.strip() for item in input(prompt).split(',') if item.strip()]

names = get_input_list("Enter names (comma separated): ")
places = get_input_list("Enter places (comma separated): ")
dates = get_input_list("Enter dates (comma separated): ")
keywords = get_input_list("Enter other keywords (comma separated): ")

additional_words = []
if input("Do you want to read from an existing wordlist? (y/n): ").lower() == 'y':
    filename = input("Enter the filename (must be in this directory): ").strip()
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            additional_words = [line.strip() for line in f.readlines()]
    else:
        print("File not found.")

target_hash = input("Enter the hash to crack: ").strip().lower()
hash_type = input("Enter hash type (md5, sha1, sha256): ").strip().lower()

def hash_word(word, method):
    if method == 'md5':
        return hashlib.md5(word.encode()).hexdigest()
    elif method == 'sha1':
        return hashlib.sha1(word.encode()).hexdigest()
    elif method == 'sha256':
        return hashlib.sha256(word.encode()).hexdigest()
    else:
        raise ValueError("Unsupported hash type.")

def leetify(word):
    combos = set()

    def helper(idx, current):
        if idx == len(word):
            combos.add(''.join(current))
            return
        char = word[idx].lower()
        subs = leet_map.get(char, [word[idx]])
        for s in subs:
            helper(idx + 1, current + [s])

    helper(0, [])
    return combos

def generate_variants(word):
    variants = set()
    base_forms = {word, word.lower(), word.upper(), word.capitalize()}
    for form in base_forms:
        variants.add(form)
        for c in special_chars:
            variants.add(form + c)
            variants.add(c + form)
        variants.update(leetify(form))
    return variants

all_inputs = names + places + dates + keywords + additional_words
MegaSet = set()

for word in all_inputs:
    MegaSet.update(generate_variants(word))

for w1 in all_inputs:
    for w2 in all_inputs:
        if w1 != w2:
            MegaSet.update(generate_variants(w1 + w2))
            MegaSet.update(generate_variants(w2 + w1))

for w1 in all_inputs:
    for w2 in all_inputs:
        for w3 in all_inputs:
            if w1 != w2 and w2 != w3 and w1 != w3:
                MegaSet.add(w1 + w2 + w3)

output_path = "MegaGigaWordlist.txt"
with open(output_path, "w", encoding="utf-8") as f:
    for word in MegaSet:
        f.write(word + "\n")

print(f"\nSaved {len(MegaSet)} entries to {output_path}. Now cracking...")

found = False
for word in MegaSet:
    if hash_word(word, hash_type) == target_hash:
        print(f"\nMATCH FOUND: {word}")
        found = True
        break

if not found:
    print("\nNo match found. Try adding more words or increasing combinations.")

