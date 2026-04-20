import asyncio
import edge_tts
import sys
import os
import re
import tempfile
import ctypes

def play_mp3_sync(file_path):
    mci = ctypes.windll.winmm.mciSendStringW
    alias = f"player_{id(file_path)}"
    mci(f'open "{file_path}" alias {alias}', None, 0, 0)
    mci(f'play {alias} wait', None, 0, 0)
    mci(f'close {alias}', None, 0, 0)

async def prefetch_and_play(text, voice, rate):
    sentences = [s.strip() for s in re.split(r'([。！？；!?;\n]+)', text) if s.strip()]
    merged_sentences = []
    temp_s = ""
    for part in sentences:
        if re.match(r'^[。！？；!?;\n]+$', part):
            if merged_sentences:
                merged_sentences[-1] += part
        else:
            merged_sentences.append(part)

    if not merged_sentences:
        return

    queue = asyncio.Queue()

    async def downloader():
        for i, sentence in enumerate(merged_sentences):
            if len(sentence.strip()) < 1:
                continue
            fd, tmp_path = tempfile.mkstemp(suffix=f"_{i}.mp3")
            os.close(fd)
            try:
                communicate = edge_tts.Communicate(sentence, voice, rate=rate)
                await communicate.save(tmp_path)
                await queue.put(tmp_path)
            except Exception as e:
                print(f"Error: {e}")
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        await queue.put(None)

    async def player():
        while True:
            tmp_path = await queue.get()
            if tmp_path is None:
                break
            try:
                await asyncio.to_thread(play_mp3_sync, tmp_path)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except:
                        pass

    await asyncio.gather(downloader(), player())

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python 娇喘播报.py <text> <voice> <rate>")
        sys.exit(1)
    text = sys.argv[1]
    voice = sys.argv[2]
    rate = sys.argv[3]
    import warnings
    if sys.platform == 'win32':
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    kernel32 = ctypes.windll.kernel32
    mutex = kernel32.CreateMutexW(None, False, "TraeReadAloudEdgeMutex")
    kernel32.WaitForSingleObject(mutex, 0xFFFFFFFF)
    try:
        asyncio.run(prefetch_and_play(text, voice, rate))
    finally:
        kernel32.ReleaseMutex(mutex)