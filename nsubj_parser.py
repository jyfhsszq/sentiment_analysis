#!/usr/bin/python
# coding=utf-8

from tree import Tree
from word_sentiment import SentimentUnit

class NsubjParser(object):
    def __init__(self, tree, words, tags):
        self.tree = tree
        self.words = words
        self.tags = tags

    def parse(self, root, start, end, sentiment_result=[]):
        if self.is_verb(root):
            self.parse_verb(root, start, end, sentiment_result)

        if self.is_noun(root):
            self.parse_n(root, start, end, sentiment_result)

    def parse_verb(self, verb, start, end, result=[]):
        if verb < start or verb > end:
            return

        v_node = self.tree.nodes[verb]
        if Tree.CHILDREN_KEY not in v_node:
            return

        children = v_node[Tree.CHILDREN_KEY]
        adv_list = []
        for child in children:
            id = child[Tree.ID]
            if self.is_verb(id):
                self.parse_verb(id, start, end, result)

            if self.is_adv(id):
                adv_list.append([self.words[id-1]])
                self.parse_adj_adv(id, start, end, adv_list)

            if self.is_noun(id):
                self.parse_n(id, start, end, result)

        result.append(SentimentUnit(self.words[verb - 1], '', adv_list))


    def parse_adj_adv(self, ad, start, end, ad_result=[]):
        if ad < start or ad > end:
            return

        ad_node = self.tree.nodes[ad]
        if Tree.CHILDREN_KEY not in ad_node:
            return
        children = ad_node[Tree.CHILDREN_KEY]
        for child in children:
            id = child[Tree.ID]
            if self.is_adv(id) or self.is_adj(id):
                ad_result.append(id)
                self.parse_adj_adv(id, start, end, ad_result)

    def parse_n(self, n, start, end, result=[]):
        if n < start or n > end:
            return

        n_node = self.tree.nodes[n]
        if Tree.CHILDREN_KEY not in n_node:
            return
        children = n_node[Tree.CHILDREN_KEY]
        adj = -1
        adv_list = []
        for child in children:
            id = child[Tree.ID]
            if self.is_noun(id):
                self.parse_n(id, start, end, result)

            if self.is_adj(id):
                adj = id
                self.parse_adj_adv(id, start, end, adv_list)

            if self.is_verb(id) and child[Tree.RELATION_KEY] in ['acl']:
                self.parse_verb(id, start, end, result)

        if adj > 0:
            result.append(SentimentUnit(self.words[n-1], self.words[adj-1], adv_list))
        else:
            result.append(SentimentUnit(self.words[n-1], '', adv_list))

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
