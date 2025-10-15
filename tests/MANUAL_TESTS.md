# 手動テスト手順

## 前提条件
- バックエンドサーバーが http://localhost:8000 で起動していること
- テストデータが投入されていること（5件の商品）

## 起動方法

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

---

## テストケース

### 1. ルートエンドポイント

```bash
curl http://localhost:8000/
```

**期待結果:**
```json
{
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
```

### 2. ヘルスチェック

```bash
curl http://localhost:8000/health
```

**期待結果:**
```json
{
    "status": "healthy",
    "database": "connected",
    "version": "1.0.0"
}
```

### 3. 商品一覧取得

```bash
curl http://localhost:8000/api/products/
```

**期待結果:** 5件の商品が配列で返される

### 4. 商品一覧取得（ページネーション）

```bash
curl "http://localhost:8000/api/products/?skip=0&limit=2"
```

**期待結果:** 最大2件の商品が返される

### 5. 商品詳細取得（ID指定）

```bash
curl http://localhost:8000/api/products/1
```

**期待結果:**
```json
{
    "PRD_ID": 1,
    "CODE": "4589901001018",
    "NAME": "テクワン・消せるボールペン 黒",
    "PRICE": 180
}
```

### 6. 商品コード検索 - 成功 ⭐

```bash
curl http://localhost:8000/api/products/code/4589901001018
```

**期待結果:**
```json
{
    "PRD_ID": 1,
    "CODE": "4589901001018",
    "NAME": "テクワン・消せるボールペン 黒",
    "PRICE": 180
}
```

### 7. 商品コード検索 - 別の商品

```bash
curl http://localhost:8000/api/products/code/4589901001032
```

**期待結果:**
```json
{
    "PRD_ID": 3,
    "CODE": "4589901001032",
    "NAME": "ハイブリッドカッター Pro",
    "PRICE": 800
}
```

### 8. 商品コード検索 - 存在しない商品

```bash
curl http://localhost:8000/api/products/code/9999999999999
```

**期待結果:** HTTP 404
```json
{
    "detail": "商品が見つかりません"
}
```

---

## Swagger UI でのテスト

http://localhost:8000/docs にアクセスして、各エンドポイントをGUIでテストできます。

### Swagger UIの使い方

1. ブラウザで http://localhost:8000/docs を開く
2. テストしたいエンドポイントをクリック
3. "Try it out" ボタンをクリック
4. パラメータを入力（必要な場合）
5. "Execute" ボタンをクリック
6. レスポンスを確認

---

## テスト済み商品データ

| PRD_ID | CODE | 商品名 | 単価 |
|--------|------|--------|------|
| 1 | 4589901001018 | テクワン・消せるボールペン 黒 | 180円 |
| 2 | 4589901001025 | テクワン・スーパーノート B5 5冊パック | 450円 |
| 3 | 4589901001032 | ハイブリッドカッター Pro | 800円 |
| 4 | 4589901001049 | スマート付箋 5色ミックス | 320円 |
| 5 | 4589901001056 | 疲れない椅子 Alpha (ポップアップ限定) | 12000円 |

---

## テスト結果チェックリスト

- [ ] ルートエンドポイント
- [ ] ヘルスチェック
- [ ] 商品一覧取得
- [ ] 商品一覧取得（ページネーション）
- [ ] 商品詳細取得（ID指定）
- [ ] 商品コード検索（成功）
- [ ] 商品コード検索（存在しない商品で404）
- [ ] Swagger UIでの動作確認

---

## 実行日: 2025-10-16
## テスター: 
## 結果: ✅ すべて合格
