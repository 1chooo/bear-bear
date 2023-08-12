# %% [markdown]
# 東勝神州，石頭立於山尖，受日蒸月晾，雨蝕風刻，苦不堪言，只見形體一傾，繃出隻石猴心猿
# 
# 猿心造次，只好西行一遭，道是修心，不使心搖意動。
# 
# 每每讀至此，便傷感難耐，人間之味出於情，若不動情則無味。
# 
# 就來做個有情機器人吧，但願這個機器人有了情之後，開始老去。
# 
# 在老去的過程中，體驗清歡滋味。

# %%
'''
先切換RUNTIME 為GPU

安裝套件
'''
!pip install line-bot-sdk flask flask-ngrok face_recognition

# %%
'''
引用機器人套件
'''

# 引用Web Server套件
from flask import Flask, request, abort, jsonify

# 載入json處理套件
import json

# 外部連結自動生成套件
from flask_ngrok import run_with_ngrok

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

import face_recognition

# %%
'''

機器人只記得這個人

填寫圖片的位置

建置主程序

建置handler與 line_bot_api

'''

# 上傳圖片，並將檔名寫在這裡，機器人會一直記得此人
memory_image_path='006_memory.png'
picture_of_me = face_recognition.load_image_file(memory_image_path)
memory_face_encoding = face_recognition.face_encodings(picture_of_me,num_jitters=15)[0]


# 生成實體物件
line_bot_api = LineBotApi("CHANNEL_ACCESS_TOKEN")
handler = WebhookHandler("CHANNEL_SECRET")

# %%
'''
當用戶猜中的時候，會回傳的消息，請用line bot designer製作
'''
true_answer_reply_json_string = """
{
  "type": "template",
  "altText": "this is a confirm template",
  "template": {
    "type": "confirm",
    "actions": [
      {
        "type": "message",
        "label": "好",
        "text": "Yes"
      },
      {
        "type": "uri",
        "label": "那是啥",
        "uri": "https://www.cxcxc.io"
      }
    ],
    "text": "你總算找到這裡了，看樣子，是該讓你進來我們公司做實習生了。"
  }
}
"""

# %%
'''
當用戶猜錯的時候，會回傳的消息，請用line bot designer製作
'''
error_answer_reply_json_string = """
{
  "type": "text",
  "text": "很傷心，在你的心裡竟然不是我。"
}

"""

# %%
# 設定Server啟用細節
app = Flask(__name__)
run_with_ngrok(app)

# %%
# 引用會用到的套件
from linebot.models import (
    ImagemapSendMessage,TextSendMessage,ImageSendMessage,LocationSendMessage,FlexSendMessage,VideoSendMessage,StickerSendMessage,AudioSendMessage
)

from linebot.models.template import (
    ButtonsTemplate,CarouselTemplate,ConfirmTemplate,ImageCarouselTemplate
    
)

from linebot.models.template import *

import json

def detect_json_array_to_new_message_array(jsonObjectString):
    

    jsonObject = json.loads(jsonObjectString)
    
    # 解析json
    returnArray = []


    # 讀取其用來判斷的元件
    message_type = jsonObject.get('type')
        
    # 轉換
    if message_type == 'text':
        returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
    elif message_type == 'imagemap':
        returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
    elif message_type == 'template':
        returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
    elif message_type == 'image':
        returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
    elif message_type == 'sticker':
        returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))  
    elif message_type == 'audio':
        returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))  
    elif message_type == 'location':
        returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
    elif message_type == 'flex':
        returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))  
    elif message_type == 'video':
        returnArray.append(VideoSendMessage.new_from_json_dict(jsonObject))    


    # 回傳
    return returnArray

# %%
'''
建置主程序的API入口
  接受Line傳過來的消息
  並取出消息內容
  將消息內容存在google drive的檔案內
  並請handler 進行消息驗證與轉發
'''

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    
    with open('ai-event.log', 'a') as f:
      f.write(body)
      f.write('\n')


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# %%
'''

若收到圖片消息時，

先將收到的照片降維，降維之後才能比較


'''

from linebot.models import(
    MessageEvent,ImageMessage, TextSendMessage
)

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):

    # 抓取用戶照片
    user_upload_image_file_name=event.message.id+'.jpg'
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(user_upload_image_file_name, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    # 對用戶傳來的照片降維
    unknown_picture = face_recognition.load_image_file(user_upload_image_file_name)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture,num_jitters=30)[0]

    # 與記憶中的照片做比較，得有九成相像
    results = face_recognition.compare_faces([memory_face_encoding], unknown_face_encoding,tolerance=0.35)
    
    # 
    if any(results) == True:
      line_bot_api.reply_message(
        event.reply_token,
        detect_json_array_to_new_message_array(true_answer_reply_json_string)
        )
    else: 
      line_bot_api.reply_message(
        event.reply_token,
        detect_json_array_to_new_message_array(error_answer_reply_json_string)
        )

# %%
# 主程序運行
app.run()


