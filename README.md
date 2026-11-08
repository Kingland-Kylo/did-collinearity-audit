# 读论文

按论文分别存放阅读材料、分析 notebook 和报告。后续论文在根目录下新增独立文件夹。

```text
读论文/
├── README.md
├── .gitattributes                    # 保持 PDF 二进制原样
├── .gitignore
├── download_data.py                 # 从官方来源获取并校验原始文件
├── .venv/                           # 本地 Python 虚拟环境，不上传
└── Motolinia-读论文/
    ├── Motolinia_复现与质疑.ipynb   # 分析代码与说明
    ├── requirements.txt             # notebook 依赖
    ├── 原文.pdf                     # 作者原文
    ├── 阅读报告/                    # 预留阅读/审计报告 PDF，当前为空
    └── 原作者文件/                  # 本地保留，Git 忽略
```

`原作者文件/` 和虚拟环境只保留在本地。notebook 提交版清空运行输出；阅读报告目录中的 `.gitkeep` 仅用于保留空目录。
