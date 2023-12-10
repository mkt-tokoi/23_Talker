import sys

import azure.cognitiveservices.speech as speechsdk
import os
from openai import OpenAI
from util import system_prompt

# OpenAIの資格情報は環境変数(OPENAI_API_KEY)から取得
openai_client = OpenAI()

# Azure Speech Serviceの資格情報を環境変数から取得
SPEECH_KEY = os.environ.get("SPEECH_KEY")
SPEECH_REGION = os.environ.get("SPEECH_REGION")

punctuations = ["。", "？ ", "！ ", "！", "？"]


def main():
    # 会話セッションを保持
    messages = [{"role": "system",
                 "content": system_prompt()
                 }]

    # 認識コンフィグレーションを設定
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language = "ja-JP"
    # 音声認識を行うオーディオ構成をマイクからのストリームとして設定
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # 音声認識器を作成
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    # 発話の評価を有効にする
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text="",
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
        enable_miscue=False)
    pronunciation_config.enable_prosody_assessment()
    pronunciation_config.apply_to(speech_recognizer)

    while True:
        # 認識結果を取得
        user_message = None

        # # キーボード入力版
        # user_message = input('user : ')

        # 音声入力版
        print("(Please speak something ...)")
        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:  # 認識成功時
            # 評価結果を取得
            pronunciation_assessment_result = speechsdk.PronunciationAssessmentResult(result)
            # 結果テキストを取得
            user_message = result.text
            score = pronunciation_assessment_result.accuracy_score
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

        # 認識成功時、AIに送信
        if user_message:
            on_new_user_message(messages, user_message, score)


def on_new_user_message(messages, new_user_message: str, score):
    print(f'user : {new_user_message} (認識率:{score}%)')
    # ユーザの発話を追加して、OpenAIに送信
    messages.append({"role": "user", "content": new_user_message})
    # 精度が悪いときはsystemに注釈させる
    if score < 80:
        messages.append({
            "role": "system",
            "content": f"[assistant向けの補足情報] 上記のuser発話の認識率は{score}%でした。"
                       f"userが実際に発話した内容と異なっている可能性に留意してください。"
        })
    # OpenAIに送信
    chat_stream = openai_client.chat.completions.create(model="gpt-4-1106-preview",
                                                        messages=messages,
                                                        stream=True)

    # レスポンスはトークン単位で分割されているので結合して「文」になるまでメッセージを組み立てられたら発声する（を繰り返す）
    response = ""
    speach_text = ""
    print("assistant : ", end="")
    for chunk in chat_stream:
        finish_reason = chunk.choices[0].finish_reason
        if finish_reason == "stop":
            break
        delta_content = chunk.choices[0].delta.content
        print(delta_content, end="")
        delta_content = delta_content.replace("\n", "")
        response += delta_content
        speach_text += delta_content
        # 最後が句読点で終わっていたら、レスポンスの途中でも発声する
        if any(response.endswith(p) for p in punctuations):
            say(speach_text)
            speach_text = ""

    # レスポンスの最後が句読点で終わっていなかったら、レスポンスの最後まで発声する
    if speach_text:
        say(speach_text)

    # 会話履歴に追加
    messages.append({"role": "assistant", "content": response})
    print('(AI speaking done)')


def say(text: str):
    if not text:
        return
    tts(text)


if __name__ == "__main__":
    tts = sys.argv[1] if len(sys.argv) > 1 else 'openai'
    if tts == 'openai': # 速度も読み仮名解釈も中くらい。英語話者っぽいイントネーション。
        from text2openai import say as _say
        tts = _say
    elif tts == 'voicepeak': # 遅い。読み仮名解釈は中くらい。
        from text2voicepeak import say as _say
        tts = _say
    elif tts == 'pyttsx3': # 最高速。読み仮名が解釈が微妙。
        from text2pyttsx3 import say as _say
        tts = _say
    elif tts == 'voiceroid': # 速度も読み仮名解釈も中くらい。
        from text2voiceroid import say as _say
        tts = _say
    else:
        raise Exception('invalid tts')

    main()
