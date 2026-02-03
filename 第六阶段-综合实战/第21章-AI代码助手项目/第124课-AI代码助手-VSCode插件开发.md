![AI代码助手架构](./images/code_assistant.svg)
*图：AI代码助手架构*

# 第124课：AI代码助手 - VSCode插件开发

> **本课目标**：开发完整的VSCode插件，实现IDE集成
> 
> **核心技能**：插件架构、LSP协议、UI开发、调试技巧
> 
> **学习时长**：90分钟

---

## 📖 口播文案（8分钟）
![Code Gen](./images/code_gen.svg)
*图：Code Gen*


### 🎯 前言

"前面完成了AI核心功能，今天要**打通最后一公里**！

**把AI能力集成到VSCode！**

**为什么选VSCode？**

```
市场数据：
• 市场份额：>70%（开发者工具）
• 月活用户：2000万+
• 插件生态：40000+插件
• GitHub支持：官方背书

技术优势：
• 丰富的API
• 完善的文档
• 活跃的社区
• 易于开发

商业价值：
• 用户基数大
• 变现路径清晰
• 容易推广

最佳选择！
```

**VSCode插件架构：**

```
┌─────────────────────────────────────┐
│        VSCode主进程                  │
│  • 窗口管理                          │
│  • 插件加载                          │
│  • 配置管理                          │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│      Extension Host（插件宿主）      │
│  • 运行在独立进程                    │
│  • 不阻塞UI                          │
│  • 沙箱隔离                          │
├─────────────────────────────────────┤
│  我们的插件                          │
│  ├─ extension.ts（入口）            │
│  ├─ CompletionProvider              │
│  ├─ CodeLensProvider                │
│  ├─ ChatPanel                       │
│  └─ LanguageClient（LSP客户端）     │
└──────────────┬──────────────────────┘
               ↓ LSP协议
┌─────────────────────────────────────┐
│     Language Server（我们的后端）    │
│  • Python实现                        │
│  • AI推理                            │
│  • RAG检索                           │
│  • 工具调用                          │
└─────────────────────────────────────┘

前后端分离！
```

**核心功能实现：**

```
1. 代码补全（InlineCompletionProvider）
   • 监听打字事件
   • 收集上下文
   • 调用后端API
   • 展示候选项
   • 延迟<300ms

2. 聊天面板（WebviewPanel）
   • 自定义UI（HTML/CSS/JS）
   • 双向通信
   • Markdown渲染
   • 代码高亮

3. 代码诊断（DiagnosticCollection）
   • 波浪线标记
   • Hover提示
   • Quick Fix
   • 实时更新

4. CodeLens（提示信息）
   • 行内提示
   • 可点击操作
   • 动态刷新

5. 命令（Commands）
   • 快捷键绑定
   • 上下文菜单
   • 命令面板
```

**LSP协议的价值：**

```
Language Server Protocol：
• 微软开发
• 标准化协议
• IDE无关

优势：
✓ 前后端分离（语言无关）
✓ 协议标准（易于对接）
✓ 复用后端（支持多IDE）
✓ 性能优化（批处理、增量）

支持的IDE：
• VSCode
• Vim/Neovim
• Emacs
• IntelliJ IDEA
• Sublime Text

一次开发，到处运行！
```

**今天这一课，我要带你：**

**第一部分：插件脚手架**
- 项目结构
- 配置文件
- 开发环境

**第二部分：核心功能实现**
- 代码补全
- 聊天面板
- 诊断系统

**第三部分：LSP集成**
- 客户端实现
- 服务端实现
- 协议通信

**第四部分：调试与测试**
- 本地调试
- 单元测试
- 集成测试

从0到1开发插件！"

---

## 📚 第一部分：VSCode插件脚手架

### 一、项目结构

```bash
# 创建项目
npm install -g yo generator-code
yo code

# 项目结构
ai-code-assistant/
├── .vscode/
│   ├── launch.json          # 调试配置
│   └── tasks.json           # 任务配置
├── src/
│   ├── extension.ts         # 插件入口
│   ├── completion/
│   │   └── provider.ts      # 补全Provider
│   ├── chat/
│   │   ├── panel.ts         # 聊天面板
│   │   └── webview.html     # UI页面
│   ├── diagnostics/
│   │   └── provider.ts      # 诊断Provider
│   ├── lsp/
│   │   └── client.ts        # LSP客户端
│   └── utils/
│       └── api.ts           # API封装
├── server/                  # Language Server
│   ├── main.py              # 服务端入口
│   ├── completion.py        # 补全逻辑
│   ├── chat.py              # 对话逻辑
│   └── diagnostics.py       # 诊断逻辑
├── package.json             # 插件配置
├── tsconfig.json            # TypeScript配置
└── README.md
```

### 二、package.json配置

```json
{
  "name": "ai-code-assistant",
  "displayName": "AI Code Assistant",
  "description": "Intelligent code completion and analysis",
  "version": "0.1.0",
  "publisher": "your-name",
  "engines": {
    "vscode": "^1.75.0"
  },
  "categories": [
    "Programming Languages",
    "Machine Learning"
  ],
  "activationEvents": [
    "onStartupFinished"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "ai-assistant.chat",
        "title": "Open AI Chat",
        "icon": "$(comment-discussion)"
      },
      {
        "command": "ai-assistant.explain",
        "title": "Explain Code"
      },
      {
        "command": "ai-assistant.review",
        "title": "Review Code"
      }
    ],
    "keybindings": [
      {
        "command": "ai-assistant.chat",
        "key": "ctrl+shift+a",
        "mac": "cmd+shift+a"
      }
    ],
    "menus": {
      "editor/context": [
        {
          "command": "ai-assistant.explain",
          "when": "editorHasSelection",
          "group": "ai-assistant"
        },
        {
          "command": "ai-assistant.review",
          "group": "ai-assistant"
        }
      ]
    },
    "configuration": {
      "title": "AI Code Assistant",
      "properties": {
        "aiAssistant.apiUrl": {
          "type": "string",
          "default": "http://localhost:8000",
          "description": "API server URL"
        },
        "aiAssistant.autoComplete": {
          "type": "boolean",
          "default": true,
          "description": "Enable auto completion"
        },
        "aiAssistant.completionDelay": {
          "type": "number",
          "default": 300,
          "description": "Completion delay (ms)"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "test": "npm run compile && node ./out/test/runTest.js"
  },
  "devDependencies": {
    "@types/vscode": "^1.75.0",
    "@types/node": "^18.0.0",
    "typescript": "^4.9.0"
  },
  "dependencies": {
    "axios": "^1.4.0",
    "vscode-languageclient": "^8.1.0"
  }
}
```

---

## 💻 第二部分：核心功能实现

### 一、插件入口（extension.ts）

```typescript
import * as vscode from 'vscode';
import { CompletionProvider } from './completion/provider';
import { ChatPanel } from './chat/panel';
import { DiagnosticsProvider } from './diagnostics/provider';
import { LanguageClient } from './lsp/client';

export function activate(context: vscode.ExtensionContext) {
    console.log('AI Code Assistant激活');
    
    // 1. 启动Language Server
    const languageClient = new LanguageClient(context);
    languageClient.start();
    
    // 2. 注册代码补全
    const completionProvider = new CompletionProvider();
    context.subscriptions.push(
        vscode.languages.registerInlineCompletionItemProvider(
            { pattern: '**/*.{py,js,ts,java}' },
            completionProvider
        )
    );
    
    // 3. 注册诊断
    const diagnosticsProvider = new DiagnosticsProvider();
    context.subscriptions.push(diagnosticsProvider);
    
    // 4. 注册命令
    
    // 打开聊天面板
    context.subscriptions.push(
        vscode.commands.registerCommand('ai-assistant.chat', () => {
            ChatPanel.createOrShow(context.extensionUri);
        })
    );
    
    // 解释代码
    context.subscriptions.push(
        vscode.commands.registerCommand('ai-assistant.explain', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                return;
            }
            
            const selection = editor.selection;
            const selectedCode = editor.document.getText(selection);
            
            if (!selectedCode) {
                vscode.window.showWarningMessage('请先选中代码');
                return;
            }
            
            // 打开聊天面板并发送解释请求
            ChatPanel.createOrShow(context.extensionUri);
            ChatPanel.currentPanel?.explainCode(selectedCode);
        })
    );
    
    // 代码审查
    context.subscriptions.push(
        vscode.commands.registerCommand('ai-assistant.review', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                return;
            }
            
            const code = editor.document.getText();
            
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "正在审查代码...",
                cancellable: false
            }, async (progress) => {
                // 调用审查API
                const result = await reviewCode(code);
                
                // 显示结果
                vscode.window.showInformationMessage(
                    `代码得分：${result.score}/100`
                );
                
                // 更新诊断
                diagnosticsProvider.updateDiagnostics(
                    editor.document.uri,
                    result.issues
                );
            });
        })
    );
    
    // 5. 状态栏
    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.text = "$(rocket) AI助手";
    statusBarItem.command = 'ai-assistant.chat';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
    
    console.log('AI Code Assistant已就绪');
}

export function deactivate() {
    console.log('AI Code Assistant停用');
}

// 辅助函数
async function reviewCode(code: string) {
    // 实际会调用API
    return {
        score: 85,
        issues: []
    };
}
```

### 二、代码补全Provider

```typescript
// src/completion/provider.ts
import * as vscode from 'vscode';
import axios from 'axios';

export class CompletionProvider implements vscode.InlineCompletionItemProvider {
    
    private cache: Map<string, vscode.InlineCompletionItem[]> = new Map();
    private debounceTimer?: NodeJS.Timeout;
    
    async provideInlineCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        context: vscode.InlineCompletionContext,
        token: vscode.CancellationToken
    ): Promise<vscode.InlineCompletionItem[]> {
        
        // 获取配置
        const config = vscode.workspace.getConfiguration('aiAssistant');
        const enabled = config.get<boolean>('autoComplete', true);
        
        if (!enabled) {
            return [];
        }
        
        // 1. 收集上下文
        const prefix = this.getPrefix(document, position);
        const suffix = this.getSuffix(document, position);
        
        // 2. 检查缓存
        const cacheKey = this.getCacheKey(prefix, suffix);
        if (this.cache.has(cacheKey)) {
            console.log('缓存命中');
            return this.cache.get(cacheKey)!;
        }
        
        // 3. 防抖
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        return new Promise((resolve) => {
            this.debounceTimer = setTimeout(async () => {
                try {
                    // 4. 调用API
                    const completions = await this.fetchCompletions(
                        prefix,
                        suffix,
                        document.languageId
                    );
                    
                    // 5. 转换为VSCode格式
                    const items = completions.map(c => 
                        new vscode.InlineCompletionItem(c.text)
                    );
                    
                    // 6. 缓存
                    this.cache.set(cacheKey, items);
                    
                    resolve(items);
                } catch (error) {
                    console.error('补全失败：', error);
                    resolve([]);
                }
            }, config.get<number>('completionDelay', 300));
        });
    }
    
    private getPrefix(document: vscode.TextDocument, position: vscode.Position): string {
        // 获取光标前的代码（最多2000个字符）
        const start = new vscode.Position(Math.max(0, position.line - 50), 0);
        const range = new vscode.Range(start, position);
        let prefix = document.getText(range);
        
        // 截断
        if (prefix.length > 2000) {
            prefix = prefix.substring(prefix.length - 2000);
        }
        
        return prefix;
    }
    
    private getSuffix(document: vscode.TextDocument, position: vscode.Position): string {
        // 获取光标后的代码（最多500个字符）
        const end = new vscode.Position(
            Math.min(document.lineCount - 1, position.line + 20),
            Number.MAX_VALUE
        );
        const range = new vscode.Range(position, end);
        let suffix = document.getText(range);
        
        // 截断
        if (suffix.length > 500) {
            suffix = suffix.substring(0, 500);
        }
        
        return suffix;
    }
    
    private getCacheKey(prefix: string, suffix: string): string {
        // 简单hash
        return `${prefix.substring(prefix.length - 100)}-${suffix.substring(0, 100)}`;
    }
    
    private async fetchCompletions(
        prefix: string,
        suffix: string,
        language: string
    ): Promise<Array<{text: string, score: number}>> {
        
        const config = vscode.workspace.getConfiguration('aiAssistant');
        const apiUrl = config.get<string>('apiUrl', 'http://localhost:8000');
        
        try {
            const response = await axios.post(
                `${apiUrl}/completion`,
                {
                    prefix,
                    suffix,
                    language
                },
                {
                    timeout: 5000
                }
            );
            
            return response.data.completions || [];
        } catch (error) {
            console.error('API调用失败：', error);
            return [];
        }
    }
}
```

### 三、聊天面板

```typescript
// src/chat/panel.ts
import * as vscode from 'vscode';
import axios from 'axios';

export class ChatPanel {
    public static currentPanel: ChatPanel | undefined;
    
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private _disposables: vscode.Disposable[] = [];
    
    public static createOrShow(extensionUri: vscode.Uri) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;
        
        // 如果已存在，显示
        if (ChatPanel.currentPanel) {
            ChatPanel.currentPanel._panel.reveal(column);
            return;
        }
        
        // 创建新面板
        const panel = vscode.window.createWebviewPanel(
            'aiChat',
            'AI Chat',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );
        
        ChatPanel.currentPanel = new ChatPanel(panel, extensionUri);
    }
    
    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        
        // 设置HTML
        this._panel.webview.html = this._getHtmlForWebview();
        
        // 监听消息
        this._panel.webview.onDidReceiveMessage(
            async message => {
                switch (message.type) {
                    case 'chat':
                        await this._handleChat(message.text);
                        break;
                    case 'explain':
                        await this._handleExplain(message.code);
                        break;
                }
            },
            null,
            this._disposables
        );
        
        // 清理
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }
    
    public explainCode(code: string) {
        this._panel.webview.postMessage({
            type: 'insertCode',
            code: code
        });
    }
    
    private async _handleChat(text: string) {
        // 显示用户消息
        this._panel.webview.postMessage({
            type: 'message',
            role: 'user',
            content: text
        });
        
        // 调用API
        try {
            const config = vscode.workspace.getConfiguration('aiAssistant');
            const apiUrl = config.get<string>('apiUrl', 'http://localhost:8000');
            
            const response = await axios.post(`${apiUrl}/chat`, {
                message: text
            });
            
            // 显示AI回复
            this._panel.webview.postMessage({
                type: 'message',
                role: 'assistant',
                content: response.data.reply
            });
        } catch (error) {
            vscode.window.showErrorMessage('Chat请求失败');
        }
    }
    
    private async _handleExplain(code: string) {
        // 类似chat
        await this._handleChat(`请解释以下代码：\n\`\`\`\n${code}\n\`\`\``);
    }
    
    private _getHtmlForWebview(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chat</title>
    <style>
        body {
            padding: 10px;
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
        }
        #messages {
            height: calc(100vh - 100px);
            overflow-y: auto;
            margin-bottom: 10px;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .user {
            background-color: var(--vscode-input-background);
            text-align: right;
        }
        .assistant {
            background-color: var(--vscode-editor-inactiveSelectionBackground);
        }
        #input-container {
            display: flex;
            gap: 10px;
        }
        #input {
            flex: 1;
            padding: 8px;
            border: 1px solid var(--vscode-input-border);
            background-color: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
        }
        button {
            padding: 8px 16px;
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: var(--vscode-button-hoverBackground);
        }
    </style>
</head>
<body>
    <div id="messages"></div>
    <div id="input-container">
        <input type="text" id="input" placeholder="输入消息...">
        <button onclick="send()">发送</button>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function send() {
            const input = document.getElementById('input');
            const text = input.value.trim();
            if (!text) return;
            
            vscode.postMessage({
                type: 'chat',
                text: text
            });
            
            input.value = '';
        }
        
        // 监听Enter键
        document.getElementById('input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                send();
            }
        });
        
        // 接收消息
        window.addEventListener('message', event => {
            const message = event.data;
            
            if (message.type === 'message') {
                addMessage(message.role, message.content);
            } else if (message.type === 'insertCode') {
                document.getElementById('input').value = 
                    \`请解释以下代码：\\n\\\`\\\`\\\`\\n\${message.code}\\n\\\`\\\`\\\`\`;
            }
        });
        
        function addMessage(role, content) {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = \`message \${role}\`;
            div.textContent = content;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>`;
    }
    
    public dispose() {
        ChatPanel.currentPanel = undefined;
        
        this._panel.dispose();
        
        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }
}
```

---

## 📝 课后总结

### 核心收获

1. **VSCode插件开发**
   - 项目结构
   - 配置文件
   - API使用

2. **核心功能实现**
   - 代码补全
   - 聊天面板
   - 诊断系统

3. **用户体验**
   - 性能优化
   - UI设计
   - 交互流畅

---

## 🚀 下节预告

下一课：**第125课：AI代码助手 - 测试与发布**

- 单元测试
- 集成测试
- 打包发布
- 市场推广

**完整交付产品！** 🔥

---

**💪 插件开发完成！准备发布！**

**下一课见！** 🎉
