import json

import websocket


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws: websocket.WebSocketApp):
    ws.send(
        json.dumps(
            {
                'type': 'client',
                'message': {'uuid': '1ce095bc-e5fa-486b-b17f-842dedd8a2e6'},
            }
        ),
    )
    print("Opened connection")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://localhost:8000/ws/notifications",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()
