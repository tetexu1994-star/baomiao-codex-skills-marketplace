# 百灵鸟 Codex 插件市场逐项对标表

- 对标来源：[https://cnb.cool/echobird/codex-plugins](https://cnb.cool/echobird/codex-plugins)
- 固定提交：`cd7d52b8bb3689f7838af8ff1722c7c6773f9312`
- 生成条目：180
- 暴喵当前插件：72
- 用途：仅生成候选判断，不复制或自动发布第三方插件。

## 结论

百灵鸟默认市场共有 **180** 个插件，其中 **36** 个没有把 `openai/plugins` 声明为上游，说明它确实聚合了多个外部来源。

| 建议 | 数量 | 含义 |
|---|---:|---|
| 已覆盖 | 0 | 暴喵已有同 ID、同上游插件 |
| 可进入候选 | 3 | 包内有许可文件且未发现脚本，可进入候选同步，不代表自动发布 |
| 需单独复核 | 168 | 缺许可证据、含脚本或与现有同名插件来源不同 |
| 暂不接入 | 9 | Proprietary、UNLICENSED 或许可证字段缺失 |

## 内容形态

| 形态 | 数量 |
|---|---:|
| App | 154 |
| Skills | 72 |
| Scripts | 9 |
| MCP | 8 |

## 许可证声明

| 声明 | 数量 |
|---|---:|
| MIT | 164 |
| Apache-2.0 | 6 |
| Proprietary | 5 |
| UNLICENSED | 2 |
| Apache-2.0 AND CC-BY-4.0 | 1 |
| LicenseRef-Figma-Developer-Terms | 1 |
| 缺失 | 1 |

## 主要声明上游

| 仓库 | 数量 |
|---|---:|
| [https://github.com/openai/plugins](https://github.com/openai/plugins) | 144 |
| [https://github.com/vercel/vercel-plugin](https://github.com/vercel/vercel-plugin) | 1 |
| [https://github.com/obra/superpowers](https://github.com/obra/superpowers) | 1 |
| [https://github.com/circleci-public/skills](https://github.com/circleci-public/skills) | 1 |
| [https://github.com/openai/plugins/tree/main/plugins/deepnote](https://github.com/openai/plugins/tree/main/plugins/deepnote) | 1 |
| — | 1 |
| [https://github.com/openai/openai/tree/master/plugins/life-science-research](https://github.com/openai/openai/tree/master/plugins/life-science-research) | 1 |
| [https://github.com/expo/skills/tree/main/plugins/expo](https://github.com/expo/skills/tree/main/plugins/expo) | 1 |
| [https://github.com/coderabbitai/codex-plugin](https://github.com/coderabbitai/codex-plugin) | 1 |
| [https://github.com/remotion-dev/remotion](https://github.com/remotion-dev/remotion) | 1 |
| [https://github.com/daloopa/daloopa-plugin-codex](https://github.com/daloopa/daloopa-plugin-codex) | 1 |
| [https://github.com/openai/plugins/tree/main/plugins/hex](https://github.com/openai/plugins/tree/main/plugins/hex) | 1 |

## 180 项逐项对标

| # | 插件 ID | 显示名称 | 分类 | 形态 | 许可声明 | 许可文件 | 声明上游 | 与暴喵关系 | 建议 | 原因 |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | linear | Linear | Productivity | App+MCP+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 同名不同源 | 需单独复核 | 包内缺少许可证证据；与现有同名插件来源不同 |
| 2 | atlassian-rovo | Atlassian Rovo | Productivity | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 1 个脚本/可执行文件 |
| 3 | google-calendar | Google Calendar | Productivity | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 1 个脚本/可执行文件 |
| 4 | gmail | Gmail | Communication | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 5 | slack | Slack | Communication | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 6 | teams | Teams | Communication | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 7 | sharepoint | SharePoint | Productivity | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 8 | outlook-email | Outlook Email | Communication | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 9 | outlook-calendar | Outlook Calendar | Productivity | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 10 | canva | Canva | Creativity | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 11 | figma | Figma | Creativity | App+MCP+Skills+Scripts | LicenseRef-Figma-Developer-Terms | LICENSE.txt | [github.com](https://github.com/openai/plugins) | 未收录 | 暂不接入 | 许可证声明为 LicenseRef-Figma-Developer-Terms |
| 12 | hugging-face | Hugging Face | Developer Tools | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 19 个脚本/可执行文件 |
| 13 | jam | Jam | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 14 | netlify | Netlify | Developer Tools | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 15 | stripe | Stripe | Finance | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 16 | vercel | Vercel | Developer Tools | App+Skills | Apache-2.0 | — | [github.com](https://github.com/vercel/vercel-plugin) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 17 | game-studio | 游戏工作室 | Developer Tools | Skills+Scripts | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 3 个脚本/可执行文件 |
| 18 | superpowers | Superpowers | Developer Tools | Skills | MIT | LICENSE | [github.com](https://github.com/obra/superpowers) | 未收录 | 需单独复核 | 含 6 个脚本/可执行文件 |
| 19 | box | Box | Productivity | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 2 个脚本/可执行文件 |
| 20 | github | GitHub | Developer Tools | App+MCP+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 2 个脚本/可执行文件 |
| 21 | circleci | CircleCI | Developer Tools | Skills | MIT | — | [github.com](https://github.com/circleci-public/skills) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 22 | google-drive | Google Drive | Productivity | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 23 | deepnote | Deepnote | Data & Analytics | App+Skills | Apache-2.0 | — | [github.com](https://github.com/openai/plugins/tree/main/plugins/deepnote) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 24 | notion | Notion | Productivity | App+MCP+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 25 | cloudflare | Cloudflare | Developer Tools | MCP+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 26 | sentry | Sentry | Developer Tools | Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 1 个脚本/可执行文件 |
| 27 | build-ios-apps | Build iOS Apps | Developer Tools | MCP+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 6 个脚本/可执行文件 |
| 28 | build-macos-apps | Build macOS Apps | Developer Tools | Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 29 | build-web-apps | Build Web Apps | Developer Tools | Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 30 | build-web-data-visualization | Build Web Data Visualization | Developer Tools | Skills | MIT | — | — | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 31 | test-android-apps | Test Android Apps | Developer Tools | Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 4 个脚本/可执行文件 |
| 32 | life-science-research | Life Science Research | Education & Research | Skills | Proprietary | — | [github.com](https://github.com/openai/openai/tree/master/plugins/life-science-research) | 未收录 | 暂不接入 | 许可证声明为 Proprietary |
| 33 | zotero | Zotero | Education & Research | Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 1 个脚本/可执行文件 |
| 34 | expo | Expo | Developer Tools | Skills | MIT | LICENSE | [github.com](https://github.com/expo/skills/tree/main/plugins/expo) | 未收录 | 需单独复核 | 含 2 个脚本/可执行文件 |
| 35 | coderabbit | CodeRabbit | Developer Tools | Skills | MIT | — | [github.com](https://github.com/coderabbitai/codex-plugin) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 36 | neon-postgres | Neon Postgres | Developer Tools | App+Skills | Apache-2.0 | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 37 | remotion | Remotion | Creativity | Skills | MIT | — | [github.com](https://github.com/remotion-dev/remotion) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 38 | plugin-eval | Plugin Eval | Developer Tools | Skills+Scripts | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 35 个脚本/可执行文件 |
| 39 | alpaca | Alpaca | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 40 | amplitude | Amplitude | Data & Analytics | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 41 | attio | Attio | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 42 | binance | Binance | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 43 | biorender | BioRender | Creativity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 44 | brand24 | Brand24 | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 45 | brex | Brex | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 46 | carta-crm | Carta CRM | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 47 | cb-insights | CB Insights | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 48 | channel99 | Channel99 | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 49 | circleback | Circleback | Communication | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 50 | clickup | ClickUp | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 51 | cloudinary | Cloudinary | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 52 | cogedim | Cogedim | Other | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 53 | common-room | Common Room | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 54 | conductor | Conductor | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 55 | coupler-io | Coupler.io | Data & Analytics | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 56 | coveo | Coveo | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 57 | cube | Cube | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 58 | daloopa | Daloopa | Finance | App+Skills+Scripts | Apache-2.0 | LICENSE | [github.com](https://github.com/daloopa/daloopa-plugin-codex) | 未收录 | 需单独复核 | 含 1 个脚本/可执行文件 |
| 59 | demandbase | Demandbase | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 60 | dnb-finance-analytics | D&B Finance Analytics | Finance | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 61 | docket | Docket | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 62 | domotz-preview | Domotz（预览版） | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 63 | dovetail | Dovetail | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 64 | dow-jones-factiva | Dow Jones Factiva | Education & Research | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 65 | egnyte | Egnyte | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 66 | finn | FINN | Travel | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 67 | fireflies | Fireflies | Communication | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 68 | fyxer | Fyxer | Communication | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 69 | govtribe | GovTribe | Education & Research | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 70 | granola | Granola | Communication | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 71 | happenstance | Happenstance | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 72 | help-scout | Help Scout | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 73 | hex | Hex | Data & Analytics | App+Skills | Proprietary | — | [github.com](https://github.com/openai/plugins/tree/main/plugins/hex) | 未收录 | 暂不接入 | 许可证声明为 Proprietary |
| 74 | highlevel | HighLevel | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 75 | hostinger | Hostinger | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 76 | hubspot | HubSpot | Business & Operations | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 77 | keybid-puls | KeyBid Puls | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 78 | marcopolo | MarcoPolo | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 79 | mem | Mem | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 80 | monday-com | Monday.com | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 81 | moody-s | Moody's | Finance | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 82 | morningstar | Morningstar | Finance | App+Skills | MIT | — | [github.com](https://github.com/Morningstar/morningstar-plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 8 个脚本/可执行文件 |
| 83 | motherduck | MotherDuck | Data & Analytics | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 84 | mt-newswires | MT Newswires | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 85 | myregistry-com | MyRegistry.com | Other | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 86 | network-solutions | Network Solutions | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 87 | omni-analytics | Omni Analytics | Data & Analytics | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 88 | otter-ai | Otter.ai | Communication | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 89 | particl-market-research | Particl Market Research | Education & Research | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 90 | pipedrive | Pipedrive | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 91 | pitchbook | PitchBook | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 92 | policynote | PolicyNote | Education & Research | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 93 | pylon | Pylon | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 94 | quartr | Quartr | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 95 | quicknode | Quicknode | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 96 | ranked-ai | Ranked AI | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 97 | razorpay | Razorpay | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 98 | read-ai | Read AI | Communication | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 99 | readwise | Readwise | Education & Research | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 100 | responsive | Responsive | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 101 | scite | Scite | Education & Research | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 102 | semrush | Semrush | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 103 | sendgrid | SendGrid | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 104 | setu-bharat-connect-billpay | Setu Bharat Connect BillPay  | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 105 | signnow | SignNow | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 106 | skywatch | SkyWatch | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 107 | statsig | Statsig | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 108 | streak | Streak | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 109 | taxdown | Taxdown | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 110 | teamwork-com | Teamwork.com | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 111 | third-bridge | Third Bridge | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 112 | tinman-ai | Tinman AI | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 113 | united-rentals | United Rentals | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 114 | vantage | Vantage | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 115 | waldo | Waldo | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 116 | weatherpromise | WeatherPromise | Travel | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 117 | windsor-ai | Windsor.ai | Data & Analytics | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 118 | yepcode | YepCode | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 119 | render | Render | Developer Tools | Skills+Scripts | MIT | LICENSE | [github.com](https://github.com/renderinc/render-codex-plugin) | 未收录 | 需单独复核 | 含 2 个脚本/可执行文件 |
| 120 | temporal | Temporal | Developer Tools | Skills | MIT | LICENSE | [github.com](https://github.com/temporalio/codex-temporal-plugin) | 未收录 | 可进入候选 | 许可文件随包，且未发现脚本/可执行文件 |
| 121 | hyperframes | HyperFrames by HeyGen | Creativity | Skills | Apache-2.0 | — | [github.com](https://github.com/heygen-com/hyperframes) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 3 个脚本/可执行文件 |
| 122 | heygen | HeyGen | Creativity | App+Skills | MIT | — | [github.com](https://github.com/heygen-com/skills) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 123 | supabase | Supabase | Developer Tools | App+Skills | MIT | LICENSE | [github.com](https://github.com/supabase-community/supabase-plugin) | 未收录 | 可进入候选 | 许可文件随包，且未发现脚本/可执行文件 |
| 124 | codex-security | Codex Security | Security | App+MCP+Skills+Scripts | Proprietary | — | [github.com](https://github.com/openai/plugins) | 未收录 | 暂不接入 | 许可证声明为 Proprietary |
| 125 | twilio-developer-kit | Twilio Developer Kit | Developer Tools | Skills | MIT | — | [github.com](https://github.com/twilio/ai) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 126 | openai-developers | OpenAI Developers | Developer Tools | App+MCP+Skills+Scripts | Proprietary | — | [github.com](https://github.com/openai/plugins/tree/main/plugins/openai-developers) | 未收录 | 暂不接入 | 许可证声明为 Proprietary |
| 127 | asana | Asana | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 128 | datadog | Datadog (Preview) | Developer Tools | App | Apache-2.0 | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 129 | zoom | Zoom | Communication | App+Skills | MIT | LICENSE | [github.com](https://github.com/zoom/zoom-plugin-codex) | 未收录 | 可进入候选 | 许可文件随包，且未发现脚本/可执行文件 |
| 130 | similarweb | Similarweb | Data & Analytics | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 131 | lseg | LSEG | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 132 | s-p | S&P Global | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 133 | datasite | Datasite | Productivity | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 134 | factset | FactSet | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 135 | zoominfo | ZoomInfo | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 136 | docusign | Docusign | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 137 | mixpanel | Mixpanel | Data & Analytics | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 138 | mixpanel-headless | Mixpanel Headless | Data & Analytics | Skills | MIT | LICENSE | [github.com](https://github.com/mixpanel/mixpanel-headless) | 未收录 | 需单独复核 | 含 3 个脚本/可执行文件 |
| 139 | aiera | Aiera | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 140 | close | Close | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 141 | apollo | Apollo | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 142 | meticulate | Meticulate | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 143 | thoughtspot | ThoughtSpot | Data & Analytics | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 144 | midpage | Midpage | Education & Research | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 4 个脚本/可执行文件 |
| 145 | clay | Clay | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 146 | calendly | Calendly | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 147 | rox | Rox | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 148 | hg-insights | HG Insights | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 149 | airtable | Airtable | Productivity | App+Skills | MIT | — | [github.com](https://github.com/airtable/skills) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 150 | convex | Convex | Developer Tools | App | UNLICENSED | — | [github.com](https://github.com/get-convex/convex-codex-plugin) | 未收录 | 暂不接入 | 许可证声明为 UNLICENSED |
| 151 | outreach | Outreach | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 152 | shutterstock | Shutterstock | Creativity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 153 | replit | Replit | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 154 | lovable | Lovable | Developer Tools | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 155 | quickbooks | QuickBooks | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 156 | intercom | Intercom | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 157 | chronograph-lp | Chronograph LP | Finance | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 158 | nvidia | NVIDIA | Developer Tools | Skills | Apache-2.0 AND CC-BY-4.0 | — | [github.com](https://github.com/NVIDIA/skills) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 80 个脚本/可执行文件 |
| 159 | posthog | PostHog | Data & Analytics | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 160 | actively | Actively | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 161 | zoho | Zoho | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 162 | fiscal-ai | Fiscal AI | Finance | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 163 | picsart | Picsart | Creativity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 164 | alation | Alation | Data & Analytics | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 165 | fal | Fal | Creativity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 166 | hebbia | Hebbia | Business & Operations | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 167 | wix | Wix | Developer Tools | App+Skills | MIT | — | [github.com](https://github.com/wix/skills) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 12 个脚本/可执行文件 |
| 168 | base44 | Base44 | Developer Tools | App+Skills | MIT | — | [github.com](https://github.com/base44/skills) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 169 | ngs-analysis | Life Sciences NGS Analysis | Education & Research | Skills+Scripts | MIT | — | [github.com](https://github.com/openai/openai) | 未收录 | 需单独复核 | 包内缺少许可证证据；含 31 个脚本/可执行文件 |
| 170 | superhuman | Superhuman Mail | Communication | App+Skills | MIT | LICENSE | [github.com](https://github.com/superhuman/mcp-mail) | 未收录 | 需单独复核 | 含 1 个脚本/可执行文件 |
| 171 | shopify | Shopify | Developer Tools | App+Skills | MIT | LICENSE | [github.com](https://github.com/Shopify/Shopify-AI-Toolkit) | 未收录 | 需单独复核 | 含 27 个脚本/可执行文件 |
| 172 | magicpath | MagicPath | Developer Tools | Skills | UNLICENSED | — | [github.com](https://github.com/MagicPathAI/agent-skills) | 未收录 | 暂不接入 | 许可证声明为 UNLICENSED |
| 173 | brighthire | BrightHire | Productivity | App+Skills | MIT | — | [github.com](https://github.com/brighthire/brighthire-codex-plugin) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 174 | catalyst-by-zoho | Catalyst by Zoho | Developer Tools | App+Skills | MIT | — | [github.com](https://github.com/catalystbyzoho) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 175 | glean | Glean | Productivity | App | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 176 | chronograph-gp | Chronograph GP | Finance | App+Skills | MIT | — | [github.com](https://github.com/openai/plugins) | 未收录 | 需单独复核 | 包内缺少许可证证据 |
| 177 | openai-ads-conversions | OpenAI Ads Conversions | Developer Tools | Skills | Proprietary | — | [github.com](https://github.com/openai/plugins/tree/main/plugins/openai-ads-conversions) | 未收录 | 暂不接入 | 许可证声明为 Proprietary |
| 178 | boltz-api-cli | Boltz | Education & Research | Skills | MIT | LICENSE | [github.com](https://github.com/boltz-bio/boltz-api-skills) | 未收录 | 需单独复核 | 含 7 个脚本/可执行文件 |
| 179 | replayio | Replay.io | Developer Tools | App+Skills+Scripts | MIT | LICENSE | [github.com](https://github.com/replayio/plugins) | 未收录 | 需单独复核 | 含 2 个脚本/可执行文件 |
| 180 | digitalocean | DigitalOcean | Developer Tools | App+Skills | 缺失 | — | [github.com](https://github.com/digitalocean/CodexPlugin) | 未收录 | 暂不接入 | 许可证声明为 缺失 |
