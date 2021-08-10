import sys
import re
import csv


def main():
    if len(sys.argv) not in (2, 3):
        print("Verwendung: liger.py anzahl_generationen {resultat.csv}")

    num_generations = int(sys.argv[1])

    generation = ("Tiger", "Löwe")  # tuple, not set, because we want to keep it ordered

    for i in range(num_generations - 1):
        crosstable = make_crosstable(generation)
        new_generation = set(crosstable.values()) - set(generation)
        generation += tuple(new_generation)

    crosstable = make_crosstable(generation)
    full_table = make_full_table(generation, crosstable)
    # pretty_print(full_table)
    print_to_csv(full_table)


def make_crosstable(generation: tuple):
    crosstable = {}
    for father in generation:
        for mother in generation:
            crosstable[father, mother] = breed(father, mother)
    return crosstable


def breed(father, mother):
    if father == mother:
        return father

    # special cases
    if father == "Tiger" and mother == "Löwe":
        return "Töwe"
    if father == "Löwe" and mother == "Tiger":
        return "Liger"

    father_prefixes = re.sub(r'ger|we$', '', father)
    return father_prefixes + "-" + mother


def make_full_table(generation, crosstable):
    table = []

    # header row
    table.append([""] + list(generation))

    # table body
    for fem_specimen in generation:
        new_row = [female(fem_specimen)]
        for specimen in generation:
            new_row.append(crosstable[specimen, fem_specimen])
        table.append(new_row)

    return table


def female(specimen):
    if specimen[-1:][0] == "e":
        return re.sub(r'e$', 'in', specimen)
    return specimen + "in"


def print_to_csv(full_table):
    if len(sys.argv) == 3:
        filename = sys.argv[2]
    else:
        filename = "liger.csv"

    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(full_table)


if __name__ == '__main__':
    main()
