"""
Locustfile - Define cómo cargar la API
Load testing script para validar performance
"""

from locust import HttpUser, task, between
import json
import random


class APIUser(HttpUser):
    """
    Simula un usuario real interactuando con API
    Cada "usuario" ejecuta tasks aleatoriamente
    """

    wait_time = between(1, 3)  # Wait 1-3 sec entre requests

    def on_start(self):
        """Ejecuta una vez cuando el usuario inicia"""
        self.prediction_id = None

    @task(3)  # Weight 3 (execute 3x más que otros)
    def predict(self):
        """POST /predict - La operación más común"""
        payload = {
            "square_feet": random.randint(500, 10000),
            "bedrooms": random.randint(1, 10),
            "age": random.randint(0, 150)
        }

        response = self.client.post(
            "/predict",
            json=payload,
            name="/predict"  # Agrupar en métricas
        )

        if response.status_code == 200:
            self.prediction_id = response.json().get("request_id")

    @task(1)  # Weight 1 (execute menos)
    def health_check(self):
        """GET /health - Monitor endpoint"""
        self.client.get(
            "/health",
            name="/health"
        )

    @task(1)
    def get_metrics(self):
        """GET /metrics - Ver performance"""
        self.client.get(
            "/metrics",
            name="/metrics"
        )

    @task(1)
    def model_info(self):
        """GET /model-info - Metadata"""
        self.client.get(
            "/model-info",
            name="/model-info"
        )
