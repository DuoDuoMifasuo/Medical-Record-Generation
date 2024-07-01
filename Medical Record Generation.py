# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json


api_key = "xx"  # 将xx改为你的api码

def generate_medical_record():
    dialogue_text = dialogue_text_box.get("1.0", tk.END).strip()
    additional_input = additional_input_box.get("1.0", tk.END).strip()

    # 确保案例提示在最前
    additional_prompts = [
      "xx", # 将xx改为一些输入提示，比如一些病历格式以及要求等
        additional_input  # 将用户的额外输入添加到最后
    ]

    # 组合所有文本内容
    combined_prompts = '\n\n'.join(additional_prompts)
    input_text = f"{combined_prompts}\n\n{dialogue_text}"
   
    url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    config = {
        "model": "gpt-4",
        "messages": [{"role": "system", "content": "你是一个专业的医生,你拥有丰富的医学专业知识，擅长写病历"},
                     {"role": "user", "content": input_text}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(config))
        if response.status_code == 200:
            summary = response.json()
            output_text = summary['choices'][0]['message']['content']
            messagebox.showinfo("生成结果", output_text)
        else:
            messagebox.showerror("错误", "API 请求失败")
    except Exception as e:
        messagebox.showerror("错误", str(e))


root = tk.Tk()
root.title("病历生成系统")

# Configure the grid
root.grid_columnconfigure(0, weight=1)


# 检查结果输入框
additional_label = tk.Label(root, text="检查结果输入:")
additional_label.grid(row=4, column=0, sticky="ew")
additional_input_box = scrolledtext.ScrolledText(root, width=100, height=10)
additional_input_box.grid(row=5, column=0, sticky="nsew")

# 对话文本输入框
dialogue_label = tk.Label(root, text="对话文本输入:")
dialogue_label.grid(row=6, column=0, sticky="ew")
dialogue_text_box = scrolledtext.ScrolledText(root, width=100, height=10)
dialogue_text_box.grid(row=7, column=0, sticky="nsew")

# 生成病历按钮
generate_button = tk.Button(root, text="生成病历", command=generate_medical_record)
generate_button.grid(row=8, column=0, sticky="ew")

# Configure grid rows and columns to have proportional sizes when window is resized
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# Start the main event loop
root.mainloop()
