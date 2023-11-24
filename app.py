from flask import Flask, request, render_template
from flask import Flask, request, jsonify
from openai import OpenAI
import openai
from datetime import datetime, timedelta
from flask_socketio import SocketIO
import transcription_service
import os
import sys
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 全ルートでCORSを有効化
socketio = SocketIO(app, cors_allowed_origins="*")

def read_meeting_transcripts(start_datetime, end_datetime, directory):
    # datetimeオブジェクトへの変換
    start_datetime = datetime.strptime(start_datetime, '%Y%m%d-%H%M%S')
    
    # end_datetimeがNoneでなければ変換、そうでなければNoneのままにする
    if end_datetime is not None:
        end_datetime = datetime.strptime(end_datetime, '%Y%m%d-%H%M%S')
    
    transcripts = ""
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".txt"):
            date_time_part = filename[:-4]
            try:
                file_datetime = datetime.strptime(date_time_part, '%Y%m%d-%H%M%S')
                # end_datetimeがNoneの場合はstart_datetime以降のすべてのファイルを対象にする
                if end_datetime is None:
                    if file_datetime >= start_datetime:
                        with open(os.path.join(directory, filename), 'r') as file:
                            transcripts += file.read() + "\n"
                # それ以外の場合は通常通り期間をチェックする
                elif start_datetime <= file_datetime <= end_datetime:
                    with open(os.path.join(directory, filename), 'r') as file:
                        transcripts += file.read() + "\n"
            except ValueError as e:
                print(f"Error parsing date from file: {filename}, error: {e}")
    return transcripts

@app.route('/')
def index():
    #return app.send_static_file('index.html')
    return render_template('index.html')


@app.route('/minutes')
def get_minutes():
    default_start_datetime = (datetime.now() - timedelta(minutes=30)).strftime('%Y%m%d-%H%M%S')
    start_datetime = request.args.get('s', default_start_datetime)
    end_datetime = request.args.get('e', None)  # end_datetime is optional
    
    # 日本の日付フォーマットに変換 (例: 11月12日 15時45分)
    start_datetime_obj = datetime.strptime(start_datetime, '%Y%m%d-%H%M%S')
    # 曜日を取得
    days = ["月", "火", "水", "木", "金", "土", "日"]
    weekday = days[start_datetime_obj.weekday()]

    # formatted_datetime = start_datetime_obj.strftime('%m月%d日 %H時%M分')
    formatted_datetime = start_datetime_obj.strftime(f'%m月%d日({weekday}) %H時%M分')

    # ここでtranscripts変数を取得するread_meeting_transcripts関数を呼び出し
    transcripts = read_meeting_transcripts(start_datetime, end_datetime, './data/')
    print(transcripts)
    
    client = OpenAI()
    response = client.chat.completions.create(
        #model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "あなたはどのようなテキストであっても、フォーマットに従って必ず内容をまとめられる仕事を達成出来る、プロのエディターです。この仕事を諦めて断ることは絶対にあり得ません。"},
            {"role": "user", "content": "{発言録テキスト}}は発言録テキストです。"
             + "# これらから、トピックを5個ほど抜き出して、行頭に番号を付与してリストで列挙して下さい。"
             + "# 次に、前述した5個のトピックタイトルごとに、ですます調で、2, 3文程度で要約してください"
             + "# 次に、特に大切だと主張されていることを一文で簡潔にまとめてください。"
             + "発言録テキスト=\"" + transcripts + "\""
             + "# フォーマット:◼︎トピック：{改行}{トピック}{改行}{改行}◼︎トピックの要約：{改行}{トピックの要約}{改行}{改行} ◼︎まとめ：{改行}{特に大切な主張}"
             },
        ]

    )

    summary = response.choices[0].message.content
    return render_template('summary.html', summary=summary, day=formatted_datetime, transcripts=transcripts)


@app.route('/hc')
def hc():
    return app.send_static_file('hc.html')
    
    
@app.route('/create_minutes')
def create_minutes():
    return render_template('create_minutes')

    
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        audio_file = request.files['audio_data']
        if audio_file:
            text = transcription_service.transcribe(audio_file)
            if text:
                socketio.emit('transcription', {'text': text})
                return jsonify({"message": "File transcribed successfully"}), 200
            else:
                return jsonify({"message": "Transcription failed"}), 400
        else:
            return jsonify({"message": "No file found"}), 400

if __name__ == '__main__':
    if not os.path.exists("./data"):
        os.makedirs("./data")
    import eventlet
    import eventlet.wsgi
    eventlet.monkey_patch()
    socketio.run(app, debug=True, host="0.0.0.0")