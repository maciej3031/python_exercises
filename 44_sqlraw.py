import sqlite3

# utworzenie połączenia z bazą danych przechowywaną na dysku lub w pamięci (':memory')

con = sqlite3.connect('test.db')  # pisząc (':memory') będziemy przechowywać bazę danych w pamięci RAM


# dostep do kolumn przez indeksy i przez nazwy
con.row_factory = sqlite3.Row


# utworzenie obiektu kursora
cur = con.cursor()


# tworzenie tabel
cur.execute("DROP TABLE IF EXISTS klasa;")

cur.execute("""CREATE TABLE IF NOT EXISTS klasa (
                id INTEGER PRIMARY KEY ASC,
                nazwa varchar(250) NOT NULL,
                profil varchar(250) DEFAULT ''
            )""")

cur.executescript("""DROP TABLE IF EXISTS uczen;
                    CREATE TABLE IF NOT EXISTS uczen(
                        id INTEGER PRIMARY KEY ASC,
                        imie varchar(250) NOT NULL,
                        nazwisko varchar(250) NOT NULL,
                        klasa_id INTEGER NOT NULL,
                        FOREIGN KEY(klasa_id) REFERENCES klasa(id)
                    )""")

# Wstawiamy jeden rekord danych
cur.execute('INSERT INTO klasa VALUES(NULL, ?, ?);',('1A', 'matematyczny'))
cur.execute('INSERT INTO klasa VALUES(NULL, ?, ?);',('1B', 'humanistyczny'))

# Wykonujemy zapytanie SQL, które pobierze id klasy "1A" z tabeli "klasa".
cur.execute('SELECT id FROM klasa WHERE nazwa = ?', ('1A',))
klasa_id = cur.fetchone()[0]

# tupla uczniowie zawiera tuple z danymi poszczególnych uczniów
uczniowie = (
    (None, 'Tomasz', 'Nowak', klasa_id),
    (None, 'Jan', 'Kos', klasa_id),
    (None, 'Piotr', 'Kowalski', klasa_id)
)

# Wstawiamy wiele rekordów
cur.executemany('INSERT INTO uczen VALUES(?,?,?,?)', uczniowie)

# Zatwierdzamy zmiany w bazie
con.commit()


# Pobieranie danych z bazy
def czytajdane():
    """Funkcja pobiera i wyświetla dane z bazy."""
    cur.execute("SELECT uczen.id,imie,nazwisko,nazwa FROM uczen, klasa WHERE uczen.klasa_id=klasa.id")
    data = cur.fetchall()
    return data
    for uczen in data:
        print(uczen['id'], uczen['imie'], uczen['nazwisko'], uczen['nazwa'])
    # print("")

print(czytajdane())


# Zmiana klasy ucznia o identyfikatorze 2
cur.execute('SELECT id FROM klasa WHERE nazwa = ?', ('1B',))
klasa_id = cur.fetchone()[0]
print(klasa_id)
cur.execute('UPDATE uczen SET klasa_id = ? WHERE id = ?', (klasa_id, 2))


# Usunięcie ucznia o identyfikatorze 3
cur.execute('DELETE FROM uczen WHERE id = ?', (3,))
con.commit()

czytajdane()


con.close()





