# Paper Tracker 

<<<<<<< HEAD
面向“机器人 / 具身智能 / 机器人操作”方向的论文自动追踪系统。  
使用更广覆盖学术元数据源（OpenAlex）实现最新前沿高质量论文自动抓取
=======
一个轻量可扩展的论文自动抓取与推送系统，主要关注机器人领域“ 具身智能 / 机器人操作 / 技能学习”等方向的相关论文，会自动抓取并筛选近一周内发表于重点期刊和会议的最新论文，具体期刊与会议清单请查看`resource.md` 文件。若在 GitHub 仓库中选择 `Watch > All Activity`，系统将在每周一自动运行，并将最新筛选结果通过 GitHub 的通知机制推送到你的 GitHub 关联邮箱。
>>>>>>> ebe865f (docs_and_resources_update)

## 1. 运行流程

1. 先在 OpenAlex 的 `sources` 中解析白名单会议/期刊来源。
2. 用 OpenAlex 的 `works` 端点按 `时间窗 + source.id` 全量抓取目标来源中的论文。
3. 对返回结果做去重、主题筛选、噪声排除和来源标准化校验。
4. 使用规则进行评分（新近性、关键词相关性、来源分）。
5. 存入 SQLite 并基于分数排序。
6. 输出报告到 `outputs/weekly/weekly-summary-YYYY-MM-DD.md`。

## 2. 安装方式

Python 版本建议：`3.11+`

```bash
pip install -r requirements.txt
```

## 3. 本地运行方式

在项目根目录 `Paper_tracker` 下执行：

```bash
python -m src.main --days-back 365 --top-n 20
```

运行后会产生：

- SQLite 数据库：`data/tracker.db`
- 每日报告：`outputs/daily/YYYY-MM-DD.md`

## 4. 自定义配置

如果你希望基于当前项目制作自己的论文追踪器，可以在本地部署后直接修改配置文件，而无需改动核心代码：

- `config/keywords.yaml`：用于自定义检索关键词与排除关键词
- `config/venues.yaml`：用于调整追踪的目标期刊与会议来源
- `config/sources.yaml`：用于调整抓取参数、时间窗相关行为以及最终筛选数量等

通过修改这些参数，可以快速构建适合自己研究方向的论文追踪器。

## 5. 目录说明

```text
Paper_tracker/
  README.md
  requirements.txt
  .gitignore
  config/
    keywords.yaml      # include / exclude 关键词配置
    sources.yaml       # 数据源配置（OpenAlex endpoint / 分页大小 / 超时）
    venues.yaml        # 会议/期刊白名单（canonical/aliases/tier/type）
    scoring.yaml       # 评分规则配置
  data/
    raw/
    normalized/
    tracker.db         # 运行后自动生成
  outputs/
    daily/
    weekly/
  src/
    main.py
    fetchers/
      arxiv_fetcher.py
    processors/
      normalize.py
      filter.py
      score.py
      dedup.py
    storage/
      sqlite_store.py
    renderers/
      markdown_report.py
    models/
      paper.py
    utils/
      logging_utils.py
      text_utils.py
  tests/
    test_filter.py
    test_score.py
    test_dedup.py
  .github/workflows/
    daily_digest.yml
```

## 6. 评分规则（MVP）

- `recency_score`：在配置窗口期内越新越高。
- `keyword_score`：命中 include 关键词越多越高（有最大命中数上限）。
- `source_score`：当前 OpenAlex 基础分，可扩展会议/期刊加权。
- `total_score`：按权重汇总并预留未来扩展项（venue/citation/code）。

相关配置位于 `config/scoring.yaml`。

## 7. 来源白名单策略（严格）

系统当前只抓取并保留 `config/venues.yaml` 中定义的来源，包含你指定的第一、二梯队会议与期刊：

- 来源名称先做标准化（忽略大小写、空格、标点）
- 支持别名映射（如 `CVPR`, `ICCV`, `ECCV`, `RSS`, `ICRA`, `IROS`, `T-RO`, `IJRR`, `RA-L` 等）
- 若无法明确匹配到白名单 `canonical_name`，该论文会被直接丢弃
- OpenAlex 当前采用“来源内全量抓取”模式：
  - 先到 `sources` 端点解析白名单 venue 对应的 `source.id`
  - 再到 `works` 端点使用 `from_publication_date + primary_location.source.id` 抓取固定时间窗内的全部论文
  - 本地再根据 `config/keywords.yaml` 做主题相关性筛选
  - 相关配置位于 `config/sources.yaml`

## 8. GitHub Actions 自动化

已提供工作流：`.github/workflows/daily_digest.yml`

- 支持手动触发（`workflow_dispatch`）
- 支持定时触发（每天一次，UTC 时间）
- 自动上传日报产物

## 9. 运行测试

```bash
pytest
```