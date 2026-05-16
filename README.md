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
