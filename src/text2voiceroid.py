import subprocess


def say(text, cid='1701'):
    """
    任意のテキストをVOICEROIDに読み上げさせる関数
    事前に、以下を起動しておく必要がある
    - VOICEROID, VOICEROID2, VOICEROID＋ 等
    - AssistantSpeak.exe (管理者権限で起動すること)
        - 輝度後に、使用製品 > 製品スキャン を実行し、話者一覧をロードしておく必要がある

    また、`seikasay2.exe`を`PATH`の通った場所に配置しておく必要がある
    """
    result = subprocess.run(
        ["seikasay2.exe", '-cid', cid, '-t', text], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


if __name__ == "__main__":
    # 合成したいテキスト
    sample_text = "こんにちは、私はボイスロイドのTTSエンジンです。"

    # 関数を呼び出し
    say(sample_text)
