import itertools
import hashlib
import os
import random
import string
import tkinter as tk
from tkinter import filedialog, messagebox

special_chars = ['@', '#', '$', '%', '^', '&', '*', '!', '?', '_', '-', '=', '+']
leet_map = {
    'a': ['a', '@', '4'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7']
}

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

def hash_word(word, method):
    h = word.encode()
    if method == 'md5':
        return hashlib.md5(h).hexdigest()
    elif method == 'sha1':
        return hashlib.sha1(h).hexdigest()
    elif method == 'sha256':
        return hashlib.sha256(h).hexdigest()
    else:
        raise ValueError("Unsupported hash type.")

def run_crack(names, places, dates, keywords, extra_words, target_hash, hash_type):
    all_inputs = names + places + dates + keywords + extra_words
    MegaSet = set()

    for word in all_inputs:
        MegaSet.add(word)  # raw word
        MegaSet.update(generate_variants(word))

    for w1 in all_inputs:
        for w2 in all_inputs:
            if w1 != w2:
                MegaSet.add(w1 + w2)
                MegaSet.add(w2 + w1)
                MegaSet.update(generate_variants(w1 + w2))
                MegaSet.update(generate_variants(w2 + w1))

    for w1 in all_inputs:
        for w2 in all_inputs:
            for w3 in all_inputs:
                if len({w1, w2, w3}) == 3:
                    MegaSet.add(w1 + w2 + w3)

    with open("MegaGigaWordlist.txt", "w", encoding="utf-8") as f:
        for word in MegaSet:
            f.write(word + "\n")

    print(f"\nSaved {len(MegaSet)} entries to MegaGigaWordlist.txt. Now cracking...")

    for word in MegaSet:
        if hash_word(word, hash_type) == target_hash:
            print(f"\nMATCH FOUND: {word}")
            return word
    print("\nNo match found.")
    return None

# GUI mode
def run_gui():
    def browse_file():
        file = filedialog.askopenfilename()
        wordlist_entry.delete(0, tk.END)
        wordlist_entry.insert(0, file)

    def crack():
        names = names_entry.get().split(',')
        places = places_entry.get().split(',')
        dates = dates_entry.get().split(',')
        keywords = keywords_entry.get().split(',')
        extra_words = []

        if wordlist_entry.get():
            try:
                with open(wordlist_entry.get(), 'r', encoding='utf-8') as f:
                    extra_words = [line.strip() for line in f.readlines()]
            except:
                messagebox.showerror("Error", "Could not read wordlist.")
                return

        hash_val = hash_entry.get().strip()
        hash_type = hash_type_var.get()

        result = run_crack(names, places, dates, keywords, extra_words, hash_val, hash_type)
        if result:
            messagebox.showinfo("Success", f"Password match: {result}")
        else:
            messagebox.showinfo("Failed", "No match found.")

    root = tk.Tk()
    root.title("MegaGigaCracker GUI")

    tk.Label(root, text="Names:").grid(row=0, column=0)
    tk.Label(root, text="Places:").grid(row=1, column=0)
    tk.Label(root, text="Dates:").grid(row=2, column=0)
    tk.Label(root, text="Keywords:").grid(row=3, column=0)
    tk.Label(root, text="Hash:").grid(row=4, column=0)
    tk.Label(root, text="Hash Type:").grid(row=5, column=0)
    tk.Label(root, text="Wordlist (optional):").grid(row=6, column=0)

    names_entry = tk.Entry(root, width=50)
    places_entry = tk.Entry(root, width=50)
    dates_entry = tk.Entry(root, width=50)
    keywords_entry = tk.Entry(root, width=50)
    hash_entry = tk.Entry(root, width=50)
    wordlist_entry = tk.Entry(root, width=50)
    hash_type_var = tk.StringVar(value="md5")

    hash_type_menu = tk.OptionMenu(root, hash_type_var, "md5", "sha1", "sha256")
    browse_button = tk.Button(root, text="Browse", command=browse_file)
    run_button = tk.Button(root, text="Crack Hash", command=crack)

    names_entry.grid(row=0, column=1)
    places_entry.grid(row=1, column=1)
    dates_entry.grid(row=2, column=1)
    keywords_entry.grid(row=3, column=1)
    hash_entry.grid(row=4, column=1)
    hash_type_menu.grid(row=5, column=1, sticky="w")
    wordlist_entry.grid(row=6, column=1)
    browse_button.grid(row=6, column=2)
    run_button.grid(row=7, column=1, pady=10)

    root.mainloop()

mode = input("Launch GUI mode? (y/n): ").strip().lower()
if mode == 'y':
    run_gui()
else:
    def get_input_list(prompt):
        return [item.strip() for item in input(prompt).split(',') if item.strip()]

    names = get_input_list("Enter names (comma separated): ")
    places = get_input_list("Enter places (comma separated): ")
    dates = get_input_list("Enter dates (comma separated): ")
    keywords = get_input_list("Enter other keywords (comma separated): ")
    extra_words = []

    if input("Read from an existing wordlist? (y/n): ").lower() == 'y':
        file = input("Enter filename: ")
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                extra_words = [line.strip() for line in f.readlines()]
        else:
            print("File not found.")

    target_hash = input("Enter the hash to crack: ").strip().lower()
    hash_type = input("Enter hash type (md5, sha1, sha256): ").strip().lower()

    run_crack(names, places, dates, keywords, extra_words, target_hash, hash_type)
