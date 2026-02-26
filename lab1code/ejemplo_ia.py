import networkx as nx
import csv
from collections import deque
import random

# Tasca 1: Construir el graf

def build_graph(nom_arxiu):
    """
    Construeix un graf no dirigit a partir d'un arxiu CSV d'arestes.
    
    Args:
        nom_arxiu: Ruta de l'arxiu CSV amb les arestes (format: node1,node2)
    
    Returns:
        Graf de NetworkX amb les arestes carregades
    """
    G = nx.Graph()
    
    try:
        with open(nom_arxiu, 'r') as arxiu:
            lector = csv.reader(arxiu)
            next(lector)  # Saltem la capçalera si n'hi ha
            
            for fila in lector:
                if len(fila) >= 2:
                    node1 = fila[0].strip()
                    node2 = fila[1].strip()
                    G.add_edge(node1, node2)
        
        print(f"Graf carregat: {G.number_of_nodes()} nodes, {G.number_of_edges()} arestes")
        return G
    
    except FileNotFoundError:
        print(f"Error: No s'ha trobat l'arxiu {nom_arxiu}")
        return None


# Tasca 2: Components BFS

def components_BFS(G):
    """
    Troba les components connexes del graf utilitzant BFS.
    
    Args:
        G: Graf de NetworkX
    
    Returns:
        Llista de llistes amb els nodes de cada component connexa
    """
    Nodes_totals = []
    Nodes_revisar = []
    llista_revisats = []
    llista_components = []
    
    for node in G.nodes:
        Nodes_totals.append(node)
    
    while len(Nodes_totals) > 0:
        node = Nodes_totals[0]
        Nodes_revisar.append(node)
        llista_revisats.append(node)
        component = []
        
        while len(Nodes_revisar) > 0:
            node_revisar = Nodes_revisar.pop(0)  # BFS: primer que entra, primer que surt
            component.append(node_revisar)
            
            for veí in G.neighbors(node_revisar):
                if veí not in llista_revisats and veí not in Nodes_revisar:
                    Nodes_revisar.append(veí)
                    llista_revisats.append(veí)
        
        llista_components.append(component)
        for node_component in component:
            if node_component in Nodes_totals:
                Nodes_totals.remove(node_component)
    
    return llista_components


# Tasca 3: Components DFS

def components_DFS(G):
    """
    Troba les components connexes del graf utilitzant DFS.
    
    Args:
        G: Graf de NetworkX
    
    Returns:
        Llista de llistes amb els nodes de cada component connexa
    """
    Nodes_totals = []
    Nodes_revisar = []
    llista_revisats = []
    llista_components = []
    
    for node in G.nodes:
        Nodes_totals.append(node)
    
    while len(Nodes_totals) > 0:
        node = Nodes_totals[0]
        Nodes_revisar.append(node)
        component = []
        
        while len(Nodes_revisar) > 0:
            node_revisar = Nodes_revisar.pop()  # DFS: últim que entra, primer que surt
            
            if node_revisar not in llista_revisats:
                llista_revisats.append(node_revisar)
                component.append(node_revisar)
                
                for veí in G.neighbors(node_revisar):
                    if veí not in llista_revisats and veí not in Nodes_revisar:
                        Nodes_revisar.append(veí)
        
        llista_components.append(component)
        for node_component in component:
            if node_component in Nodes_totals:
                Nodes_totals.remove(node_component)
    
    return llista_components


# Tasca 4: Experiment tallant arestes

def experiment_tallant_arestes(nom_arxiu, num_experiments=10):
    """
    Experimenta quantes arestes cal tallar aleatòriament per passar 
    d'una component connexa a dues components.
    
    Estratègia d'optimització:
    - Comprova cada 10 talls al principi (quan és improbable la divisió)
    - Comprova cada tall quan estem prop del mínim teòric
    
    Args:
        nom_arxiu: Arxiu CSV amb les arestes del graf
        num_experiments: Nombre d'experiments a realitzar
    
    Returns:
        Llista amb el nombre d'arestes tallades en cada experiment
    """
    G_original = build_graph(nom_arxiu)
    if G_original is None:
        print("Error: No s'ha pogut carregar el graf")
        return []
    
    # Comprovem el nombre inicial de components
    components_inicials = components_BFS(G_original)
    num_components_inicial = len(components_inicials)
    
    print(f"\n=== INICI DE L'EXPERIMENT ===")
    print(f"Graf carregat: {G_original.number_of_nodes()} nodes, {G_original.number_of_edges()} arestes")
    print(f"Components connexes inicials: {num_components_inicial}")
    
    # Si ja té més d'una component, agafem la més gran
    if num_components_inicial > 1:
        print(f"El graf ja té {num_components_inicial} components.")
        print("Treballarem amb la component més gran.")
        
        # Agafem la component més gran
        component_gran = max(components_inicials, key=len)
        G_original = G_original.subgraph(component_gran).copy()
        print(f"Component més gran: {G_original.number_of_nodes()} nodes, {G_original.number_of_edges()} arestes")
    
    resultats = []
    
    for experiment in range(num_experiments):
        print(f"\n--- Experiment {experiment + 1}/{num_experiments} ---")
        
        # Fem una còpia del graf per cada experiment
        G_copia = G_original.copy()
        arestes = list(G_copia.edges())
        random.shuffle(arestes)
        
        num_talls = 0
        total_arestes = len(arestes)
        
        # Tallem arestes una a una fins trobar una divisió
        for aresta in arestes:
            G_copia.remove_edge(*aresta)
            num_talls += 1
            
            # OPTIMITZACIÓ: No comprovem cada tall al principi
            # Els primers 80% de talls, comprovem cada 10
            # L'últim 20%, comprovem cada tall
            if num_talls < total_arestes * 0.8:
                if num_talls % 10 != 0:
                    continue
            
            # Comprovem si s'ha dividit el graf
            components_actuals = components_BFS(G_copia)
            num_components_actual = len(components_actuals)
            
            if num_components_actual > 1:
                print(f"✓ Primera divisió trobada després de tallar {num_talls} arestes")
                print(f"  Nombre de components: {num_components_actual}")
                
                # Mostrem les mides de les components
                mides = sorted([len(c) for c in components_actuals], reverse=True)
                print(f"  Mides de les components: {mides[:5]}{'...' if len(mides) > 5 else ''}")
                
                resultats.append(num_talls)
                break
        
        if num_talls == len(arestes):
            print(f"S'han tallat totes les arestes ({num_talls})")
            resultats.append(num_talls)
    
    # Mostrem estadístiques finals
    if resultats:
        print(f"\n{'='*50}")
        print(f"=== RESULTATS DE L'EXPERIMENT ===")
        print(f"{'='*50}")
        print(f"Experiments realitzats: {len(resultats)}")
        print(f"Mitjana d'arestes tallades: {sum(resultats) / len(resultats):.2f}")
        print(f"Mínim: {min(resultats)} arestes")
        print(f"Màxim: {max(resultats)} arestes")
        print(f"Desviació: {max(resultats) - min(resultats)} arestes")
        print(f"Percentatge respecte total: {(sum(resultats) / len(resultats)) / G_original.number_of_edges() * 100:.2f}%")
        print(f"{'='*50}\n")
    
    return resultats


# BONUS: Experiment eliminant nodes amb estratègia

def experiment_eliminant_nodes_estrategic(nom_arxiu, num_experiments=10):
    """
    BONUS: Experimenta eliminant nodes de forma estratègica.
    
    Estratègia: Eliminar primer els nodes amb menys connexions (grau baix).
    Hipòtesi: Els nodes amb poc grau són més fàcils de desconnectar
    i podrien dividir el graf més ràpidament.
    
    Args:
        nom_arxiu: Arxiu CSV amb les arestes del graf
        num_experiments: Nombre d'experiments a realitzar
    
    Returns:
        Llista amb el nombre de nodes eliminats en cada experiment
    """
    G_original = build_graph(nom_arxiu)
    if G_original is None:
        print("Error: No s'ha pogut carregar el graf")
        return []
    
    # Comprovem el nombre inicial de components
    components_inicials = components_BFS(G_original)
    num_components_inicial = len(components_inicials)
    
    print(f"\n=== INICI DE L'EXPERIMENT (NODES ESTRATÈGIC) ===")
    print(f"Graf carregat: {G_original.number_of_nodes()} nodes")
    print(f"Components connexes inicials: {num_components_inicial}")
    print(f"Estratègia: Eliminar nodes amb GRAU BAIX primer")
    
    # Si ja té més d'una component, agafem la més gran
    if num_components_inicial > 1:
        component_gran = max(components_inicials, key=len)
        G_original = G_original.subgraph(component_gran).copy()
        print(f"Component més gran: {G_original.number_of_nodes()} nodes")
    
    resultats = []
    
    for experiment in range(num_experiments):
        print(f"\n--- Experiment {experiment + 1}/{num_experiments} ---")
        
        G_copia = G_original.copy()
        num_eliminats = 0
        
        while G_copia.number_of_nodes() > 0:
            # ESTRATÈGIA: Ordenem nodes per grau (de menor a major)
            nodes_ordenats = sorted(G_copia.nodes(), key=lambda n: G_copia.degree(n))
            
            # Eliminem el node amb menys connexions
            node_a_eliminar = nodes_ordenats[0]
            G_copia.remove_node(node_a_eliminar)
            num_eliminats += 1
            
            # Comprovem si s'ha dividit el graf
            if G_copia.number_of_nodes() > 0:
                components_actuals = components_BFS(G_copia)
                num_components_actual = len(components_actuals)
                
                if num_components_actual > 1:
                    print(f"✓ Primera divisió trobada després d'eliminar {num_eliminats} nodes")
                    print(f"  Nombre de components: {num_components_actual}")
                    
                    mides = sorted([len(c) for c in components_actuals], reverse=True)
                    print(f"  Mides de les components: {mides[:5]}{'...' if len(mides) > 5 else ''}")
                    
                    resultats.append(num_eliminats)
                    break
        
        if num_eliminats == G_original.number_of_nodes():
            print(f"S'han eliminat tots els nodes ({num_eliminats})")
            resultats.append(num_eliminats)
    
    # Mostrem estadístiques finals
    if resultats:
        print(f"\n{'='*50}")
        print(f"=== RESULTATS DE L'EXPERIMENT (NODES ESTRATÈGIC) ===")
        print(f"{'='*50}")
        print(f"Experiments realitzats: {len(resultats)}")
        print(f"Mitjana de nodes eliminats: {sum(resultats) / len(resultats):.2f}")
        print(f"Mínim: {min(resultats)} nodes")
        print(f"Màxim: {max(resultats)} nodes")
        print(f"Percentatge respecte total: {(sum(resultats) / len(resultats)) / G_original.number_of_nodes() * 100:.2f}%")
        print(f"{'='*50}\n")
    
    return resultats


def experiment_eliminant_nodes_aleatori(nom_arxiu, num_experiments=10):
    """
    BONUS: Experimenta eliminant nodes de forma ALEATÒRIA (comparació).
    
    Args:
        nom_arxiu: Arxiu CSV amb les arestes del graf
        num_experiments: Nombre d'experiments a realitzar
    
    Returns:
        Llista amb el nombre de nodes eliminats en cada experiment
    """
    G_original = build_graph(nom_arxiu)
    if G_original is None:
        return []
    
    components_inicials = components_BFS(G_original)
    num_components_inicial = len(components_inicials)
    
    print(f"\n=== EXPERIMENT (NODES ALEATORI) ===")
    print(f"Estratègia: Eliminar nodes ALEATÒRIAMENT")
    
    if num_components_inicial > 1:
        component_gran = max(components_inicials, key=len)
        G_original = G_original.subgraph(component_gran).copy()
    
    resultats = []
    
    for experiment in range(num_experiments):
        print(f"\n--- Experiment {experiment + 1}/{num_experiments} ---")
        
        G_copia = G_original.copy()
        nodes = list(G_copia.nodes())
        random.shuffle(nodes)
        
        num_eliminats = 0
        
        for node in nodes:
            G_copia.remove_node(node)
            num_eliminats += 1
            
            if G_copia.number_of_nodes() > 0:
                components_actuals = components_BFS(G_copia)
                num_components_actual = len(components_actuals)
                
                if num_components_actual > 1:
                    print(f"✓ Primera divisió després d'eliminar {num_eliminats} nodes")
                    resultats.append(num_eliminats)
                    break
        
        if num_eliminats == len(nodes):
            resultats.append(num_eliminats)
    
    if resultats:
        print(f"\n=== RESULTATS (NODES ALEATORI) ===")
        print(f"Mitjana de nodes eliminats: {sum(resultats) / len(resultats):.2f}")
        print(f"Mínim: {min(resultats)} nodes")
        print(f"Màxim: {max(resultats)} nodes\n")
    
    return resultats


# Funció principal per comparar estratègies (BONUS)

def comparar_estrategies(nom_arxiu):
    """
    BONUS: Compara les diferents estratègies d'eliminació.
    """
    print("\n" + "="*60)
    print("COMPARACIÓ D'ESTRATÈGIES")
    print("="*60)
    
    # Experiment 1: Tallar arestes aleatòriament
    print("\n1. TALLANT ARESTES ALEATÒRIAMENT:")
    resultats_arestes = experiment_tallant_arestes(nom_arxiu, num_experiments=5)
    
    # Experiment 2: Eliminar nodes amb grau baix
    print("\n2. ELIMINANT NODES (GRAU BAIX PRIMER):")
    resultats_nodes_estrategic = experiment_eliminant_nodes_estrategic(nom_arxiu, num_experiments=5)
    
    # Experiment 3: Eliminar nodes aleatòriament
    print("\n3. ELIMINANT NODES (ALEATORI):")
    resultats_nodes_aleatori = experiment_eliminant_nodes_aleatori(nom_arxiu, num_experiments=5)
    
    # Comparació final
    print("\n" + "="*60)
    print("COMPARACIÓ FINAL")
    print("="*60)
    
    if resultats_arestes:
        print(f"Arestes (aleatori): Mitjana = {sum(resultats_arestes)/len(resultats_arestes):.2f}")
    
    if resultats_nodes_estrategic:
        print(f"Nodes (grau baix):  Mitjana = {sum(resultats_nodes_estrategic)/len(resultats_nodes_estrategic):.2f}")
    
    if resultats_nodes_aleatori:
        print(f"Nodes (aleatori):   Mitjana = {sum(resultats_nodes_aleatori)/len(resultats_nodes_aleatori):.2f}")
    
    print("="*60 + "\n")


# Codi d'exemple per executar
if __name__ == "__main__":
    # Exemple d'ús
    arxiu = "lastfm_asia_edges.csv"
    
    # Tasca 1: Construir el graf
    print("=== TASCA 1: Construir el graf ===")
    G = build_graph(arxiu)
    
    if G is not None:
        # Tasca 2 i 3: Trobar components
        print("\n=== TASQUES 2 i 3: Trobar components ===")
        components_bfs = components_BFS(G)
        components_dfs = components_DFS(G)
        print(f"Nombre de components (BFS): {len(components_bfs)}")
        print(f"Nombre de components (DFS): {len(components_dfs)}")
        
        # Mostrem les mides de les 5 components més grans
        if components_bfs:
            mides = sorted([len(c) for c in components_bfs], reverse=True)
            print(f"Mides de les 5 components més grans: {mides[:5]}")
        
        # Tasca 4: Experiment
        print("\n=== TASCA 4: Experiment tallant arestes ===")
        experiment_tallant_arestes(arxiu, num_experiments=5)
        
        # BONUS: Comparar estratègies (descomenta per executar - tarda més)
        # print("\n=== BONUS: Comparar estratègies ===")
        # comparar_estrategies(arxiu)

