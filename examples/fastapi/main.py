#!/usr/bin/env python3
import frontend
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from cachetools import cached, LRUCache, TTLCache

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms = TTLCache(maxsize=1000, ttl=24 * 60 * 60)
app.rooms = rooms

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.post('/upload')
def upload(body: Dict):
    roomid = body['roomid']
    if roomid not in rooms:
        app.rooms[roomid] = {}
    room = app.rooms[roomid]
    label = body['label']
    if label in ('img1', 'img2'):
        # for pixelmatch
        room[label] = body['image']
        room.pop('img_diff', None)
    return {}

frontend.init(app)

if __name__ == '__main__':
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)