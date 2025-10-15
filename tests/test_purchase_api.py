"""
購入API のテスト
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).resolve().parents[1]))

from starlette.testclient import TestClient
from main import app

client = TestClient(app)


def test_purchase_success():
    """購入処理成功のテスト"""
    purchase_data = {
        "items": [
            {"PRD_ID": 1, "CODE": "4589901001018", "NAME": "テクワン・消せるボールペン 黒", "PRICE": 180},
            {"PRD_ID": 2, "CODE": "4589901001025", "NAME": "テクワン・スーパーノート B5 5冊パック", "PRICE": 450}
        ]
    }

    response = client.post("/api/purchase", json=purchase_data)

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "transaction_id" in data
    assert data["transaction_id"] > 0
    assert data["total_amount"] == 630  # 180 + 450
    assert data["total_amount_ex_tax"] == 630
    assert data["items_count"] == 2


def test_purchase_multiple_same_product():
    """同じ商品を複数購入するテスト"""
    purchase_data = {
        "items": [
            {"PRD_ID": 1, "CODE": "4589901001018", "NAME": "テクワン・消せるボールペン 黒", "PRICE": 180},
            {"PRD_ID": 1, "CODE": "4589901001018", "NAME": "テクワン・消せるボールペン 黒", "PRICE": 180},
            {"PRD_ID": 1, "CODE": "4589901001018", "NAME": "テクワン・消せるボールペン 黒", "PRICE": 180}
        ]
    }

    response = client.post("/api/purchase", json=purchase_data)

    assert response.status_code == 201
    data = response.json()
    assert data["total_amount"] == 540  # 180 * 3
    assert data["items_count"] == 3


def test_purchase_with_custom_codes():
    """カスタム店舗コード等を指定したテスト"""
    purchase_data = {
        "items": [
            {"PRD_ID": 3, "CODE": "4589901001032", "NAME": "ハイブリッドカッター Pro", "PRICE": 800}
        ],
        "emp_cd": "EMP001",
        "store_cd": "ST001",
        "pos_no": "P01"
    }

    response = client.post("/api/purchase", json=purchase_data)

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["total_amount"] == 800


def test_purchase_empty_list():
    """空の購入リストでエラーになるテスト"""
    purchase_data = {"items": []}
    response = client.post("/api/purchase", json=purchase_data)
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Purchase list cannot be empty"


def test_purchase_high_value():
    """高額商品の購入テスト"""
    purchase_data = {
        "items": [
            {"PRD_ID": 5, "CODE": "4589901001056", "NAME": "疲れない椅子 Alpha (ポップアップ限定)", "PRICE": 12000},
            {"PRD_ID": 5, "CODE": "4589901001056", "NAME": "疲れない椅子 Alpha (ポップアップ限定)", "PRICE": 12000}
        ]
    }

    response = client.post("/api/purchase", json=purchase_data)

    assert response.status_code == 201
    data = response.json()
    assert data["total_amount"] == 24000  # 12000 * 2

