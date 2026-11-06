# 2026-11-06 内容质量试跑（中国标准时间）

授权：用户“现在试着跑下，我看看内容质量”（pt41u）。本轮只增加两篇内容、真实媒体、许可文本和安全生成产物；不改 UI、JS/CSS、交互、schema、构建/预览脚本或测试。起点为干净的 main，`801d1918e00d3ddba9865793e0b144d4daa524a6`。媒体清单只追加一个新图片数据条目，旧条目与清单头字段不变；它不是前端逻辑改动。

## 入选及来源完整性

### 1. CaptureFlow：边录屏边上传，支持 Docker 自托管

- 维度：建造者真实产物和可按文档复查的自托管流程。
- 站内：`https://xnews.qiaomu.ai/a/captureflow-screen-recorder`。
- 作者原帖：`https://x.com/sardorml/status/2118616954085024133`，2026-11-06 16:10:18 中国标准时间。
- 完整关联 README：`https://github.com/sardorml/captureflow/blob/c5792345e7d5e47084c5e829b3f11c98a432c859/README.md`。实际读取普通分支和固定提交，内容一致；README 的最近改动为 2026-11-04 15:20:58 中国标准时间，未假称当天发行。
- 原文区逐字保留 root post、评论者 @progerallworld 的已取得完整上下文、作者两次回复和完整 README。回复顺序为 16:19:47、16:29:28 中国标准时间，另一个日文公告属于不同 conversation，没有冒充本线程续段。公开作者时间线查询未分页，也未遗漏返回范围中的同线程作者段落；不能声称未来没有新回复。
- 评论者的 Bug 报告用途、作者的认同和 PR 演示补充分别归因，不把评论者的话当作者原话。
- 媒体：两张正文/附件图片；0 视频、0 音频。X 原帖截图 HTTP 200 image/jpeg，163405 字节，原始字节缓存为 `/media/captureflow-screen-recorder-image-5129d6d002.jpg`。固定提交 README 概览图 HTTP 200 image/png，2244892 字节，完整取回并用 Read 检视；只保留原始外链，不把 2.24 MB 大图装入站点。第一次 1.8 MB 下载上限主动停止，不是访问阻断；随后有界取回到研究目录。没有 cookie、私有登录、视频重试或绕过封锁。
- 两张均为产品概览，不能仅凭文件在 README 开头就声称它验证了合并后的某个中文段落。使用诚实的 `after_body` / `source_metadata_only` 标注块，中文与原文区、RSS 各自只出现一次，全部有原作回退。没有编造图表、字幕或画面含义。
- README 的 Logo、动态版本/CI/社交徽章及部署按钮是文档导航/身份元素，不充当新闻图片；全部原始 Markdown 引用仍在 `original.text_md`，没有删除原文。两张实质产品配图均已纳入媒体数组。
- 未安装产品、连接 MCP、试录或试播。作者对 MCP 用途的声明保持归因；Chrome 已上架/macOS 签名版未发布、Whisper 可选服务、Docker 不需 Cloudflare 均按原文限定。

### 2. checkwash 用 Git diff 检查测试弱化，Alpha 版仍有漏检和误报

- 维度：技术深潜、失败/误报证据与检查机制边界，不是泛化“Agent 最佳实践”。
- 站内：`https://xnews.qiaomu.ai/a/checkwash-test-weakening`。
- 作者原帖：`https://x.com/kartg123451/status/2118550260104769565`，2026-11-06 11:45:17 中国标准时间。
- 完整关联 README：`https://github.com/taipei49314/checkwash/blob/0ebd5ad890c252b4546dbd692ac0414fdbc201cc/README.md`。普通分支与固定提交内容一致，最近修改于 2026-11-05 03:16:25 中国标准时间。原帖之后公开作者时间线只返回该 root，无同线程续段。
- 原文保存完整 root 与全部 README，不只保存帖子标题、导语或 GitHub 搜索摘要。原帖无媒体，README 没有实质正文插图，只有 CI/PyPI/许可徽章；原始徽章链接保留。`original.media` 和 `rewrite_media` 都为空，没有造图、造视频。
- 没安装/执行 checkwash，没有修改自己的 CI、规则集、钩子、测试或分支保护。文档命令只是文章内容，不执行其中的外部写入建议。
- 22 个检测器、22461 项测试按 README 自述归因，明确后者是收集分母；不是本站通过数。历史误报、版本/样本/调优口径和当前已知漏检均保留，不能拿 1.72% 当当前通用误报率。

## 逐段信息账本与独立二审

二审另对最终 JSON 的标题、导读、全文、媒体引用逐项回到完整源文本，不是只检查上一版草稿或检测器分数。补充文档链接是查证入口，未打开的子文档没有被冒充已读。上游源码/发行包没有运行，命令没有冒充实测。

### CaptureFlow 覆盖

| 完整源段/章节 | 中文对应与核对重点 |
|---|---|
| root + 两次作者回复 + 评论上下文 | 开头与“能录什么”；MCP 自述、评论归属、PR 描述、扩展观看分别保留 |
| README opening / hero / Features 8 项 | 即时链接、边录边传、三种采集范围、摄像头/麦克风、表情评论/观看者、截图标注、三种可见性、整团队按存储、全功能开源 |
| Where it runs / Get started | Chrome 可用、macOS 源码/签名版状态、现代浏览器；免费账户与三个存储方案，没有编造免费额度 |
| Docker | APP_URL、两条启动命令、./data 三类内容、无 CF 账户、兼容 Whisper 与可选 profile |
| Cloudflare | Workers/D1/R2、四个手动命令、数据库 ID、DEPLOY 路径、实例端点与公司邮箱域限制 |
| Development / Checks | Node 24.13+、pnpm10/corepack、取得源码、四个开发命令与端口、四条检查命令，未伪称运行 |
| Monorepo details | 六个 app、六个 package、单向依赖、Swift 二进制/重建/双架构，不删“细枝末节” |
| Links / Contributing / License | 官方入口、先读规范、安全私报、AGPL/MIT 例外及组合构建范围 |

### checkwash 覆盖

| 完整源段/章节 | 中文对应与核对重点 |
|---|---|
| root / opening | Git diff、本地/无LLM/分析时无网/不执行代码；105.3→正数的同一例子 |
| Claude Code | Python3.11+、本地/共享配置路径、Stop/SessionStart、五项规则、三种编辑工具、claude-p 拒绝、交互未验证、Bash 绕开、非合并门禁 |
| Try it | 固定发行、Windows curl.exe/别名、Mac/Linux/GitBash、两次提交、未提交/两点/三点、v0.8 子目录范围 |
| CI | pull_request、只读权限、三个完整 SHA、checkout 选项、Python3.12、必需且无条件状态检查、规则集新增不替换、doctor 不验证线上保护、升级顺序 |
| Findings | 退出码0/1/2、默认high但warn可过、90/40是强度而非测试期待值、JSON、指纹/理由/基础侧豁免、90/180天、旧.greenwash迁移、不得自行豁免 |
| Limits | alpha、Python主支持/JS有限、无实效+0/模板/AUTHORS可赚修复证据、#419记录未修、两种加严方式及误报代价、doctor配置能力局限 |
| Table tests | v0.8三个each/for缺口；v0.9单元/可计数条件，describe.each行与计算标题仍缺口 |
| Refactor measures | 22/60=36.7%历史，4/60回放，其中2/57严格限定，三个样例错误；v0.10重新核查6/60含新增两项已知误报，不覆盖历史运行结果 |
| Oversize details | 1,000,000字节、unread/term/SARIF/hook/IR差异、检测必读文件、.py/全部pytest配置、根scripts、200字节/shebang/对象ID、无扩展名/64,000,000字节、v0.8与v0.9差异 |
| Oversize continued | JSON-only拒读侧、符号链接目标例外、生成目录例外、根锁文件及清单、stderr/退出码、Stop通常放行与工作区超限窄例外，不删难处理限制 |
| Action trust boundary | ≤0.7工作目录劫持、0.8修复、旧版结果仅参考/关comment-pr、候选CI不是推荐发行证据 |
| Action pin | v0.11 tag第二父的父、doctor一行差异、Action不导入doctor、两个可接受pin、自动更新器/zizmor仅文档推断未实跑、11月4日引擎、CLI不更新Action |
| Options / evidence | 两种pipx安装、8真实篡改+1正常修复不是覆盖保证、六仓1800分母/46/31/15及2.56/1.72/0.83%、v0.3调优语料非留出、24/1800 opaque不证明判决变化、35diff三评审不是46全体、独立v0.3.1重构样本 |
| References / final caveats | 后续核验入口与未满足1.0、两个评测项目、coverage/Ruff/mypy有限预览与legacy比较仍红、Apache、零运行依赖、22/22461口径 |

二审纠正：把“2/57严格限定样本”明确写成“57个限定案例中2个被阻断”，避免分母歧义；没有添加作者未说的性能、收益、趋势或亲身使用体验。概览媒体不伪造逐段证据；原帖发布时间与 README 修改/发行日期分别处理。没有套“不是X而是Y”、空预告、虚构类比或结尾升华。

## 搜索台账与暂缓

- OpenCLI 预检：`opencli list -f yaml`，不可用（command not found）；没有尝试登录或私有账户替代。
- X 公开搜索2次，各20条：① `("I built" OR "my workflow" OR "reproduce") (agent OR LLM) has:links lang:en -is:retweet -is:reply`；② `(postmortem OR "cost per" OR "failed" OR "benchmark") (agent OR coding) has:links lang:en -is:retweet -is:reply`。范围为 11月5日04:25 至 11月6日16:25 中国标准时间；第二次明确补充成本/失败/评测维度。另做公开候选详情批读和两位作者公开续帖核对，不读取自己的账户/私信/Lists/书签。
- WebSearch 2次：① `AI engineering workflow postmortem cost benchmark builder November 5 2026 November 6 2026`；② `site:simonwillison.net "November" "2026" coding agents workflow`。关联一手资料用 WebFetch/公开普通curl与 GitHub 内置只读工具取得，没有写爬虫。
- 去重：按当前13篇的source.url与事件核对，两项都不是原有事件换标题。第二次检查时仓库仍无他人变更。
- 暂缓 KYB、vet402、渗透测试等 X Article：本轮搜索只有标题/导语，未取得足以作为全文的正文，不凭片段收录。
- 暂缓 Python vs Rust 推理性能视频：只有帖子和视频元数据，没有完整字幕或实际视频分析，不根据“约2倍”一句写性能结论。
- SWE-in-a-team：实际公开正文读到，但日期为8月31日、10月22日更新；不当作这24–36小时的新内容。
- Onkar 多Agent成本复盘：读到完整公开正文及发布元数据，但本轮优先两份可固定开源版本、保留完整材料的产物，不为了凑三篇再加一条相近评审主题。
- Arize 换模型实验：读到完整正文，暂留后续对论文/评测器原始产物核验，不拿搜索表格冒充独立复现。

## 构建、保护及发布门

- 完整 `npm test`：15篇，25个Python测试 + 17个reader DOM/state测试全部通过。没有改测试来放行。
- 第一稿的合成开头插图触发两条现有“全文HTML连续子串”断言；该断言不兼容真正的段中媒体。未修改测试/渲染器。产品概览也没有中文逐段一一对应证据，最后采用已有的诚实文末源媒体机制。后续真正有明确段落插图时，应交给Codex调整断言，而非由内容代理偷偷改测试。
- 现有简单 Markdown 渲染器不会正确排版 README fenced code/reference links/表格；所有原始Markdown仍完整保存，中文命令逐条使用行内code，并保留固定GitHub原文回退。本轮不越权修解析器，不把这项格式局限说成内容缺失已修复。
- 13篇旧JSON逐文件SHA-256不变；旧RSS的13个item逐元素字节等价；旧文章HTML、JS/CSS、Worker、构建脚本、schema、测试和编辑提示词均保持原样。
- 原有7个媒体映射原样保留；仅新增一个163405字节JPEG，缓存总量503325字节。PNG不打包。许可文本随公开站点提供。
- 本地HTTP旧/新文章与媒体检查正常；全RSS可解析、15个稳定GUID、新中文/完整原文与每张媒体在两个区块各出现一次。public目录没有QA夹具。
- 没有要求新一轮浏览器QA，没有声称新内容已做浏览器像素/播放验收。既有 `video.twimg.com` 浏览器HTTP403限制不变，不绕过、不声称播放成功；本次两篇没有视频或音频附件。
- 部署/提交结果在本轮最终交接与研究目录的验证记录中报告；没有因本文件写有“站内URL”就声称已上线。
