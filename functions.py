import cv2
from cvzone.HandTrackingModule import HandDetector

def move_player(direction, _distance, _change):
    if direction == 'forward':
        if 20 <= _distance <= 40:
                _change = -0.5
        elif 40 < _distance <= 70:
                _change = -1
        elif 70 < _distance <= 100:
                _change = -2
        else:
            _change = 0
    elif direction == 'left':
        if 20 <= _distance <= 40:
            _change = -0.5
        elif 40 < _distance <= 70:
            _change = -1
        elif 70 < _distance <= 100:
            _change = -2
        else:
             _change = 0
    elif direction == 'right':
        if 20 <= _distance <= 40:
            _change = +0.5
        elif 40 < _distance <= 70:
            _change = +1
        elif 70 < _distance <= 100:
            _change = +2
        else:
             _change = 0
    return _change
