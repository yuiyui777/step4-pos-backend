"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session
from typing import Optional, List
import sys
from pathlib import Path
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).resolve().parents[1]))

from models import ProductMaster, Transaction, TransactionDetail
from app import schemas


# ==================== Product CRUD ====================

def get_product_by_code(db: Session, code: str) -> Optional[ProductMaster]:
    """商品コードで商品を取得"""
    return db.query(ProductMaster).filter(ProductMaster.CODE == code).first()


def get_product_by_id(db: Session, product_id: int) -> Optional[ProductMaster]:
    """商品IDで商品を取得"""
    return db.query(ProductMaster).filter(ProductMaster.PRD_ID == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[ProductMaster]:
    """商品一覧を取得"""
    return db.query(ProductMaster).offset(skip).limit(limit).all()


def create_product(db: Session, code: str, name: str, price: int) -> ProductMaster:
    """商品を作成"""
    db_product = ProductMaster(CODE=code, NAME=name, PRICE=price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, name: str = None, price: int = None) -> Optional[ProductMaster]:
    """商品を更新"""
    db_product = get_product_by_id(db, product_id)
    if db_product:
        if name is not None:
            db_product.NAME = name
        if price is not None:
            db_product.PRICE = price
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """商品を削除"""
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False


# ==================== Transaction CRUD ====================

def get_transaction(db: Session, transaction_id: int) -> Optional[Transaction]:
    """取引を取得"""
    return db.query(Transaction).filter(Transaction.TRD_ID == transaction_id).first()


def get_transactions(db: Session, skip: int = 0, limit: int = 100) -> List[Transaction]:
    """取引一覧を取得"""
    return db.query(Transaction).offset(skip).limit(limit).all()


def create_transaction(
    db: Session,
    emp_cd: str = None,
    store_cd: str = None,
    pos_no: str = None,
    total_amt: int = None,
    ttl_amt_ex_tax: int = None
) -> Transaction:
    """取引を作成"""
    db_transaction = Transaction(
        EMP_CD=emp_cd,
        STORE_CD=store_cd,
        POS_NO=pos_no,
        TOTAL_AMT=total_amt,
        TTL_AMT_EX_TAX=ttl_amt_ex_tax
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# ==================== Transaction Detail CRUD ====================

def get_transaction_details(db: Session, transaction_id: int) -> List[TransactionDetail]:
    """指定された取引の明細一覧を取得"""
    return db.query(TransactionDetail).filter(TransactionDetail.TRD_ID == transaction_id).all()


def create_transaction_detail(
    db: Session,
    trd_id: int,
    dtl_id: int,
    prd_id: int,
    prd_code: str,
    prd_name: str,
    prd_price: int,
    tax_cd: str = None
) -> TransactionDetail:
    """取引明細を作成"""
    db_detail = TransactionDetail(
        TRD_ID=trd_id,
        DTL_ID=dtl_id,
        PRD_ID=prd_id,
        PRD_CODE=prd_code,
        PRD_NAME=prd_name,
        PRD_PRICE=prd_price,
        TAX_CD=tax_cd
    )
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail


# ==================== Purchase CRUD ====================

def create_purchase(db: Session, purchase_request: schemas.PurchaseRequest) -> Transaction:
    """
    購入処理を実行
    APIファンクション(Lv2)の仕様を実装
    """
    # 1-1. 取引テーブルへ登録する
    # とりあえず合計金額0でヘッダーを作成
    new_transaction = Transaction(
        DATETIME=datetime.utcnow(),
        EMP_CD=purchase_request.emp_cd or '999999999',  # 仕様書より固定値またはリクエストから
        STORE_CD=purchase_request.store_cd or '30',     # 仕様書より固定値またはリクエストから
        POS_NO=purchase_request.pos_no or '90',         # 仕様書より固定値またはリクエストから
        TOTAL_AMT=0,
        TTL_AMT_EX_TAX=0,
    )
    db.add(new_transaction)
    db.flush()  # これで new_transaction.TRD_ID が採番される

    total_amount = 0

    # 1-2. 取引明細へ登録する
    for index, item in enumerate(purchase_request.items):
        new_detail = TransactionDetail(
            TRD_ID=new_transaction.TRD_ID,
            DTL_ID=index + 1,  # 明細IDは1から連番
            PRD_ID=item.PRD_ID,
            PRD_CODE=item.CODE,
            PRD_NAME=item.NAME,
            PRD_PRICE=item.PRICE,
            TAX_CD='10'  # 仕様書より固定値（消費税10%）
        )
        db.add(new_detail)
        total_amount += item.PRICE

    # 1-3. 合計や税金額を計算する (今回は合計金額のみ)
    # 1-4. 取引テーブルを更新する
    new_transaction.TOTAL_AMT = total_amount
    new_transaction.TTL_AMT_EX_TAX = total_amount  # 税計算は未実装のため同額

    return new_transaction

