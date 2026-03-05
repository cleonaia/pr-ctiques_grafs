import networkx as nx
import time, json


# Tasca 1: Construir el graf
def build_graph(nom_arxiu):
  G=nx.Graph()
  if '.json' in nom_arxiu:
    try:            
      with open(nom_arxiu, "r") as fitxer:
        data = json.load(fitxer)

      for node, neighbors in data.items():
        for n in neighbors:
           G.add_edge(int(node), n)
    
    except FileNotFoundError:
      raise FileNotFoundError
    
  else:    
    try:
      with open(nom_arxiu, 'r') as arxiu:
        arxiu.readline()
        for line in arxiu:
          if line[:-1]=='\n':
            line=line[:-1]
          Aresta=line.strip().split(',')
          G.add_edge(Aresta[0], Aresta[1])
  
    except FileNotFoundError:
      raise FileNotFoundError
    
  return G
    
# Tasca 2: Components BFS

def components_BFS(G):
  t0=time.time()
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

      
      if Nodes_revisar == []:
        Revisar=False
      else:
        Node_actual=Nodes_revisar.pop(0)
    if Nodes_tots !=[]:
      Node_actual=Nodes_tots[0]
      Llista_revisats.append(Node_actual)
      Component+=1
      Revisar=True
    else:
      Buit=True
  t1=time.time()
  return Llista_components, t1-t0


# Tasca 3: Components DFS
def components_DFS(G):
  t2=time.time()
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
  t3=time.time()
  return Llista_components, t3-t2
