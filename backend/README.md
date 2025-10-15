# POSアプリケーション - バックエンド

FastAPIベースのPOSシステムバックエンドAPI

## プロジェクト構造

```
backend/
├── main.py              # ✅ FastAPIメインアプリ（Port 8000）
├── config.py            # 設定管理
├── database.py          # データベース接続
├── app/
│   ├── crud.py         # ✅ データベースCRUD操作
│   └── schemas.py      # ✅ Pydanticスキーマ
├── models/              # SQLAlchemyモデル
│   ├── product_master.py
│   ├── transaction.py
│   └── transaction_detail.py
├── routers/             # APIルーター
│   └── products.py     # 商品関連エンドポイント
├── alembic/             # データベースマイグレーション
├── tests/               # テストコード
└── seed_data.py         # テストデータ投入スクリプト
```

## 設計思想

### レイヤーアーキテクチャ

```
main.py (FastAPI)
    ↓
routers/ (エンドポイント定義)
    ↓
app/crud.py (ビジネスロジック)
    ↓
models/ (データモデル)
    ↓
database.py (DB接続)
```

### ベストプラクティス

- ✅ **単一責任の原則**: 各ファイルが明確な責任を持つ
- ✅ **CRUD分離**: DB操作は`app/crud.py`に集約
- ✅ **スキーマ検証**: `app/schemas.py`でデータ検証
- ✅ **ルーター分離**: 機能ごとに`routers/`で管理

## セットアップ

### 1. 仮想環境の作成と有効化

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```env
DATABASE_URL=mysql+pymysql://username:password@hostname:3306/yui
APP_NAME=POS API
DEBUG=True
```

### 4. データベースマイグレーション

```bash
# マイグレーションを適用
alembic upgrade head
```

### 5. テストデータ投入

```bash
python seed_data.py
```

## 起動方法

### 開発サーバー

```bash
uvicorn main:app --reload
```

または

```bash
python main.py
```

サーバーは **http://localhost:8000** で起動します。

## API エンドポイント

### システム

- `GET /` - ルート（API情報）
- `GET /health` - ヘルスチェック

### 商品管理

- `GET /api/products/` - 商品一覧取得
- `GET /api/products/{product_id}` - 商品詳細（ID指定）
- `GET /api/products/code/{code}` - 商品詳細（コード指定）⭐

### パラメータ

**商品一覧取得**:
- `skip` (int): スキップする件数（デフォルト: 0）
- `limit` (int): 取得する最大件数（デフォルト: 100）

## 使用例

### 商品コード検索

```bash
curl http://localhost:8000/api/products/code/4589901001018
```

レスポンス:
```json
{
  "PRD_ID": 1,
  "CODE": "4589901001018",
  "NAME": "テクワン・消せるボールペン 黒",
  "PRICE": 180
}
```

### 商品一覧取得

```bash
curl "http://localhost:8000/api/products/?skip=0&limit=10"
```

### ヘルスチェック

```bash
curl http://localhost:8000/health
```

## テスト

### 手動テスト

```bash
# 商品コード検索
curl http://localhost:8000/api/products/code/4589901001018

# 商品一覧
curl http://localhost:8000/api/products/
```

詳細は `tests/MANUAL_TESTS.md` を参照。

### 自動テスト

```bash
pytest tests/ -v
```

## 開発ガイド

### 新しいエンドポイントを追加

1. **CRUD操作を定義** (`app/crud.py`):
```python
def get_something(db: Session, id: int):
    return db.query(Model).filter(Model.id == id).first()
```

2. **スキーマを定義** (`app/schemas.py`):
```python
class Something(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
```

3. **ルーターを作成** (`routers/something.py`):
```python
@router.get("/{id}", response_model=schemas.Something)
def get_something(id: int, db: Session = Depends(get_db)):
    result = crud.get_something(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result
```

4. **main.pyに登録**:
```python
from routers import something
app.include_router(something.router)
```

### データベースマイグレーション

```bash
# 新しいマイグレーション作成
alembic revision --autogenerate -m "説明"

# マイグレーション適用
alembic upgrade head

# ロールバック
alembic downgrade -1

# 履歴確認
alembic history
```

## APIドキュメント

サーバー起動後、以下のURLでSwagger UIにアクセス：

**http://localhost:8000/docs**

## トラブルシューティング

### データベース接続エラー

```bash
# 接続情報を確認
cat .env

# 接続テスト
python -c "from database import engine; engine.connect()"
```

### ポート既に使用中

```bash
# プロセスを確認
lsof -i :8000

# 強制終了
pkill -f "uvicorn main:app"
```

### マイグレーションエラー

```bash
# 現在のバージョン確認
alembic current

# 最新に更新
alembic upgrade head
```

## コード品質

### リンター

```bash
# flake8
pip install flake8
flake8 .

# black (フォーマッター)
pip install black
black .
```

### 型チェック

```bash
pip install mypy
mypy .
```

## パフォーマンス

- **データベース接続プール**: SQLAlchemyで自動管理
- **SSL接続**: Azure MySQL用に最適化
- **インデックス**: 商品コード（CODE）にUNIQUEインデックス

## セキュリティ

- ✅ 環境変数で接続情報管理
- ✅ SSL/TLS接続必須
- ✅ CORS設定
- ✅ 入力検証（Pydantic）

## 次のステップ

1. 取引登録API実装
2. 取引明細API実装
3. 認証・認可機能
4. ロギング強化
5. キャッシング

## 関連ドキュメント

- [データベーススキーマ設計書](../docs/database-schema.md)
- [開発環境セットアップ](../docs/development.md)
- [Azure MySQL セットアップ](../docs/azure-database-setup.md)
