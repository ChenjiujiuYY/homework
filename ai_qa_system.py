"""
人工智能基础问答系统
基于关键词匹配的知识库问答系统，支持可视化交互界面。
"""

import tkinter as tk
from tkinter import messagebox
import re


# ============================================================
# 1. 构建知识库
# ============================================================

KNOWLEDGE_BASE = {
    "什么是人工智能？": {
        "answer": "人工智能（Artificial Intelligence，简称 AI）是计算机科学的一个分支，致力于创建能够模拟人类智能行为的系统，包括学习、推理、感知、理解语言和做出决策等能力。",
        "keywords": {"人工智能", "AI", "定义", "概念", "计算机科学"},
        "category": "基础概念",
    },
    "机器学习是什么？": {
        "answer": "机器学习（Machine Learning）是人工智能的一个子领域，它使计算机系统能够从数据中自动学习并改进，而无需显式编程。核心思想是通过算法让机器从大量数据中发现规律并进行预测或决策。",
        "keywords": {"机器学习", "ML", "数据", "算法", "自动学习"},
        "category": "基础概念",
    },
    "深度学习和机器学习有什么区别？": {
        "answer": "深度学习是机器学习的一个子集，使用多层神经网络来处理数据。机器学习依赖人工特征提取，而深度学习能自动从原始数据中学习特征表示。深度学习在图像识别、自然语言处理等任务上表现尤为突出，但通常需要更多数据和计算资源。",
        "keywords": {"深度学习", "机器学习", "区别", "神经网络", "特征提取"},
        "category": "基础概念",
    },
    "Python在人工智能中的作用是什么？": {
        "answer": "Python 是人工智能领域最流行的编程语言，拥有丰富的 AI 生态库：NumPy 用于数值计算，Pandas 用于数据处理，Scikit-learn 用于传统机器学习，TensorFlow 和 PyTorch 用于深度学习。其语法简洁、社区活跃，非常适合快速原型开发。",
        "keywords": {"Python", "编程语言", "NumPy", "TensorFlow", "PyTorch", "库"},
        "category": "工具与语言",
    },
    "什么是神经网络？": {
        "answer": "神经网络是一种受人脑神经元结构启发的计算模型，由大量相互连接的节点（神经元）组成。数据通过输入层、隐藏层和输出层逐层传递，每个连接都有权重，网络通过训练不断调整这些权重以学习任务。",
        "keywords": {"神经网络", "神经元", "层", "权重", "训练", "深度学习"},
        "category": "核心算法",
    },
    "什么是自然语言处理？": {
        "answer": "自然语言处理（Natural Language Processing，NLP）是人工智能的一个分支，专注于让计算机理解、解释和生成人类语言。应用包括机器翻译、情感分析、语音识别、文本摘要和聊天机器人等。",
        "keywords": {"自然语言处理", "NLP", "语言理解", "机器翻译", "文本"},
        "category": "应用领域",
    },
    "什么是计算机视觉？": {
        "answer": "计算机视觉（Computer Vision）是人工智能的一个领域，让计算机能够从图像和视频中获取高级理解。主要任务包括图像分类、目标检测、图像分割、人脸识别等，广泛应用于自动驾驶、医疗影像和安防监控。",
        "keywords": {"计算机视觉", "图像", "视频", "人脸识别", "目标检测"},
        "category": "应用领域",
    },
    "监督学习和无监督学习有什么区别？": {
        "answer": "监督学习使用带标签的训练数据，即每条数据都有对应的正确答案，模型学习输入到输出的映射（如分类、回归）。无监督学习使用无标签数据，模型需要自行发现数据中的结构和模式（如聚类、降维）。两者是机器学习最基本的两种学习范式。",
        "keywords": {"监督学习", "无监督学习", "标签", "聚类", "分类", "回归"},
        "category": "核心算法",
    },
    "强化学习是什么？": {
        "answer": "强化学习（Reinforcement Learning）是机器学习的第三大范式，智能体通过与环境交互、尝试不同动作并获得奖励或惩罚信号来学习最优策略。AlphaGo 击败围棋世界冠军就是强化学习的经典成功案例。",
        "keywords": {"强化学习", "智能体", "环境", "奖励", "策略", "AlphaGo"},
        "category": "核心算法",
    },
    "什么是大语言模型？": {
        "answer": "大语言模型（Large Language Model，LLM）是一种基于 Transformer 架构的大规模深度学习模型，通过在海量文本数据上进行预训练来学习语言模式。代表模型包括 GPT 系列、Claude、LLaMA 等，能够进行文本生成、问答、翻译、编程等多种任务。",
        "keywords": {"大语言模型", "LLM", "Transformer", "GPT", "预训练", "生成"},
        "category": "核心算法",
    },
    "什么是过拟合？": {
        "answer": "过拟合（Overfitting）是指机器学习模型在训练数据上表现很好，但在新数据上表现差的现象。原因是模型过于复杂，记住了训练数据的噪声而非真正的规律。常用解决方法包括：增加训练数据、正则化、Dropout、提前停止训练等。",
        "keywords": {"过拟合", "泛化", "正则化", "Dropout", "模型复杂度"},
        "category": "核心算法",
    },
    "什么是数据集？训练集、验证集和测试集有什么区别？": {
        "answer": "数据集是用于训练和评估机器学习模型的数据集合。训练集（Training Set）用于训练模型参数；验证集（Validation Set）用于调整超参数和监控训练过程，防止过拟合；测试集（Test Set）用于最终评估模型的泛化能力，仅在训练完成后使用一次。",
        "keywords": {"数据集", "训练集", "验证集", "测试集", "超参数"},
        "category": "数据与评估",
    },
    "什么是卷积神经网络？": {
        "answer": "卷积神经网络（Convolutional Neural Network，CNN）是一种专门用于处理网格状数据（如图像）的深度学习模型。它通过卷积层自动提取空间特征，利用池化层降低维度，全连接层进行分类或回归。CNN 在图像识别、视频分析和医学影像处理中广泛应用。",
        "keywords": {"卷积神经网络", "CNN", "卷积层", "池化层", "图像识别"},
        "category": "核心算法",
    },
    "什么是生成式AI？": {
        "answer": "生成式 AI（Generative AI）是一类能够创造新内容的人工智能系统，包括文本、图像、音频、视频和代码等。主要技术包括生成对抗网络（GAN）、变分自编码器（VAE）和扩散模型（Diffusion Model）。代表产品有 ChatGPT、Midjourney、Stable Diffusion 等。",
        "keywords": {"生成式AI", "GAN", "扩散模型", "ChatGPT", "Midjourney", "内容生成"},
        "category": "应用领域",
    },
    "什么是模型评估指标？": {
        "answer": "模型评估指标用于量化机器学习模型的性能。常见指标包括：准确率（Accuracy）、精确率（Precision）、召回率（Recall）、F1 分数用于分类任务；均方误差（MSE）、平均绝对误差（MAE）用于回归任务；ROC 曲线和 AUC 用于综合评估分类器性能。",
        "keywords": {"评估指标", "准确率", "精确率", "召回率", "F1", "MSE"},
        "category": "数据与评估",
    },
    "人工智能的伦理问题有哪些？": {
        "answer": "人工智能面临的主要伦理问题包括：算法偏见与公平性（模型可能放大社会偏见）、隐私保护（数据收集和使用中的隐私风险）、透明度和可解释性（黑箱决策难以解释）、就业影响（自动化可能导致失业）、深度伪造（AI 生成虚假内容）以及自主武器等问题。",
        "keywords": {"伦理", "偏见", "公平性", "隐私", "透明度", "可解释性"},
        "category": "伦理与社会",
    },
    "TensorFlow和PyTorch有什么区别？": {
        "answer": "TensorFlow 由 Google 开发，采用静态计算图，适合工业部署，有 TensorBoard 可视化和 TFLite 移动端部署等生态优势。PyTorch 由 Meta 开发，采用动态计算图，更灵活直观，适合研究和实验。目前学术界偏爱 PyTorch，工业界两者均有广泛使用。",
        "keywords": {"TensorFlow", "PyTorch", "比较", "计算图", "Google", "Meta", "部署"},
        "category": "工具与语言",
    },
    "什么是迁移学习？": {
        "answer": "迁移学习（Transfer Learning）是将在一个任务上学到的知识应用到另一个相关任务上的技术。例如，将在 ImageNet 上预训练的图像分类模型微调到医学影像分类任务中。它能显著减少训练时间和所需数据量，是深度学习中的重要技术。",
        "keywords": {"迁移学习", "预训练", "微调", "知识迁移", "数据量"},
        "category": "核心算法",
    },
}


def extract_all_keywords():
    """从知识库中提取所有关键词，存入集合（自动去重）"""
    all_keywords = set()
    for qa in KNOWLEDGE_BASE.values():
        all_keywords.update(qa["keywords"])
    return all_keywords


ALL_KEYWORDS = extract_all_keywords()


def categorize_knowledge_base():
    """按类别对知识库进行分类，返回 {category: [question, ...]} 字典"""
    categories = {}
    for question, qa in KNOWLEDGE_BASE.items():
        cat = qa["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(question)
    return categories


CATEGORIES = categorize_knowledge_base()


# ============================================================
# 2. 问答匹配逻辑
# ============================================================

def tokenize(text):
    """
    从文本中提取关键词，返回集合。
    支持中英文混合分词：英文按空格分词，中文按单字拆分后合并相邻汉字为 2-4 字词组。
    """
    words = set()
    # 提取英文单词
    en_words = re.findall(r'[a-zA-Z]+', text)
    for w in en_words:
        words.add(w.lower())
    # 提取中文部分，进行简单切分（2-4 字词组）
    cn_chars = re.findall(r'[一-鿿]+', text)
    for segment in cn_chars:
        # 按单字加入，同时加入常见 2 字、3 字、4 字组合
        for i in range(len(segment)):
            words.add(segment[i])
            if i + 1 < len(segment):
                words.add(segment[i:i + 2])
            if i + 2 < len(segment):
                words.add(segment[i:i + 3])
            if i + 3 < len(segment):
                words.add(segment[i:i + 4])
    return words


def match_question(user_input):
    """
    关键词匹配逻辑：
    1. 提取用户输入的关键词集合
    2. 与知识库中每个问题的关键词集合求交集
    3. 交集元素最多的问题为最佳匹配
    4. 若无交集，返回 None
    """
    user_keywords = tokenize(user_input)
    best_question = None
    best_score = 0

    for question, qa in KNOWLEDGE_BASE.items():
        # 将用户输入的词与知识库关键词求交集
        intersection = user_keywords & qa["keywords"]
        score = len(intersection)
        if score > best_score:
            best_score = score
            best_question = question

    return best_question if best_score > 0 else None


# ============================================================
# 3. 可视化交互界面（Tkinter GUI）
# ============================================================

class QAInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("人工智能基础问答系统")
        self.root.geometry("980x640")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        self.query_history = []  # 记录所有用户提问

        self._build_ui()

    def _build_ui(self):
        # ---- 标题 ----
        title_frame = tk.Frame(self.root, bg="#2563eb", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        tk.Label(
            title_frame,
            text="人工智能基础问答系统",
            font=("PingFang SC", 18, "bold"),
            fg="white",
            bg="#2563eb",
        ).pack(expand=True)

        # ---- 主体区域 ----
        main_frame = tk.Frame(self.root, bg="#f0f4f8")
        main_frame.pack(fill="both", expand=True, padx=16, pady=(12, 8))

        # 左侧：问题输入 + 回答显示
        left_frame = tk.Frame(main_frame, bg="#f0f4f8")
        left_frame.pack(side="left", fill="both", expand=True)

        tk.Label(
            left_frame,
            text="请输入您的问题：",
            font=("PingFang SC", 12),
            bg="#f0f4f8",
            anchor="w",
        ).pack(fill="x")

        # 输入框
        self.input_entry = tk.Entry(left_frame, font=("PingFang SC", 13), bd=2, relief="groove")
        self.input_entry.pack(fill="x", pady=(4, 8))
        self.input_entry.bind("<Return>", lambda e: self._submit())

        # 提交按钮
        submit_btn = tk.Button(
            left_frame,
            text="提交问题",
            font=("PingFang SC", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            cursor="hand2",
            command=self._submit,
        )
        submit_btn.pack(pady=(0, 10), ipadx=16, ipady=4)

        # 回答展示区
        tk.Label(
            left_frame,
            text="系统回答：",
            font=("PingFang SC", 12),
            bg="#f0f4f8",
            anchor="w",
        ).pack(fill="x")

        self.answer_text = tk.Text(
            left_frame,
            font=("PingFang SC", 12),
            height=12,
            wrap="word",
            state="disabled",
            bd=2,
            relief="groove",
            bg="#ffffff",
        )
        self.answer_text.pack(fill="both", expand=True, pady=(4, 0))

        # ---- 右侧：知识库分类浏览 ----
        right_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="groove", width=280)
        right_frame.pack(side="right", fill="y", padx=(12, 0))
        right_frame.pack_propagate(False)

        tk.Label(
            right_frame,
            text="知识库分类",
            font=("PingFang SC", 11, "bold"),
            bg="#e0e7ff",
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        canvas = tk.Canvas(right_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#ffffff")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for cat, questions in CATEGORIES.items():
            tk.Label(
                scroll_frame,
                text=f"【{cat}】",
                font=("PingFang SC", 10, "bold"),
                bg="#ffffff",
                fg="#2563eb",
                anchor="w",
            ).pack(fill="x", padx=8, pady=(6, 2))
            for q in questions:
                lbl = tk.Label(
                    scroll_frame,
                    text=f"  · {q}",
                    font=("PingFang SC", 9),
                    bg="#ffffff",
                    fg="#374151",
                    anchor="w",
                    cursor="hand2",
                )
                lbl.pack(fill="x", padx=8, pady=1)
                # 点击问题直接填充输入框并提交
                lbl.bind("<Button-1>", lambda e, question=q: self._fill_and_submit(question))

        # ---- 底部状态栏 ----
        status_frame = tk.Frame(self.root, bg="#e0e7ff", height=28)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        self.status_label = tk.Label(
            status_frame,
            text="知识库共 {} 个问题 | 已记录 0 次提问".format(len(KNOWLEDGE_BASE)),
            font=("PingFang SC", 9),
            bg="#e0e7ff",
            fg="#374151",
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=12)

    def _fill_and_submit(self, question):
        """点击右侧问题后填充输入框并自动提交"""
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, question)
        self._submit()

    def _submit(self):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        # 检查退出指令
        if user_input == "退出":
            self._show_answer("感谢使用，再见！\n\n您的提问记录共 {} 条：\n{}".format(
                len(self.query_history),
                "\n".join(f"  {i+1}. {q}" for i, q in enumerate(self.query_history))
            ))
            self.root.after(1500, self.root.destroy)
            return

        # 记录提问
        self.query_history.append(user_input)

        # 匹配回答
        matched_question = match_question(user_input)
        if matched_question:
            answer = f"【匹配问题】{matched_question}\n\n{KNOWLEDGE_BASE[matched_question]['answer']}"
        else:
            answer = "抱歉，未找到相关答案，请尝试其他问题。"

        self._show_answer(answer)
        self.input_entry.delete(0, "end")
        self._update_status()

    def _show_answer(self, text):
        self.answer_text.config(state="normal")
        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", text)
        self.answer_text.config(state="disabled")

    def _update_status(self):
        self.status_label.config(
            text="知识库共 {} 个问题 | 已记录 {} 次提问".format(
                len(KNOWLEDGE_BASE), len(self.query_history)
            )
        )


# ============================================================
# 主入口
# ============================================================

def main():
    # 打印知识库统计信息
    print("=" * 50)
    print("  人工智能基础问答系统")
    print("=" * 50)
    print(f"知识库问题数：{len(KNOWLEDGE_BASE)}")
    print(f"关键词总数：  {len(ALL_KEYWORDS)}")
    print(f"分类数：      {len(CATEGORIES)}")
    for cat, qs in CATEGORIES.items():
        print(f"  [{cat}] {len(qs)} 个问题")
    print("=" * 50)

    root = tk.Tk()
    app = QAInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
