import pyautogui as pgui
import time
import sys
import vlc
import os
import json


# サーバーとの通信完了までの待ち時間
SERVER_COM_COMP_WAIT_TIME = 1

# JSONキー一覧
OPE_KEY_NAME = "name"
OPE_KEY_OPERATIONS = "operations"
OPE_KEY_TYPE = "type"
OPE_KEY_X = "x"
OPE_KEY_Y = "y"
OPE_KEY_IMG_PATH = "img_path"
OPE_KEY_WAIT_TIME_SEC = "wait_time_sec"
OPE_KEY_COMMENT = "comment"

# オペレーション一覧
OPE_TYPE_CLICK = "click"
OPE_TYPE_WAIT = "wait"


class AutoOperation:

    file_path = ""

    def __init__(self, file_path):
        self.file_path = file_path

    def is_exist_operation_file(self):
        if not os.path.isfile(self.file_path):
            print("file not exist. file_path:{0}", self.file_path)
            return -1

        return 0

    def load_operation(self):

        result = 0

        try:

            fp = open(self.file_path, 'r', encoding="utf-8_sig")
            self.operation_content = json.load(fp)
            print(self.operation_content)

        except json.JSONDecodeError as e:
            print("JsonDecodeError occurred")
            print(e)
            result = -1
        except Exception as e:
            print("An exception occurred")
            print(e)
            result = -1
        finally:
            fp.close()

        return result

    def prepare(self):

        if 0 != self.is_exist_operation_file():
            return -1

        if 0 != self.load_operation():
            return -1

        return 0

    def play_end_sound(self):
        mp = vlc.MediaPlayer()
        mp.set_mrl('end_sound.mp3')

        mp.play()
        time.sleep(1)
        mp.stop()

        return 0

    def is_exist_json_key(self, json: json, key: str):
        try:
            json[key]
        except KeyError as e:
            print("not exist key. key:{0}", key)
            print(e)
            return -1
        return 0

    def click_and_wait(self, x, y):

        pgui.click(x, y)

        time.sleep(SERVER_COM_COMP_WAIT_TIME)

        return 0

    def click_operation(self, operation: json):

        if 0 == self.is_exist_json_key(operation, OPE_KEY_X) and 0 == self.is_exist_json_key(operation, OPE_KEY_Y):
            return self.click_and_wait(operation[OPE_KEY_X], operation[OPE_KEY_Y])

        if 0 == self.is_exist_json_key(operation, OPE_KEY_IMG_PATH):
            # TODO
            print("TODO")
            return 0

        return -1

    def wait_operation(self, operation: json):
        # TODO
        wait_time_sec = 3
        time.sleep(wait_time_sec)

        return 0

    def exec_operation(self, operation: json):

        if 0 != self.is_exist_json_key(operation, OPE_KEY_TYPE):
            return -1

        if OPE_TYPE_CLICK == operation[OPE_KEY_TYPE]:
            return self.click_operation(operation)

        if OPE_TYPE_WAIT == operation[OPE_KEY_TYPE]:
            return self.wait_operation(operation)

        return 0

    def exec_operations(self):

        if 0 != self.is_exist_json_key(self.operation_content, OPE_KEY_OPERATIONS):
            return -1

        for itr in self.operation_content["operations"]:
            print("exec_ope")
            if 0 != self.exec_operation(itr):
                return -1

        return 0

    def run(self):

        if 0 != self.prepare():
            return -1

        if 0 != self.exec_operations():
            return -1

        return 0


def main(file_path):
    ap = AutoOperation(file_path)
    ap.run()


if __name__ == '__main__':

    pgui.FAILSAFE = True

    args = sys.argv

    if 2 <= len(args):
        main(args[1])
    else:
        print(pgui.position())
