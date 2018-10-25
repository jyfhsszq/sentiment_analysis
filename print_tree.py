class Node:
    def __init__(self, value='$', left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __nonzero__(self):
        return self.value != '$'

    def __str__(self):
        buf, out = [self], []
        while buf:
            out.append("{}".format([node.value for node in buf]))
            if any(node for node in buf):
                children = []
                for node in buf:
                    for subnode in (node.left, node.right):
                        children.append(subnode if subnode else Node())
                buf = children
            else:
                break
        return "\n".join(out)

if __name__ == "__main__":
    root = Node(1, Node(2, Node(4)), Node(3, Node(5), Node(6)))
    print root