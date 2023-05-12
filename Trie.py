class nodeTrie:
    def __init__(self, position: int):
        # Símbolo do nó é a posição do prefixo
        self.position = position
        # Filhos são dois, pois o alfabeto é {0,1}
        self.children = [None, None]


class BinaryTrie:
    def __init__(self):
        self.root = nodeTrie('')  # Raiz da Trie

    # Insere nova string na Trie
    def insertString(self, key: str, position: int):
        observedNode = self.root
        for x in key:
            index = int(x)
            if observedNode.children[index] == None:
                observedNode.children[index] = nodeTrie(position)
            observedNode = observedNode.children[index]

    # Procura por palavra na Trie
    def searchString(self, key: str):
        observedNode = self.root
        for x in key:
            index = int(x)
            if observedNode.children[index] == None:
                return -1
            observedNode = observedNode.children[index]
        return observedNode.position
