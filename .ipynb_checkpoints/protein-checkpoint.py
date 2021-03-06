# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'codon_generation'))
	print(os.getcwd())
except:
	pass
# %%
from random import *
import csv
import itertools


# %%
DNA_codon_table = [
        ("ATG","M/Start"), ("ATA","I"), ("ATC","I"), ("ATT","I"), ("ACG","T"), ("ACA","T"),
        ("ACC","T"), ("ACT", "T"), ("AAG","K"), ("AAA","K"), ("AAC","N"), ("AAT","N"),
        ("AGG","R"), ("AGA","R"), ("AGC","S"), ("AGT","S"), 
        ("GTG","V"), ("GTA","V"), ("GTC","V"), ("GTT","V"), ("GCG","A"), ("GCA","A"), ("GCC","A"), ("GCT","A"), 
        ("GAG","E"), ("GAA","E"), ("GAC","D"), ("GAT","D"), ("GGG","G"), ("GGA","G"), ("GGC","G"), ("GGT","G"), 
        ("CTG","L"), ("CTA","L"), ("CTC","L"), ("CTT","L"), ("CCG","P"), ("CCA","P"), ("CCC","P"), ("CCT","P"),
        ("CAG","Q"), ("CAA","Q"), ("CAC","H"), ("CAT","H"), ("CGG","R"), ("CGA","R"), ("CGC","R"), ("CGT","R"),
        ("TTG","L"), ("TTA","L"), ("TTC","F"), ("TTT","F"), ("TCG","S"), ("TCA","S"), ("TCC","S"), ("TCT","S"),
        ("TAC","Y"), ("TAT","Y"), ("TGG","W"), ("TGC","C"), ("TGT","C"), ("TAG","Amber/Stop"),
        ("TAA","Ochre/Stop"),("TGA","Opal/Stop")
]

Amin = ["A", "T", "G", "C"]

stop = ["TAG", "TAA", "TGA"]


# %%
len(DNA_codon_table)


# %%
def create_protein(aminos, seq_length, rule=-1):
    protein = []
    tmp = []
    for j in range(0, seq_length):  #generating one specific protein sequence
        if(rule == -1):
            protein.append(aminos[randint(0, len(aminos)-1)])  #DNA sequences
        else:
            tmp = aminos[randint(0, len(aminos)-1)]
            while(Amin[rule % 4] in tmp):
                tmp = aminos[randint(0, len(aminos)-1)]
            protein.append(tmp)
    return protein


# %%
def num_comb(val, codon_dict):
    pos_comb = 0
    for key, value in codon_dict.items():
        if value == val:
            pos_comb += 1
    return pos_comb


# %%
def find_comb(val, codon_dict, rule=-1):
    combs = []
    for key, value in codon_dict.items():
        if value == val:
            if(rule != -1):
                if(not Amin[rule % 4] in key):
                    combs.append(key)
            else:
                combs.append(key)
    return combs


# %%
def create_sequences(protein, num_seq, rule=-1):
    '''
        1. Protein sequence
        2. used_key lists for each amino acid
                           -OR-
           lists of possible key values for each key
    '''
    sequence = []
    tmp = []
    amino_list = []
    for i in range(0, len(protein)):
        amino_list.append(False)
    amino_list[0] = True
    codon_dict = dict(DNA_codon_table)
    #print(codon_dict)
    seq_count = 0
    comb_dict = {}
    #comb_list = []
    for i in range(0, len(protein)):
        #print(codon_dict[protein[i]])
        combs = find_comb(codon_dict[protein[i]], codon_dict, rule)
        #print(type(comb_dict))
        comb_dict[i] = combs
        #comb_list.append(combs)
    #print(comb_dict)
    index = 0
    comb_tracker = [0 for i in range(0,len(protein))]
    #print(comb_tracker)
    while 1:
        for i in range(0, len(protein)):
            if(amino_list[i] == True):
                key = comb_dict[i][seq_count % len(comb_dict[i])]
                #print(key)
                tmp.append(key)
                comb_tracker[i] += 1
            else:
                tmp.append(comb_dict[i][0])
            #print(tmp)
            #print(comb_dict[i])
            #print("length of comb_dict[i] ", len(comb_dict[i]))
            if comb_tracker[i] == len(comb_dict[i]):
                #print("i: ", i)
                if( i != len(protein)-1):
                    amino_list[i+1] = True
                else:
                    amino_list[i] = True
        print(amino_list)
       # print(comb_tracker)
        seq_count += 1
        sequence.append(list(tmp))
        tmp.clear()
        if(seq_count == (num_seq)):
            break
    #print(sequence)
    return sequence


# %%
def create_set(num_aminos, seq_length, num_classes, seq_per_class):
    s = ""
    if num_aminos < 3:
        print("Need more aminos")
        return
    rand_aminos = []
    classes = []
    seq = []
    for i in range(1, num_aminos-3): #-2 because of start and stop codons
        rand_aminos.append(DNA_codon_table[randint(1, 62)][0])  #looking at DNA

    for i in range(0, num_classes):  #generating diffferent proteins
        protein = create_protein(rand_aminos, seq_length, i)
        print("protein ", protein)
        seq_list = create_sequences(protein, seq_per_class, i)
        for j in seq_list:
            j.insert(0, "ATG")
            j.append(choice(stop))
            seq.append(''.join(j))
            classes.append(i)
            #print(j)
        #print(type(seq_new))
    #print(seq)
    return classes, seq


# %%
num_aminos = 64
seq_length = 4500
num_classes = 4
seq_per_class = 30
keys, val = create_set(num_aminos, seq_length, num_classes, seq_per_class)
print(len(keys))
#print(len(val))
#list of tuples (x,y) where x is a string and y is index
fout = str(num_aminos) + '_' + str(seq_length) + '_' + str(num_classes) + '_' + str(seq_per_class)
print(fout)
with open('../data/data%s.csv' % fout, 'w') as f:
#with open('data/64_30_30_10.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['class', 'sequence'])
    for i in range(0, len(keys)):
        writer.writerow([keys[i], val[i]])
'''
try:
    myfile = open('data/data%s.csv' % fout, "r+") # or "a+", whatever you need
except IOError:
    print ("Could not open file!")
'''

# %%


