""""

Задание 1

0) Повторение понятий из биологии (ДНК, РНК, нуклеотид, протеин, кодон)

1) Построение статистики по входящим в последовательность ДНК нуклеотидам 
для каждого гена (например: [A - 46, C - 66, G - 23, T - 34])

2) Перевод последовательности ДНК в РНК (окей, Гугл)

3) Перевод последовательности РНК в протеин*


*В папке files вы найдете файл rna_codon_table.txt - 
в нем содержится таблица переводов кодонов РНК в аминокислоту, 
составляющую часть полипептидной цепи белка.


Вход: файл dna.fasta с n-количеством генов

Выход - 3 файла:
 - статистика по количеству нуклеотидов в ДНК
 - последовательность РНК для каждого гена
 - последовательность кодонов для каждого гена

 ** Если вы умеете в matplotlib/seaborn или еще что, 
 welcome за дополнительными баллами за
 гистограммы по нуклеотидной статистике.
 (Не забудьте подписать оси)

P.S. За незакрытый файловый дескриптор - караем штрафным дезе.

"""

import matplotlib.pyplot as plt
from collections import Counter
from collections import defaultdict


def translate_from_dna_to_rna(dna):
    """Transcription -- synthesis RNA from DNA"""
    complementarity = {'A': 'U', 'T': 'A', 'G': 'C', 'C': 'G'}
    rna = defaultdict(list)
    print(dna)
    for gene, dnas in dna.items():
        for nucleotides in dnas:
            rna[gene].append(''.join(
                [complementarity[nucleotide] for nucleotide in nucleotides]))
    return rna


def count_nucleotides(dna):
    """DNA nucleotide statistics and creating graphs"""
    num_of_nucleotides = {}
    counter = Counter()
    for key, val in dna.items():
        for i in val:
            counter += Counter(i)
        num_of_nucleotides[key] = counter
        counter = Counter()

        """creating graphs"""
        x_val = (num_of_nucleotides[key].values())
        y_val = range(len(x_val))
        plt.bar(y_val, x_val)
        plt.xticks(y_val, num_of_nucleotides[key])
        plt.ylabel('Amount, [units]')
        plt.xlabel('Nucleotides')
        plt.title(str(key))
        plt.savefig(f'./files/{key}.jpg')
        plt.close()
    return num_of_nucleotides


def translate_rna_to_protein(rna, codons):
    """Protein from RNA"""
    protein = defaultdict(str)

    def find_triplets(x):
        return [x[i:i + 3] for i in range(0, len(x), 3)]

    for key, val in rna.items():
        for triplets in val:
            triplets = find_triplets(triplets)
            for triplet in triplets:
                if len(triplet) == 3:
                    protein[key] += (codons[triplet])
                else:
                    pass
    return protein


def main():
    # read the file dna.fasta
    path = './files/dna.fasta'
    with open(path) as f:
        dna = defaultdict(list)
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                key = line
            else:
                dna[key].append(line)

    # read the codon translation table
    path = './files/rna_codon_table.txt'
    with open(path) as f:
        lines = f.read().split()
        codon = iter(lines)
        codons = dict(zip(codon, codon))

    count_nucl = count_nucleotides(dna)
    rna = translate_from_dna_to_rna(dna)
    protein = translate_rna_to_protein(rna, codons)

    # DNA nucleotide statistics
    with open('./files/statistics.txt', 'w') as f:
        for gene, dnas in count_nucl.items():
            f.write(gene + ':\n[')
            for dna, number in dnas.items():
                f.write(f'{dna} - {number}, ')
            f.seek(f.tell() - 2)
            f.write(']\n')

    # RNA sequence for each gene
    with open('./files/rna.txt', 'w') as f:
        for gene, rnas in rna.items():
            f.write(gene + ':\n')
            for r in rnas:
                f.write(r + '\n')

    # Codon sequence for each gene
    with open('./files/protein.txt', 'w') as f:
        for gene, codons in protein.items():
            f.write(gene + ':\n')
            f.write(codons + '\n')


if __name__ == '__main__':
    main()
