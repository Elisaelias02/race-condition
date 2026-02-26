from flask import Flask, request, jsonify
from models import db, User, Wallet, PromoCode
import time

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    email = request.json["email"]
    
    # ¿Hay vulnerabilidad aquí?
    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify(error="Email ya registrado"), 409
    
    user = User(email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user_id=user.id), 201


@app.route("/transfer", methods=["POST"])
def transfer():
    sender_id = request.json["from"]
    receiver_id = request.json["to"]
    amount = request.json["amount"]
    
    # ¿Hay vulnerabilidad aquí?
    sender = Wallet.query.get(sender_id)
    receiver = Wallet.query.get(receiver_id)
    
    if sender.balance < amount:
        return jsonify(error="Fondos insuficientes"), 400
    
    time.sleep(0.05)  # procesamiento
    sender.balance -= amount
    receiver.balance += amount
    db.session.commit()
    return jsonify(ok=True)


@app.route("/apply-promo", methods=["POST"])
def apply_promo():
    user_id = request.json["user_id"]
    code = request.json["code"]
    
    # ¿Hay vulnerabilidad aquí?
    promo = PromoCode.query.filter_by(code=code).first()
    
    if promo.times_used >= promo.max_uses:
        return jsonify(error="Codigo agotado"), 400
    
    promo.times_used += 1
    # aplicar descuento al usuario...
    db.session.commit()
    return jsonify(ok=True, discount=promo.discount)
