from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def read_album(durata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select a.id, a.title, a.artist_id, sum(t.milliseconds) as durata
                    from album a, track t
                    where a.id = t.album_id 
                    group by a.id, a.artist_id, a.title 
                    having sum(t.milliseconds) > %s """

        cursor.execute(query, (durata,))

        for row in cursor:
            result.append(Album(row['id'],row['title'],row['artist_id'], row['durata']/60000))

        cursor.close()
        conn.close()
        return result

    def read_connection(dizionario_nodi, durata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.album_id as album1 , t1.album_id as album2
                    from playlist_track pt, playlist_track pt1, track t, track t1
                    where pt.playlist_id = pt1.playlist_id 
                    and pt.track_id < pt1.track_id
                    and t.id = pt.track_id 
                    and t1.id= pt1.track_id	
                    and t.album_id != t1.album_id
                    and t.album_id in (select a.id
                                        from album a, track t2
                                        where a.id = t2.album_id
                                        group by a.id
                                        having sum(t2.milliseconds) > %s)
                    and t1.album_id in  (select a1.id
                                        from album a1, track t3
                                        where a1.id = t3.album_id
                                        group by a1.id
                                        having sum(t3.milliseconds) > %s) """

        cursor.execute(query, (durata,durata))

        for row in cursor:
            result.append([dizionario_nodi[row['album1']], dizionario_nodi[row['album2']]])

        cursor.close()
        conn.close()
        return result