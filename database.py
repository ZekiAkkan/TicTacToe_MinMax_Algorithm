import sqlite3

class DataBase:
    
    def __init__(self):
        self.conn = sqlite3.connect("game_database.db")
        self.cursor = self.conn.cursor()
        self.__tabloOlustur()

    def __tabloOlustur(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS MoveTablo (h1 INT, h2 INT, h3 INT, h4 INT, h5 INT, h6 INT, h7 INT, h8 INT, h9 INT)")
        self.conn.commit()

    def veriEkle(self, h1, h2, h3, h4, h5, h6, h7, h8, h9):
        if not self.hamleVarMi(h1, h2, h3, h4, h5, h6, h7, h8, h9):
            self.cursor.execute("INSERT INTO MoveTablo (h1, h2, h3, h4, h5, h6, h7, h8, h9) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (h1, h2, h3, h4, h5, h6, h7, h8, h9))
            self.conn.commit()

    def hamleVarMi(self, h1, h2, h3, h4, h5, h6, h7, h8, h9):
        self.cursor.execute("SELECT * FROM MoveTablo WHERE h1=? AND h2=? AND h3=? AND h4=? AND h5=? AND h6=? AND h7=? AND h8=? AND h9=?",
                            (h1, h2, h3, h4, h5, h6, h7, h8, h9))
        return self.cursor.fetchone() is not None

    def get_all_moves(self):
        self.cursor.execute("SELECT * FROM MoveTablo")
        return self.cursor.fetchall()
