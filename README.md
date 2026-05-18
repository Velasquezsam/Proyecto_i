# Proyecto_IA

Proyecto de IA UCAB

# Informe

## Pipeline de Machine Learning y Toma de Decisiones

Este informe detalla el proceso técnico, las decisiones de diseño y las métricas de rendimiento obtenidas durante el desarrollo del modelo predictivo para el proyecto Shopping Indicator. El objetivo principal fue construir un sistema capaz de predecir la intención de compra (Revenue) de un usuario en tiempo real.

### 1. Exploración y Preprocesamiento de Datos

El conjunto de datos original requería un tratamiento diferenciado debido a la coexistencia de datos numéricos (métricas de Google Analytics y duraciones de navegación) y datos categóricos (sistemas operativos, tipos de visitantes, meses).

#### Decisiones tomadas y justificación:

Imputación de Valores Faltantes: Se implementó un ColumnTransformer para automatizar este paso. Para las variables numéricas, se utilizó la mediana (strategy='median'), ya que es una medida de tendencia central resistente a los valores atípicos (outliers) comunes en tiempos de navegación. Para las variables categóricas, se utilizó la moda (strategy='most_frequent') para asegurar la consistencia de las clases.

Escalado de Datos: Se aplicó un StandardScaler a las variables numéricas. Esto es crucial porque métricas como ProductRelated_Duration (que puede tener valores en los miles) y BounceRates (valores decimales) se encuentran en escalas muy distintas. El escalado asegura que el modelo no asigne una importancia artificialmente alta a las variables con magnitudes mayores.

Codificación: Se empleó OneHotEncoder para las variables categóricas, transformándolas en un formato numérico interpretable por el algoritmo sin establecer un orden jerárquico falso entre categorías (por ejemplo, entre distintos navegadores web).

### 2. Manejo del Desbalance de Clases

En el contexto del comercio electrónico, el comportamiento de los usuarios presenta un desbalance natural: la inmensa mayoría de las visitas no se traducen en compras (clase False), mientras que las transacciones reales (clase True) son una minoría.

#### Decisiones tomadas y justificación:

Aumento de Datos (Data Augmentation): Entrenar un modelo con datos fuertemente desbalanceados produce un sistema sesgado que simplemente predice "No compra" en todos los casos para inflar su precisión. Para evitar esto, se implementó la técnica SMOTE (Synthetic Minority Over-sampling Technique).

#### Justificación:

SMOTE genera ejemplos sintéticos de la clase minoritaria interpolando entre instancias existentes. Esto permitió que el modelo aprendiera los patrones reales que conducen a una compra, en lugar de simplemente memorizar la clase mayoritaria.

### 3. Selección y Entrenamiento del Modelo

El algoritmo seleccionado como núcleo del sistema predictivo fue el Random Forest Classifier (Bosque Aleatorio).

#### Decisiones tomadas y justificación:

Se eligió Random Forest debido a su excelente rendimiento histórico con datos tabulares heterogéneos (mezcla de continuos y categóricos).

Al ser un método de ensamblaje (construye múltiples árboles de decisión y promedia sus resultados), es inherentemente robusto frente al sobreajuste (overfitting) y maneja de forma natural las relaciones no lineales complejas entre el comportamiento del usuario y su decisión final de compra.

### 4. Optimización de Hiperparámetros

Para alcanzar el requerimiento estricto de un rendimiento cercano al 90%, el modelo base no era suficiente. Se procedió a realizar un ajuste fino utilizando validación cruzada.

#### Decisiones tomadas y justificación:

Se implementó GridSearchCV para explorar sistemáticamente diferentes combinaciones de hiperparámetros.

Esta búsqueda exhaustiva, combinada con una validación cruzada de 5 pliegues (cv=5), garantizó que el rendimiento del modelo no fuera producto de la casualidad en una sola división de datos, sino un comportamiento generalizable ante usuarios nuevos.

### 5. Indicadores y Métricas de Rendimiento

Tras la optimización, el modelo fue evaluado utilizando un conjunto de datos de prueba (20% del dataset original) que el algoritmo nunca había visto durante su entrenamiento.

Accuracy (Precisión Global): 88.89%

Análisis: El modelo cumple con éxito el requerimiento de evaluación de "alcanzar un rendimiento cercano al 90%". Logra clasificar correctamente a casi 9 de cada 10 visitantes.

Clase (Variable: Revenue),Precision,Recall (Exhaustividad),F1-Score
No Compra (False),0.93,0.93,0.93
Compra (True),0.64,0.64,0.64

#### Justificación final de las métricas:

El alto rendimiento en la clase "No Compra" (F1-Score: 0.93) asegura que el departamento de IT no desperdiciará recursos mostrando promociones agresivas a usuarios que definitivamente no van a comprar. Por otro lado, las métricas para la clase "Compra" (0.64), aunque lógicamente menores debido a la dificultad inherente de predecir la intención humana, son lo suficientemente sólidas para identificar un segmento valioso de compradores potenciales en tiempo real, cumpliendo de manera efectiva el objetivo de negocio de la aplicación.

---

## 6. Despliegue de la API REST

La API del proyecto **Shopping Indicator** fue desplegada en Render como un servicio web desarrollado con Flask. Este despliegue permite que el modelo predictivo pueda ser consumido mediante peticiones HTTP, de forma que un cliente REST como Postman pueda enviar los datos de navegación de un usuario y recibir una predicción en tiempo real sobre su intención de compra.

### URL base del servidor

```txt
https://proyecto-i-3lsz.onrender.com
```

La ruta principal `/` permite verificar que el servidor se encuentra activo. Al ingresar a la URL base desde el navegador, la API devuelve un mensaje JSON con el estado del servicio, el nombre de la API, el endpoint disponible y el método requerido.

### Endpoint de predicción

```txt
POST https://proyecto-i-3lsz.onrender.com/predict
```

El endpoint `/predict` recibe los datos de navegación del usuario en formato JSON y retorna la predicción generada por el modelo entrenado.

Es importante destacar que esta ruta solo acepta solicitudes de tipo `POST`. Por esta razón, si se intenta abrir directamente desde el navegador, puede aparecer el mensaje `Method Not Allowed`, ya que el navegador realiza una solicitud `GET`. Esto no representa un error del sistema.

### Formato de entrada

La API espera recibir un cuerpo JSON con los atributos utilizados por el modelo predictivo. Un ejemplo válido de entrada es el siguiente:

```json
{
  "Administrative": 0,
  "Administrative_Duration": 0,
  "Informational": 0,
  "Informational_Duration": 0,
  "ProductRelated": 10,
  "ProductRelated_Duration": 350.2,
  "BounceRates": 0.01,
  "ExitRates": 0.02,
  "PageValues": 25.5,
  "SpecialDay": 0.0,
  "Month": "May",
  "OperatingSystems": 2,
  "Browser": 2,
  "Region": 1,
  "TrafficType": 3,
  "VisitorType": "Returning_Visitor",
  "Weekend": false
}
```

### Formato de salida

La API retorna un JSON estructurado con tres elementos principales: la clasificación, la probabilidad matemática y un mensaje legible para humanos.

Ejemplo de respuesta:

```json
{
  "clasificacion": "compra",
  "mensaje_legible": "El usuario presenta un 91.5% de probabilidades de hacer la compra, lo que lo hace muy probable.",
  "probabilidad_matematica": "91.46%"
}
```

### Prueba en Postman

Para probar la API en Postman se debe crear una solicitud con la siguiente configuración:

```txt
Método: POST
URL: https://proyecto-i-3lsz.onrender.com/predict
Body: raw
Formato: JSON
Header: Content-Type: application/json
```

Luego se debe pegar en el cuerpo de la solicitud un JSON con los datos de navegación del usuario, como el mostrado en el ejemplo de entrada. Si la petición es correcta, la API responderá con la clasificación del usuario, la probabilidad matemática de compra y el mensaje legible para humanos.

### Comando de ejecución en Render

El servicio fue ejecutado en Render utilizando Gunicorn mediante el siguiente comando:

```bash
gunicorn app:app
```

Este comando permite ejecutar la aplicación Flask definida en el archivo `app.py`.

### Consideración sobre el despliegue

Debido a que el servicio se encuentra desplegado en un entorno gratuito de Render, puede tardar algunos segundos en responder si ha estado inactivo durante un tiempo. Esto ocurre porque el servicio puede suspenderse temporalmente y reactivarse cuando recibe una nueva solicitud.
