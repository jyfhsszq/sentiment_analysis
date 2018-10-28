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
            if(self.is_verb(id)):
                self.parse_verb(id, result)

            if(self.is_adv(id)):
                adv_list = [id]
                self.parse_adv(id, adv_list)
                result.append(SentimentUnit(verb, '', adv_list))

    def parse_adv(self, adv, result=[]):
        adv_node = self.tree.nodes[adv]
        if Tree.CHILDREN_KEY in adv_node:
            children = adv_node[Tree.CHILDREN_KEY]
            for child in children:
                id = child[Tree.ID]
                if self.is_adv(id):
                    self.parse_adv(id, result)

    def find_words_list(self, number_list):
        return [self.words[id] for id in number_list]

    def is_verb(self, node_id):
        tag = self.tags[node_id-1][1]
        return tag.startswith('VB')

    def is_adv(self, node_id):
        tag = self.tags[node_id-1][1]
        return tag.startswith('RB')
