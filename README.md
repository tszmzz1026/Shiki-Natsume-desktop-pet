这是四季夏目桌宠，灵感来源于https://www.bilibili.com/video/BV1xaVv6LEa4/?spm_id_from=333.337.search-card.all.click&amp;vd_source=46fd7374e49810c8909c9bf1ab9ec827

自己做了人物卡和语音卡，在一定的程度上修复了原来程序存在的tts语音问题

实际运行图长这样



<img width="307" height="307" alt="Snipaste_2026-08-31_17-58-15" src="https://github.com/user-attachments/assets/8051b0f2-b1e5-406a-bddf-e7f59b9ebd71" />

## 下载与安装

[下载最新 Windows 完整包](https://github.com/tszmzz1026/Shiki-Natsume-desktop-pet/releases/latest)

1. 解压到纯英文路径，例如 `D:\sakura-natsume`。
2. 双击 `install.bat` 安装依赖。
3. 双击 `start.bat` 启动，并在设置中填写模型 API。

完整包已包含四季夏目角色、立绘和 Git LFS 语音模型，无需另外执行 `git lfs pull`。



# Sakura Natsume 桌宠完整使用手册

本文档面向从本仓库源码运行「四季夏目（Shiki Natsume）桌宠」的用户。
内容包括：独立可用性说明、环境安装、角色包、首次配置、每个设置页、
日常使用、工具、长期记忆、TTS 语音、MCP、插件、数据文件、更新维护、
测试以及常见问题。

## 1. 这个仓库现在包含什么

```text
sakura-natsume/
├─ main.py                  # 程序入口
├─ install.bat / start.bat  # Windows 安装/启动
├─ app/                     # 桌宠核心代码
├─ characters/Natsume/      # 四季夏目角色包（已加入仓库，使用 Git LFS）
│  ├─ character.json        # 角色清单
│  ├─ card.md               # 角色卡
│  ├─ portraits/            # 默认立绘与表情立绘
│  └─ voice/                # GPT-SoVITS 语音模型与参考音频
├─ plugins/                 # 内置插件（Playwright 浏览器等）
├─ sdk/                     # 插件开发 SDK
├─ third_party/             # mem0 等内置第三方依赖
├─ tools/mcp/               # Windows MCP 服务
├─ tests/                   # 单元/集成测试
└─ docs/                    # 文档
```

角色包目前包含：

- `character.json`：角色 id、显示名、立绘、语气、语音引用。
- `card.md`：四季夏目的角色设定与系统提示词。
- `portraits/`：14 张 PNG 立绘，随语气切换表情。
- `voice/models/`：GPT 模型、SoVITS 模型和底模，共 6 个大文件。
- `voice/refs/`：语气参考音频（`tone_refs`、`refs_padded`）。

语音模型文件较大，仓库使用 Git LFS 管理；普通网页 ZIP 不会包含这些文件，
请使用 `git clone` 配合 `git lfs pull` 获取完整角色包。

## 2. 源码能否独立使用

可以运行，但需要补齐运行环境，不是“解压即用”。

仓库源码已包含四季夏目角色文件，但仍按 `.gitignore` 排除了：

| 内容 | 是否在仓库 | 是否必须 |
|---|---|---|
| `runtime/` 内置 Python | 否 | 可选 |
| `characters/Natsume/` 角色包 | 是（LFS） | 必须 |
| `tts/` GPT-SoVITS 整合包 | 否 | 可选 |
| `data/config/*.yaml` 本地配置 | 否 | 运行后生成 |
| LLM API Key | 否 | 必须 |

最小可用路径：

1. 准备 Python 3.10+ 或 `runtime/`。
2. 确保 `characters/Natsume/character.json` 存在。
3. 运行 `install.bat` 安装依赖。
4. 配置一个 OpenAI 兼容的 LLM API（推荐多模态模型）。
5. 运行 `start.bat`。

不配置 TTS 也可以使用，只是没有语音，只显示字幕。

## 3. Windows 安装

### 3.1 基础条件

- Windows 10/11 64 位。
- 项目路径必须是纯英文和数字，例如 `C:\sakura-natsume`。
  PySide6 在含中文的路径下可能崩溃，`install.bat`/`start.bat` 会主动拒绝启动。
- 没有 `runtime/` 时，需要安装 Python 3.10+ 并加入 PATH。
- 磁盘空间建议预留 3GB 以上（依赖 + 角色包 + 可选 TTS）。

### 3.2 安装依赖

如果仓库里没有 `runtime/`，有两种方式：

方式一：使用系统 Python。

```powershell
cd C:\sakura-natsume
python -m pip install -r requirements.txt
python -m pip install -r requirements.txt --progress-bar off
```

方式二：双击 `install.bat`，脚本会自动：

1. 优先寻找 `runtime/python.exe`，找不到再用系统 `python`。
2. 使用阿里云/清华镜像安装依赖。
3. 验证 PySide6 与 Playwright 是否可以导入。

安装完成后，再执行一次 Chrome 浏览器组件安装（可用可不用）：

```powershell
python -m playwright install chromium
```

如果使用内置 runtime：

```powershell
runtime\python.exe -m playwright install chromium
```

### 3.3 获取完整角色包

从 GitHub 克隆仓库后执行：

```powershell
git clone https://github.com/tszmzz1026/Shiki-Natsume-desktop-pet.git
cd Shiki-Natsume-desktop-pet
git lfs pull
```

也可以把已经存在的 `characters/Natsume/` 目录直接复制到项目根目录。
程序启动时会扫描 `characters/*/character.json`。

### 3.4 启动

```powershell
start.bat
```

等价命令：

```powershell
python main.py
```

运行时若发现没有角色包，会打开首次配置窗口，此时可直接导入 `.char`。

## 4. macOS / Linux 安装

```bash
cd sakura-natsume
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

macOS 注意事项：

- python.org 安装的 Python 需要先运行
  `/Applications/Python 3.x/Install Certificates.command`，否则 SSL 报错。
- Apple Silicon 如果处于 Rosetta/x86 环境，需要追加
  `pip install -r requirements-macos-intel.txt`。
- 内置 TTS 整合包是 Windows runtime，macOS/Linux 请使用
  `custom-gpt-sovits` 方式连接自己启动的 GPT-SoVITS 服务。
- 详细内容见 `docs/MACOS_SETUP.md`。

## 5. 首次运行与设置窗口

设置窗口左侧有 9 个分类：

`角色 / 外观 / 模型 / 语音 / 隐私 / 工具 / 插件 / 系统 / 记忆`

### 5.1 角色

- 显示当前角色与角色包状态。
- 点击“导入 .char”导入完整角色包（含立绘、角色卡、可选语音）。
- 从下拉框切换当前角色。
- 可导出完整 `.char`、单角色包或语音包。
- 可为当前角色单独导入语音模型包。

角色包目录结构：

```text
characters/<角色id>/
├─ character.json
├─ card.md
├─ portraits/
└─ voice/
   ├─ models/
   └─ refs/
```

本仓库已经准备好 `characters/Natsume/`，一般情况下无需再导入。

### 5.2 外观

- 跟随角色主题，或手动编辑主色、强调色、背景色、气泡色。
- 可以启用 AI 配色：让模型根据默认立绘生成主题色。
- 窗口视觉效果可选纯色、高斯模糊、亚克力等。
- 可调整立绘缩放比例、输入栏宽度、气泡高度、面板垂直偏移等。

### 5.3 模型（LLM API）

字段：

- Base URL：OpenAI 兼容地址，通常以 `/v1` 结尾。
- API Key：密钥，一般以 `sk-` 开头。
- 模型名：服务商提供的模型名，可点击“检测模型”自动获取。
- 高级参数：temperature、top_p、max_tokens 可选。

重要：

- 建议使用多模态（图像识别）模型，否则“屏幕观察/截图”功能会失败。
- 官方文档明确不建议使用 DeepSeek 系列。
- 配置保存在 `data/config/api.yaml`，已被 `.gitignore` 忽略。

示例：

```yaml
llm:
  base_url: "https://api.openai.com/v1"
  api_key: "sk-你的密钥"
  model: "gpt-4.1-mini"
  timeout_seconds: 60
```

### 5.4 语音（TTS）

可选功能。不启用时桌宠只使用字幕。

提供三种 provider：

| Provider | 说明 |
|---|---|
| GPT-SoVITS 整合包（GPU） | Windows，软件内一键下载，适合 NVIDIA 显卡 |
| Genie TTS 整合包（CPU） | 适合无独显/CPU 推理 |
| 自定义 GPT-SoVITS | macOS/Linux，或自行启动的外置服务 |

字段：

- API URL：默认 `http://127.0.0.1:9880/tts`。
- TTS 工作目录：本地整合包路径，例如 `D:/sakura/tts/g50`。
- TTS Python：自定义 provider 使用的 Python 解释器。
- 推理配置：可选 `tts_infer.yaml` 路径。
- 参考语言/文本语言：一般跟随角色包，默认 `ja` 或 `zh`。
- 超时：单次 TTS 请求超时秒数。

手动配置示例：

```yaml
tts:
  provider: gpt-sovits
  enabled: true
  gpt_sovits:
    api_url: "http://127.0.0.1:9880/tts"
    work_dir: "D:/sakura/tts/g50"
    python_path: ""
    tts_config_path: ""
    ref_lang: ja
    text_lang: ja
    timeout_seconds: 60
```

### 5.5 隐私（主动关怀）

- 允许模型主动获取屏幕信息：控制桌宠能否定期查看屏幕，也是手动截图的开关。
- 主动检查间隔：1-120 分钟，决定多久主动看一次屏幕。
- 主动打扰冷却：1-120 分钟，避免连续主动发言。
- 单次最多发送截图：1-20 张，限制单次上下文中的截图数量。

关闭“允许模型主动获取屏幕信息”后，主动关怀循环停止，
手动框选截图按钮也会被禁用。

### 5.6 工具（MCP）

- Web 搜索 MCP：默认开启，提供网页搜索能力，由内置 stdio 服务启动。
- Windows MCP 桌面控制：实验性功能，默认关闭。
  开启后提供 App、Snapshot、Screenshot、Click、Type、Wait 等桌面工具。
- Windows MCP 保存后需要重启程序才生效。
- 第三方工具设置面板也会出现在这里（如 Playwright 浏览器设置）。

### 5.7 插件

插件表按“启用/名称/版本/优先级/来源/介绍”展示：

- `playwright_browser`：默认启用，提供浏览器导航、搜索、截图、点击、
  填表、执行 JS 等工具。
- `example_plugin`：示例插件，默认关闭。
- 修改启用状态后需要重启程序。

### 5.8 系统

- 登录时自动启动。
- 终端调试日志、完整请求/回复正文、文件运行日志。
- 字幕逐字间隔。
- 回复分段停顿。
- 气泡无操作后自动隐藏，及隐藏等待时长。

### 5.9 记忆

- 查看长期记忆列表。
- 搜索、新增、编辑、删除记忆。
- 手动导入 `all-MiniLM-L6-v2` 离线 ZIP。
- 首次使用会显示“长期记忆系统正在初始化...”，此时程序会在后台下载
  本地向量模型。

## 6. 日常使用

### 6.1 主界面

桌宠窗口包含：

- 立绘区，根据回复语气自动切换表情。
- 对话气泡，逐字显示字幕。
- 输入栏，可输入消息并发送。
- 截图按钮：点击后全屏框选，把截图附加到下一条消息；右键按钮清除已附加截图。

### 6.2 截图与屏幕观察

- 手动：点输入栏截图图标，框选区域后发送。
- 自动：开启隐私设置中的“允许模型主动获取屏幕信息”，桌宠会按间隔
  抓取屏幕摘要并纳入主动关怀上下文。
- 手动截图需要多模态模型，否则会提示模型不支持图像。

### 6.3 托盘菜单

右键桌宠图标或托盘图标：

- 隐藏至托盘 / 显示桌宠
- 显示中文字幕
- 完整访问权限
- 保持置顶
- 历史记录
- 运行日志
- 设置
- 退出

### 6.4 历史记录

历史窗口支持：

- 刷新。
- 清空历史。
- “清除并保存至记忆”：清空聊天记录前先整理成长期记忆。

### 6.5 权限模式

- 默认情况下高风险工具（打开网页、打开本地文件夹、浏览器操作等）
  执行前会弹确认面板。
- 托盘开启“完整访问权限”后，跳过部分确认，直接执行工具。
- 建议只在信任角色与可信模型时开启。

## 7. 内置工具能力

对话时模型可以调用以下内置工具：

| 工具 | 能力 |
|---|---|
| `screen_observe` | 查看当前屏幕并生成视觉摘要 |
| `get_current_time` | 获取本机时间与时区 |
| `add_todo` / `list_todos` / `complete_todo` | 待办管理 |
| `add_reminder` | 创建一次性提醒，支持“3 分钟后”相对时间 |
| `list_reminders` / `cancel_reminder` | 提醒管理 |
| `read_note` / `write_note` | 读写 `data/notes/` 下的文本笔记 |
| `open_url` | 打开网页（需确认） |
| `open_local_folder` | 打开本地文件夹（需确认） |
| `memory_search` | 搜索长期记忆 |
| `memory_remember` | 保存长期记忆 |
| `memory_forget` | 删除记忆 |
| `search_tools` / `list_tool_groups` | 搜索和列出当前可用工具组 |

启用 Playwright 插件后额外提供：

- `playwright_navigate`：打开网页。
- `playwright_get_text`：读取页面文本。
- `playwright_search_web`：网页搜索。
- `playwright_screenshot`：网页截图。
- `playwright_click` / `playwright_fill`：页面操作。
- `playwright_evaluate`：执行页面 JavaScript（高风险）。

启用 Windows MCP 后提供桌面 App/Snapshot/Screenshot/Click/Type/Wait 工具。

## 8. 长期记忆系统

记忆基于仓库内置的 mem0 与 Qdrant，使用本地
`sentence-transformers/all-MiniLM-L6-v2` 生成向量。

- 数据位置：`data/memory.json`、`data/memory_curation_state.json`。
- 首次启动后台下载模型；下载失败时可设置：
  ```powershell
  set HF_ENDPOINT=https://hf-mirror.com
  ```
- 也可从设置页“记忆”手动导入离线 ZIP。
- 系统会定期整理候选记忆，默认对话 8 轮后触发一次整理。
- 敏感信息（密码、token、密钥、身份证、银行卡）不应被保存到记忆。

## 9. TTS 语音深入说明

四季夏目角色包的 `voice/` 目录包含 GPT 模型、SoVITS 模型和语气参考音频。
程序启动后会：

1. 读取角色包 `character.json` 中的 `voice` 配置。
2. 根据 settings 的 TTS provider 创建对应播放器。
3. 把角色微调模型推送到本地 GPT-SoVITS 服务。
4. 根据回复中的语气标签选择参考音频。

如果角色没有 `voice/`，或 TTS 配置无效，程序会自动降级为字幕模式，
并在日志中提示 `TTS 配置无效，已禁用 TTS`。

Windows 内置整合包下载器会将包安装到 `data/tts_bundles/` 或指定
`work_dir`。不同电脑需要重新设置本机路径。

## 10. MCP 与插件开发

- MCP 配置：`data/config/mcp.yaml`。
- Web 搜索：默认启用，调用 `app/agent/mcp/web_search_server.py`。
- Windows MCP：默认关闭，通过 `tools/mcp/Windows-MCP-0.8.0` 运行，
  工具包含 App、Snapshot、Screenshot、Click、Type、Wait。
- 插件目录：`plugins/`；仓库内置 Playwright 插件。
- SDK 文档：`docs/SAKURA_PLUGIN_SDK.md`。
- 第三方插件会安装到 `plugins/`，但 `.gitignore` 只保留仓库内置插件与示例。

## 11. 配置与数据文件

### 11.1 配置

| 文件 | 内容 |
|---|---|
| `data/config/api.yaml` | LLM 与 TTS 配置，含 API Key，不入库 |
| `data/config/characters.yaml` | 当前角色 id |
| `data/config/system_config.yaml` | 主动关怀、UI、MCP、调试设置 |
| `data/config/mcp.yaml` | MCP 服务配置 |
| `data/config/plugins.yaml` | 插件启用与优先级 |

### 11.2 运行时数据

| 路径 | 内容 |
|---|---|
| `data/tasks.json` | 待办 |
| `data/reminders.json` | 提醒 |
| `data/notes/` | 文本笔记 |
| `data/chat_history/` | 聊天历史 |
| `data/memory.json` | 长期记忆 |
| `data/visual_observations/` | 屏幕观察记录 |
| `data/runtime_events/` | 运行时事件日志 |
| `data/logs/` | 文件运行日志 |
| `data/cache/tts/` | TTS 临时音频缓存 |

以上路径已在 `.gitignore` 中，不会上传 GitHub。

## 12. 更新与维护

```powershell
git pull
git lfs pull
python -m pip install -r requirements.txt
python main.py
```

如果旧版本 TTS 目录结构有变化，启动时会出现“TTS 整合包迁移”窗口，
迁移过程中不要强制关闭程序。

升级依赖后如果启动报错，优先重跑 `install.bat`。

## 13. 测试与开发

```powershell
python -m pytest
```

只跑单元测试：

```powershell
python -m pytest tests/unit
```

只跑某个文件：

```powershell
python -m pytest tests/unit/test_tts.py -v
```

开发插件参考：

- `plugins/example_plugin/plugin.py`
- `docs/SAKURA_PLUGIN_SDK.md`

## 14. 常见问题（FAQ）

### 14.1 启动报“项目路径包含非英文字符”

把项目移动到纯英文路径，例如 `D:\sakura-natsume`。

### 14.2 找不到角色包

确认存在 `characters/Natsume/character.json`。
从 GitHub 拉取后执行 `git lfs pull`。

### 14.3 克隆后语音模型是几百字节的文本

那些是 Git LFS 指针，需要执行：

```powershell
git lfs pull
```

### 14.4 API 401 / 测试失败

- 检查 Base URL 是否以 `/v1` 结尾。
- 检查 API Key 是否复制完整、无空格。
- 检查模型名是否正确。
- 多模态功能需要模型支持图像输入。

### 14.5 截图或屏幕观察报错

- 检查模型是否支持图像。
- 检查“隐私”中“允许模型主动获取屏幕信息”是否开启。
- 检查 API 请求是否有上下文长度限制。

### 14.6 没有声音

- 确认角色包有 `voice/`。
- 确认 TTS 已启用。
- 确认 `work_dir` 指向本机实际整合包路径。
- 确认 GPT-SoVITS 服务在 `http://127.0.0.1:9880/tts`。
- 查看运行日志中的 TTS 错误。

### 14.7 记忆模型下载失败

```powershell
set HF_ENDPOINT=https://hf-mirror.com
python main.py
```

或在“记忆”设置页手动导入离线 ZIP。

### 14.8 Playwright 工具不可用

```powershell
python -m playwright install chromium
```

### 14.9 Windows MCP 工具不出现

在“工具”设置页开启 Windows MCP，保存后重启程序。

### 14.10 日志位置

- 终端：运行程序的控制台。
- 文件：`data/logs/`。
- 设置页开启“输出文件运行日志”后才会写文件日志。
