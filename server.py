import time
from flask import Flask, jsonify

app = Flask(__name__)
inventario = {"stock": 3, "vendidos": 0}

@app.route("/comprar")
def comprar():
    if inventario["stock"] <= 0:
        return jsonify(error="Sin stock"), 409
    
    time.sleep(0.1)  
    
    inventario["stock"] -= 1
    inventario["vendidos"] += 1
    return jsonify(ok=True, stock_restante=inventario["stock"])

if __name__ == '__main__':
    app.run(debug=True)
