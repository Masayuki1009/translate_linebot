import os
import deepl
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Header, Query, Request, HTTPException
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from app.db.dbbase import DbBase
from app.db.session import engine, make_session
from app.models.message import Message

load_dotenv() #check .env file and add data to 環境変数

db_session = make_session()
DbBase.metadata.create_all(engine) # created DB

ACCESS_TOKEN = os.environ.get("LINE_MESSAGE_API_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("LINE_MESSAGE_API_SECRET")
DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY")
translater = deepl.Translator(DEEPL_AUTH_KEY)

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = FastAPI(id="first fastAPI server", openapi_url="/openapi.json")
api_router = APIRouter()

@api_router.post(path="/callback")
async def callback(request: Request, x_line_signature=Header(None)):
          body = await request.body()
          body = body.decode("utf-8")

          handler.handle(body, x_line_signature) #signiture validation
          return

# do when validation(line31) is okay
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
          # check text if it is message or command
          if event.message.text == "history":
            # check which user requested
            user_id = event.source.sender_id
            try:
                found_messages = db_session.query(Message).filter(Message.user_id == str(user_id)).all()
            except:
                raise HTTPException(status_code=404, detail="user is not found_messages")
            print(found_messages)
            # print(texts)
            result_text = ""

            for found_message_item in found_messages:
                text = found_message_item.text
                translated = found_message_item.translated_text
                template = f"{text} => {translated}\n"
                result_text += template
            
            result_text = result_text.rstrip()
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"you registed {result_text}")
                )
            except Error as error:
                print(error)
          else:
            print(event)
            
            # translate text
            translated = translater.translate_text(event.message.text, target_lang="JA")
            print(translated)
            print(type(translated))
            #get info
            text = event.message.text
            translated_text = translated
            user_id = event.source.sender_id
            new_message = Message(
                text = event.message.text,
                translated_text = str(translated), # or translated.text
                user_id = event.source.sender_id
                )
            # add info on DB
            db_session.add(new_message)
            db_session.commit()
          try:
                # reply message
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"thank you!, you sent {translated}!")
          )
          except Error as error:
                    print(error)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=os.environ.get("PORT") or 5555 , log_level="debug")
