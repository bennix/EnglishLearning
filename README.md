
# 英语单词学习助手 (English Word Learning Assistant)

这是一个基于 Gradio 的交互式英语学习工具，它能够帮助用户通过图像、例句和语音来学习英语单词。

## 功能特点

- 📝 支持上传 JSON 格式的单词列表
- 🖼️ 为单词生成相关的图像描述和可视化
- 🔊 生成单词相关的例句并提供语音朗读
- 📱 友好的 Web 界面，支持在线访问
- ⚡ 针对 Apple Silicon (M系列芯片) 优化

## 安装要求

```bash
pip install gradio
pip install ollama
pip install edge-tts
pip install mflux
pip install Pillow
pip install numpy
```



## 环境要求

- Python 3.10+
- Ollama (需要安装 llama2 模型)
- FLUX AI
- 支持 MPS 的 Apple Silicon Mac

## 使用方法

1. 克隆仓库：
```bash
git clone [repository-url]
cd [repository-name]
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python main.py
```

4. 在浏览器中访问显示的地址（通常是 http://localhost:7860）

## JSON 文件格式

需要上传的 JSON 文件格式示例：
```json
[
  {
    "word": "example",
    "translations": [
      {
        "translation": "示例"
      }
    ]
  }
]
```

JSON 文件可以来自 https://github.com/KyleBing/english-vocabulary/tree/master/json

## 使用流程

1. 点击"上传 JSON 文件"按钮上传单词列表
2. 点击"加载单词列表"按钮加载单词
3. 从下拉菜单选择要学习的单词
4. 点击"生成图像"按钮生成相关图像
5. 点击"生成句子和语音"按钮获取例句和发音

## 技术栈

- Gradio：Web 界面框架
- Ollama：文本生成
- Edge TTS：语音合成
- FLUX AI：图像生成
- PIL：图像处理
- NumPy：数组操作

## 性能优化

- 使用单例模式复用 Flux1 实例
- 优化图像生成参数
- 实现内存管理和清理
- 针对 M 系列芯片优化

## 注意事项

- 首次运行时需要下载相关模型
- 图像生成可能需要一定时间
- 建议使用支持 MPS 的设备运行

## 许可证

MIT

