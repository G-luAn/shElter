import asyncio
import edge_tts
import sys
import os
import re
import tempfile
import ctypes

# Windows 原生 MP3 播放，无需第三方库
def play_mp3_sync(file_path):
    mci = ctypes.windll.winmm.mciSendStringW
    alias = f"player_{id(file_path)}"
    # 打开文件
    mci(f'open "{file_path}" alias {alias}', None, 0, 0)
    # 播放并等待完成
    mci(f'play {alias} wait', None, 0, 0)
    # 关闭句柄
    mci(f'close {alias}', None, 0, 0)

async def prefetch_and_play(text, voice, rate):
    # 按常见标点符号分割长文本
    sentences = [s.strip() for s in re.split(r'([。！？；!?;\n]+)', text) if s.strip()]
    
    # 重新组合标点和句子
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
    download_tasks = []

    # 异步下载任务
    async def downloader():
        for i, sentence in enumerate(merged_sentences):
            # 跳过太短的无效内容
            if len(sentence.strip()) < 1:
                continue
                
            fd, tmp_path = tempfile.mkstemp(suffix=f"_{i}.mp3")
            os.close(fd) # 关闭文件描述符让edge_tts去写
            
            try:
                communicate = edge_tts.Communicate(sentence, voice, rate=rate)
                await communicate.save(tmp_path)
                await queue.put(tmp_path)
            except Exception as e:
                print(f"Error downloading '{sentence}': {e}")
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        # 放入结束标志
        await queue.put(None)

    # 播放任务
    async def player():
        while True:
            tmp_path = await queue.get()
            if tmp_path is None:
                break
                
            try:
                # 在单独的线程中阻塞播放，防止阻塞异步下载
                await asyncio.to_thread(play_mp3_sync, tmp_path)
            except Exception as e:
                print(f"Error playing {tmp_path}: {e}")
            finally:
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except:
                        pass

    # 并发运行下载和播放
    await asyncio.gather(
        downloader(),
        player()
    )

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python stream_play_edge.py <text> <voice> <rate>")
        sys.exit(1)
        
    text = sys.argv[1]
    voice = sys.argv[2]
    rate = sys.argv[3]
    
    # 防止 Windows 下 asyncio 报错
    import warnings
    if sys.platform == 'win32':
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
    # 使用 Windows 命名互斥锁实现全局队列，防止多次调用时语音同时播放
    kernel32 = ctypes.windll.kernel32
    mutex = kernel32.CreateMutexW(None, False, "TraeReadAloudEdgeMutex")
    kernel32.WaitForSingleObject(mutex, 0xFFFFFFFF) # 无限期等待，直到获取到锁
    
    try:
        asyncio.run(prefetch_and_play(text, voice, rate))
    finally:
        kernel32.ReleaseMutex(mutex)
