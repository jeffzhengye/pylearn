# -*- coding: utf-8 -*-
import argparse
import gzip
import math
import numpy
import numpy as np
from numpy.linalg import norm
import re
import sys, os
import codecs
from multiprocessing import Pool, cpu_count, Manager
from functools import partial
import logging
from scipy.spatial import distance
import heapq
from blist import sortedlist
from profilehooks import profile
from copy import deepcopy
sys.path.append("../")
from util.text_normalizer import clean_word
from bidict import bidict
import cPickle
import gzip
import os
import sys
import timeit
import itertools

import theano
import theano.tensor as T
from copy import deepcopy

class Rotrofit(object):
	def __init__(self, q_old, alpha, gazs):
		self.q_old = q_old
		self.q_new = theano.shared(
			value = deepcopy(q_old).astype(theano.config.floatX),
			name='q_new',
            borrow=True
			)
		self.alpha = alpha
		self.gazs = gazs

	def norm2(self, ma):
		return T.sqrt(T.sum(ma**2, axis=1))

	def cost(self):
		z = self.q_new - self.q_old
		costA = T.sum(self.norm2(z))*self.alpha
		for i in range(self.q_old.shape[0]):
			num_neighbours = T.sum(self.gaz[i])
			z1 = self.q_new - self.q_new[i]
			costA += self.gazs[i] * self.norm2(z1) / num_neighbours
		return costA


def train(q_input, gazs_input, alpha_input, learning_rate=0.01, iters=10):
	q_old = T.matrix('q_old')
	gazs_relation = T.matrix('gazs_relation')
	alpha = T.lscalar('alpha')
	retrofitter = Rotrofit(q_old, alpha, gazs_relation)
	cost = retrofitter.cost()
	g_q_new = T.grad(cost=cost, wrt=retrofitter.q_new)
	updates = [(retrofitter.q_new, retrofitter.q_new - learning_rate * g_q_new)]
    train_model = theano.function(
        inputs=[],
        outputs=cost,
        updates=updates,
        givens={
            q_old: q_input,
            gazs_relation: gazs_input, 
            alpha: alpha_input
        }
    )
    for i in range(iters):
    	cost_ = train_model()
    	print cost_


def main(input, base=None, dimension=200):

    wordVecs = read_word_vecs(input)

    if base:
      print 'use read_gaz_lexicon'
      lexicon, term_id_bidict = read_gaz_lexicon(base = base)
    else:
      raise Exception('parameter format error.')
      #lexicon = read_lexicon(lexicon, wordVecs)
    if not lexicon:
        logger.info("active_gazetteers is empty")
        return
    num_of_work_terms = len(term_id_bidict)
    inv = term_id_bidict.inv

    gaz_weights = np.zeros((num_of_work_terms, num_of_work_terms), dtype=numpy.int)
	for gaz_set in lexicon.values():
		ids = [term_id_bidict[x] for x in gaz_set]
		for i, j in itertools.combinations(ids, 2);
			gaz_weights[i, j] = 1

    work_embedding = []
    for i in range(num_of_work_terms):
    	gaz_word = inv[i]
    	if gaz_word in wordVecs:
    		work_embedding.append(wordVecs[gaz_word])
		else:
			work_embedding.append(np.random.ranf(dimension).astype('float32', copy=False))
	work_embedding = np.vstack(work_embedding)

	train(work_embedding, gaz_weights, 1)


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=None, help="Input word vecs")
    parser.add_argument("-l", "--lexicon", type=str, default=None, help="gaz base dir")
    parser.add_argument("-o", "--output", type=str, help="Output word vecs")
    parser.add_argument("-n", "--numiter", type=int, default=10, help="Num iterations")
    args = parser.parse_args()
    main(args.input, base=args.lexicon)