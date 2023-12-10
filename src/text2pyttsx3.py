import pyttsx3

# TTSエンジンの初期化
engine = pyttsx3.init()

out_paths = list()


def say(text):
    # 音声合成して再生
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    # 合成したいテキスト
    sample_text = "こんにちは、私はPythonのTTSエンジンです。"

    # 関数を呼び出し
    say(sample_text)
