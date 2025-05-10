# =============================================================================
# PROGRAM: Random DNA Sequence Generator in FASTA Format
# CONTEXT: Bioinformatics university assignment
# PURPOSE: This script generates a random DNA sequence (A, C, G, T) of user-defined
# length, inserts the user's name (non-biological characters), calculates
# sequence statistics, and saves everything to a .fasta file with proper formatting.
# =============================================================================

import random
import sys

# === INPUT: DNA sequence length ===
# ORIGINAL
# try:
#     length = int(input("Enter the sequence length: "))
#     if length <= 0:
#         raise ValueError("Length must be a positive integer.")
# except ValueError as e:
#     print(f"Invalid input: {e}")
#     sys.exit(1)

# MODIFIED (added accuracy for length that is a multiple of 3)
while True:
    try:
        length = int(input("Enter the sequence length: "))
        if length <= 0:
            print("Length must be a positive integer.")
        elif length % 3 != 0:
            print("For biological accuracy, the sequence length should be divisible by 3.")
            adjust = input("Would you like to adjust the length to the nearest multiple of 3? (y/n): ").strip().lower()
            if adjust == 'y':
                length -= length % 3
                print(f"Adjusting length to {length}.")
                break
            else:
                continue
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# === INPUT: Sequence ID ===
# ORIGINAL:
# sequence_id = input("Enter the sequence ID: ")

# MODIFIED (added filename sanitization to avoid OS errors with invalid characters):
sequence_id = input("Enter the sequence ID: ").strip().replace(" ", "_")
invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
for char in invalid_chars:
    sequence_id = sequence_id.replace(char, '_')

# === INPUT: Sequence Description ===
# ORIGINAL:
# description = input("Provide a description of the sequence: ")

# MODIFIED (added input validation to ensure the description only contains alphabetic characters and spaces):
while True:
    description = input("Provide a description of the sequence: ").strip()
    if all(c.isalpha() or c.isspace() for c in description):
        break
    else:
        print("Invalid description. Please use letters and spaces only.")

# === INPUT: User Name ===
name = input("Enter your name: ").strip()

# === DNA Sequence Generation ===
sequence = ''.join(random.choices("ACGT", k=length))
insert_position = random.randint(0, len(sequence))
sequence_with_name = sequence[:insert_position] + name + sequence[insert_position:]

# === Save to FASTA File ===
filename = f"{sequence_id}.fasta"
with open(filename, "w") as fasta_file:
    fasta_file.write(f">{sequence_id} {description}\n")

    # ORIGINAL:
    # fasta_file.write(sequence_with_name + "\n")

    # MODIFIED (formatting sequence into 60-character lines for FASTA readability):
    for i in range(0, len(sequence_with_name), 60):
        fasta_file.write(sequence_with_name[i:i + 60] + "\n")

# === STATISTICS Calculation ===
# ORIGINAL:
# count_A = sequence.count("A")
# count_C = sequence.count("C")
# count_G = sequence.count("G")
# count_T = sequence.count("T")
# total = count_A + count_C + count_G + count_T
# percent_A = (count_A / total) * 100
# percent_C = (count_C / total) * 100
# percent_G = (count_G / total) * 100
# percent_T = (count_T / total) * 100
# cg_ratio = ((count_C + count_G) / total) * 100

# MODIFIED (moved statistics into a reusable function for better structure and reusability):
def calculate_stats(seq):
    count_A = seq.count("A")
    count_C = seq.count("C")
    count_G = seq.count("G")
    count_T = seq.count("T")
    total = count_A + count_C + count_G + count_T
    if total == 0:
        return 0, 0, 0, 0, 0
    percent_A = (count_A / total) * 100
    percent_C = (count_C / total) * 100
    percent_G = (count_G / total) * 100
    percent_T = (count_T / total) * 100
    cg_ratio = ((count_C + count_G) / total) * 100
    return percent_A, percent_C, percent_G, percent_T, cg_ratio

# Use function
percent_A, percent_C, percent_G, percent_T, cg_ratio = calculate_stats(sequence)

# === Output ===
print(f"\nThe sequence was saved to the file {filename}")
print("Sequence statistics:")
print(f"A: {percent_A:.1f}%")
print(f"C: {percent_C:.1f}%")
print(f"G: {percent_G:.1f}%")
print(f"T: {percent_T:.1f}%")
print(f"%CG: {cg_ratio:.1f}")
