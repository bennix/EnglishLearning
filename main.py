import gradio as gr
import json
from mflux import Flux1, Config
import ollama
import edge_tts
import asyncio
import os
from pathlib import Path
import tempfile
import numpy as np
from PIL import Image

async def text_to_speech(text, voice="en-US-ChristopherNeural"):
    """生成语音文件"""
    communicate = edge_tts.Communicate(text, voice)
    audio_path = Path(tempfile.mktemp(suffix=".mp3"))
    await communicate.save(str(audio_path))
    return str(audio_path)

def load_words(json_file):
    """加载单词列表"""
    try:
        with open(json_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        sorted_words = sorted(data, key=lambda x: x['word'])
        # 每个单词单独一行
        word_list = [f"{item['word']}: {item['translations'][0]['translation']}" for item in sorted_words]
        print(f"Loaded {len(word_list)} words")  # 调试信息
        return word_list
    except Exception as e:
        print(f"Error loading words: {str(e)}")
        return []

# 在文件顶部添加全局变量
_flux_instance = None

def get_flux_instance():
    """获取或创建 Flux1 实例"""
    global _flux_instance
    if _flux_instance is None:
        _flux_instance = Flux1.from_alias(
            alias="schnell",
            quantize=4,
        )
    return _flux_instance

def generate_image(selected_word):
    """生成图像"""
    try:
        if not selected_word:
            return None
        
        word = selected_word.split(':')[0].strip()
        translation = selected_word.split(':')[1].strip()
        
        # 使用 llama2 模型生成描述
        prompt = f"Based on the word '{word}' meaning '{translation}', create a vivid image description in English."
        image_prompt = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
        
        print(f"Generated prompt: {image_prompt['message']['content']}")
        
        # 使用复用的 Flux1 实例
        flux = get_flux_instance()
        
        # 清理 GPU 内存
        import gc
        gc.collect()
        if hasattr(flux, 'clear_memory'):
            flux.clear_memory()
        
        generated_image = flux.generate_image(
            seed=2,
            prompt=image_prompt['message']['content'],
            config=Config(
                num_inference_steps=1,
                height=384,
                width=384,
            )
        )
        
        print("Image generated, processing...")
        
        # 处理图像
        if hasattr(generated_image, 'image'):
            image = generated_image.image
            print("Using image attribute")
        elif hasattr(generated_image, 'images'):
            image = generated_image.images[0]
            print("Using images[0]")
        else:
            print("Converting to numpy array")
            image = Image.fromarray(np.array(generated_image))
        
        if not isinstance(image, Image.Image):
            print("Converting to PIL Image")
            image = Image.fromarray(np.array(image))
        
        print("Image processing completed")
        return image
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def generate_sentence_audio(selected_word):
    """生成句子和音频"""
    try:
        if not selected_word:
            return "", None
        
        word = selected_word.split(':')[0].strip()
        translation = selected_word.split(':')[1].strip()
        
        # 使用更快的模型生成句子
        sentence_prompt = f"Create a simple English sentence using the word '{word}'."
        example_sentence = ollama.chat(model="mistral", messages=[{"role": "user", "content": sentence_prompt}])
        
        # 生成语音
        audio_path = asyncio.run(text_to_speech(example_sentence['message']['content']))
        
        return example_sentence['message']['content'], audio_path
    except Exception as e:
        print(f"Error generating sentence and audio: {str(e)}")
        return "", None

# 创建Gradio界面
with gr.Blocks() as app:
    gr.Markdown("# 英语单词学习助手")
    
    with gr.Row():
        with gr.Column(scale=1):
            json_input = gr.File(label="上传JSON文件")
            load_btn = gr.Button("加载单词列表")
        
        with gr.Column(scale=2):
            word_dropdown = gr.Dropdown(
                label="单词列表",
                choices=[],
                interactive=True,
                allow_custom_value=True,
                scale=2
            )
    
    with gr.Row():
        generate_image_btn = gr.Button("生成图像")
        generate_sentence_btn = gr.Button("生成句子和语音")
    
    with gr.Row():
        image_output = gr.Image(label="生成的图像")
    
    with gr.Row():
        sentence_output = gr.Textbox(label="示例句子")
        audio_output = gr.Audio(label="句子发音")
    
    def update_word_list(json_file):
        """更新单词列表"""
        if json_file is None:
            return gr.Dropdown(choices=[])
        word_list = load_words(json_file)
        print(f"Updating word list with {len(word_list)} words")
        return gr.Dropdown(choices=word_list)
    
    # 设置事件处理
    load_btn.click(
        fn=update_word_list,
        inputs=[json_input],
        outputs=[word_dropdown]
    )
    
    generate_image_btn.click(
        fn=generate_image,
        inputs=[word_dropdown],
        outputs=[image_output]
    )
    
    generate_sentence_btn.click(
        fn=generate_sentence_audio,
        inputs=[word_dropdown],
        outputs=[sentence_output, audio_output]
    )

# 启动应用
app.launch(share=True)