*Note: For English readers, please scroll down for the English version of this README.*

**概要**  
AutoWriteMinutesは、ブラウザで動作する議事録作成ツールです。音声を自動的にテキスト化し、議事録の要約を生成します。WindowsのブラウザやiPhoneのSafariでの動作が確認されています。

**インストール方法**  
1. レポジトリのクローンを作成します: `git clone https://github.com/daishir0/AutoWriteMinutes`
2. requirements.txt で必要な依存関係をインストールします。
3. `ffmpeg`をインストールし、パスを設定してください。
4. `export OPENAI_API_KEY='OPENAI-API-KEY'`を実行し、環境変数にOpenAIのAPIキーを設定してください。

**使い方**  
1. ターミナルで `python app.py` を実行して、サーバーを起動します。
2. ブラウザで `http://localhost:5000` を開きます。
3. 「文字おこしを開始する」ボタンをクリックして録音を開始します。録音された発言は `./data/` に保存されます。
4. 議事録を作成するには、`https://www.yourserver.net:5000/minutes?s=YYYYMMDD-HHMMSS&e=YYYYMMDD-HHMMSS` 形式のURLにアクセスします。例えば、2023年11月4日の13時から13時30分までの議事録を作成する場合は、`https://www.yourserver.net:5000/minutes?s=20231104-130000&e=20231104-133000` とします。

**注意点**  
サーバーのアドレス `https://www.yourserver.net:5000` は、適宜、ご自身の環境に合わせて変更してください。

**ライセンス**  
MITライセンス

---


**Overview**  
AutoWriteMinutes is a browser-based meeting minute creation tool that automatically transcribes audio and generates meeting summaries. It has been tested and confirmed to work on browsers in Windows and Safari on iPhone.

**Installation**  
1. Clone the repository: `git clone https://github.com/daishir0/AutoWriteMinutes`
2. Install the necessary dependencies by using requirements.txt.
3. Install `ffmpeg` and set the path accordingly.
4. Execute `export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'` to set your OpenAI API key as an environment variable.

**Usage**  
1. Run the server by executing `python app.py` in the terminal.
2. Open `http://www.yourserver.net:5000` in your browser.
3. Click on the "文字おこしを開始する" button to begin recording. The transcriptions are saved in `./data/`.
4. To create meeting minutes, access the URL in the format `https://www.yourserver.net:5000/minutes?s=YYYYMMDD-HHMMSS&e=YYYYMMDD-HHMMSS`. For example, to create minutes for a meeting from 13:00 to 13:30 on November 4, 2023, use `https://yourserver.net:5000/minutes?s=20231104-130000&e=20231104-133000`.

**Note**  
The server address is set to `http://www.yourserver.net:5000`. Please change it according to your environment.

**License**  
MIT License
