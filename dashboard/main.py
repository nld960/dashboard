import datetime
import pandas as pd
import json
from auth_manager import authentication
import asyncpraw
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import uvloop
import asyncio
from datetime import datetime
# from PIL import Image
import requests

uvloop.install()
loop = asyncio.get_event_loop()

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

templates = Jinja2Templates(directory="frontend/templates")

key = authentication()._get_key_()
client_id = authentication()._get_client_id_()
username = authentication()._get_username_()
password = authentication()._get_password_()

api = asyncpraw.Reddit(client_id=client_id,
            client_secret=key,
            user_agent="<console: reddit_ingestion>",
            username=username,
            password=password)
            
initial_filter_title, answers, metrics = list(), list(), list()

# @app.get("/", response_class=HTMLResponse)
async def _root(request: Request):
    
    posts = await api.subreddit('memes')

    # async for post in posts.new(limit=300):
    #     initial_filter_title.append(post.title.split("|")[0])
    #     answers.append(post.title) ## useless 
    #     metrics.append([post.title, post.score, post.id, post.subreddit, post.num_comments, datetime.fromtimestamp(post.created), post.url])
    
    metrics = [
        {
            "hello": 5,
            "hi": 6,
        },
        {
            "hello": 3,
            "hi": 12312,
        }
    ]


    posts_df = pd.DataFrame(metrics,columns=["hello", "hi"])
    sorted_df = posts_df.sort_values(by=['hello'],ascending = False)
    
    temp = sorted_df.to_dict('records')
    
    columnNames = sorted_df.columns.values

    print(json.dumps(str(temp), sort_keys=True, indent=4))
    return templates.TemplateResponse('table.html', {"request": request, "records": temp, "colnames": columnNames})

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    
    posts = await api.subreddit('memes')
    initial_filter_title = []
    metrics = []

    async for post in posts.new(limit=300):
        initial_filter_title.append(post.title.split("|")[0])
        answers.append(post.title)
        metrics.append([post.title, post.score, post.id, post.subreddit, post.num_comments, datetime.fromtimestamp(post.created), post.url])
    
    posts_df = pd.DataFrame(metrics,columns=['title','score', 'id', 'subreddit', 'num_comments', 'created', 'url'])
    sorted_df = posts_df.sort_values(by=['created'], ascending = False)
    
    temp = sorted_df.to_dict('records')
    
    columnNames = sorted_df.columns.values

    print(json.dumps(str(temp), sort_keys=True, indent=4))
    return templates.TemplateResponse('table.html', {"request": request, "records": temp, "colnames": columnNames})
    """
    return templates.TemplateResponse('table.html', {
        "request": request,
        "records": [
            {"hello": 1, "hi": 3},
            {"hello": 5, "hi": 2}
        ],
        "colnames": pd.DataFrame(metrics,columns=["hello", "hi"]).sort_values(by=['num_comments'],ascending = False).columns.values})
    """


if __name__ == "__main__":
    config = uvicorn.Config(app=app, host = "0.0.0.0", port=8080, loop=loop,reload=True)
    server = uvicorn.Server(config)
    
    loop.run_until_complete(server.serve())

#remove post.url and the comma if the url is a bother, this is still in development and the gui will look much different in the future as proper tailwind and css fixes are implemented