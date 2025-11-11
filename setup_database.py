import sqlite3

# Conecta ao banco (vai criar o arquivo 'leilao.db')
con = sqlite3.connect("leilao.db")
cur = con.cursor()

# 1. Tabela de Itens (Nosso "DynamoDB")
cur.execute("""
    CREATE TABLE IF NOT EXISTS ItensLeilao (
        itemId TEXT PRIMARY KEY,
        nome TEXT,
        lance_atual REAL DEFAULT 0,
        ultimo_lance_usuario TEXT
    )
""")

# 2. Tabela de Lances (Nossa "Fila SQS")
cur.execute("""
    CREATE TABLE IF NOT EXISTS Lances (
        lanceId INTEGER PRIMARY KEY AUTOINCREMENT,
        itemId TEXT,
        userId TEXT,
        valorLance REAL,
        status TEXT  -- (PENDENTE, PROCESSADO)
    )
""")

# Insere um item de teste
try:
    cur.execute("INSERT INTO ItensLeilao (itemId, nome) VALUES ('item123', 'Playstation 5')")
except sqlite3.IntegrityError:
    pass # Item já existe

con.commit()
con.close()

print("Banco 'leilao.db' criado com sucesso.")