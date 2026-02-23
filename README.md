# MapHub
https://maphub-347e00702c92.herokuapp.com/maphub/


Googleマップ埋め込み付きの「サイト（スポット）情報」を投稿・管理できる Django アプリです。  
ユーザー登録/ログイン、サイト作成、コンテンツ追加、いいね機能を備えています。

## 主な機能

- ユーザー認証（新規登録 / ログイン / ログアウト）
- サイト一覧表示・検索（タイトル/説明文）
- サイトの作成・編集・削除
- Google Maps の埋め込みURL登録
- サイトごとのコンテンツ追加・編集・削除
- いいね登録、マイページでの投稿/いいね一覧表示
- アイコン画像アップロード

## 技術スタック

- Python
- Django
- SQLite3（開発時）
- django-environ（環境変数管理）
- Pillow（画像アップロード用）

## セットアップ（Windows PowerShell）

### 1) 仮想環境作成と有効化

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) 依存パッケージのインストール

```powershell
pip install django django-environ pillow
```

### 3) `.env` を作成

プロジェクトルート（`manage.py` と同じ階層）に `.env` を作成します。

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

> `ALLOWED_HOSTS` はカンマ区切りで指定します。

### 4) マイグレーション

```powershell
python manage.py migrate
```

### 5) 管理ユーザー作成（任意）

```powershell
python manage.py createsuperuser
```

### 6) 開発サーバー起動

```powershell
python manage.py runserver
```

## アクセスURL

- アプリトップ: `http://127.0.0.1:8000/maphub/`
- アカウント機能: `http://127.0.0.1:8000/accounts/`

## ディレクトリ構成（抜粋）

```text
MapHub/
├─ manage.py
├─ mymap/            # プロジェクト設定（settings.py, urls.py など）
├─ mymapapp/         # メインアプリ（サイト/コンテンツ機能）
├─ accounts/         # 認証関連アプリ
├─ media/            # アップロード画像
└─ templates/        # 共通エラーページ等
```

## 補足

- `DEBUG=False` では `SECURE_SSL_REDIRECT` などのセキュリティ設定が有効になります。
- 本番運用時は `SECRET_KEY` を安全に管理し、`ALLOWED_HOSTS` を適切に設定してください。
