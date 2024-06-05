import requests
import json
import socketio
from typing import Callable

class YTMD:
    namespace = "/api/v1/realtime"

    def __init__(self, app_id: str,
                app_name: str, 
                app_version: str,
                host: str = "127.0.0.1",
                port: int = 9863,
                token: str = None):
        self.id = app_id
        self.name = app_name
        self.version = app_version
        self.host = host
        self.port = port
        self.token = token

        self.url = f"http://{self.host}:{self.port}/api/v1"

        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

        self.socket = socketio.Client(logger=False)
        self.registered_events = []

    def register_event(self, event: str, callback: Callable):
        if not callable(callback):
            raise Exception("Callback must be a function")
        
        if event in self.registered_events:
            raise Exception(f"Event {event} is already registered")

        self.socket.on(event, callback, namespace=self.namespace)
        self.registered_events.append(event)

    def connect(self):
        self._check_token()

        if not self.registered_events:
            raise Exception("No events registered")
        
        try:
            self.socket.connect(
                f"ws://{self.host}:9863",
                auth={'token': self.token}, transports=["websocket"],
                namespaces=[self.namespace]
            )
        except Exception as e:
            raise Exception(f"Failed to connect to YTMD: {e}")

    def authenticate(self):
        code = self.request_code()
        
        if code.status_code == 200:
            token = self.request_token(code.json()["code"])
            
            if token.status_code == 200:
                token = token.json()["token"]
                self.update_token(token)
                return token
            else:
                raise Exception(f"Failed to obtain token: {token.text}")
        
        raise Exception(f"Failed to obtain code: {code.text}")
    
    def update_token(self, token: str):
        self.token = token
        self.session.headers.update({"Authorization": token})
    
    def request_code(self):
        url = self.url + "/auth/requestcode"
        data = {
            "appId": self.id,
            "appName": self.name,
            "appVersion": self.version
        }
        return self.session.post(url, data=json.dumps(data))
    
    def request_token(self, code: str):
        url = self.url + "/auth/request"
        data = {
            "appId": self.id,
            "code": code
        }
        return self.session.post(url, data=json.dumps(data))

    def _check_token(self):
        if not self.token or not self.session.headers.get("Authorization"):
            raise Exception("Token is required to communicate with YTMD application. Please authenticate first.")
    
    def _command(self, command: str, data: int = None):
        self._check_token()

        url = self.url + "/command"
        request_data = { "command": command }
        
        if data:
            request_data["data"] = data

        return self.session.post(url, data=json.dumps(request_data))
    
    def get_version(self):
        url = "http://" + f"{self.host}:{self.port}" + "/metadata"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()['apiVersions']
        
        raise Exception(f"Failed to obtain metadata: {response.text}")

    def get_state(self):
        self._check_token()
        return self.session.get(self.url + "/state")
    
    def get_playlists(self):
        self._check_token()
        return self.session.get(self.url + "/playlists")
    
    def toggle_playback(self):
        return self._command("playPause")
    
    def play(self):
        return self._command("play")
    
    def pause(self):
        return self._command("pause")
    
    def volume_up(self):
        return self._command("volumeUp")
    
    def volume_down(self):
        return self._command("volumeDown")
    
    def set_volume(self, volume: int):
        return self._command("setVolume", volume)
    
    def mute(self):
        return self._command("mute")
    
    def umute(self):
        return self._command("unmute")
    
    def seek_to(self, time: int):
        return self._command("seekTo", time)
    
    def next(self):
        return self._command("next")
    
    def previous(self):
        return self._command("previous")
    
    def repeatMode(self, mode: int):
        return self._command("repeatMode", mode)
    
    def shuffle(self):
        return self._command("shuffle")
    
    def play_index(self, index: int):
        return self._command("playQueueIndex", index)
    
    def toggle_like(self):
        return self._command("toggleLike")
    
    def toggle_dislike(self):
        return self._command("toggleDislike")