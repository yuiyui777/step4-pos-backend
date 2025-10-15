"""
商品API のテスト
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).resolve().parents[1]))

from starlette.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


def test_health_check():
    """ヘルスチェックのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data


def test_get_products():
    """商品一覧取得のテスト"""
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5  # テストデータが5件以上


def test_get_product_by_id():
    """商品詳細取得（ID）のテスト"""
    response = client.get("/api/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["PRD_ID"] == 1
    assert "CODE" in data
    assert "NAME" in data
    assert "PRICE" in data


def test_get_product_by_code_success():
    """商品コード検索成功のテスト"""
    response = client.get("/api/products/code/4589901001018")
    assert response.status_code == 200
    data = response.json()
    assert data["CODE"] == "4589901001018"
    assert data["NAME"] == "テクワン・消せるボールペン 黒"
    assert data["PRICE"] == 180


def test_get_product_by_code_not_found():
    """商品コード検索（存在しない商品）のテスト"""
    response = client.get("/api/products/code/9999999999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "商品が見つかりません"


def test_get_products_with_pagination():
    """ページネーション付き商品一覧のテスト"""
    response = client.get("/api/products/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2

