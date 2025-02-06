import networkx as nx
import matplotlib.pyplot as plt

class Nodo:
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo
        self.hijos = []

class ArbolParseo:
    def __init__(self):
        self.contador_nodos = 0
        self.grafo = nx.DiGraph()
        self.posiciones = {}

    def construir_arbol(self, expresion):
        pila = []
        raiz = Nodo("<exp>", "<exp>")
        actual = raiz

        for char in expresion:
            if char == '(':
                nuevo = Nodo("<exp>", "<exp>")
                actual.hijos.append(nuevo)
                pila.append(actual)
                actual = nuevo  
            elif char.isnumeric():
                actual.hijos.append(Nodo(char, "num"))
            elif char in "+-*/":
                actual.hijos.append(Nodo(char, "<op>"))
            elif char == ')':
                if pila:
                    actual = pila.pop()

        return raiz

    def agregar_nodos_al_grafo(self, nodo, parent=None, x=0, y=0, nivel=1):
        self.contador_nodos += 1
        nodo_id = self.contador_nodos

        etiqueta = nodo.tipo 
        self.grafo.add_node(nodo_id, label=etiqueta)
        self.posiciones[nodo_id] = (x, -y)

        if parent is not None:
            self.grafo.add_edge(parent, nodo_id)

        if nodo.hijos:
            n = len(nodo.hijos)
            for i, hijo in enumerate(nodo.hijos):
                self.agregar_nodos_al_grafo(hijo, nodo_id, x + (i - (n - 1) / 2) * 2 / nivel, y + 1, nivel + 1)

    def dibujar_arbol(self):
        labels = nx.get_node_attributes(self.grafo, "label")
        plt.figure(figsize=(8, 5))
        nx.draw(self.grafo, self.posiciones, with_labels=True, labels=labels, node_color="white", edge_color="black", node_size=3000, font_size=10, font_weight="bold")
        plt.show()


expresiones = ["(2+1)*3", "2*(3+1)", "(2*1)+(4+5)", "((5+2)-3*(2*1))"]

for exp in expresiones:
    arbol = ArbolParseo()
    raiz = arbol.construir_arbol(exp)
    arbol.agregar_nodos_al_grafo(raiz)
    arbol.dibujar_arbol()

