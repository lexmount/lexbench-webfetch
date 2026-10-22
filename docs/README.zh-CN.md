<div align="center">

<img src="assets/overview.png" alt="LexBench Web Fetch — Measure what comes back." width="100%">

[English](../README.md) · 简体中文

[![CI](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml/badge.svg)](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/code-MIT-51735b)](../LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-356a91)](../pyproject.toml)

[任务集](#任务集) · [快速开始](#快速开始) · [评测协议](protocol.md) · [参与贡献](../CONTRIBUTING.md)

</div>

---

LexBench Web Fetch 规定抓取系统需要交付哪些内容：网页正文、名称与链接对应的记录、指定资源，或可用的文件。任务的验收规则区分“请求成功”和“交付内容符合要求”。

这个 benchmark 独立于浏览器、服务商和执行脚手架，不依赖 Browser Eval。可以用自己的工具读取 JSON 任务定义，也可以导出经过校验的输入，交给 [Browser Eval](https://github.com/lexmount/browser-eval) 执行。

```mermaid
flowchart LR
    A[版本固定的任务与验收规则] --> B[待测抓取系统]
    B --> C[保存的响应或交付文件]
    A --> D[按任务要求验收]
    C --> D
    E[哈希绑定的参考输入] --> D
```

## 任务集

| 任务集 | 任务记录数 | 范围 |
| --- | ---: | --- |
| `webfetch` | 150 | 网页、文档、图片、视频和挑战页面 |
| `dynamic-content` | 100 | 初始页面响应后加载的正文与记录 |
| `popular-sites` | 100 | 常用网站上与任务相关的内容 |
| `access-restrictions` | 100 | 曾观察到访问限制的网址 |

四组任务分别固定版本，共 450 条任务记录，不代表去重后的 450 个网站，也不直接合成总榜。访问限制描述的是历史观察，网址今天的表现可能不同。WebMainBench、WCXB 和 WebArena 仍是各自独立的上游 benchmark。

每组提供可读的 `tasks.json`、包含原始完整任务哈希的目录，以及绑定可执行数据集和参考文件的清单。详见[数据结构与使用权](data.md)。任务原文和冻结的验收规则保留原语言。

## 快速开始

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)，然后运行：

```sh
git clone https://github.com/lexmount/lexbench-webfetch.git
cd lexbench-webfetch
uv sync --frozen
uv run --frozen lexbench-webfetch list
uv run --frozen lexbench-webfetch validate
```

这一步检查公开任务定义，无需浏览器、API Key 或 Browser Eval。它不访问网站，也不计算评测分数。

复现冻结任务集需要取得获准使用的原始输入。所需文件及哈希列在 `src/lexbench_webfetch/definitions/registry.json` 中。本仓库不分发第三方页面快照，目前也没有公开的完整输入下载包。

```sh
uv run --frozen lexbench-webfetch verify-inputs \
  --suite webfetch --source /absolute/path/approved-inputs
uv run --frozen lexbench-webfetch export \
  --suite webfetch --source /absolute/path/approved-inputs \
  --output /absolute/path/new-input-directory
```

导出工具只复制清单内的文件，并打印可执行数据集路径。缺文件、内容变化或符号链接都会使校验失败，已有输出目录不会被复用。

## 对保存的响应评分

本仓库自带评分器，无需安装 Browser Eval：

```sh
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/answer.txt
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/missing.txt
```

第一份响应通过，第二份失败。若回答含有结构化链接或图片等字段，可通过 `--metadata /absolute/path/metadata.json` 提供，文件内容须为 JSON 对象。元数据不能指定文件验收结果。实际评分时，请使用已校验数据集中的完整任务 JSON。公开任务文件中的参考正文只有哈希绑定，不能替代完整验收输入。文件任务通过可重复的 `--file /absolute/path/file` 提供真实文件；评分器检查字节签名、长度和声明的哈希，不接受调用者自报的通过标记。可选的树结构任务需要先运行 `uv sync --frozen --extra tree`。

使用独立采集的参考输入编译已审定的访问受限任务规则：

```sh
uv run --frozen lexbench-webfetch compile-access-restrictions \
  --evidence-home /absolute/path/reference-data-home --output /absolute/path/new-dataset.json
```

## 执行评测

执行工具读取任务网址与提示词，保存响应或文件，再按任务规则和已校验的参考输入验收。记录 benchmark 提交版本、任务集 ID、输入哈希、待测方法版本、执行策略和评分器版本。分数与耗时的报告方式见[评测协议](protocol.md)。

如果已在另一目录安装 Browser Eval，可在 Browser Eval 根目录运行：

```sh
uv run --frozen browser-harness-eval validate \
  --dataset /absolute/path/new-input-directory/dataset.json
uv run --frozen browser-harness-eval run \
  --dataset /absolute/path/new-input-directory/dataset.json \
  --provider-config configs/providers.quickstart.json --providers http
```

普通运行用于诊断。正式比较实时网站时，还需要完成调用前后的参考内容认证。输入校验只能证明文件版本相符，不能证明网站今天仍然符合旧参考。详见 [Browser Eval 接入说明](https://github.com/lexmount/browser-eval/blob/main/docs/benchmarks.md)。

## 评分规则

0.3 版对事实、标记和固定锚点中的拉丁文使用单词边界匹配。正文事实只匹配返回内容，单独返回的文档标题不能补足正文。中文短语仍按原文匹配，数字和货币保留原有的数值边界检查。

任务可设置 `page_identity_required: true`，要求返回的最终网址符合任务声明；缺少网址或网址不符都会判为未通过。动态任务需要区分完整语言标签时，可再设置 `document_language_match: "exact"`，默认值为 `"primary"`，只比较主语言。这些检查适用于所有接口。没有要求网址元数据的冻结任务，继续按原有内容规则验收。

离线评分会重新计算派生字段，保留原始参考哈希、调用时限证据和文件指纹。文件结论需要当前文件验收依据；旧的通过标记不能认证本次重评分。汇总在原有成功调用耗时之外，提供全部调用的 `mean_all_attempts_ms`、`all_attempts_p50_ms` 和 `all_attempts_p95_ms`，包含失败调用与超时。

上述修改不改写冻结题目，也不自动认证历史成绩。更正分数仍需建立新的证据修订，绑定评分器版本和回归用例。

## 仓库内容

| 路径 | 用途 |
| --- | --- |
| `src/lexbench_webfetch/definitions/` | 任务定义、目录和冻结输入清单 |
| `src/lexbench_webfetch/benchmark.py` | 独立的定义检查与输入导出 |
| `src/lexbench_webfetch/scoring.py` | 统一的任务验收与内容诊断 |
| `src/lexbench_webfetch/risk_control_dataset.py` | 将已审定的访问受限任务规则编译为数据集 |
| `docs/protocol.md` | 验收、证据、耗时和结果报告规则 |
| `tests/` | 输入接受、拒绝及导出行为测试 |

浏览器适配器、凭据、实测结果、报告生成器和托管配置由执行脚手架或外部证据存储管理。任务模型、确定性验收评分、文件字节校验和任务编译由本仓库维护，Browser Eval 通过固定版本的依赖直接调用。本仓库没有实测排行榜。

## 参与贡献

修改任务或提交结果前，请阅读 [CONTRIBUTING](../CONTRIBUTING.md)。`make check` 会检查任务定义和输入工具。安全问题请参阅 [SECURITY](../SECURITY.md)。

项目自有代码和任务定义采用 [MIT 许可](../LICENSE)，第三方原始材料保留各自使用条件，详见 [THIRD_PARTY](../THIRD_PARTY.md)。

## 引用 LexBench Web Fetch

在公开作品中使用本仓库的任务定义或评分工具时，请引用仓库，并记录具体提交和任务集。GitHub 的引用入口读取 [CITATION.cff](../CITATION.cff)。0.3.0 版可这样引用：

```bibtex
@software{lexbench_webfetch_2026,
  author = {{LexBench Web Fetch contributors}},
  title = {LexBench Web Fetch},
  year = {2026},
  version = {0.3.0},
  url = {https://github.com/lexmount/lexbench-webfetch}
}
```

如果还使用了 [Browser Eval](https://github.com/lexmount/browser-eval#cite-browser-eval) 执行脚手架，请单独引用。上游来源或 benchmark 也应按各自的署名要求引用，本仓库的引用不能替代它们。使用其他版本时，请相应修改示例中的版本号和年份，并注明实际 tag 或提交。
