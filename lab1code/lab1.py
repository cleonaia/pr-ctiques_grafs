import networkx as nx

# Tasca 1: Construir el graf
def build_graph(nom_arxiu):
  G=nx.graph()
  try:
    arxiu=open(nom_arxiu, 'r')
  
  except FileNotFoundError:
    raise FileNotFoundError
  
  else:
    arxiu.readline()
    for line in arxiu:
      Aresta=list(line.split(','))
      G.add_edge(Aresta)
    return G
    
# Tasca 2: Components BFS

def components_BFS(G):
  Nodes_tots=[]
  Nodes_revisar=[]
  Llista_revisats=[]
  Llista_components=[]
  for node in G.nodes():
    Nodes_tots.append(node)
  Node_actual=Nodes_tots[0]
  Llista_components.append([Node_actual])
  Buit=False
  Revisar=True
  Component=1
  while not Buit:
    while Revisar:
      for node in all_neighbors(Node_actual)
        if node not in Llista_revisats:
          Nodes_revisar.append()
      
      Llista_revisats.append(Node_actual)
      Nodes_tots.pop(Node_actual)
      
      if len(Llista_components)<Component:
        Llista_components.append([Node_actual])
      else:
        Llista_components[Component].append(Node_actual)

      Nodes_revisar=Nodes_revisar[1:]
      if Nodes_revisar == []:
        Revisar=False
      else:
        Node_actual=Nodes_revisar[0]
    if Nodes_tots !=[]:
      Node_actual=Nodes_tots[0]
    else:
      Buit=True

# Tasca 3: Components DFS
def components_DFS(G):


# Tasca 4: Experiment tallant arestes
def experiment_cut_edges():
