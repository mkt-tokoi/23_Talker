from openai import OpenAI
import sys
import subprocess

from util import play_mp3
import os

client = OpenAI()

out_paths = list()

def say(text: str):
    spoken_response = client.audio.speech.create(
        model="tts-1",
        voice="fable",
        input=text
    )

    outfile_count = len(out_paths)
    if outfile_count > 0:
        out_file_name = f'output{outfile_count}.mp3'
    else:
        out_file_name = 'output.mp3'
    out_paths.append(out_file_name)
    out_path = os.path.join('out_voice', out_file_name)

    # save to file
    spoken_response.stream_to_file(out_path)

    # play
    play_mp3(out_path)


def say_in_subprocess(speech_recognizer, text: str):
    subprocess.run(['python', 'text2openai.py', text])


if __name__ == "__main__":
    # 合成したいテキスト
    # sample_text = "こんにちは、私はOpenAIのTTSエンジンです。"

    # 関数を呼び出し
    say(sys.argv[1])
