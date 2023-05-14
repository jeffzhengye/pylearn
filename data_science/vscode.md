# shortcut

| short cut        | functions                               |
| :--------------- | :-------------------------------------- |
| ctrt + T         | search symbols like class               |
| ctrt + shift + O | find variable/functions in current file |
| ctrt + O         | open file in current directory          |
| ctrt + =         | zoom in                                 |
| ctrl + shift + P | search all                              |
| ctrl+P, ctrl+E   | search file by name                     |
| ctrt+LeftArrow   | collapse outline                        |
| ctrl + K + S     | keyboard shortcuts                      |
| ctrl + R         | open recent workspace                   |

- more: https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf


# vscode

## set PYTHONPATH

### 方法1

- launch.json 中设置

```
"configurations": [
        {
            "name": "main: debug, env-dev",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "${workspaceFolder}/rule_based_nlu",
            "env": {
                "CONTENT_API_ENV": "dev",
                "PYTHONPATH": "${workspaceFolder}:${env:PYTHONPATH}"
            },
            "envFile": "${workspaceFolder}/.env"
        }
]
```

### 方法2

- 通过envFile设置PYTHONPATH
- 在launch.json 里面configurations 中设置 envFile, 如上。但最好修改默认名称，免得被扫描

### 方法3

- "terminal.integrated.env.windows": {"PYTHONPATH": "${workspaceFold}:${env:PYTHONPATH}"}
- 在settings.json 中设置，但只能在vscode 系统集成的terminal中生效。