"""
@author: Aniol Rovirà & Leo Aguayo
"""

import networkx as nx
import time, json, random


# Tasca 1: construim un graf no dirigit des d'un CSV d'arestes o, si cal,
# des d'un JSON que guarda cada node amb els seus veins.

def build_graph(nom_arxiu):
  # G sera el graf final que retornara la funcio.
  G=nx.Graph()

  # Si el nom del fitxer conte .json, assumim format node -> llista de veins
  
  if '.json' in nom_arxiu:
    try:
      with open(nom_arxiu, "r") as fitxer:
        data = json.load(fitxer)

      # Afegim una aresta per cada relacio que apareix al JSON
      for node, neighbors in data.items():
        for n in neighbors:
           G.add_edge(int(node), n)

    except FileNotFoundError:
      raise FileNotFoundError

  else:
    try:
      with open(nom_arxiu, 'r') as arxiu:
        # La primera linia es la capcalera del CSV
        arxiu.readline()
        for line in arxiu:
          if line[:-1]=='\n':
            line=line[:-1]
          Aresta=line.strip().split(',')
          G.add_edge(Aresta[0], Aresta[1])

    except FileNotFoundError:
      raise FileNotFoundError

  return G


# Tasca 2: BFS agrupa els nodes per components connexes explorant-los en amplada

def components_BFS(G):
  Time_BFS1=time.time()

  # Nodes_tots guarda els nodes que encara no s'han assignat definitivament a una component
  # Nodes_revisar fa de cua BFS i Llista_revisats evita repetir nodes
  
  Nodes_tots=[]
  Nodes_revisar=[]
  Llista_revisats=[]
  Llista_components=[]

  for node in G.nodes():
    Nodes_tots.append(node)

  if Nodes_tots ==[]:
    return Llista_components
  else:
    Node_actual=Nodes_tots[0]

  Llista_revisats.append(Node_actual)
  Buit=False
  Revisar=True
  Component=1

  # El bucle extern serveix per recorre totes les components del graf
  
  while not Buit:
    # El bucle intern recorre nomes la component actual
    while Revisar:
      for node in G.neighbors(Node_actual):
        if node not in Llista_revisats:
          Nodes_revisar.append(node)
          Llista_revisats.append(node)

      # Un cop processat el node actual, l'eliminem del conjunt general i l'afegim a la component que estem construint
      
      Nodes_tots.remove(Node_actual)

      if len(Llista_components)<Component:
        Llista_components.append([Node_actual])
      else:
        Llista_components[Component-1].append(Node_actual)

      # En BFS es processa el primer node pendent, com una cua
      
      if Nodes_revisar == []:
        Revisar=False
      else:
        Node_actual=Nodes_revisar.pop(0)

    # Si queden nodes sense visitar, iniciem la seguent component
    
    if Nodes_tots !=[]:
      Node_actual=Nodes_tots[0]
      Llista_revisats.append(Node_actual)
      Component+=1
      Revisar=True
    else:
      Buit=True

  Time_BFS2=time.time()
  print("Temps que ha trigat BFS: ",Time_BFS2-Time_BFS1)
  return Llista_components


# Tasca 3: DFS segueix la mateixa idea, pero explorant sempre l'ultim pendent

def components_DFS(G):
  Time_DFS1=time.time()

  # Fem servir les mateixes estructures que a BFS, pero la llista de pendents es tractara com una pila per obtenir un recorregut en profunditat
  
  Nodes_tots=[]
  Nodes_revisar=[]
  Llista_revisats=[]
  Llista_components=[]

  for node in G.nodes():
    Nodes_tots.append(node)

  if Nodes_tots ==[]:
    return Llista_components
  else:
    Node_actual=Nodes_tots[0]

  Llista_revisats.append(Node_actual)
  Buit=False
  Revisar=True
  Component=1

  # Igual que a BFS, el bucle extern canvia de component i l'intern explora completament la component en que ens trobem
  
  while not Buit:
    while Revisar:
      for node in G.neighbors(Node_actual):
        if node not in Llista_revisats:
          Nodes_revisar.append(node)
          Llista_revisats.append(node)

      Nodes_tots.remove(Node_actual)

      if len(Llista_components)<Component:
        Llista_components.append([Node_actual])
      else:
        Llista_components[Component-1].append(Node_actual)

      # En DFS es processa l'ultim node pendent, com una pila
      if Nodes_revisar == []:
        Revisar=False
      else:
        Node_actual=Nodes_revisar.pop()

    if Nodes_tots!=[]:
      Node_actual=Nodes_tots[0]
      Llista_revisats.append(Node_actual)
      Component+=1
      Revisar=True
    else:
      Buit=True

  Time_DFS2=time.time()
  print("Temps que ha trigat DFS: ", Time_DFS2-Time_DFS1)
  return Llista_components


# Tasca 4: tallem arestes aleatories una a una fins que el graf deixa de ser connex

def experiment_cut_edges(G):
  Time_experiment1=time.time()

  # Primer comprovem si el graf ja estava separat abans de fer cap tall
  
  Nombre_comp=components_DFS(G)
  Count=0

  if len(Nombre_comp)!=1:
    print("No hi ha una sola component")

  else:
    # Treballem directament sobre el graf rebut i anem eliminant arestes en un ordre aleatori fins que apareixen dues o mes components
    
    Tallar=True
    edges=list(G.edges())
    random.shuffle(edges)

    while Tallar:
      # En aquesta versio es talla una aresta cada vegada
      edges_tallar=edges[:1]
      edges=edges[1:]
      for edge in edges_tallar:
          G.remove_edge(edge[0], edge[1])
      Count+=1

      # Després de cada tall, comprovem si encara hi ha una sola component
      
      Nombre_comp=components_DFS(G)
      if len(Nombre_comp)!=1:
          Tallar=False

  Time_experiment2=time.time()
  print("Temps que ha trigat l'experiment de tallar arestes: ", Time_experiment2-Time_experiment1)
  return Count


# Carreguem el dataset petit i executem la prova principal

nom_arxiu='lastfm_asia_edges.csv'
G=build_graph(nom_arxiu)

# NetworkX imprimeix un resum curt del nombre de nodes i arestes del graf

print(G)

# Bloc de prova opcional per comparar BFS i DFS manualment

LLCBFS=components_BFS(G)
LLCDFS=components_DFS(G)
print(LLCBFS, len(LLCBFS))
print(LLCDFS, len(LLCDFS))
print(len(LLCBFS), len(LLCDFS))


Count=experiment_cut_edges(G)
print("\n", Count)


# Experiment 
