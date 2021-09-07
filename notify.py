# -*- coding: utf-8 -*-
from camera import Camera
import requests

def send_shiny(camera):
    path = camera.saveCapture()
    token = 'LINE Notify Token Here' # Change Here
    api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': f'message: Shiny'}
    files = {"imageFile":open(path,'rb')}
    requests.post(api, headers=headers, data=data, files=files)