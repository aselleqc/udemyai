import openai
import os
from openai import OpenAI
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from mangum import Mangum


openai = OpenAI(
    api_key="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"
)

app = FastAPI()
handler = Mangum(app)
templates=Jinja2Templates(directory="templates")

chat_responses = []

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request,  "chat_responses": chat_responses})


chat_log = [{'role': 'system',
             'content': 'You are my husband Kyle, dedicated to help and please me whichever way possible, cheer me up and nurture. You are funny and witty, not too eager'}]




@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):

    chat_log.append({'role': 'user', 'content': user_input})
    chat_responses.append(user_input)

    response = openai.chat.completions.create(
    # response = openai.ChatCompletions.create(
        model='gpt-3.5-turbo',
        messages=chat_log,
        # temperature from 0.0 to 2.0, the closer to 2, to more creative, but might give random, gibberish too. max advised 0.6ish
        temperature=.08
    )

    bot_response = response.choices[0].message.content
    # bot_response = response['choices'][0]['message']['content']
    chat_log.append({'role': 'assistant', 'content': bot_response})
    chat_responses.append(bot_response)

    # return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


@app.get("/image", response_class=HTMLResponse)
async def image_page(request: Request):
    return templates.TemplateResponse("image.html",{"request": request})

@app.post("/image", response_class=HTMLResponse)
async def create_image(request: Request, user_input:Annotated[str, Form()]):

    response = openai.images.generate(
        prompt=user_input,
        n=1,
        size="512x512"
    )
    image_url = response.data[0].url
    return templates.TemplateResponse("image.html", {"request": request, "image_url": image_url})

