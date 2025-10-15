"""
テストデータ投入スクリプト
商品マスタに5件のテストデータを投入します
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import ProductMaster

# テストデータ
test_products = [
    {
        "CODE": "4589901001018",
        "NAME": "テクワン・消せるボールペン 黒",
        "PRICE": 180
    },
    {
        "CODE": "4589901001025",
        "NAME": "テクワン・スーパーノート B5 5冊パック",
        "PRICE": 450
    },
    {
        "CODE": "4589901001032",
        "NAME": "ハイブリッドカッター Pro",
        "PRICE": 800
    },
    {
        "CODE": "4589901001049",
        "NAME": "スマート付箋 5色ミックス",
        "PRICE": 320
    },
    {
        "CODE": "4589901001056",
        "NAME": "疲れない椅子 Alpha (ポップアップ限定)",
        "PRICE": 12000
    }
]


def seed_products():
    """商品マスタにテストデータを投入"""
    db = SessionLocal()
    
    try:
        # 既存データを確認
        existing_count = db.query(ProductMaster).count()
        print(f"現在の商品数: {existing_count}件")
        
        if existing_count > 0:
            print("既にデータが存在します。")
            choice = input("既存データを削除して新しいデータを投入しますか？ (y/n): ")
            if choice.lower() == 'y':
                db.query(ProductMaster).delete()
                db.commit()
                print("既存データを削除しました。")
            else:
                print("データ投入をキャンセルしました。")
                return
        
        # テストデータを投入
        for product_data in test_products:
            product = ProductMaster(**product_data)
            db.add(product)
        
        db.commit()
        print(f"\n✅ {len(test_products)}件の商品データを投入しました！\n")
        
        # 投入したデータを確認
        products = db.query(ProductMaster).all()
        print("=" * 80)
        print(f"{'PRD_ID':<10}{'CODE':<20}{'NAME':<35}{'PRICE':>10}")
        print("=" * 80)
        for p in products:
            print(f"{p.PRD_ID:<10}{p.CODE:<20}{p.NAME:<35}{p.PRICE:>10}円")
        print("=" * 80)
        
    except Exception as e:
        db.rollback()
        print(f"❌ エラーが発生しました: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 80)
    print("商品マスタ テストデータ投入スクリプト")
    print("=" * 80)
    print()
    seed_products()

