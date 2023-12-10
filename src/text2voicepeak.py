import os
import subprocess
import time

import simpleaudio as sa

# voicepeak.exeのパス
voicepeak_path = "C:/Program Files/VOICEPEAK/voicepeak.exe"

# wav出力先
outpath = "output.wav"


def say(script, narrator="Japanese Female 1", happy=50, sad=50, angry=50, fun=50):
    """
    任意のテキストをVOICEPEAKのナレーターに読み上げさせる関数
    script: 読み上げるテキスト（文字列）
    narrator: ナレーターの名前（文字列）
    happy: 嬉しさの度合い
    sad: 悲しさの度合い
    angry: 怒りの度合い
    fun: 楽しさの度合い
    """
    # 引数を作成
    args = [
        voicepeak_path,
        "-s", script,
        "-n", narrator,
        "-o", outpath,
        "-e", f"happy={happy},sad={sad},angry={angry},fun={fun}"
    ]
    # プロセスを実行
    # start_time = time.time()
    process = subprocess.Popen(args)

    # プロセスが終了するまで待機
    process.communicate()
    # end_time = time.time()
    # print(f"VOICEPEAKの実行時間: {end_time - start_time}秒")

    # 音声を再生
    wave_obj = sa.WaveObject.from_wave_file(outpath)
    play_obj = wave_obj.play()
    play_obj.wait_done()

    # wavファイルを削除
    os.remove(outpath)


if __name__ == "__main__":
    # 合成したいテキスト
    sample_text = "こんにちは、私はボイスピークのTTSエンジンです。"

    # 関数を呼び出し
    say(sample_text)
