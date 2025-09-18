# simple_netcheck.py 說明文件

## 概述

`simple_netcheck.py` 是一個超簡單的網路測試工具，不需要依賴 speedtest，使用 Python 標準庫測試到全球各大網站和 Vultr 機房的連接性能。

## 功能特色

- **純 Python 標準庫實現**：無需安裝額外依賴套件
- **全球測試站點**：包含知名網站和 Vultr 全球機房
- **多層測試指標**：DNS 解析、TCP 連接、HTTP 請求分別測量
- **智能評分系統**：根據延遲自動計算 0-100 分的連接評分
- **靈活的篩選選項**：可按地區或站點類型過濾
- **詳細結果報告**：提供排行榜和地區統計
- **JSON 結果匯出**：支援將測試結果保存為 JSON 格式

## 測試站點

### 全球知名網站 (global)
- 台灣：www.gov.tw
- 日本：www.yahoo.co.jp
- 韓國：www.naver.com
- 新加坡：www.straitstimes.com
- 香港：www.scmp.com
- 馬來西亞：www.thestar.com.my
- 澳大利亞：www.abc.net.au
- 英國：www.bbc.com
- 德國：www.spiegel.de
- 美國：www.nytimes.com, www.latimes.com

### Vultr 全球機房 (vultr)
覆蓋亞洲、歐洲、北美、南美、非洲、大洋洲共 32 個機房位置。

## 使用方法

### 基本用法

```bash
# 測試所有站點（預設）
python3 simple_netcheck.py

# 只測試知名網站
python3 simple_netcheck.py --sites global

# 只測試 Vultr 機房
python3 simple_netcheck.py --sites vultr
```

### 進階選項

```bash
# 按地區篩選
python3 simple_netcheck.py --region Asia
python3 simple_netcheck.py --region Europe

# 調整超時時間
python3 simple_netcheck.py --timeout 15.0

# 保存結果為 JSON
python3 simple_netcheck.py --output results.json

# 列出所有可用測試站點
python3 simple_netcheck.py --list
```

### 命令列參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--region` | 只測試特定地區 | 無（測試所有地區） |
| `--timeout` | 連接超時時間（秒） | 10.0 |
| `--output` | 保存結果為 JSON 檔案 | 無 |
| `--list` | 列出所有測試站點 | 否 |
| `--sites` | 選擇站點類型：global/vultr/all | all |

## 測試指標說明

### 測量項目
1. **DNS 解析時間**：域名解析為 IP 位址的時間
2. **TCP 連接時間**：建立 TCP 連接的時間
3. **HTTP 請求時間**：完成 HTTP 請求的時間
4. **總延遲**：以上三項的總和

### 評分系統
- 100 分：< 50ms
- 90 分：50-100ms
- 80 分：100-200ms
- 60 分：200-500ms
- 40 分：500-1000ms
- 20 分：1000-2000ms
- 10 分：> 2000ms

## 輸出範例

```
🌐 簡單網路連接測試
📍 測試全球主要網站的連接性能
============================================================
[ 1/11] 測試 台北, 台灣           ✅   45.2ms (評分: 100)
[ 2/11] 測試 東京, 日本           ✅   67.8ms (評分:  90)
[ 3/11] 測試 首爾, 南韓           ✅  123.4ms (評分:  80)

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
  North America  : 平均延遲  201.3ms (2 個站點)
```

## 適用場景

- **網路診斷**：快速檢測網路連接品質
- **機房選擇**：比較不同地區機房的連接性能
- **網路監控**：定期檢查網路狀況
- **教育學習**：理解網路連接的各個階段
- **無依賴環境**：在無法安裝額外套件的環境中使用

## 技術實作

### 核心函數

- `test_connection_speed(host, timeout)`: 測試單一主機的連接性能
- `calculate_score(result)`: 根據延遲計算評分
- `main()`: 主程式邏輯，處理命令列參數和結果顯示

### 錯誤處理

- 支援 Ctrl+C 中斷測試
- DNS 解析失敗時給出明確錯誤訊息
- TCP 連接失敗時仍顯示 DNS 解析結果
- HTTP 請求失敗時仍保留 DNS 和 TCP 結果

## 注意事項

1. **網路環境影響**：測試結果會受到當前網路狀況影響
2. **防火牆限制**：某些網路環境可能阻擋對特定站點的連接
3. **測試間隔**：避免過於頻繁測試，以免被目標伺服器限制
4. **結果參考性**：測試結果僅供參考，實際使用體驗可能有所不同