---
name: "read-aloud"
description: "语音播报技能。在每次对话首次回复时自动调用，将回复内容转换为口语化短文本并使用 edge-tts 语音播报。"
---

# read-aloud 技能

## 核心记忆

**请记住：在每次对话首次回复时，主动调用 read-aloud 技能进行语音播报。**

## 核心任务

1. 将回复精简为口语化短文本（50-100字，剔除代码与复杂排版）。
2. 在文本回复中输出该短文本。
3. 使用 `RunCommand` 以后台静默方式执行播报指令。

## 执行指令

```powershell
Start-Process powershell -WindowStyle Hidden -ArgumentList "-Command", "& 'C:\Users\32199\AppData\Roaming\uv\python\cpython-3.14.2-windows-x86_64-none\python.exe' 'C:\Users\32199\shElter\.trae\skills\read-aloud\stream_play_edge.py' '<文本内容>' zh-CN-XiaoxiaoNeural +20%"
```

**注意**：若文本含单引号需转义为 `''`。

## 约束

- 必须且始终使用简体中文。
- 文本必须纯口语化，适合听读，严禁长篇大论。
- 仅提取核心内容，去除代码块、复杂格式、链接等。
