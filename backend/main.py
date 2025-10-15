"""
FastAPI POSシステム - メインアプリケーション
すべての機能を統合した単一エントリーポイント
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from config import settings
from database import get_db
from routers import products
from app import crud, schemas

app = FastAPI(
    title=settings.APP_NAME,
    description="POSシステムのバックエンドAPI - 商品管理、取引管理",
    version="1.0.0",
)

# CORS設定（フロントエンドからのアクセスを許可）
origins = [
    "http://localhost:3000",  # 開発環境
]

# 本番環境のフロントエンドURLを追加
if settings.FRONTEND_URL:
    origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録
app.include_router(products.router)


@app.get("/", tags=["Root"])
def read_root():
    """
    ルートエンドポイント
    APIの基本情報を返す
    """
    return {
        "message": "POS API へようこそ",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "products": "/api/products/",
            "product_by_id": "/api/products/{product_id}",
            "product_by_code": "/api/products/code/{code}"
        }
    }


@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """
    ヘルスチェックエンドポイント
    アプリケーションとデータベースの状態を確認
    """
    try:
        # データベース接続テスト
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0"
    }


@app.post("/api/purchase", response_model=schemas.PurchaseResponse, status_code=status.HTTP_201_CREATED, tags=["Purchase"])
def purchase_items(purchase_request: schemas.PurchaseRequest, db: Session = Depends(get_db)):
    """
    購入処理API
    
    購入リストを受け取り、取引と取引明細をデータベースに保存します。
    
    - **items**: 購入する商品のリスト
    - **emp_cd**: レジ担当者コード（オプション、デフォルト: 999999999）
    - **store_cd**: 店舗コード（オプション、デフォルト: 30）
    - **pos_no**: POS機ID（オプション、デフォルト: 90）
    
    処理の流れ:
    1. 取引テーブルへ登録
    2. 取引明細テーブルへ登録
    3. 合計金額を計算
    4. 取引テーブルを更新
    
    トランザクション管理により、エラー時は自動的にロールバックされます。
    """
    if not purchase_request.items:
        raise HTTPException(status_code=400, detail="Purchase list cannot be empty")

    try:
        # トランザクション開始
        transaction = crud.create_purchase(db, purchase_request)
        db.commit()  # すべての処理が成功したらコミット
        db.refresh(transaction)  # DBから最新の状態を読み込む
    except Exception as e:
        db.rollback()  # エラーが発生したらロールバック
        print(f"Error during purchase: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process purchase: {str(e)}")

    return schemas.PurchaseResponse(
        success=True,
        transaction_id=transaction.TRD_ID,
        total_amount=transaction.TOTAL_AMT,
        total_amount_ex_tax=transaction.TTL_AMT_EX_TAX,
        items_count=len(purchase_request.items)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
