#!/usr/bin/python
# coding=utf-8

b = [(8, 7), (5, 3), (2, 1), (1, 1), (3, 1), (7, 7), (4, 3), (6, 3), (9, 7)]
a = [(u'ROOT', 0, 2), (u'nsubj', 2, 1), (u'det', 4, 3), (u'nsubj', 12, 4), (u'case', 7, 5), (u'nmod:poss', 7, 6), (u'nmod', 4, 7), (u'advmod', 12, 8), (u'mwe', 8, 9), (u'nsubj', 12, 10), (u'aux', 12, 11), (u'ccomp', 2, 12), (u'dobj', 12, 13), (u'advmod', 16, 14), (u'case', 16, 15), (u'nmod', 12, 16), (u'nsubj', 18, 17), (u'acl:relcl', 16, 18), (u'dobj', 18, 19), (u'punct', 2, 20)]
c = [(u'advmod', 0, 1), (u'advmod', 0, 2), (u'det', 0, 3), (u'advmod1', 1, 4), (u'advmod', 1, 5), (u'advmod', 2, 6), (u'nmod', 2, 7), (u'advmod2', 3, 8)]

class Tree(object):
    ID = 'id'
    CHILDREN_KEY = 'children'
    RELATION_KEY = 'relation'
    MAX_INT = 999999999

    def __init__(self, nodelist):
        forest = []
        self.nodes = {}

        for relation, node_id, child_id in nodelist:
            #create current node if necessary
            if node_id not in self.nodes:
                node = { self.ID : node_id}
                self.nodes[node_id] = node
            else:
                node = self.nodes[node_id]

            if node_id == 0:
                # add node to forest
                forest.append( node )

            # create parent node if necessary
            if child_id not in self.nodes:
                child = { self.ID : child_id, self.RELATION_KEY : relation}
                self.nodes[child_id] = child
            else:
                child = self.nodes[child_id]
                child[self.RELATION_KEY] = relation
            # create children if necessary
            if self.CHILDREN_KEY not in node:
                node[self.CHILDREN_KEY] = []
            #add node to children of parent
            node[self.CHILDREN_KEY].append(child)
        #print nodes[12]
        #return forest[0]

    def find_advs(self, node_id):
        core_node = self.nodes[node_id]
        # result = []
        # children = core_node[self.CHILDREN_KEY]
        # adv_list = [child for child in children if cmp(child[self.RELATION_KEY], "advmod") is 0]
        # if adv_list:
        #     for adv in adv_list:
        #         result.append(adv)

        return self.broad_search(core_node)



    '''
    def broad_search(self, node=None):
        if node:
            r = [node]
            if self.CHILDREN_KEY in node:
                children = node[self.CHILDREN_KEY]
                l =  [child for child in children if cmp(child[self.RELATION_KEY], "advmod") is 0]
                if l:
                    for item in l:
                        r.append(self.broad_search(item))
                else:
                    return r
            else:
                return r
    '''

    def broad_search(self, node=None, res=[]):
        if node:
            if self.CHILDREN_KEY in node:
                children = node[self.CHILDREN_KEY]
                l = [child for child in children if cmp(child[self.RELATION_KEY], "advmod") is 0 or cmp(child[self.RELATION_KEY], "mwe") is 0]
                res.extend(l)
                for item in l:
                    self.broad_search(item, res)

    '''
    :param nsubj relaton core words Id
    :return [(core node id, sub tree scope->min node Id, sub tree scope->max node Id), ...]
             example: [(2, 1, 2), (12, 3, 13)]
    '''
    def find_sub_tree(self, core_ids):
        sub_tree_node_list = []

        for i, core_id in enumerate(core_ids):
            end = Tree.MAX_INT
            if (i+1) < core_ids.__len__():
                end = self.find_min_node(self.nodes[core_ids[i+1]], Tree.MAX_INT)-1
                sub_tree_node_list.append((core_id, self.find_min_node(self.nodes[core_id], Tree.MAX_INT), end))
            else:
                sub_tree_node_list.append((core_id, self.find_min_node(self.nodes[core_id], Tree.MAX_INT), end))
        return sub_tree_node_list


    def find_sub_tree_by_nsubj(self, nsubj_list):
        nsubj_governor_list = [y for (x, y, z) in nsubj_list]
        return self.find_sub_tree(nsubj_governor_list)


    def find_min_node(self, node, min_value):
        #min_value = 999999999
        if self.CHILDREN_KEY in node:
            children = node[self.CHILDREN_KEY]
            for child in children:
                if(child[self.ID] < min_value):
                    min_value = child[self.ID]
                    return self.find_min_node(child, min_value)

        return min_value



if __name__ == '__main__':
    c = [(u'advmod', 0, 1), (u'advmod', 0, 2), (u'det', 0, 3), (u'advmod1', 1, 4), (u'advmod', 1, 5), (u'advmod', 2, 6),
         (u'nmod', 2, 7), (u'advmod2', 3, 8)]
    a = [(u'ROOT', 0, 2), (u'nsubj', 2, 1), (u'det', 4, 3), (u'nsubj', 12, 4), (u'case', 7, 5), (u'nmod:poss', 7, 6),
         (u'nmod', 4, 7), (u'advmod', 12, 8), (u'mwe', 8, 9), (u'nsubj', 12, 10), (u'aux', 12, 11), (u'ccomp', 2, 12),
         (u'dobj', 12, 13), (u'advmod', 16, 14), (u'case', 16, 15), (u'nmod', 12, 16), (u'nsubj', 18, 17),
         (u'acl:relcl', 16, 18), (u'dobj', 18, 19), (u'punct', 2, 20)]

    tree = Tree(a)
    node = tree.nodes[12]
    result = []
    tree.broad_search(node, result)
    print [node[Tree.ID] for node in result]
    print result

    min_value = Tree.MAX_INT
    print tree.find_min_node(tree.nodes[12], min_value)

    print tree.find_sub_tree([2, 12, 16])

    print tree.find_sub_tree_by_nsubj([(u'nsubj', 2, 1),(u'nsubj', 12, 4),(u'nsubj', 12, 10),(u'nsubj', 18, 17)])
