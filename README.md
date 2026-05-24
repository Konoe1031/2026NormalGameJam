# krebx

2026 Game Jam 作品，使用 Python + [pygame](https://www.pygame.org/) 製作的遊戲。

## 系統需求

- **Python 3.10 以上**（建議 **3.11**）。

確認 Python 版本：

```bash
python --version
```

## 安裝步驟

### 1. 建立虛擬環境

> 環境只需建立一次。`.venv/` 已被 `.gitignore` 忽略，不會進版控。

**Windows（PowerShell）**

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

啟用成功後，命令列開頭會出現 `(.venv)`。

### 2. 安裝依賴套件

```bash
pip install -r requirements.txt
```

> 備註：`requirements.txt` 是 UTF-16 編碼，但 pip 能正常讀取，不需另外處理。

## 執行遊戲

確認虛擬環境已啟用（命令列開頭有 `(.venv)`），然後執行：

```bash
python main.py
```

遊戲視窗大小為 960×720，會從主畫面（home）開始。

之後每次要玩，只要重新啟用虛擬環境再執行 `main.py` 即可：

- Windows：`.venv\Scripts\Activate.ps1` → `python main.py`
- macOS / Linux：`source .venv/bin/activate` → `python main.py`

## 操作方式

| 動作 | 按鍵 |
|------|------|
| 移動 | 方向鍵 或 `W` `A` `S` `D` |
| 互動 / 拾取 | `E` |
| 背包 | `Tab`（按住開啟，放開關閉） |
| 防護 / 阻止 | `Left Shift` |
| 設定選單 | `Esc` |
| 跳過教學、推進劇情 | `Space` 或 `Enter` |

> 背包、防護、設定的按鍵可在遊戲內的設定選單中重新綁定。

## 常見問題

- **匯入時報錯 / 出現語法錯誤**：很可能是用到太舊的 Python。請確認 `python --version` 為 3.10 以上，並用該版本重建 `.venv`。
- **`pygame` 找不到**：確認虛擬環境已啟用（開頭要有 `(.venv)`），再重新 `pip install -r requirements.txt`。
- **中文字顯示空白**：專案已內建字型 `src/fonts/`，正常情況下各作業系統都能顯示中文；若仍異常，請確認字型檔有隨專案一起取得。
