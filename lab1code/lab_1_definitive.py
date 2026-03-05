# Lab1: Codi fet per Leo Aguayo i Aniol Rovirà 

import networkx as nx
import csv
import random
import os

# Tasca 1: Construir el graf

def build_graph(nom_arxiu):
    """
    Construeix un graf no dirigit a partir d'un arxiu CSV d'arestes.
    """
    G = nx.Graph()
    try:
        with open(nom_arxiu, "r", encoding="utf-8") as arxiu:
            lector = csv.reader(arxiu)
            next(lector, None)  # Saltem la capçalera si n'hi ha

            for fila in lector:
                if len(fila) >= 2:
                    node1 = fila[0].strip()
                    node2 = fila[1].strip()
                    if node1 and node2:
                        G.add_edge(node1, node2)

        print(f"Graf carregat: {G.number_of_nodes()} nodes, {G.number_of_edges()} arestes")
        return G

    except FileNotFoundError:
        print(f"Error: No s'ha trobat l'arxiu {nom_arxiu}")
        return None


# Tasca 2: Components BFS

def components_BFS(G):
    # Llistes per controlar els nodes
    Nodes_tots = []
    Nodes_revisar = []
    Llista_revisats = []
    Llista_components = []

    # Posem tots els nodes a la llista
    for node in G.nodes():
        Nodes_tots.append(node)

    # Si no hi ha nodes, retornem llista buida
    if not Nodes_tots:
        return []

    # Comencem amb el primer node
    Node_actual = Nodes_tots.pop(0)
    Llista_revisats.append(Node_actual)
    Component_actual = [Node_actual]

    Buit = False
    Revisar = True

    while not Buit:
        while Revisar:
            # Mirem els veïns del node actual
            for node in G.neighbors(Node_actual):
                if node not in Llista_revisats:
                    Nodes_revisar.append(node)
                    Llista_revisats.append(node)

            # Si hi ha nodes per revisar, agafem el següent
            if Nodes_revisar:
                Node_actual = Nodes_revisar.pop(0)
                Component_actual.append(Node_actual)
                if Node_actual in Nodes_tots:
                    Nodes_tots.remove(Node_actual)
            else:
                # Ja hem acabat aquesta component
                Revisar = False
                Llista_components.append(Component_actual)

        # Mirem si queden més nodes per explorar (nova component)
        if Nodes_tots:
            Node_actual = Nodes_tots.pop(0)
            Llista_revisats.append(Node_actual)
            Component_actual = [Node_actual]
            Revisar = True
        else:
            Buit = True

    return Llista_components


# Tasca 3: Components DFS

def components_DFS(G):
    """
    Troba les components connexes del graf utilitzant DFS.
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

                for vei in G.neighbors(node_revisar):
                    if vei not in llista_revisats and vei not in Nodes_revisar:
                        Nodes_revisar.append(vei)

        llista_components.append(component)
        for node_component in component:
            if node_component in Nodes_totals:
                Nodes_totals.remove(node_component)

    return llista_components


# Tasca 4: Experiment tallant arestes

def experiment_tallant_arestes(nom_arxiu, num_experiments=10):
    """
    Experimenta quantes arestes cal tallar aleatòriament per passar
    d'una component connexa a més d'una component.
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
        component_gran = max(components_inicials, key=len)
        G_original = G_original.subgraph(component_gran).copy()
        print(f"Component més gran: {G_original.number_of_nodes()} nodes, {G_original.number_of_edges()} arestes")

    resultats = []

    for experiment in range(num_experiments):
        print(f"\n--- Experiment {experiment + 1}/{num_experiments} ---")

        # Fem una còpia del graf i barregem les arestes
        G_copia = G_original.copy()
        arestes_originals = list(G_copia.edges())
        random.shuffle(arestes_originals)

        total_arestes = len(arestes_originals)
        salts = 100
        trobat = False
        num_talls = 0

        for i in range(0, total_arestes, salts):
            # Tallem les següents arestes
            limit = min(i + salts, total_arestes)
            for j in range(i, limit):
                if j < len(arestes_originals):
                    G_copia.remove_edge(*arestes_originals[j])
                    num_talls += 1

            # Mirem si ja s'ha dividit
            components_actuals = components_BFS(G_copia)
            if len(components_actuals) > 1:
                print(f"  Divisió entre {i} i {limit}")
                trobat = True

                # Ara busquem exactament on – tornem enrere
                G_copia = G_original.copy()
                for k in range(i):
                    G_copia.remove_edge(*arestes_originals[k])

                # I anem un a un dins l'interval
                for k in range(i, limit):
                    G_copia.remove_edge(*arestes_originals[k])
                    components_refinat = components_BFS(G_copia)
                    if len(components_refinat) > 1:
                        num_talls = k + 1
                        components_actuals = components_refinat
                        break

                break

        # Si no s'ha trobat encara, possiblement cal tallar-les totes
        if not trobat:
            num_talls = total_arestes
            components_actuals = components_BFS(G_copia)

        # Mostrem resultats d'aquest experiment
        if len(components_actuals) > 1:
            print(f"✓ Primera divisió trobada després de tallar {num_talls} arestes")
            print(f"  Nombre de components: {len(components_actuals)}")
            mides = sorted([len(c) for c in components_actuals], reverse=True)
            print(f"  Mides de les components: {mides[:5]}{'...' if len(mides) > 5 else ''}")
        else:
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
        print(f"Rang: {max(resultats) - min(resultats)} arestes")
        print(f"Percentatge respecte total: {(sum(resultats) / len(resultats)) / G_original.number_of_edges() * 100:.2f}%")
        print(f"{'='*50}\n")

    return resultats


# BONUS: Experiment eliminant nodes amb estratègia

def experiment_eliminant_nodes_estrategic(nom_arxiu, num_experiments=10):
    """
    BONUS: elimina nodes començant pels de grau més alt
    i mira quan es trenca la component principal.
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
    print(f"Estratègia: Eliminar nodes amb més connexions primer")

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
            # Ordenem els nodes pel seu grau (de major a menor)
            nodes_ordenats = sorted(G_copia.nodes(), key=lambda n: G_copia.degree(n), reverse=True)

            # Eliminem el que té més connexions
            node_a_eliminar = nodes_ordenats[0]
            grau_eliminat = G_copia.degree(node_a_eliminar)
            G_copia.remove_node(node_a_eliminar)
            num_eliminats += 1

            # Comprovem si s'ha dividit el graf
            if G_copia.number_of_nodes() > 0:
                components_actuals = components_BFS(G_copia)
                num_components_actual = len(components_actuals)

                if num_components_actual > 1:
                    print(f"✓ Divisió després d'eliminar {num_eliminats} nodes")
                    print(f"  (últim node tenia grau {grau_eliminat})")
                    print(f"  Components: {num_components_actual}")

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
        print(f"=== RESULTATS NODES ESTRATÈGIC ===")
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
    BONUS: elimina nodes de forma ALEATÒRIA (comparació).
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


# Funció principal per executar proves bàsiques

if __name__ == "__main__":
    directori_actual = os.path.dirname(os.path.abspath(__file__))
    arxiu = os.path.join(directori_actual, "lastfm_asia_edges.csv")

    print("=== TASCA 1: Construir el graf ===")
    G = build_graph(arxiu)

    if G is not None:
        print("\n=== TASQUES 2 i 3: Trobar components ===")
        components_bfs = components_BFS(G)
        components_dfs = components_DFS(G)
        print(f"Nombre de components (BFS): {len(components_bfs)}")
        print(f"Nombre de components (DFS): {len(components_dfs)}")

        if components_bfs:
            mides = sorted([len(c) for c in components_bfs], reverse=True)
            print(f"Mides de les 5 components més grans: {mides[:5]}")

        print("\n=== TASCA 4: Experiment tallant arestes ===")
        experiment_tallant_arestes(arxiu, num_experiments=5)

        # BONUS (descomenta si vols provar-ho):
        # comparar_estrategies(arxiu)
