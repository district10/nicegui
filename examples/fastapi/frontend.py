from fastapi import FastAPI, Query

from nicegui import app, ui
from starlette.requests import Request
import base64
import cv2
import numpy as np

def parse_dataurl_image(room, label, output_label):
    dataurl = room.get(label)
    if dataurl is None or not isinstance(dataurl, str):
        return dataurl
    img = room.get(output_label)
    if img is not None:
        return img
    typ, img = dataurl.split(';base64,', 1)
    img = base64.b64decode(img)
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 3:
        B, G, R = cv2.split(img)
        A = np.ones(B.shape, dtype=B.dtype) * 255
        img = cv2.merge((R, G, B, A))
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
    room[output_label] = img
    return img


def encode_as_dataurl(img):
    success, buffer = cv2.imencode('.png', img)
    base64_bytes = base64.b64encode(buffer.tobytes())
    base64_str = base64_bytes.decode('ascii')
    data_url = f'data:image/png;base64,{base64_str}'
    return data_url


def init(fastapi_app: FastAPI) -> None:
    @ui.page('/show')
    def show():
        ui.label('Hello, FastAPI!')

        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')


    @ui.page('/pixelmatch')
    def pixelmatch(request: Request):
        roomid = request.query_params.get('roomid')
        if not roomid:
            raise Exception('?roomid=<IS_MISSING>')
        room = app.fastapi_app.rooms.get(roomid)
        if room is None:
            ui.label(f'room={roomid} expired')
            return
        img1 = parse_dataurl_image(room, 'img1', 'img1:cv2')
        img2 = parse_dataurl_image(room, 'img2', 'img2:cv2')
        if img1 is None or img2 is None:
            ui.label(f'room={roomid} has neither img1 nor img2')
            return
        assert img1.shape == img2.shape, f'invalid image, shape not match: {img1.shape} != {img2.shape}'
        diff = room.get('img_diff')
        if diff is None:
            from pybind11_pixelmatch import pixelmatch, Options, Color
            diff = np.zeros(img1.shape, dtype=img1.dtype)
            options = Options()
            options.diffColor = Color(0, 255, 0, 255)
            options.diffColorAlt = Color(255, 0, 0, 255)
            pixelmatch(img1, img2, output=diff, options=options)
            assert diff.shape == img2.shape
            room['img_diff'] = encode_as_dataurl(diff)
            room['img_diff:cv2'] = diff
        with ui.row():
            with ui.column():
                ui.image(room['img1']).classes('w-[300px] h-[200px]')
            with ui.column():
                ui.image(room['img2']).classes('w-[300px] h-[200px]')
        ui.label('Diff')
        ui.image(room['img_diff']).classes('w-[300px] h-[200px]')

    ui.run_with(
        fastapi_app,
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )

    app.fastapi_app = fastapi_app
    ui.run_with(
        fastapi_app,
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )
