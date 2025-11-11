import sqlite3
import json
from flask import Flask, request, jsonify

# Instale o Flask: pip install flask

app = Flask(__name__)

# Este é o nosso "API Gateway" + "Lambda 1 (Recepcionista)"
@app.route("/lance/<string:item_id>", methods=["POST"])
def dar_lance(item_id):
    
    dados = request.get_json()
    user_id = dados['userId']
    valor_lance = dados['valorLance']
    
    try:
        # A Lambda 1 SÓ enfileira o trabalho.
        # Ela insere na nossa "Fila SQS" (a tabela Lances) com status PENDENTE.
        con = sqlite3.connect("leilao.db")
        cur = con.cursor()
        
        cur.execute(
            "INSERT INTO Lances (itemId, userId, valorLance, status) VALUES (?, ?, ?, ?)",
            (item_id, user_id, valor_lance, "PENDENTE")
        )
        con.commit()
        con.close()
        
        print(f"[API] Lance recebido de {user_id} e enfileirado.")
        
        # Responde RÁPIDO para o usuário
        return jsonify({"status": "Lance recebido!"}), 202

    except Exception as e:
        print(f"[API] Erro: {e}")
        return jsonify({"status": "Erro"}), 400

# Roda o servidor de API
if __name__ == "__main__":
    print("Servidor de API (Lambda 1) rodando em http://127.0.0.1:5000")
    app.run(port=5000)