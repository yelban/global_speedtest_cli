# 全球網路速度測試工具

這是一套基於 Python 的網路連接性和速度測試工具集合，可測試全球伺服器和資料中心的網路性能。

## 🚀 主要特色

- **無外部依賴**：僅使用 Python 標準函式庫
- **全球覆蓋**：測試全球網站和資料中心的連接
- **多種測試模式**：命令列和互動式介面
- **全面指標**：DNS 解析、TCP 連接、HTTP 回應時間
- **即時進度**：即時下載進度和速度監控
- **彈性配置**：可自訂測試參數和伺服器選擇
- **結果匯出**：支援將測試結果儲存為 JSON 格式

## 📦 內含工具

### 1. simple_netcheck.py
輕量級網路連接測試工具，測量到全球網站和 Vultr 資料中心的連接性能。

**主要功能：**
- 測試 DNS 解析、TCP 連接和 HTTP 回應時間
- 包含 11 個主要全球網站和 32 個 Vultr 資料中心
- 智慧評分系統（根據延遲給出 0-100 分）
- 地區篩選和統計
- 無需外部依賴

### 2. vultr_speedtest.py
針對 Vultr 全球資料中心和台灣 HiNet 伺服器的綜合速度測試工具。

**主要功能：**
- 即時進度顯示的下載速度測試
- 支援 100MB 和 1GB 測試檔案
- Ping 延遲測量
- 快速測試和完整下載模式
- 台灣 HiNet 測速整合

### 3. interactive_vultr_test.py
Vultr 速度測試工具的互動式選單介面。

**主要功能：**
- 友善的文字選單系統
- 多種測試模式（快速、地區、特定伺服器）
- 可配置的測試設定
- 自動結果儲存和統計
- 進度視覺化

## 🌍 支援的測試位置

### 全球知名網站
- 台灣、日本、南韓、新加坡、香港、馬來西亞
- 澳大利亞、英國、德國、美國

### Vultr 資料中心（32 個位置）
- **亞洲**：東京、大阪、首爾、新加坡、孟買、德里、班加羅爾、特拉維夫
- **歐洲**：倫敦、曼徹斯特、法蘭克福、巴黎、阿姆斯特丹、華沙、斯德哥爾摩、馬德里
- **北美**：亞特蘭大、芝加哥、達拉斯、火奴魯魯、洛杉磯、邁阿密、紐約、西雅圖、硅谷、多倫多、墨西哥城
- **南美**：聖保羅、聖地牙哥
- **非洲**：約翰內斯堡
- **大洋洲**：墨爾本、雪梨

### 台灣 HiNet
- 來自 HiNet 官方測速伺服器的 250MB 和 2GB 測試檔案

## 🛠️ 安裝

無需安裝！這些工具僅使用 Python 標準函式庫。

### 系統需求
- Python 3.6 或更高版本
- 網路連接
- 可用的 `ping` 命令（用於延遲測試）

### 快速開始
```bash
git clone <repository-url>
cd global-netcheck
```

## 📖 使用方法

### 簡單網路檢查
```bash
# 測試所有站點（預設）
python3 simple_netcheck.py

# 只測試全球知名網站
python3 simple_netcheck.py --sites global

# 只測試 Vultr 資料中心
python3 simple_netcheck.py --sites vultr

# 按地區篩選
python3 simple_netcheck.py --region Asia

# 儲存結果為 JSON
python3 simple_netcheck.py --output results.json

# 列出所有可用測試站點
python3 simple_netcheck.py --list
```

### Vultr 速度測試（命令列）
```bash
# 測試預設伺服器組合
python3 vultr_speedtest.py --default

# 測試特定伺服器
python3 vultr_speedtest.py --server tokyo

# 測試多個伺服器
python3 vultr_speedtest.py --servers tokyo singapore new_york

# 測試所有伺服器
python3 vultr_speedtest.py --all

# 使用 1GB 測試檔案和快速模式
python3 vultr_speedtest.py --server tokyo --size 1GB --quick

# 列出所有可用伺服器
python3 vultr_speedtest.py --list
```

### 互動式 Vultr 測試
```bash
# 啟動互動式介面
python3 interactive_vultr_test.py
```

然後按照選單提示：
1. 選擇測試模式（快速測試、地區測試等）
2. 配置測試設定（檔案大小、下載模式）
3. 執行測試並查看結果
4. 選擇性儲存結果為 JSON

## 📊 理解結果

### 簡單網路檢查輸出
```
🌐 簡單網路連接測試
📍 測試全球主要網站的連接性能
============================================================
[ 1/11] 測試 台北, 台灣           ✅   45.2ms (評分: 100)
[ 2/11] 測試 東京, 日本           ✅   67.8ms (評分:  90)

============================================================
🏆 測試結果排行 (按總延遲排序):
排名  地點                總延遲      DNS      TCP      HTTP     評分
----------------------------------------------------------------------
1     台北, 台灣           45.2ms    12.3ms   15.6ms   17.3ms   100
2     東京, 日本           67.8ms    18.7ms   23.1ms   26.0ms    90

🥇 最佳連接: 台北, 台灣 (45.2ms)

📊 地區統計:
  Asia           : 平均延遲   89.4ms (8 個站點)
  Europe         : 平均延遲  156.7ms (2 個站點)
```

### Vultr 速度測試輸出
```
測試 日本-東京 (hnd-jp-ping.vultr.com)...
    正在測試延遲...
    正在測試下載速度...
    檔案大小: 100.0 MB
    [████████████████████] 100.0% | 100.0MB | 89.5 Mbps
日本-東京: ↓ 89.5 Mbps | ping 35.2 ms

📊 測試摘要:
成功測試: 5/6 個伺服器
平均下載速度: 78.3 Mbps
最快伺服器: 日本-東京 (89.5 Mbps)
```

## 🎯 評分系統 (simple_netcheck.py)

- **100 分**：< 50ms（優秀）
- **90 分**：50-100ms（很好）
- **80 分**：100-200ms（良好）
- **60 分**：200-500ms（普通）
- **40 分**：500-1000ms（較差）
- **20 分**：1000-2000ms（很差）
- **10 分**：> 2000ms（不可接受）

## 🔧 配置選項

### 命令列參數

#### simple_netcheck.py
| 選項 | 說明 | 預設值 |
|------|------|--------|
| `--region` | 按地區篩選 | 所有地區 |
| `--timeout` | 連接超時時間（秒） | 10.0 |
| `--output` | 儲存結果為 JSON 檔案 | 無 |
| `--sites` | 站點類型：global/vultr/all | all |
| `--list` | 列出所有測試站點 | False |

#### vultr_speedtest.py
| 選項 | 說明 | 預設值 |
|------|------|--------|
| `--server` | 測試特定伺服器 | 無 |
| `--servers` | 測試多個伺服器 | 無 |
| `--default` | 測試預設伺服器組合 | False |
| `--all` | 測試所有伺服器 | False |
| `--size` | 測試檔案大小：100MB/1GB | 100MB |
| `--cooldown` | 測試間隔（秒） | 2.0 |
| `--timeout` | 測試超時時間（秒） | 30 |
| `--quick` | 快速測試模式 | False |
| `--no-progress` | 隱藏進度條 | False |

## 📁 輸出檔案

### JSON 匯出格式
```json
{
  "server_key": "tokyo",
  "server_name": "日本-東京",
  "server_host": "hnd-jp-ping.vultr.com",
  "ping_ms": 35.2,
  "download_mbps": 89.5,
  "downloaded_bytes": 104857600,
  "test_duration": 9.3,
  "timestamp": "2024-03-15T10:30:45.123456+00:00"
}
```

## 🚨 重要注意事項

1. **網路影響**：速度測試會消耗頻寬，特別是 1GB 檔案
2. **防火牆限制**：某些網路可能會阻擋到特定伺服器的連接
3. **測試頻率**：避免過度測試以防止速率限制
4. **結果解釋**：結果反映當前網路狀況，可能會有變化
5. **鍵盤中斷**：所有工具都支援 Ctrl+C 安全取消

## 🎯 使用場景

- **網路診斷**：快速評估網路連接品質
- **伺服器選擇**：比較不同資料中心位置的性能
- **網路監控**：定期網路性能檢查
- **教育學習**：理解網路連接的各個階段
- **VPS 主機**：為應用程式選擇最佳伺服器位置

## 🤝 貢獻

歡迎提交問題報告、功能請求或拉取請求來改善這些工具。

## 📄 授權

此專案為開源專案。請查看授權檔案以獲取詳細資訊。

## 📚 相關文件

- [simple_netcheck.py 說明文件](simple_netcheck.md)
- [interactive_vultr_test.py 說明文件](interactive_vultr_test.md)
- [English README](README.md)
- [Japanese README](README.ja.md)