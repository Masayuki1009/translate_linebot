import os
import deepl
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Header, Request
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

load_dotenv() #check .env file and add data to 環境変数


ACCESS_TOKEN = os.environ.get("LINE_MESSGAE_API_ACCESS_TOKEN")
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
          print(event)
          translated_text = translater.translate_text(event.message.text, target_lang="JA")
          try:
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"thank you!, you sent {translated_text}!")
          )
          except Error as error:
                    print(error)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=5555, log_level="debug")
