"""
Integration Tests for FastAPI Backend Endpoints & Chatbot API.
"""

from fastapi.testclient import TestClient
from PIL import Image
import numpy as np
import io
import pytest

from backend.app.main import app

client = TestClient(app)


def create_dummy_image_bytes(width=224, height=224, color=(128, 64, 32)):
    img = Image.new('RGB', (width, height), color=color)
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_model_info_endpoint():
    response = client.get("/api/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["primary_model"] == "SwinMultimodalEDL"


def test_image_quality_endpoint():
    img_bytes = create_dummy_image_bytes(224, 224)
    files = {"file": ("test_lesion.jpg", img_bytes, "image/jpeg")}
    response = client.post("/api/image-quality", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "is_valid" in data


def test_prediction_endpoint():
    img_bytes = create_dummy_image_bytes(224, 224)
    files = {"image": ("test_lesion.jpg", img_bytes, "image/jpeg")}
    data = {
        "age": "54.0",
        "sex": "Male",
        "lesion_location": "anterior torso",
        "evolution": "static",
        "itching": "false",
        "bleeding": "false",
        "pain": "false",
        "observed_color": "brown",
        "prior_allergies": "true",
        "allergy_details": "Latex",
        "ongoing_medications": "false",
        "medication_details": ""
    }
    response = client.post("/api/predict", files=files, data=data)
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "success"
    assert res["risk_level"] in ["LOW RISK", "SUSPICIOUS", "EXPERT REVIEW RECOMMENDED"]
    assert "is_cancerous" in res
    assert "cancer_status_label" in res
    assert "biopsy_required" in res
    assert "surgery_required" in res
    assert "visit_urgency" in res
    assert "healing_measures" in res
    assert len(res["all_7_predictions"]) == 7


def test_chatbot_endpoint():
    payload = {
        "message": "Do I need a biopsy for my skin lesion?",
        "triage_context": {
            "top_class_human": "Melanoma (Malignant)",
            "risk_level": "SUSPICIOUS",
            "biopsy_required": True,
            "surgery_required": True,
            "visit_urgency": "URGENT (Within 24-48 Hours)"
        }
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "biopsy" in data["reply"].lower()
