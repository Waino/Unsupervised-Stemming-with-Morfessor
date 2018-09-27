#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import codecs
import sys
import morfessor
import flatcat

average_morph_length = float(sys.argv[1])
input_dir = sys.argv[2]
output_dir = sys.argv[3]

def filetowordlist(path, sfx, output, output_freq):
    filedict = {}
    allwordlist = []
    fw = codecs.open(output, 'w', encoding='utf-8')
    for item in os.listdir(path):
        if sfx in item:
            wordlist = []
            for line in codecs.open(path+item, 'r', encoding='utf-8'):
                lines = line.strip().split()
                for word in lines:
                    wd = ''
                    for letter in word:
                        if letter.isalpha():
                            wd = wd+letter
                        else:
                            wd = wd + ' '
                    w = wd.split()
                    for d in w:
                        wordlist.append(d.lower())
                        allwordlist.append(d.lower())
                        fw.write(d.lower() + '\n')
            filedict[item] = wordlist
    print('counting word frequencies ...')
    fw_freq = codecs.open(output_freq, 'w', encoding='utf-8')
    for word in set(allwordlist):
        fw_freq.write(str(allwordlist.count(word)) + ' ' + word + '\n')
    return filedict, allwordlist

print('loading and preprocessing data ...')
files, allwordlist = filetowordlist(input_dir, '.txt', 'TempOut.txt', 'Freq.txt')

def Base_SegModel(data, average_morph_length):
    io = morfessor.MorfessorIO()
    train_data = list(io.read_corpus_file(data))
    baseline_model = morfessor.BaselineModel(corpusweight=1.0)
    updater = morfessor.baseline.MorphLengthCorpusWeight(average_morph_length)
    baseline_model.set_corpus_weight_updater(updater)
    baseline_model.load_data(train_data, count_modifier=lambda x: 1)
    baseline_model.train_batch()

    return baseline_model

print('training the baseline ...')
baseline_model = Base_SegModel('TempOut.txt', average_morph_length)
corpusweight = baseline_model._corpus_coding.weight
print('using corpus weight {}'.format(corpusweight))

def Base_Segmentation(segmodel, fl, output):
    f = codecs.open(fl, 'r', encoding='utf-8')
    fw = codecs.open(output, 'w', encoding='utf-8')
    wordlist = []
    for line in f:
        lines = line.strip().split()
        wordlist.append((line[0], lines[1]))
    for count, word in wordlist:
        seg = segmodel.viterbi_segment(word)
        fw.write(count + ' ')
        for i in range(len(seg[0])):
            fw.write(seg[0][i])
            if len(seg[0][i:]) > 1:
                fw.write(' ' + '+' + ' ')
        fw.write('\n')
    return wordlist

a = Base_Segmentation(baseline_model, 'Freq.txt', 'Seg_output.txt')

print('training the stemming model ...')
def ModelTraining(segmentation_file):
    io = flatcat.FlatcatIO()
    morph_usage = flatcat.categorizationscheme.MorphUsageProperties()
    model = flatcat.FlatcatModel(morph_usage, corpusweight=corpusweight)
    model.add_corpus_data(io.read_segmentation_file(segmentation_file))
    model.initialize_hmm()
    model.train_batch()
    return model

model = ModelTraining('Seg_output.txt')

print('stemming ...')
def Segment(files, model, output_path):
    segdict = {}
    for file in files:
        seglist = []
        fw = codecs.open(output_path + file, 'w', encoding='utf-8')
        wordlist = files[file]
        for word in wordlist:
            ana = model.viterbi_analyze(word)
            for construct in ana[0]:
                if construct.category == 'STM':
                    fw.write(construct.morph + ' ')
                seglist.append(construct.morph)
        segdict[file] = seglist
    return segdict

sg = Segment(files, model, output_dir)
print('Finished!')
