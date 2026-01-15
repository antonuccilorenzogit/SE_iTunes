import copy
from ctypes import HRESULT

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._node_list= []
        self._node_dict= {}
        self._edge_list= []
        self._result = []
        self._durata_reale = 0

    def build_graph(self,durata):
        self.G = nx.Graph()
        self._node_list = DAO.read_album(durata)

        for album in self._node_list:
            self.G.add_node(album)
            self._node_dict[album.id] = album

        self._edge_list = DAO.read_connection(self._node_dict, durata)
        self.G.add_edges_from(self._edge_list)

        print(self.G)

    def get_connected_component(self, album_id):
        album= self._node_dict[int(album_id)]
        return nx.bfs_tree(self.G, album)

    def _cerca_massimo_cammino(self, durata_max, album_partenza):
        self._result = [album_partenza]
        self._durata_reale = 0
        self.ricorsione([album_partenza],album_partenza.durata,durata_max )

        return self._result, self._durata_reale

    def ricorsione(self, risultato_parziale,durata_parziale, durata_max):
        if durata_parziale > durata_max:
            return
        if len(risultato_parziale) > len(self._result):
            self._result= copy.deepcopy(risultato_parziale)
            self._durata_reale= copy.deepcopy(durata_parziale)
            print(self._result)
            print(self._durata_reale)

        for vicino in self.G.neighbors(risultato_parziale[-1]):
            print(vicino.title)
            if vicino not in risultato_parziale:
                risultato_parziale.append(vicino)
                self.ricorsione(risultato_parziale,durata_parziale + vicino.durata, durata_max)
                risultato_parziale.pop()



