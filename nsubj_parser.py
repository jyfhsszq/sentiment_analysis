#!/usr/bin/python
# coding=utf-8

from tree import Tree
from word_sentiment import SentimentUnit

class NsubjParser(object):
    def __init__(self, tree, words, tags):
        self.tree = tree
        self.words = words
        self.tags = tags

    def parse(self, root, result=[]):
        if self.is_verb(root):
            self.parse_verb(root, result)

    def parse_verb(self, verb, result=[]):
        v_node = self.tree.nodes[verb]
        children = v_node[Tree.CHILDREN_KEY]
        for child in children:
            id = child[Tree.ID]
            if self.is_verb(id):
                self.parse_verb(id, result)

            if self.is_adv(id):
                adv_list = [id]
                self.parse_adj_adv(id, adv_list)
                result.append(SentimentUnit(verb, '', adv_list))

            if self.is_noun(id):
                self.parse_n(id, result)

    def parse_adj_adv(self, ad, result=[]):
        ad_node = self.tree.nodes[ad]
        if Tree.CHILDREN_KEY not in ad_node:
            return
        children = ad_node[Tree.CHILDREN_KEY]
        for child in children:
            id = child[Tree.ID]
            if self.is_adv(id) or self.is_adj(id):
                self.parse_adj_adv(id, result)

    def parse_n(self, n, result=[]):
        n_node = self.tree.nodes[n]
        if Tree.CHILDREN_KEY not in n_node:
            return
        children = n_node[Tree.CHILDREN_KEY]
        for child in children:
            id = child[Tree.ID]
            if self.is_noun(id):
                self.parse_n(id, result)

            adj = -1
            adv_list = []
            if self.is_adj(id):
                adj = id
                self.parse_adj_adv(id, adv_list)

            if adj > 0 or adv_list.__len__() > 0:
               result.append(SentimentUnit(n, adj, adv_list))

    def find_words_list(self, number_list):
        return [self.words[id] for id in number_list]

    def is_verb(self, node_id):
        tag = self.tags[node_id-1][1]
        return tag.startswith('VB')

    def is_adv(self, node_id):
        tag = self.tags[node_id-1][1]
        return tag.startswith('RB')

    def is_noun(self, node_id):
        tag = self.tags[node_id-1][1]
        return tag.startswith('N')

    def is_adj(self, node_id):
        tag = self.tags[node_id-1][1]
        return tag.startswith('JJ')
