#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from random import *


# In[2]:


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

stop = ["TAG", "TAA", "TGA"]


# In[3]:


len(DNA_codon_table)


# In[4]:


def create_protein(aminos, seq_length):
    protein = []
    for j in range(0, seq_length):  #generating one specific protein sequence
        protein.append(aminos[randint(0, len(aminos)-1)])  #DNA sequences
    return protein


# In[5]:


def num_comb(val, codon_dict):
    pos_comb = 0
    for key, value in codon_dict.items():
        if value == val:
            pos_comb += 1
    return pos_comb


# In[6]:


def find_comb(val, codon_dict):
    combs = []
    for key, value in codon_dict.items():
        if value == val:
            combs.append(key)
    return combs


# In[7]:


def create_sequences(protein, num_seq):
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
    for i in range(0, len(protein)):
        #print(codon_dict[protein[i]])
        combs = find_comb(codon_dict[protein[i]], codon_dict)
        #print(type(comb_dict))
        comb_dict[i] = combs
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
                if( i != len(protein)):
                    amino_list[i+1] = True
                else:
                    amino_list[i] = True
        #print(amino_list)
       # print(comb_tracker)
        seq_count += 1
        sequence.append(list(tmp))
        tmp.clear()
        if(seq_count == (num_seq)):
            break
    #print(sequence)
    return sequence


# In[8]:


def create_set(num_aminos, seq_length, num_classes, seq_per_class):
    s = ""
    if num_aminos < 3:
        print("Need more aminos")
        return
    rand_aminos = []
    classes = {}
    for i in range(1, num_aminos-3): #-2 because of start and stop codons
        rand_aminos.append(DNA_codon_table[randint(1, 62)][0])  #looking at DNA
    for i in range(0, num_classes):  #generating diffferent proteins
        seq_new = []
        protein = create_protein(rand_aminos, seq_length)
        #print(protein)
        seq = create_sequences(protein, seq_per_class)
        for j in seq:
            j.insert(0, "ATG")
            j.append(choice(stop))
            seq_new.append(''.join(j))
            #print(j)
        #print(type(seq_new))
        classes[i] = seq_new
    return classes


# In[9]:


create_set(20,10, 6, 8)
#list of tuples (x,y) where x is a string and y is index


# In[ ]:




