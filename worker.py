import sqlite3
import time
from decimal import Decimal

def processar_fila():
    con = sqlite3.connect("leilao.db")
    con.row_factory = sqlite3.Row # Para acessar por nome da coluna
    cur = con.cursor()
    
    print("\n[WORKER] Procurando lances PENDENTES...")
    
    # 1. Pega os lances da "fila" (tabela Lances)
    cur.execute("SELECT * FROM Lances WHERE status = 'PENDENTE'")
    lances_pendentes = cur.fetchall()
    
    if not lances_pendentes:
        con.close()
        return

    # 2. REQUISITO: Loop "FOR"
    for lance in lances_pendentes:
        print(f"[WORKER] Processando lance {lance['lanceId']}...")
        
        try:
            # 3. Busca o lance atual do item no "DynamoDB"
            cur.execute("SELECT lance_atual FROM ItensLeilao WHERE itemId = ?", (lance['itemId'],))
            item = cur.fetchone()
            
            lance_atual = Decimal(str(item['lance_atual']))
            novo_lance = Decimal(str(lance['valorLance']))

            # 4. REQUISITO: Lógica "IF/ELSE"
            if novo_lance > lance_atual:
                # Se o novo lance for maior, atualiza o item
                cur.execute(
                    "UPDATE ItensLeilao SET lance_atual = ?, ultimo_lance_usuario = ? WHERE itemId = ?",
                    (str(novo_lance), lance['userId'], lance['itemId'])
                )
                print(f"[WORKER] SUCESSO: Item {lance['itemId']} atualizado para {novo_lance}.")
            else:
                # Se for menor ou igual, não faz nada (só marca como processado)
                print(f"[WORKER] FALHA: Lance {novo_lance} é menor que o atual {lance_atual}.")

            # 5. Marca o lance como processado (remove da "fila")
            cur.execute("UPDATE Lances SET status = 'PROCESSADO' WHERE lanceId = ?", (lance['lanceId'],))
            con.commit() # Salva as mudanças

        except Exception as e:
            print(f"[WORKER] Erro ao processar lance {lance['lanceId']}: {e}")
            con.rollback() # Desfaz

    con.close()

# Roda o "Worker" (Lambda 2) em loop infinito
if __name__ == "__main__":
    print("Worker (Lambda 2) iniciado. Verificando a fila a cada 10 segundos...")
    while True:
        processar_fila()
        time.sleep(10) # Espera 10 segundos