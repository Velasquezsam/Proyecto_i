from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# 1. Cargar el modelo entrenado
# Asegúrate de que el nombre coincida exactamente con tu archivo .pkl
modelo = joblib.load('shopping_indicator_model_V2.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 2. Recibir los datos del cliente en formato JSON
        datos_entrada = request.get_json()
        
        # Convertir el JSON en un DataFrame de Pandas (el formato que espera el modelo)
        df_entrada = pd.DataFrame([datos_entrada])
        
        # 3. Realizar la predicción y obtener la probabilidad
        prediccion = modelo.predict(df_entrada)[0] # Devuelve True/False o 1/0 dependiendo de cómo lo entrenaste
        probabilidades = modelo.predict_proba(df_entrada)[0] 
        
        # Asumiendo que la clase 1 (o True) es "compra" y está en la posición 1 del arreglo de probabilidades
        probabilidad_compra = probabilidades[1] * 100
        
        # 4. Estructurar la respuesta según los requerimientos
        clasificacion = "compra" if prediccion else "no compra"
        
        # Lógica para el mensaje legible ("human readable entry")
        if probabilidad_compra > 80:
            mensaje = f"El usuario presenta un {probabilidad_compra:.1f}% de probabilidades de hacer la compra, lo que lo hace muy probable."
        elif probabilidad_compra > 50:
            mensaje = f"El usuario presenta un {probabilidad_compra:.1f}% de probabilidades de hacer la compra, lo que lo hace bastante probable."
        else:
            mensaje = f"El usuario presenta un {probabilidad_compra:.1f}% de probabilidades de hacer la compra, es poco probable que realice una transacción."
            
        # 5. Armar el JSON de salida estricto
        respuesta_json = {
            "clasificacion": clasificacion,
            "probabilidad_matematica": f"{probabilidad_compra:.2f}%",
            "mensaje_legible": mensaje
        }
        
        return jsonify(respuesta_json), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # El servidor correrá en el puerto 5000 por defecto
    app.run(debug=True)