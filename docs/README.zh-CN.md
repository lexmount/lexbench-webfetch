<div align="center">

<img src="assets/overview.png" alt="LexBench Web Fetch — 评测实际返回的内容。" width="100%">

[English](../README.md) · **简体中文**

[![CI](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml/badge.svg)](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/code-Apache--2.0-51735b)](../LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-356a91)](../pyproject.toml)

[任务集](#任务集) · [快速开始](#快速开始) · [评分](#给响应评分) · [参与贡献](../CONTRIBUTING.md)

</div>

LexBench Web Fetch 提供网页获取任务和评分工具，评测正文、带有效链接的记录、资源和文件。可以使用自己的运行器，也可以接入 [Browser Eval](https://github.com/lexmount/browser-eval)。

## 任务集

| 任务集 | 题数 | 范围 |
| --- | ---: | --- |
| `webfetch` | 150 | 网页、文档、图片、视频和挑战页 |
| `dynamic-content` | 100 | 初始响应之后加载的内容和记录 |
| `popular-sites` | 100 | 常用网站的内容 |
| `access-restrictions` | 100 | 曾观察到访问限制的 URL |
| `articles` | 100 | 文章正文、初始评论和帖子列表 |

题库共五个任务集、550 条题目。公开定义包含任务说明和验收规则，完整冻结参考输入需另行获取。详见[数据与获取方式](../docs/data.md)和[文章验收要求](../src/lexbench_webfetch/definitions/evaluation/articles/README.md)。

## 快速开始

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)，然后运行：

```sh
git clone https://github.com/lexmount/lexbench-webfetch.git
cd lexbench-webfetch
uv sync --frozen
uv run --frozen lexbench-webfetch list
uv run --frozen lexbench-webfetch validate
```

这些命令离线检查仓库自带的定义，无需浏览器或 API 密钥。

导出任务集前，先获取其输入清单列出的冻结文件，再运行：

```sh
uv run --frozen lexbench-webfetch export \
  --suite webfetch --source /absolute/path/approved-inputs \
  --output /absolute/path/new-input-directory
```

导出会验证输入哈希，将清单中的文件写入新目录。仓库不分发完整参考快照，目前也没有公开输入包。所需文件和获取条件见[数据指南](../docs/data.md)。

## 给响应评分

用一个应通过和一个应失败的示例试跑：

```sh
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/answer.txt
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/missing.txt
```

实际评测应使用经过验证的数据集中的完整任务。结构化响应字段通过 `--metadata metadata.json` 传入，交付文件通过 `--file /absolute/path/file` 传入。评分要求和结果发布规则见[评测协议](../docs/protocol.md)。

## 版本与运行

运行 `uv run --frozen lexbench-webfetch version` 查看安装的题库版本。标签格式为 `bench-v主版本.次版本.补丁版本`。每份报告通过 `benchmark-release.json` 固定所选题目和评分源码，升级包不会替换这份选择。

用 `release` 固定评测版本，用 `compare-releases` 检查结果是否可比。命令和主版本、次版本、补丁版本规则见[版本说明](../docs/versions.md)。

执行浏览器或服务调用并生成报告，请按 [Browser Eval 接入指南](https://github.com/lexmount/browser-eval/blob/main/docs/benchmarks.md)操作。

## 参与贡献

修改任务要求或评分前，请阅读 [CONTRIBUTING](../CONTRIBUTING.md)。运行 `make check` 检查定义和测试。

[安全](../SECURITY.md) · [第三方内容](../THIRD_PARTY.md) · [Apache 2.0](../LICENSE)

## 引用 LexBench Web Fetch

使用以下引用或 [CITATION.cff](../CITATION.cff)，并注明评测版本和任务集。

```bibtex
@software{lexbench_webfetch_2026,
  author = {{LexBench Web Fetch contributors}},
  title = {LexBench Web Fetch},
  year = {2026},
  version = {0.3.0},
  url = {https://github.com/lexmount/lexbench-webfetch}
}
```
