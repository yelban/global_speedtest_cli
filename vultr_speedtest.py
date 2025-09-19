#!/usr/bin/env python3
"""
Vultr Global Speed Test
透過下載 Vultr 機房測試檔案來測試網路速度
"""

import argparse
import time
import sys
from typing import Dict, List, Optional, Any
import urllib.request
import urllib.error
from urllib.parse import urljoin
import json
import datetime as dt
import threading
import subprocess
import signal

# 多語言支持
LANGUAGES = {
    "en": {
        "title": "🚀 Vultr Global Speed Test",
        "description": "Network speed test using Vultr datacenter test files",
        "available_servers": "Available speed test servers:",
        "taiwan_hinet": "TAIWAN HINET:",
        "linode_global": "LINODE GLOBAL:",
        "vultr_global": "VULTR GLOBAL:",
        "testing_server": "[INFO] Testing",
        "testing_latency": "Testing latency...",
        "testing_download": "Testing download speed...",
        "file_size": "File size",
        "ping": "ping",
        "download": "download",
        "test_failed": "Test failed",
        "unknown_error": "Unknown error",
        "interrupted": "⏹️  Testing interrupted by user",
        "completed_tests": "completed",
        "no_tests": "❌ No tests completed, exiting",
        "successful_tests": "Successfully tested",
        "servers": "servers",
        "avg_download_speed": "Average download speed",
        "starting_test": "Starting test for",
        "invalid_server_keys": "Invalid server keys",
        "use_list_to_see": "Use --list to see all available servers",
        "please_specify": "Please specify servers to test, use --help for usage",
        "result_saved_to": "[INFO] Results saved to",
        "connection_error": "Connection error",
        "test_timeout": "Test duration too short",
        "server_not_found": "Server not found"
    },
    "zh": {
        "title": "🚀 Vultr 全球機房網路速度測試",
        "description": "透過下載 Vultr 機房測試檔案來測試網路速度",
        "available_servers": "可用的測速伺服器:",
        "taiwan_hinet": "TAIWAN HINET:",
        "linode_global": "LINODE GLOBAL:",
        "vultr_global": "VULTR GLOBAL:",
        "testing_server": "[INFO] 測試",
        "testing_latency": "正在測試延遲...",
        "testing_download": "正在測試下載速度...",
        "file_size": "檔案大小",
        "ping": "ping",
        "download": "↓",
        "test_failed": "測試失敗",
        "unknown_error": "未知錯誤",
        "interrupted": "⏹️  測試被使用者中斷",
        "completed_tests": "已完成",
        "no_tests": "❌ 沒有完成任何測試，程式結束",
        "successful_tests": "成功測試",
        "servers": "個伺服器",
        "avg_download_speed": "平均下載速度",
        "starting_test": "開始測試",
        "invalid_server_keys": "無效的伺服器鍵值",
        "use_list_to_see": "使用 --list 查看所有可用伺服器",
        "please_specify": "請指定要測試的伺服器，使用 --help 查看使用說明",
        "result_saved_to": "[INFO] 結果已儲存至",
        "connection_error": "連接錯誤",
        "test_timeout": "測試時間過短",
        "server_not_found": "找不到伺服器"
    },
    "ja": {
        "title": "🚀 Vultr グローバルスピードテスト",
        "description": "Vultr データセンターのテストファイルを使用したネットワーク速度テスト",
        "available_servers": "利用可能な速度テストサーバー:",
        "taiwan_hinet": "TAIWAN HINET:",
        "linode_global": "LINODE GLOBAL:",
        "vultr_global": "VULTR GLOBAL:",
        "testing_server": "[INFO] テスト中",
        "testing_latency": "レイテンシをテスト中...",
        "testing_download": "ダウンロード速度をテスト中...",
        "file_size": "ファイルサイズ",
        "ping": "ping",
        "download": "↓",
        "test_failed": "テスト失敗",
        "unknown_error": "不明なエラー",
        "interrupted": "⏹️  ユーザーによってテストが中断されました",
        "completed_tests": "完了",
        "no_tests": "❌ テストが完了しませんでした。プログラムを終了します",
        "successful_tests": "成功したテスト",
        "servers": "サーバー",
        "avg_download_speed": "平均ダウンロード速度",
        "starting_test": "テスト開始",
        "invalid_server_keys": "無効なサーバーキー",
        "use_list_to_see": "--list を使用してすべての利用可能なサーバーを表示",
        "please_specify": "テストするサーバーを指定してください。使用方法は --help を参照",
        "result_saved_to": "[INFO] 結果を保存しました",
        "connection_error": "接続エラー",
        "test_timeout": "テスト時間が短すぎます",
        "server_not_found": "サーバーが見つかりません"
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Get localized text based on language"""
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, LANGUAGES["en"][key])

def get_server_name(server: Dict[str, Any], lang: str = "en") -> str:
    """Get localized server name"""
    if "names" in server:
        return server["names"].get(lang, server["names"].get("en", "Unknown"))
    else:
        # Fallback for old format
        return server.get("name", "Unknown")

# 台灣 HiNet 測速伺服器
HINET_SERVERS = {
    "taiwan": {
        "hinet_250m": {
            "names": {"en": "Taiwan-HiNet (250MB)", "zh": "台灣-HiNet (250MB)", "ja": "台湾-HiNet (250MB)"},
            "host": "http.speed.hinet.net",
            "test_url": "http://http.speed.hinet.net/test_250m.zip",
            "file_size": "250MB"
        },
        "hinet_2g": {
            "names": {"en": "Taiwan-HiNet (2GB)", "zh": "台灣-HiNet (2GB)", "ja": "台湾-HiNet (2GB)"},
            "host": "http.speed.hinet.net",
            "test_url": "http://http.speed.hinet.net/test_2048m.zip",
            "file_size": "2GB"
        }
    }
}

# Linode 全球測速伺服器
LINODE_SERVERS = {
    "asia": {
        "tokyo2": {
            "names": {"en": "Japan-Tokyo 2", "zh": "日本-東京 2", "ja": "日本-東京 2"},
            "host": "speedtest.tokyo2.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.tokyo2.linode.com/100MB-tokyo2.bin",
                "1GB": "https://speedtest.tokyo2.linode.com/1GB-tokyo2.bin"
            }
        },
        "tokyo3": {
            "names": {"en": "Japan-Tokyo 3", "zh": "日本-東京 3", "ja": "日本-東京 3"},
            "host": "jp-tyo-3.speedtest.linode.com",
            "test_urls": {
                "100MB": "https://jp-tyo-3.speedtest.linode.com/100MB-tokyo3.bin",
                "1GB": "https://jp-tyo-3.speedtest.linode.com/1GB-tokyo3.bin"
            }
        },
        "singapore": {
            "names": {"en": "Singapore", "zh": "新加坡", "ja": "シンガポール"},
            "host": "speedtest.singapore.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.singapore.linode.com/100MB-singapore.bin",
                "1GB": "https://speedtest.singapore.linode.com/1GB-singapore.bin"
            }
        },
        "mumbai": {
            "names": {"en": "India-Mumbai", "zh": "印度-孟買", "ja": "インド-ムンバイ"},
            "host": "speedtest.mumbai1.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.mumbai1.linode.com/100MB-mumbai.bin",
                "1GB": "https://speedtest.mumbai1.linode.com/1GB-mumbai.bin"
            }
        }
    },
    "north_america": {
        "fremont": {
            "names": {"en": "USA-Fremont", "zh": "美國-弗里蒙特", "ja": "米国-フリーモント"},
            "host": "speedtest.fremont.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.fremont.linode.com/100MB-fremont.bin",
                "1GB": "https://speedtest.fremont.linode.com/1GB-fremont.bin"
            }
        },
        "newark": {
            "names": {"en": "USA-Newark", "zh": "美國-紐瓦克", "ja": "米国-ニューアーク"},
            "host": "speedtest.newark.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.newark.linode.com/100MB-newark.bin",
                "1GB": "https://speedtest.newark.linode.com/1GB-newark.bin"
            }
        },
        "atlanta": {
            "names": {"en": "USA-Atlanta", "zh": "美國-亞特蘭大", "ja": "米国-アトランタ"},
            "host": "speedtest.atlanta.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.atlanta.linode.com/100MB-atlanta.bin",
                "1GB": "https://speedtest.atlanta.linode.com/1GB-atlanta.bin"
            }
        },
        "dallas": {
            "names": {"en": "USA-Dallas", "zh": "美國-達拉斯", "ja": "米国-ダラス"},
            "host": "speedtest.dallas.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.dallas.linode.com/100MB-dallas.bin",
                "1GB": "https://speedtest.dallas.linode.com/1GB-dallas.bin"
            }
        },
        "toronto": {
            "names": {"en": "Canada-Toronto", "zh": "加拿大-多倫多", "ja": "カナダ-トロント"},
            "host": "speedtest.toronto1.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.toronto1.linode.com/100MB-toronto.bin",
                "1GB": "https://speedtest.toronto1.linode.com/1GB-toronto.bin"
            }
        }
    },
    "europe": {
        "london": {
            "names": {"en": "UK-London", "zh": "英國-倫敦", "ja": "英国-ロンドン"},
            "host": "speedtest.london.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.london.linode.com/100MB-london.bin",
                "1GB": "https://speedtest.london.linode.com/1GB-london.bin"
            }
        },
        "frankfurt": {
            "names": {"en": "Germany-Frankfurt", "zh": "德國-法蘭克福", "ja": "ドイツ-フランクフルト"},
            "host": "speedtest.frankfurt.linode.com",
            "test_urls": {
                "100MB": "https://speedtest.frankfurt.linode.com/100MB-frankfurt.bin",
                "1GB": "https://speedtest.frankfurt.linode.com/1GB-frankfurt.bin"
            }
        }
    }
}

# Vultr 全球機房配置
VULTR_SERVERS = {
    "asia": {
        "tokyo": {
            "names": {"en": "Japan-Tokyo", "zh": "日本-東京", "ja": "日本-東京"},
            "host": "hnd-jp-ping.vultr.com",
            "ip": "108.61.201.151"
        },
        "osaka": {
            "names": {"en": "Japan-Osaka", "zh": "日本-大阪", "ja": "日本-大阪"},
            "host": "osk-jp-ping.vultr.com",
            "ip": "64.176.34.94"
        },
        "seoul": {
            "names": {"en": "South Korea-Seoul", "zh": "韓國-首爾", "ja": "韓国-ソウル"},
            "host": "sel-kor-ping.vultr.com",
            "ip": "141.164.34.61"
        },
        "singapore": {
            "names": {"en": "Singapore", "zh": "新加坡", "ja": "シンガポール"},
            "host": "sgp-ping.vultr.com",
            "ip": "45.32.100.168"
        },
        "bangalore": {
            "names": {"en": "India-Bangalore", "zh": "印度-班加羅爾", "ja": "インド-バンガロール"},
            "host": "blr-in-ping.vultr.com",
            "ip": "139.84.130.100"
        },
        "delhi": {
            "names": {"en": "India-Delhi NCR", "zh": "印度-德里NCR", "ja": "インド-デリー"},
            "host": "del-in-ping.vultr.com",
            "ip": "139.84.162.104"
        },
        "mumbai": {
            "names": {"en": "India-Mumbai", "zh": "印度-孟買", "ja": "インド-ムンバイ"},
            "host": "bom-in-ping.vultr.com",
            "ip": "65.20.66.100"
        },
        "tel_aviv": {
            "names": {"en": "Israel-Tel Aviv", "zh": "以色列-特拉維夫", "ja": "イスラエル-テルアビブ"},
            "host": "tlv-il-ping.vultr.com",
            "ip": "64.176.162.16"
        }
    },
    "europe": {
        "london": {
            "names": {"en": "UK-London", "zh": "英國-倫敦", "ja": "イギリス-ロンドン"},
            "host": "lon-gb-ping.vultr.com",
            "ip": "108.61.196.101"
        },
        "manchester": {
            "names": {"en": "UK-Manchester", "zh": "英國-曼徹斯特", "ja": "イギリス-マンチェスター"},
            "host": "man-uk-ping.vultr.com",
            "ip": "64.176.178.136"
        },
        "frankfurt": {
            "names": {"en": "Germany-Frankfurt", "zh": "德國-法蘭克福", "ja": "ドイツ-フランクフルト"},
            "host": "fra-de-ping.vultr.com",
            "ip": "108.61.210.117"
        },
        "paris": {
            "names": {"en": "France-Paris", "zh": "法國-巴黎", "ja": "フランス-パリ"},
            "host": "par-fr-ping.vultr.com",
            "ip": "108.61.209.127"
        },
        "amsterdam": {
            "names": {"en": "Netherlands-Amsterdam", "zh": "荷蘭-阿姆斯特丹", "ja": "オランダ-アムステルダム"},
            "host": "ams-nl-ping.vultr.com",
            "ip": "108.61.198.102"
        },
        "warsaw": {
            "names": {"en": "Poland-Warsaw", "zh": "波蘭-華沙", "ja": "ポーランド-ワルシャワ"},
            "host": "waw-pl-ping.vultr.com",
            "ip": "70.34.242.24"
        },
        "stockholm": {
            "names": {"en": "Sweden-Stockholm", "zh": "瑞典-斯德哥爾摩", "ja": "スウェーデン-ストックホルム"},
            "host": "sto-se-ping.vultr.com",
            "ip": "70.34.194.86"
        },
        "madrid": {
            "names": {"en": "Spain-Madrid", "zh": "西班牙-馬德里", "ja": "スペイン-マドリード"},
            "host": "mad-es-ping.vultr.com",
            "ip": "208.76.222.30"
        }
    },
    "north_america": {
        "atlanta": {
            "names": {"en": "USA-Atlanta", "zh": "美國-亞特蘭大", "ja": "アメリカ-アトランタ"},
            "host": "ga-us-ping.vultr.com",
            "ip": "108.61.193.166"
        },
        "chicago": {
            "names": {"en": "USA-Chicago", "zh": "美國-芝加哥", "ja": "アメリカ-シカゴ"},
            "host": "il-us-ping.vultr.com",
            "ip": "107.191.51.12"
        },
        "dallas": {
            "names": {"en": "USA-Dallas", "zh": "美國-達拉斯", "ja": "アメリカ-ダラス"},
            "host": "tx-us-ping.vultr.com",
            "ip": "108.61.224.175"
        },
        "honolulu": {
            "names": {"en": "USA-Honolulu", "zh": "美國-火奴魯魯", "ja": "アメリカ-ホノルル"},
            "host": "hon-hi-us-ping.vultr.com",
            "ip": "208.72.154.76"
        },
        "los_angeles": {
            "names": {"en": "USA-Los Angeles", "zh": "美國-洛杉磯", "ja": "アメリカ-ロサンゼルス"},
            "host": "lax-ca-us-ping.vultr.com",
            "ip": "108.61.219.200"
        },
        "miami": {
            "names": {"en": "USA-Miami", "zh": "美國-邁阿密", "ja": "アメリカ-マイアミ"},
            "host": "fl-us-ping.vultr.com",
            "ip": "104.156.244.232"
        },
        "new_york": {
            "names": {"en": "USA-New York", "zh": "美國-紐約", "ja": "アメリカ-ニューヨーク"},
            "host": "nj-us-ping.vultr.com",
            "ip": "108.61.149.182"
        },
        "seattle": {
            "names": {"en": "USA-Seattle", "zh": "美國-西雅圖", "ja": "アメリカ-シアトル"},
            "host": "wa-us-ping.vultr.com",
            "ip": "108.61.194.105"
        },
        "silicon_valley": {
            "names": {"en": "USA-Silicon Valley", "zh": "美國-硅谷", "ja": "アメリカ-シリコンバレー"},
            "host": "sjo-ca-us-ping.vultr.com",
            "ip": "104.156.230.107"
        },
        "toronto": {
            "names": {"en": "Canada-Toronto", "zh": "加拿大-多倫多", "ja": "カナダ-トロント"},
            "host": "tor-ca-ping.vultr.com",
            "ip": "149.248.50.81"
        },
        "mexico_city": {
            "names": {"en": "Mexico-Mexico City", "zh": "墨西哥-墨西哥城", "ja": "メキシコ-メキシコシティ"},
            "host": "mex-mx-ping.vultr.com",
            "ip": "216.238.66.16"
        }
    },
    "south_america": {
        "sao_paulo": {
            "names": {"en": "Brazil-São Paulo", "zh": "巴西-聖保羅", "ja": "ブラジル-サンパウロ"},
            "host": "sao-br-ping.vultr.com",
            "ip": "216.238.98.118"
        },
        "santiago": {
            "names": {"en": "Chile-Santiago", "zh": "智利-聖地牙哥", "ja": "チリ-サンティアゴ"},
            "host": "scl-cl-ping.vultr.com",
            "ip": "64.176.2.7"
        }
    },
    "africa": {
        "johannesburg": {
            "names": {"en": "South Africa-Johannesburg", "zh": "南非-約翰內斯堡", "ja": "南アフリカ-ヨハネスブルグ"},
            "host": "jnb-za-ping.vultr.com",
            "ip": "139.84.226.78"
        }
    },
    "oceania": {
        "melbourne": {
            "names": {"en": "Australia-Melbourne", "zh": "澳大利亞-墨爾本", "ja": "オーストラリア-メルボルン"},
            "host": "mel-au-ping.vultr.com",
            "ip": "67.219.110.24"
        },
        "sydney": {
            "names": {"en": "Australia-Sydney", "zh": "澳大利亞-雪梨", "ja": "オーストラリア-シドニー"},
            "host": "syd-au-ping.vultr.com",
            "ip": "108.61.212.117"
        }
    }
}

# 預設測試組合
DEFAULT_TEST_SET = ["hinet_250m", "tokyo", "singapore", "new_york", "paris", "sydney"]

class SpeedTest:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def ping_test(self, host: str) -> float:
        """測試延遲"""
        try:
            # 使用 ping 命令測試延遲
            result = subprocess.run(
                ["ping", "-c", "3", host],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                # 解析 ping 結果，提取平均延遲
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'avg' in line or '平均' in line:
                        # macOS/Linux: time=xx.xx ms
                        import re
                        match = re.search(r'(\d+\.?\d*)\s*ms', line)
                        if match:
                            return float(match.group(1))
            return -1
        except KeyboardInterrupt:
            # 重新拋出 KeyboardInterrupt 讓上層處理
            raise
        except Exception:
            return -1

    def download_test(self, host: str, test_size: str = "100MB", show_progress: bool = True, quick_test: bool = False, custom_url: str = None, lang: str = "en") -> Dict[str, Any]:
        """下載速度測試"""
        if custom_url:
            test_url = custom_url
        else:
            # Vultr 使用的實際測試檔案路徑
            if test_size == "100MB":
                test_url = f"http://{host}/vultr.com.100MB.bin"
            else:
                test_url = f"http://{host}/vultr.com.1000MB.bin"

        try:
            # 準備進度追蹤
            start_time = time.time()
            total_downloaded = 0
            chunk_size = 8192
            last_update = start_time
            speed_samples = []

            # 創建請求
            req = urllib.request.Request(test_url)
            req.add_header('User-Agent', 'Vultr-SpeedTest/1.0')

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                content_length = response.headers.get('Content-Length')
                if content_length:
                    total_size = int(content_length)
                else:
                    # 根據 URL 判斷檔案大小
                    if "250m" in test_url.lower():
                        total_size = 250 * 1024 * 1024  # 250MB
                    elif "2048m" in test_url.lower():
                        total_size = 2048 * 1024 * 1024  # 2048MB
                    elif "1000MB" in test_url or "1GB" in test_url:
                        total_size = 1000 * 1024 * 1024  # 1000MB
                    else:
                        total_size = 100 * 1024 * 1024  # 100MB fallback

                if show_progress:
                    print(f"    {get_text('file_size', lang)}: {total_size / 1024 / 1024:.1f} MB")
                    print("    ", end="", flush=True)

                # 下載資料並計算速度
                while total_downloaded < total_size:
                    chunk_start = time.time()
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break

                    chunk_time = time.time() - chunk_start
                    total_downloaded += len(chunk)
                    current_time = time.time()
                    elapsed = current_time - start_time

                    # 計算即時速度 (每0.5秒更新一次)
                    if show_progress and (current_time - last_update) >= 0.5:
                        if elapsed > 0:
                            current_speed_mbps = (total_downloaded / elapsed) / 1024 / 1024 * 8
                            progress_percent = (total_downloaded / total_size) * 100
                            downloaded_mb = total_downloaded / 1024 / 1024

                            # 清除當前行並顯示進度
                            progress_bar = "█" * int(progress_percent // 5) + "░" * (20 - int(progress_percent // 5))
                            print(f"\r    [{progress_bar}] {progress_percent:.1f}% | "
                                  f"{downloaded_mb:.1f}MB | {current_speed_mbps:.1f} Mbps",
                                  end="", flush=True)
                        last_update = current_time

                    # 限制下載時間，避免過長
                    if elapsed > self.timeout:
                        break

                    # 如果是快速測試模式，可以提前結束
                    if quick_test and elapsed >= 5 and total_downloaded >= 1048576:  # 至少5秒和1MB
                        # 但如果是100MB測試且速度很快，至少下載10MB
                        if test_size == "100MB" and total_downloaded < 10485760 and elapsed < 10:
                            continue
                        break

                if show_progress:
                    print()  # 換行

            end_time = time.time()
            elapsed = end_time - start_time

            if elapsed > 0:
                speed_bps = total_downloaded / elapsed
                speed_mbps = speed_bps / 1024 / 1024 * 8  # 轉換為 Mbps

                return {
                    "success": True,
                    "speed_mbps": speed_mbps,
                    "downloaded_bytes": total_downloaded,
                    "elapsed_seconds": elapsed,
                    "test_url": test_url
                }
            else:
                return {"success": False, "error": get_text("test_timeout", lang)}

        except KeyboardInterrupt:
            # 重新拋出 KeyboardInterrupt 讓上層處理
            raise
        except urllib.error.URLError as e:
            return {"success": False, "error": f"{get_text('connection_error', lang)}: {e}"}
        except Exception as e:
            return {"success": False, "error": f"{get_text('test_failed', lang)}: {e}"}

def get_server_by_key_with_zone(key: str, zone: str = None) -> Optional[Dict[str, str]]:
    """根據鍵值和指定區域獲取伺服器資訊"""
    if zone:
        # 如果指定了區域，只在該區域查找
        if zone == "hinet":
            for region, servers in HINET_SERVERS.items():
                if key in servers:
                    server = servers[key].copy()
                    server["key"] = key
                    server["region"] = region
                    server["provider"] = "hinet"
                    return server
        elif zone == "linode":
            for region, servers in LINODE_SERVERS.items():
                if key in servers:
                    server = servers[key].copy()
                    server["key"] = key
                    server["region"] = region
                    server["provider"] = "linode"
                    return server
        elif zone == "vultr":
            for region, servers in VULTR_SERVERS.items():
                if key in servers:
                    server = servers[key].copy()
                    server["key"] = key
                    server["region"] = region
                    server["provider"] = "vultr"
                    return server
        return None
    else:
        # 如果沒指定區域，使用預設順序
        return get_server_by_key(key)

def get_server_by_key(key: str) -> Optional[Dict[str, str]]:
    """根據鍵值獲取伺服器資訊"""
    # 先檢查 HiNet 伺服器
    for region, servers in HINET_SERVERS.items():
        if key in servers:
            server = servers[key].copy()
            server["key"] = key
            server["region"] = region
            server["provider"] = "hinet"
            return server

    # 檢查 Linode 伺服器
    for region, servers in LINODE_SERVERS.items():
        if key in servers:
            server = servers[key].copy()
            server["key"] = key
            server["region"] = region
            server["provider"] = "linode"
            return server

    # 再檢查 Vultr 伺服器
    for region, servers in VULTR_SERVERS.items():
        if key in servers:
            server = servers[key].copy()
            server["key"] = key
            server["region"] = region
            server["provider"] = "vultr"
            return server
    return None

def list_all_servers(lang: str = "en"):
    """列出所有可用的伺服器"""
    print(get_text("available_servers", lang))
    print("=" * 50)

    # 顯示 HiNet 伺服器
    print(f"\n{get_text('taiwan_hinet', lang)}")
    for region, servers in HINET_SERVERS.items():
        for key, server in servers.items():
            server_name = get_server_name(server, lang)
            print(f"  {key:<15} - {server_name}")

    # 顯示 Linode 伺服器
    print(f"\n{get_text('linode_global', lang)}")
    for region, servers in LINODE_SERVERS.items():
        print(f"\n{region.upper().replace('_', ' ')}:")
        for key, server in servers.items():
            server_name = get_server_name(server, lang)
            print(f"  {key:<15} - {server_name}")

    # 顯示 Vultr 伺服器
    print(f"\n{get_text('vultr_global', lang)}")
    for region, servers in VULTR_SERVERS.items():
        print(f"\n{region.upper().replace('_', ' ')}:")
        for key, server in servers.items():
            server_name = get_server_name(server, lang)
            print(f"  {key:<15} - {server_name}")

def test_single_server(key: str, test_size: str = "100MB", show_progress: bool = True, quick_test: bool = False, lang: str = "en", zone: str = None) -> Dict[str, Any]:
    """測試單一伺服器"""
    server = get_server_by_key_with_zone(key, zone)
    if not server:
        zone_info = f" in zone '{zone}'" if zone else ""
        return {"success": False, "error": f"{get_text('server_not_found', lang)}: {key}{zone_info}"}

    try:
        server_name = get_server_name(server, lang)
        print(f"{get_text('testing_server', lang)} {server_name} ({server['host']})...")

        speed_test = SpeedTest()

        # Ping 測試
        if show_progress:
            print(f"    {get_text('testing_latency', lang)}")
        ping_ms = speed_test.ping_test(server["host"])

        # 下載測試
        if show_progress:
            print(f"    {get_text('testing_download', lang)}")

        # 檢查不同提供商的伺服器，使用對應的測試 URL
        if server.get("provider") == "hinet":
            download_result = speed_test.download_test(server["host"], test_size, show_progress, quick_test, server.get("test_url"), lang)
        elif server.get("provider") == "linode":
            # Linode 伺服器使用 test_urls 中對應大小的 URL
            test_url = server.get("test_urls", {}).get(test_size)
            download_result = speed_test.download_test(server["host"], test_size, show_progress, quick_test, test_url, lang)
        else:
            download_result = speed_test.download_test(server["host"], test_size, show_progress, quick_test, None, lang)

        result = {
            "server_key": key,
            "server_name": server_name,
            "server_host": server["host"],
            "server_ip": server.get("ip", "N/A"),
            "region": server["region"],
            "ping_ms": ping_ms,
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat()
        }

        if download_result["success"]:
            result.update({
                "download_mbps": download_result["speed_mbps"],
                "downloaded_bytes": download_result["downloaded_bytes"],
                "test_duration": download_result["elapsed_seconds"],
                "test_url": download_result["test_url"]
            })
        else:
            result["error"] = download_result["error"]

        return result

    except KeyboardInterrupt:
        # 重新拋出 KeyboardInterrupt 讓上層處理
        raise

def test_multiple_servers(server_keys: List[str], test_size: str = "100MB",
                         cooldown: float = 2.0, show_progress: bool = True, quick_test: bool = False, lang: str = "en", zone: str = None) -> List[Dict[str, Any]]:
    """測試多個伺服器"""
    results = []

    try:
        for i, key in enumerate(server_keys):
            result = test_single_server(key, test_size, show_progress, quick_test, lang, zone)
            results.append(result)

            # 顯示結果
            if "download_mbps" in result:
                print(f"{result['server_name']}: "
                      f"{get_text('download', lang)} {result['download_mbps']:.1f} Mbps | "
                      f"{get_text('ping', lang)} {result['ping_ms']:.1f} ms")
            else:
                print(f"{result['server_name']}: {get_text('test_failed', lang)} - {result.get('error', get_text('unknown_error', lang))}")

            # 等待間隔（除了最後一個）
            if i < len(server_keys) - 1 and cooldown > 0:
                time.sleep(cooldown)

    except KeyboardInterrupt:
        print(f"\n\n{get_text('interrupted', lang)} ({len(results)}/{len(server_keys)} {get_text('completed_tests', lang)})")
        if len(results) == 0:
            print(get_text('no_tests', lang))
            return results

    return results

def main():
    parser = argparse.ArgumentParser(description="Vultr Global Speed Test Tool")
    parser.add_argument("--server", "-s", help="Test specific server (use --list to see available servers)")
    parser.add_argument("--zone", choices=["vultr", "linode", "hinet"],
                       help="Specify provider zone (vultr/linode/hinet). When server key conflicts, this determines which provider to use.")
    parser.add_argument("--servers", nargs="+", help="Test multiple specific servers")
    parser.add_argument("--default", action="store_true", help="Test default server combination")
    parser.add_argument("--all", action="store_true", help="Test all servers")
    parser.add_argument("--list", action="store_true", help="List all available servers")
    parser.add_argument("--size", default="100MB", choices=["100MB", "1GB"],
                       help="Test file size (default: 100MB)")
    parser.add_argument("--cooldown", type=float, default=2.0,
                       help="Test interval in seconds (default: 2.0)")
    parser.add_argument("--output", help="Save results as JSON file")
    parser.add_argument("--timeout", type=int, default=30,
                       help="Single test timeout in seconds (default: 30)")
    parser.add_argument("--no-progress", action="store_true",
                       help="Do not show progress bar")
    parser.add_argument("--quick", action="store_true",
                       help="Quick test mode (partial download, default is full download)")
    parser.add_argument("--lang", choices=["en", "zh", "ja"], default="en",
                       help="Display language: en(English), zh(Traditional Chinese), ja(Japanese)")

    args = parser.parse_args()

    if args.list:
        list_all_servers(args.lang)
        return

    # 決定要測試的伺服器
    if args.server:
        server_keys = [args.server]
    elif args.servers:
        server_keys = args.servers
    elif args.default:
        server_keys = DEFAULT_TEST_SET
    elif args.all:
        server_keys = []
        # 加入 HiNet 伺服器
        for region, servers in HINET_SERVERS.items():
            server_keys.extend(servers.keys())
        # 加入 Linode 伺服器
        for region, servers in LINODE_SERVERS.items():
            server_keys.extend(servers.keys())
        # 加入 Vultr 伺服器
        for region, servers in VULTR_SERVERS.items():
            server_keys.extend(servers.keys())
    else:
        print(get_text("please_specify", args.lang))
        return

    # 驗證伺服器鍵值
    invalid_keys = [key for key in server_keys if get_server_by_key_with_zone(key, args.zone) is None]
    if invalid_keys:
        zone_info = f" in zone '{args.zone}'" if args.zone else ""
        print(f"{get_text('invalid_server_keys', args.lang)}: {invalid_keys}{zone_info}")
        print(get_text("use_list_to_see", args.lang))
        return

    print(f"{get_text('starting_test', args.lang)} {len(server_keys)} {get_text('servers', args.lang)}...")
    print("=" * 50)

    # 執行測試
    SpeedTest.timeout = args.timeout
    show_progress = not args.no_progress
    quick_test = args.quick
    results = test_multiple_servers(server_keys, args.size, args.cooldown, show_progress, quick_test, args.lang, args.zone)

    # 儲存結果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n{get_text('result_saved_to', args.lang)} {args.output}")

    # 顯示摘要
    successful_tests = [r for r in results if "download_mbps" in r]
    if successful_tests:
        print(f"\n{get_text('successful_tests', args.lang)} {len(successful_tests)}/{len(results)} {get_text('servers', args.lang)}")
        avg_speed = sum(r["download_mbps"] for r in successful_tests) / len(successful_tests)
        print(f"{get_text('avg_download_speed', args.lang)}: {avg_speed:.1f} Mbps")

if __name__ == "__main__":
    main()