"""
商品関連のAPIルーター
CRUD操作とスキーマを使用したベストプラクティス実装
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).resolve().parents[1]))

from database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)


@router.get("/", response_model=List[schemas.Product], summary="商品一覧取得")
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    商品マスタから全商品を取得
    
    - **skip**: スキップする件数（デフォルト: 0）
    - **limit**: 取得する最大件数（デフォルト: 100）
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=schemas.Product, summary="商品詳細取得（ID指定）")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDの商品を取得
    
    - **product_id**: 商品ID
    """
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product


@router.get("/code/{code}", response_model=schemas.Product, summary="商品詳細取得（コード指定）")
def get_product_by_code(code: str, db: Session = Depends(get_db)):
    """
    商品コードで商品を取得
    
    - **code**: 商品コード（バーコード）
    """
    product = crud.get_product_by_code(db, code)
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product
