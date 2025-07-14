# from create import bot, db
# from helps_func.works import send
import speech_recognition as sr
import ffmpeg
from pydub import AudioSegment

import os
# from keyboards import reply
# from states.states import State_Voice


async def voice_message_handler(message, state):
    await state.set_state(State_Voice.text)
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f"handlers/voice_handler/{message.from_user.id}.mp3")
    text = main_convert(str(message.from_user.id))
    print(text)
    if text:
        text = text.replace('- k', '-к')
        text = text.replace('- к', '-к')
        text = text.replace('комментарий', '-к')
        text = text.replace('комментарии', '-к')
        text = text.replace('комент', '-к')
        text = text.replace('коммент', '-к')
        text = text.replace('ком', '-к')
        text = text.replace('комм', '-к')
        text = text.replace('минус комментарий', '-к')
        text = text.replace('минусовка', '-к')

        text_final = []
        for element in text.split():
            lst = [el for el in element]
            for i in range(len(lst) - 1):
                if lst[i] == '.' and lst[i + 1].isdigit():
                    lst[i] = ''

            text_final.append(''.join(lst))
        text_final = ' '.join(text_final)
        print(text_final)
        await state.update_data(text=text_final)
        await send(message.from_user.id, f'Вы сказали:\n{text_final}', markup=reply.voice_input())


def main_convert(file_name):
    text = None
    try:
        convert_to_aiff(file_name)
        text = aiff_to_text(file_name)
    except Exception as e:
        print(e)
    if os.path.isfile(f'handlers/voice_handler/out_{file_name}.aiff'):
        os.remove(f'handlers/voice_handler/out_{file_name}.aiff')
    if os.path.isfile(f'handlers/voice_handler/{file_name}.mp3'):
        os.remove(f'handlers/voice_handler/{file_name}.mp3')
        return text


def convert_to_aiff(file_name):
    # input_file = 'пробитие.mp3'
    output_file = 'out_1229555610.aiff'
    # ffmpeg.input(filename=input_file).output(output_file, loglevel="quiet").run(overwrite_output=True)
    file = ffmpeg.input(file_name)
    file = file.output(output_file, loglevel="quiet")
    file.run(overwrite_output=True)
    # sound = AudioSegment.from_mp3("пробитие.mp3")
    # sound.export("file.aiff", format="aiff")


def aiff_to_text(file_name):
    r = sr.Recognizer()
    with sr.AudioFile(f'handlers/voice_handler/out_{file_name}.aiff') as source:
        audio = r.record(source)

    text = r.recognize_google(audio, language="ru-RU")
    return text
