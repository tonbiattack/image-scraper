# ImageScraper

ImageScraper は、指定された Web ページから画像をスクレイピングし、ローカルに保存する Python スクリプトです。<br>
Selenium と BeautifulSoup を使用して、設定ファイルで指定された URL から画像をダウンロードし、指定されたフォルダに保存します。<br>
進行状況は`progress.json`に記録され、プログラムの途中で停止した場合でも、どこまで処理が進んだかを追跡できます。

## 機能

- 複数の Web ページから画像をスクレイピング
- 各ページに対して指定された数の画像をダウンロード
- ダウンロードした画像をローカルの指定フォルダに保存
- `.gif` ファイルの除外
- 進行状況の記録と追跡

## 使用技術

- Python 3
- Selenium
- BeautifulSoup
- requests
- webdriver_manager

## 使い方

1. 依存関係のインストール：

   ```
   pip install selenium bs4 requests webdriver_manager
   ```

2. `config.json` ファイルを編集して、スクレイピングする URL と画像数を指定します。

3. `save_folder.txt` に画像を保存するフォルダのパスを記載します。

4. スクリプトを実行します：
   ```
   python image_scraper.py
   ```

## 設定

### save_folder.txt

このファイルには、ダウンロードした画像を保存するディレクトリのパスを記載します。例えば：

### config.json

```text
C:/Users/yourname/Documents/Images/
```

<br>

このファイルでは、スクレイピングする URL とページごとの画像数を指定します。以下はその例です：

```json
{
  "pages": {
    "https://example.com/page1": 5,
    "https://example.com/page2": 3
  }
}
```

## カスタマイズ

スクリプトには、go_to_next_page 関数が含まれています。<br>
これは、Web サイトによって異なるページ遷移のメカニズムに対応するためのものです。特定のサイトに合わせてこの関数をカスタマイズすることで、異なるタイプのページ遷移に柔軟に対応できます。

## 注意事項

- このスクリプトは、個人的な使用を目的としています。Web サイトの利用規約に違反しないようにしてください。<br>
- スクレイピングによってサーバーに負荷をかけすぎないよう注意してください。<br>
- このスクリプトの使用によって生じたいかなる問題に対しても、作者は責任を負いません。
