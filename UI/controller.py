import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""

        try:
            durata=int(self._view.txt_durata.value)*60*1000
            self._model.build_graph(durata)
            self._view.dd_album.options.clear()
            for node in self._model._node_list:
                self._view.dd_album.options.append(ft.DropdownOption(
                    key=node.id,
                    content=ft.Text(node.title)))
            self._view.lista_visualizzazione_1.controls.append(ft.Text(self._model.G))
            self._view.update()


        except ValueError:
            self._view.show_alert('La durata inserita non è valida. Inserire un numero.')

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""



    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        album_id = self._view.dd_album.value
        componente_connessa = self._model.get_connected_component(album_id)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Dimensione Componente {len(componente_connessa)}'))
        durata = 0
        for node in componente_connessa:
            durata += node.durata
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Durata Totale: {durata} minuti'))
        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        durata_max= int(self._view.txt_durata_totale.value)
        album_id = self._view.dd_album.value
        album_partenza= self._model._node_dict[int(album_id)]
        lista_album, durata_totale= self._model._cerca_massimo_cammino(durata_max, album_partenza)
        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f'set trovato:{len(lista_album)} album, Durata Totale: {durata_totale}'))
        for album in lista_album:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f'{album}'))
        self._view.update()

