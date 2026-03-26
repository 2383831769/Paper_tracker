# Paper Tracker 

A lightweight and extensible paper tracking and notification system focused on robotics research, especially **embodied intelligence / robot manipulation / skill learning**. The system automatically collects and filters the latest papers published in major journals and conferences over the past week. For the full list of tracked journals and conferences, please refer to `resource.md`. If you choose `Watch > All Activity` on the GitHub repository, the workflow will run automatically every Monday and deliver the latest filtered results to your GitHub-associated email through GitHub notifications.

## 1. Workflow

1. Resolve whitelisted conference and journal sources from OpenAlex `sources`.
2. Fetch all papers from target sources within the configured time window through the OpenAlex `works` endpoint using `source.id + publication date`.
3. Deduplicate the results, apply topic filtering, remove noisy topics, and normalize source names.
4. Score papers using rule-based signals such as recency, keyword relevance, and source quality.
5. Store results in SQLite and rank papers by score.
6. Output the report to `outputs/weekly/weekly-summary-YYYY-MM-DD.md`.

## 2. Installation

Recommended Python version: `3.11+`

```bash
pip install -r requirements.txt
```

## 3. Local Usage

Run the following command in the project root `Paper_tracker`:

```bash
python -m src.main --days-back 365 --top-n 20
```

After execution, the project will generate:

- SQLite database: `data/tracker.db`
- Detailed report: `outputs/daily/YYYY-MM-DD.md`
- Weekly summary for release publishing: `outputs/weekly/weekly-summary-YYYY-MM-DD.md`

## 4. Customization

If you want to build your own paper tracker based on this project, you can deploy it locally and customize the configuration files directly without modifying the core code:

- `config/keywords.yaml`: define inclusion and exclusion keywords
- `config/venues.yaml`: adjust the target journals and conferences to track
- `config/sources.yaml`: tune fetching behavior, time-window-related settings, and final selection size

By changing these parameters, you can quickly build a tracker tailored to your own research interests.

## 5. Project Structure

```text
Paper_tracker/
  README.md
  requirements.txt
  .gitignore
  config/
    keywords.yaml      # include / exclude keyword configuration
    sources.yaml       # data source configuration (OpenAlex endpoint / page size / timeout)
    venues.yaml        # conference and journal whitelist (canonical/aliases/tier/type)
    scoring.yaml       # scoring configuration
  data/
    raw/
    normalized/
    tracker.db         # generated after running the pipeline
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

## 6. Scoring Rules (MVP)

- `recency_score`: newer papers receive higher scores within the configured time window
- `keyword_score`: papers matching more include keywords receive higher scores, up to a configured cap
- `source_score`: currently based on OpenAlex source weighting, extensible to venue-level weighting
- `total_score`: weighted combination of all current scoring dimensions, with room for future factors such as venue, citation, and code availability

Relevant configuration is stored in `config/scoring.yaml`.

## 7. Source Whitelist Policy (Strict)

The system only fetches and keeps papers from the sources defined in `config/venues.yaml`, including the first-tier and second-tier conferences and journals you specified.

- Source names are normalized to ignore case, spaces, and punctuation differences
- Alias matching is supported (for example `CVPR`, `ICCV`, `ECCV`, `RSS`, `ICRA`, `IROS`, `T-RO`, `IJRR`, `RA-L`, etc.)
- Any paper that cannot be clearly matched to a whitelisted `canonical_name` is discarded
- OpenAlex currently runs in a “fetch all papers from whitelisted sources within a time window” mode:
  - First resolve `source.id` values from the OpenAlex `sources` endpoint
  - Then fetch all papers within the configured time window through the OpenAlex `works` endpoint using `from_publication_date + primary_location.source.id`
  - Finally apply topic relevance filtering locally based on `config/keywords.yaml`
  - Related source configuration is stored in `config/sources.yaml`

## 8. GitHub Actions Automation

The repository includes a workflow file at `.github/workflows/daily_digest.yml`.

- Supports manual triggering (`workflow_dispatch`)
- Supports scheduled weekly execution
- Automatically uploads generated report artifacts

## 9. Run Tests

```bash
pytest
```

---

## 中文说明

一个轻量可扩展的论文自动抓取与推送系统，主要关注机器人领域“具身智能 / 机器人操作 / 技能学习”等方向的相关论文，会自动抓取并筛选近一周内发表于重点期刊和会议的最新论文，具体期刊与会议清单请查看 `resource.md` 文件。若在 GitHub 仓库中选择 `Watch > All Activity`，系统将在每周一自动运行，并将最新筛选结果通过 GitHub 的通知机制推送到你的 GitHub 关联邮箱。

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
- 详细报告：`outputs/daily/YYYY-MM-DD.md`
- 用于发布的周报摘要：`outputs/weekly/weekly-summary-YYYY-MM-DD.md`

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
- 支持每周定时触发（UTC 时间）
- 自动上传日报产物

## 9. 运行测试

```bash
pytest
```
