# MCP Novel Game Server

![alt text](static/images/image.png)

[ビジュアルノベルゲームのMCPサーバーの作り方](https://note.com/gotalab/n/n34b4fcc46d22)

## English

### Overview
This repository is a novel game server that supports multi-branch scenario stories (visual novels) in both English and Japanese. 

**This repository is designed as a resource to help you better understand MCP (Model Context Protocol) Resources.**

You can run, edit, and add new scenarios easily. The server supports scenario files written in YAML and can be extended with your own stories.

> **Note:** On Cline, everything works out-of-the-box. On other environments like Claude Desktop and Cursor, please use `server_tool.py` to launch and manage the server properly.

### How to Use

#### 1. Install dependencies
```
uv sync
```

#### 2. Run the server
```json
{
    "novel-game-server": {
            "command": "uv",
            "args": [
                "--directory",
                "/Users/username/Documents/projects/mcp-novel-game-server", ## Replace with your project root
                "run",
                "src/server.py"
            ]
        }
}
```

#### 3. Play or test a scenario
- Place your scenario files in `src/stories/<your_story>/`
- You can select scenarios via the server's interface or by specifying scenario IDs in your client.

#### 4. Add a new scenario
- Create a new directory under `src/stories/` (e.g. `villainess_rose` or `villainess_rose_ja`)
- Add scenario YAML files (see existing examples)
- Add a `meta.yaml` describing the scenario

#### 5. File structure
```
project-root/
├── src/
│   ├── server.py
│   └── stories/
│       ├── villainess_rose/
│       ├── villainess_rose_ja/
│       └── ...
├── mcp_example.json
├── pyproject.toml
└── README.md
```

### Notes
- Use `uv` as the package manager and runner.
- Scenarios can be written in English or Japanese.
- See `src/stories/README.md` for scenario tree and details.

---

## 日本語

### 概要
このリポジトリは、分岐型ノベルゲーム（ビジュアルノベル）サーバーです。英語・日本語両対応。

**MCP（Model Context Protocol）のリソースを理解するためのリソースとして設計されています。**

YAML形式でシナリオを追加・編集できます。

> **注意:** Cline環境ではそのまま動作しますが、それ以外の環境（例えばClaude DesktopやCursor）では `server_tool.py` を使ってサーバーの起動・管理を行ってください。

### 使い方

#### 1. 依存パッケージのインストール
```
uv sync
```

#### 2. サーバーの起動
```json
{
    "novel-game-server": {
            "command": "uv",
            "args": [
                "--directory",
                "/Users/username/Documents/projects/mcp-novel-game-server", ## ご自身のプロジェクトルートに変更してください
                "run",
                "src/server.py"
            ]
        }
}
```

#### 3. シナリオのプレイ・テスト
- `src/stories/<your_story>/` にシナリオファイルを配置
- サーバーのUIまたはクライアントからシナリオIDを指定して選択可能

#### 4. 新しいシナリオの追加
- `src/stories/` 配下に新しいディレクトリを作成（例: `villainess_rose` や `villainess_rose_ja`）
- YAMLファイルでシナリオを作成
- シナリオ説明用の `meta.yaml` も追加

#### 5. ファイル構成例
```
project-root/
├── src/
│   ├── server.py
│   └── stories/
│       ├── villainess_rose/
│       ├── villainess_rose_ja/
│       └── ...
├── mcp_example.json
├── pyproject.toml
└── README.md
```

### 注意
- パッケージ管理・実行は `uv` を利用してください。
- シナリオは英語・日本語どちらでも作成可能です。
- シナリオの詳細やツリーは `src/stories/README.md` を参照してください。