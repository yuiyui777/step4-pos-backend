from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# データベースエンジンの作成
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # 接続の健全性チェック
    pool_recycle=3600,   # 1時間ごとに接続をリサイクル
    connect_args={
        "ssl": {"ca": None}  # Azure MySQLはSSL必須（証明書検証なし）
    }
)

# セッションファクトリーの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()


def get_db():
    """
    データベースセッションを取得する依存性注入関数
    
    使用例:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

