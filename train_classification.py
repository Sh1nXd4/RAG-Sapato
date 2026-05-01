import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import MultiLabelBinarizer
from collections import Counter

mlflow.set_experiment("Foodhunter_Classification")


# =========================================
#  FUNÇÃO DE AVALIAÇÃO
# =========================================
def avaliar(nome, y_test, pred):
    acc = accuracy_score(y_test, pred)
    prec = precision_score(y_test, pred, zero_division=0)
    rec = recall_score(y_test, pred)
    f1 = f1_score(y_test, pred)

    print("\n" + "="*50)
    print(f" MODELO: {nome}")
    print(f"Acurácia : {acc:.4f}")
    print(f"Precisão : {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-score : {f1:.4f}")
    print("="*50)

    return acc, prec, rec, f1


# =========================================
#  PIPELINE PRINCIPAL
# =========================================
def train_models():

    print("\n INICIANDO TREINAMENTO...\n")

    df = pd.read_parquet('gold/gold_data.parquet')

    print(f" Registros: {len(df)}")

    # =========================================
    #  TARGET (SEM DATA LEAKAGE)
    # =========================================
    df['is_recommended'] = (df['stars'] >= 3.5).astype(int)

    print("\n Distribuição:")
    print(df['is_recommended'].value_counts(normalize=True))

    # =========================================
    #  FEATURES
    # =========================================
    features_base = [
        'review_count',
        'price_range',
        'has_delivery',
        'has_outdoor'
    ]

    df = df.dropna(subset=features_base)

    df['has_delivery'] = df['has_delivery'].astype(int)
    df['has_outdoor'] = df['has_outdoor'].astype(int)

    # =========================================
    #  CATEGORIAS (REDUZIDAS)
    # =========================================
    print("\n Processando categorias...")

    all_categories = [cat for sublist in df['categories_list'] for cat in sublist]
    freq = Counter(all_categories)

    TOP_N = 30
    top_categories = set([cat for cat, _ in freq.most_common(TOP_N)])

    df['categories_filtered'] = df['categories_list'].apply(
        lambda cats: [c for c in cats if c in top_categories]
    )

    mlb = MultiLabelBinarizer()
    categories_encoded = mlb.fit_transform(df['categories_filtered'])

    df_categories = pd.DataFrame(
        categories_encoded,
        columns=mlb.classes_,
        index=df.index
    )

    print(f" Categorias usadas: {len(mlb.classes_)}")

    # =========================================
    # DATASET FINAL
    # =========================================
    X = pd.concat([df[features_base], df_categories], axis=1)
    y = df['is_recommended']

    # =========================================
    # SPLIT
    # =========================================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("\n  Split:")
    print(f"Treino: {len(X_train)} | Teste: {len(X_test)}")

    resultados = {}

    # =========================================
    # NAIVE BAYES
    # =========================================
    print("\n Treinando Naive Bayes...")
    model = GaussianNB()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc, prec, rec, f1 = avaliar("Naive Bayes", y_test, pred)
    resultados["Naive Bayes"] = f1

    # =========================================
    # DECISION TREE
    # =========================================
    print("\n Treinando Decision Tree...")
    model = DecisionTreeClassifier(max_depth=6, class_weight='balanced')
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc, prec, rec, f1 = avaliar("Decision Tree", y_test, pred)
    resultados["Decision Tree"] = f1

    # =========================================
    # REDE NEURAL
    # =========================================
    print("\nTreinando Rede Neural...")
    model = MLPClassifier(max_iter=400)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc, prec, rec, f1 = avaliar("Neural Network", y_test, pred)
    resultados["Neural Network"] = f1

    # =========================================
    # LOGISTIC REGRESSION (COM THRESHOLD)
    # =========================================
    print("\n Treinando Logistic Regression...")

    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_train, y_train)

    #  ajuste de threshold
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob > 0.35).astype(int)

    acc, prec, rec, f1 = avaliar("Logistic Regression", y_test, pred)
    resultados["Logistic Regression"] = f1

    # =========================================
    # MELHOR MODELO
    # =========================================
    melhor = max(resultados, key=resultados.get)

    print("\n MELHOR MODELO:")
    print(f" {melhor}")

    print("\n TREINAMENTO FINALIZADO!\n")


# =========================================
# EXECUÇÃO
# =========================================
if __name__ == "__main__":
    train_models()