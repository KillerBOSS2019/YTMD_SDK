from YTMDSDK import Events, YTMD, Parser
from time import sleep
import json

ytmd = YTMD("touchportalytmd", "TouchPortalYTMD", "1.0.0")

# ytmd.authenticate()
ytmd.update_token("b60f60f7afe43e41488d2eb1bd0ca1bfc30ff94c0bf65d82ec3362eb200f3ca0700284f979d7ff97f87e3fbbef57daded7787d8125e996e9b854c10db3ef046086442d9135559d017ee9c25ad1e75b14d6acaa1c435b63d77f442d6f0d55cfdb9c7f394eccbe066854e1698c7af68aa531b35513d332063abed71853d4ffd410f1fd563f47e69950dbb17103ff8528d37e8f132e858eba8348b8d300adf06fe926594c0b3830fd5429df76d7760625b71834c2a87137347ff5e649ab1051962981243847c4c39e12acc6539529e48b65e4e0d15f58a50e279ca861f57d4dba849460280f1a6bdccf9632f33befb87505c0d9c3cc43b77003bc2d685c3e632f21")

def on_connect():
    print("Connected to YTMD")

def on_disconnect():
    print("Disconnected from YTMD")

def on_error(data):
    print("Error from YTMD: " + json.loads(data))

def on_state_update(data):
    parser = Parser(data)
    # print("Player: " + str(parser.player_state))
    # print("Player State: " + parser.player_state.state)
    # print("Player video progress: " + str(parser.player_state.video_progress))
    # print("Player volume: " + str(parser.player_state.volume))
    # print("Player muted: " + str(parser.player_state.muted))
    # print("Player ad playing: " + str(parser.player_state.adPlaying))
    # print("Player auto play: " + str(parser.player_state.auto_play))
    # print("Player is generating: " + str(parser.player_state.isGenerating))
    # print("Player is infinite: " + str(parser.player_state.isInfinite))
    # print("Player repeat mode: " + parser.player_state.repeatMode)
    # print("Player selected item index: " + str(parser.player_state.selectedItemIndex))
    print("Player queue: " + str(parser.player_state.queue))

ytmd.register_event(Events.connect, on_connect)
ytmd.register_event(Events.disconnect, on_disconnect)
ytmd.register_event(Events.error, on_error)
ytmd.register_event(Events.state_update, on_state_update)

ytmd.connect()
sleep(60)