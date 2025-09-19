# 全球網路速度測試工具

基於 Vultr、Linode 全球機房和台灣 HiNet 測試檔案的網路速度測試工具，支援 45+ 個地區機房測試。

## 功能特色

- 🎯 **準確測試**: 預設完整下載測試檔案，確保測試結果準確性
- ⚡ **快速模式**: 可選部分下載模式，適合快速檢測
- 🌍 **多元覆蓋**: 涵蓋台灣 HiNet + 全球 Vultr 32 個機房 + Linode 11 個機房
- 🔧 **靈活選擇**: 支援單一機房、地區、自訂組合或完整測試
- 📈 **實時進度**: 顯示下載進度條、即時速度和已下載數據量
- 📊 **詳細報告**: 提供下載速度、延遲和測試詳情
- 💾 **結果儲存**: 支援 JSON 格式結果輸出
- 🆕 **多語言支援**: 支援英文、繁體中文、日文介面
- 🆕 **提供商選擇**: 使用 --zone 參數指定測試 Vultr 或 Linode 機房

## 使用方式

### 1. 命令列工具 (vultr_speedtest.py)

#### 基本用法

```bash
# 查看所有可用機房
python vultr_speedtest.py --list

# 測試單一機房
python vultr_speedtest.py --server tokyo

# 測試預設機房組合 (台灣HiNet、東京、新加坡、紐約、巴黎、悉尼)
python vultr_speedtest.py --default

# 測試多個指定機房
python vultr_speedtest.py --servers tokyo singapore paris

# 測試所有機房
python vultr_speedtest.py --all
```

#### 進階選項

```bash
# 指定測試檔案大小
python vultr_speedtest.py --server tokyo --size 1GB

# 調整測試間隔
python vultr_speedtest.py --default --cooldown 5.0

# 設定超時時間
python vultr_speedtest.py --server tokyo --timeout 60

# 快速測試模式 (部分下載)
python vultr_speedtest.py --server tokyo --quick

# 不顯示進度條 (適合腳本使用)
python vultr_speedtest.py --server tokyo --no-progress

# 儲存結果
python vultr_speedtest.py --default --output results.json

# 🆕 指定提供商區域 (解決機房代碼衝突)
python vultr_speedtest.py --server singapore --zone linode
python vultr_speedtest.py --server singapore --zone vultr

# 🆕 多語言介面
python vultr_speedtest.py --server tokyo --lang zh  # 繁體中文
python vultr_speedtest.py --server tokyo --lang ja  # 日文
python vultr_speedtest.py --server tokyo --lang en  # 英文
```

### 2. 互動式介面 (interactive_vultr_test.py)

```bash
# 啟動互動式介面
python interactive_vultr_test.py

# 🆕 指定語言和提供商偏好
python interactive_vultr_test.py --lang zh --zone linode
```

提供選單式操作介面：
- 快速測試推薦機房
- 按地區選擇測試
- 選擇特定機房
- 完整測試所有機房
- 自訂測試組合

每個測試選項都會提供：
- 檔案大小選擇 (100MB / 1GB)
- 下載模式選擇 (完整下載 / 快速測試)
- 測試間隔設定

## 可用機房列表

### 台灣 HiNet (2 個機房)
- `hinet_250m` - 台灣-HiNet (250MB)
- `hinet_2g` - 台灣-HiNet (2GB)

### 🆕 Linode 全球機房 (11 個機房)
#### 亞洲 (4 個機房)
- `tokyo2` - 日本-東京 2
- `tokyo3` - 日本-東京 3
- `singapore` - 新加坡 (⚠️ 與 Vultr 同名，需使用 --zone linode)
- `mumbai` - 印度-孟買

#### 北美 (5 個機房)
- `fremont` - 美國-弗里蒙特
- `newark` - 美國-紐瓦克
- `atlanta` - 美國-亞特蘭大 (⚠️ 與 Vultr 同名，需使用 --zone linode)
- `dallas` - 美國-達拉斯 (⚠️ 與 Vultr 同名，需使用 --zone linode)
- `toronto` - 加拿大-多倫多 (⚠️ 與 Vultr 同名，需使用 --zone linode)

#### 歐洲 (2 個機房)
- `london` - 英國-倫敦 (⚠️ 與 Vultr 同名，需使用 --zone linode)
- `frankfurt` - 德國-法蘭克福 (⚠️ 與 Vultr 同名，需使用 --zone linode)

### Vultr 全球機房 (32 個機房)
#### 亞洲 (8 個機房)
- `tokyo` - 日本-東京
- `osaka` - 日本-大阪
- `seoul` - 韓國-首爾
- `singapore` - 新加坡
- `bangalore` - 印度-班加羅爾
- `delhi` - 印度-德里NCR
- `mumbai` - 印度-孟買
- `tel_aviv` - 以色列-特拉維夫

### 歐洲 (8 個機房)
- `london` - 英國-倫敦
- `manchester` - 英國-曼徹斯特
- `frankfurt` - 德國-法蘭克福
- `paris` - 法國-巴黎
- `amsterdam` - 荷蘭-阿姆斯特丹
- `warsaw` - 波蘭-華沙
- `stockholm` - 瑞典-斯德哥爾摩
- `madrid` - 西班牙-馬德里

### 北美 (11 個機房)
- `atlanta` - 美國-亞特蘭大
- `chicago` - 美國-芝加哥
- `dallas` - 美國-達拉斯
- `honolulu` - 美國-火奴魯魯
- `los_angeles` - 美國-洛杉磯
- `miami` - 美國-邁阿密
- `new_york` - 美國-紐約
- `seattle` - 美國-西雅圖
- `silicon_valley` - 美國-硅谷
- `toronto` - 加拿大-多倫多
- `mexico_city` - 墨西哥-墨西哥城

### 南美 (2 個機房)
- `sao_paulo` - 巴西-聖保羅
- `santiago` - 智利-聖地牙哥

### 非洲 (1 個機房)
- `johannesburg` - 南非-約翰內斯堡

### 大洋洲 (2 個機房)
- `melbourne` - 澳大利亞-墨爾本
- `sydney` - 澳大利亞-悉尼

## 測試原理

1. **延遲測試**: 使用 ping 命令測試到目標機房的網路延遲
2. **速度測試**:
   - 下載測試檔案：
     - **HiNet**: 台灣中華電信提供的 250MB 或 2GB 檔案
     - **Vultr**: 全球機房提供的 100MB 或 1GB 檔案
   - **完整下載模式** (預設): 下載整個測試檔案，確保最高準確性
   - **快速測試模式**: 部分下載 (至少 5 秒或 1MB)，適合快速檢測
   - 自動控制測試時間避免超時

## 輸出範例

```
開始測試 3 個伺服器...
==================================================
[INFO] 測試 台灣-HiNet (250MB) (http.speed.hinet.net)...
    正在測試延遲...
    正在測試下載速度...
    檔案大小: 250.0 MB
    [███████████████████░] 95.6% | 239.0MB | 269.0 Mbps
台灣-HiNet (250MB): ↓ 268.9 Mbps | ping 0.5 ms

[INFO] 測試 日本-東京 (hnd-jp-ping.vultr.com)...
    正在測試延遲...
    正在測試下載速度...
    檔案大小: 100.0 MB
    [████████████████░░░░] 83.1% | 83.1MB | 211.6 Mbps
日本-東京: ↓ 223.6 Mbps | ping 0.2 ms

[INFO] 測試 澳大利亞-悉尼 (syd-au-ping.vultr.com)...
    正在測試延遲...
    正在測試下載速度...
    檔案大小: 100.0 MB
    [███████████████████░] 95.7% | 95.7MB | 123.3 Mbps
澳大利亞-悉尼: ↓ 125.1 Mbps | ping 0.3 ms

成功測試 3/3 個伺服器
平均下載速度: 205.9 Mbps
```

**進度顯示說明:**
- `[████████░░░░]` 進度條，每個█代表5%
- `91.5%` 當前下載進度百分比
- `91.5MB` 已下載數據量
- `197.0 Mbps` 即時下載速度

## 系統需求

- Python 3.6+
- 網路連接
- ping 命令 (系統內建)

## 使用建議

1. **首次使用**: 建議先使用 `--default` 測試預設機房組合
2. **地區測試**: 根據需求選擇特定地區進行測試
3. **完整測試**: 使用 `--all` 時建議在網路狀況良好時執行
4. **結果比較**: 可儲存不同時間的測試結果進行網路品質比較

## 限制說明

- 測試結果受當地網路狀況、ISP 路由、時間等因素影響
- 部分機房可能因網路政策限制無法訪問
- 測試結果僅供參考，實際使用體驗可能有差異

## 🆕 新功能重點說明

### 機房代碼衝突處理
當多個提供商有相同機房代碼時（如 `singapore`、`london`、`frankfurt` 等），系統會按以下優先順序選擇：

1. **HiNet** (最高優先級)
2. **Linode** (中等優先級)
3. **Vultr** (最低優先級)

**範例：**
```bash
# 不指定 zone，預設選擇 Linode Singapore
python vultr_speedtest.py --server singapore

# 明確指定測試 Vultr Singapore
python vultr_speedtest.py --server singapore --zone vultr

# 明確指定測試 Linode Singapore
python vultr_speedtest.py --server singapore --zone linode
```

### 多語言支援
所有工具現在支援三種語言介面：
- `--lang en`: 英文 (預設)
- `--lang zh`: 繁體中文
- `--lang ja`: 日文

語言設定會影響所有輸出文字，包括機房名稱、進度訊息、錯誤訊息等。