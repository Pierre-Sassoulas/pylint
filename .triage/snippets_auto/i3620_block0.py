import flask
import serial


def initialize():
    print(flask.Blueprint)
    #print(flask.Config.from_pyfile)
    #print(flask.Config.from_json)
    try:
        serial.Serial()
    except serial.SerialException as exc:
        if isinstance(exc.strerror, str) and "could not open port" in exc.strerror:
            print(exc)
            return
        raise
