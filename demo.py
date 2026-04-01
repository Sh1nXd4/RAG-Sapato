import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import os

# Configure S3/MinIO credentials
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minio123"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"

mlflow.set_tracking_uri("http://localhost:3000")
mlflow.set_experiment("meu_experimento_1")

with mlflow.start_run():
    X, y = make_regression(n_samples=100, n_features=1, noise=0.1)
    model = LinearRegression()
    model.fit(X, y)

    mlflow.log_param("coeficiente", model.coef_[0])
    mlflow.log_metric("score", model.score(X, y))
    mlflow.sklearn.log_model(model, "modelo")

    print(f"Modelo salvo no MLflow: {mlflow.get_artifact_uri()}")