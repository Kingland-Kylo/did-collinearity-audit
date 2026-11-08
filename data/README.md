# 数据来源与获取

来源：Lucia Motolinia，Harvard Dataverse，V1，DOI [10.7910/DVN/NOMC0H](https://doi.org/10.7910/DVN/NOMC0H)。

Dataverse 的使用条款明确要求：数据集不得在 Harvard Dataverse 之外分发，所有下载应直接从 Dataverse 进行。因此仓库不包含原始数据、作者原代码或其压缩包，也不使用镜像与 Git LFS 重新托管。

```bash
python data/download.py
python data/download.py --check
```

文件写入 `data/raw/`，此目录被 Git 忽略。`sources.json` 固定文件 ID、官方 URL 和 SHA256。已有文件仅在哈希匹配时复用；哈希不匹配会停止，不自动替换来源。显式使用 `--force` 才重新下载。下载记录保存在同样被忽略的 `data/raw/download_record.json`。

| 文件 | 官方文件 ID | 用途 |
|---|---:|---|
| allres.csv | 3892153 | 完整会议级回归数据；`format=original` 返回原始 CSV |
| replication_analysis.do | 3892146 | 作者正文分析代码 |
| replication_appendix.do | 3892135 | 作者附录代码，保留供查阅；本项目未全面重跑附录 |
| replication_cleaning_CTM.R | 3892151 | 作者文本及 CTM 处理代码，保留供查阅 |
| particularistic.csv | 3892157 | 作者定向立法主题分类编号 |

`allres.csv` 为 6,890 行 × 471 列，包含450个主题份额。本项目沿用已估计份额，不重新训练 CTM；若要重新训练，应从 Dataverse 另行获取所需逐字稿、RData 和辅助文件。

原始下载文件的使用条款由来源决定，不适用仓库为新写 Python 实现选择的 MIT 许可证。`output/` 只包含会议级数据计算出的聚合诊断与图形，不包含原始逐行数据。
