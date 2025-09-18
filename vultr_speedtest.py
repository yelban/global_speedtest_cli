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

# 台灣 HiNet 測速伺服器
HINET_SERVERS = {
    "taiwan": {
        "hinet_250m": {
            "name": "台灣-HiNet (250MB)",
            "host": "http.speed.hinet.net",
            "test_url": "http://http.speed.hinet.net/test_250m.zip",
            "file_size": "250MB"
        },
        "hinet_2g": {
            "name": "台灣-HiNet (2GB)",
            "host": "http.speed.hinet.net",
            "test_url": "http://http.speed.hinet.net/test_2048m.zip",
            "file_size": "2GB"
        }
    }
}

# Vultr 全球機房配置
VULTR_SERVERS = {
    "asia": {
        "tokyo": {
            "name": "日本-東京",
            "host": "hnd-jp-ping.vultr.com",
            "ip": "108.61.201.151"
        },
        "osaka": {
            "name": "日本-大阪",
            "host": "osk-jp-ping.vultr.com",
            "ip": "64.176.34.94"
        },
        "seoul": {
            "name": "韓國-首爾",
            "host": "sel-kor-ping.vultr.com",
            "ip": "141.164.34.61"
        },
        "singapore": {
            "name": "新加坡",
            "host": "sgp-ping.vultr.com",
            "ip": "45.32.100.168"
        },
        "bangalore": {
            "name": "印度-班加羅爾",
            "host": "blr-in-ping.vultr.com",
            "ip": "139.84.130.100"
        },
        "delhi": {
            "name": "印度-德里NCR",
            "host": "del-in-ping.vultr.com",
            "ip": "139.84.162.104"
        },
        "mumbai": {
            "name": "印度-孟買",
            "host": "bom-in-ping.vultr.com",
            "ip": "65.20.66.100"
        },
        "tel_aviv": {
            "name": "以色列-特拉維夫",
            "host": "tlv-il-ping.vultr.com",
            "ip": "64.176.162.16"
        }
    },
    "europe": {
        "london": {
            "name": "英國-倫敦",
            "host": "lon-gb-ping.vultr.com",
            "ip": "108.61.196.101"
        },
        "manchester": {
            "name": "英國-曼徹斯特",
            "host": "man-uk-ping.vultr.com",
            "ip": "64.176.178.136"
        },
        "frankfurt": {
            "name": "德國-法蘭克福",
            "host": "fra-de-ping.vultr.com",
            "ip": "108.61.210.117"
        },
        "paris": {
            "name": "法國-巴黎",
            "host": "par-fr-ping.vultr.com",
            "ip": "108.61.209.127"
        },
        "amsterdam": {
            "name": "荷蘭-阿姆斯特丹",
            "host": "ams-nl-ping.vultr.com",
            "ip": "108.61.198.102"
        },
        "warsaw": {
            "name": "波蘭-華沙",
            "host": "waw-pl-ping.vultr.com",
            "ip": "70.34.242.24"
        },
        "stockholm": {
            "name": "瑞典-斯德哥爾摩",
            "host": "sto-se-ping.vultr.com",
            "ip": "70.34.194.86"
        },
        "madrid": {
            "name": "西班牙-馬德里",
            "host": "mad-es-ping.vultr.com",
            "ip": "208.76.222.30"
        }
    },
    "north_america": {
        "atlanta": {
            "name": "美國-亞特蘭大",
            "host": "ga-us-ping.vultr.com",
            "ip": "108.61.193.166"
        },
        "chicago": {
            "name": "美國-芝加哥",
            "host": "il-us-ping.vultr.com",
            "ip": "107.191.51.12"
        },
        "dallas": {
            "name": "美國-達拉斯",
            "host": "tx-us-ping.vultr.com",
            "ip": "108.61.224.175"
        },
        "honolulu": {
            "name": "美國-火奴魯魯",
            "host": "hon-hi-us-ping.vultr.com",
            "ip": "208.72.154.76"
        },
        "los_angeles": {
            "name": "美國-洛杉磯",
            "host": "lax-ca-us-ping.vultr.com",
            "ip": "108.61.219.200"
        },
        "miami": {
            "name": "美國-邁阿密",
            "host": "fl-us-ping.vultr.com",
            "ip": "104.156.244.232"
        },
        "new_york": {
            "name": "美國-紐約",
            "host": "nj-us-ping.vultr.com",
            "ip": "108.61.149.182"
        },
        "seattle": {
            "name": "美國-西雅圖",
            "host": "wa-us-ping.vultr.com",
            "ip": "108.61.194.105"
        },
        "silicon_valley": {
            "name": "美國-硅谷",
            "host": "sjo-ca-us-ping.vultr.com",
            "ip": "104.156.230.107"
        },
        "toronto": {
            "name": "加拿大-多倫多",
            "host": "tor-ca-ping.vultr.com",
            "ip": "149.248.50.81"
        },
        "mexico_city": {
            "name": "墨西哥-墨西哥城",
            "host": "mex-mx-ping.vultr.com",
            "ip": "216.238.66.16"
        }
    },
    "south_america": {
        "sao_paulo": {
            "name": "巴西-聖保羅",
            "host": "sao-br-ping.vultr.com",
            "ip": "216.238.98.118"
        },
        "santiago": {
            "name": "智利-聖地牙哥",
            "host": "scl-cl-ping.vultr.com",
            "ip": "64.176.2.7"
        }
    },
    "africa": {
        "johannesburg": {
            "name": "南非-約翰內斯堡",
            "host": "jnb-za-ping.vultr.com",
            "ip": "139.84.226.78"
        }
    },
    "oceania": {
        "melbourne": {
            "name": "澳大利亞-墨爾本",
            "host": "mel-au-ping.vultr.com",
            "ip": "67.219.110.24"
        },
        "sydney": {
            "name": "澳大利亞-雪梨",
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

    def download_test(self, host: str, test_size: str = "100MB", show_progress: bool = True, quick_test: bool = False, custom_url: str = None) -> Dict[str, Any]:
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
                    print(f"    檔案大小: {total_size / 1024 / 1024:.1f} MB")
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
                return {"success": False, "error": "測試時間過短"}

        except KeyboardInterrupt:
            # 重新拋出 KeyboardInterrupt 讓上層處理
            raise
        except urllib.error.URLError as e:
            return {"success": False, "error": f"連接錯誤: {e}"}
        except Exception as e:
            return {"success": False, "error": f"測試失敗: {e}"}

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

    # 再檢查 Vultr 伺服器
    for region, servers in VULTR_SERVERS.items():
        if key in servers:
            server = servers[key].copy()
            server["key"] = key
            server["region"] = region
            server["provider"] = "vultr"
            return server
    return None

def list_all_servers():
    """列出所有可用的伺服器"""
    print("可用的測速伺服器:")
    print("=" * 50)

    # 顯示 HiNet 伺服器
    print("\nTAIWAN HINET:")
    for region, servers in HINET_SERVERS.items():
        for key, server in servers.items():
            print(f"  {key:<15} - {server['name']}")

    # 顯示 Vultr 伺服器
    print(f"\nVULTR GLOBAL:")
    for region, servers in VULTR_SERVERS.items():
        print(f"\n{region.upper().replace('_', ' ')}:")
        for key, server in servers.items():
            print(f"  {key:<15} - {server['name']}")

def test_single_server(key: str, test_size: str = "100MB", show_progress: bool = True, quick_test: bool = False) -> Dict[str, Any]:
    """測試單一伺服器"""
    server = get_server_by_key(key)
    if not server:
        return {"success": False, "error": f"找不到伺服器: {key}"}

    try:
        print(f"[INFO] 測試 {server['name']} ({server['host']})...")

        speed_test = SpeedTest()

        # Ping 測試
        if show_progress:
            print("    正在測試延遲...")
        ping_ms = speed_test.ping_test(server["host"])

        # 下載測試
        if show_progress:
            print("    正在測試下載速度...")

        # 檢查是否為 HiNet 伺服器，使用自訂 URL
        if server.get("provider") == "hinet":
            download_result = speed_test.download_test(server["host"], test_size, show_progress, quick_test, server.get("test_url"))
        else:
            download_result = speed_test.download_test(server["host"], test_size, show_progress, quick_test)

        result = {
            "server_key": key,
            "server_name": server["name"],
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
                         cooldown: float = 2.0, show_progress: bool = True, quick_test: bool = False) -> List[Dict[str, Any]]:
    """測試多個伺服器"""
    results = []

    try:
        for i, key in enumerate(server_keys):
            result = test_single_server(key, test_size, show_progress, quick_test)
            results.append(result)

            # 顯示結果
            if "download_mbps" in result:
                print(f"{result['server_name']}: "
                      f"↓ {result['download_mbps']:.1f} Mbps | "
                      f"ping {result['ping_ms']:.1f} ms")
            else:
                print(f"{result['server_name']}: 測試失敗 - {result.get('error', '未知錯誤')}")

            # 等待間隔（除了最後一個）
            if i < len(server_keys) - 1 and cooldown > 0:
                time.sleep(cooldown)

    except KeyboardInterrupt:
        print(f"\n\n⏹️  測試被使用者中斷 (已完成 {len(results)}/{len(server_keys)} 個測試)")
        if len(results) == 0:
            print("❌ 沒有完成任何測試，程式結束")
            return results

    return results

def main():
    parser = argparse.ArgumentParser(description="Vultr 全球機房網路速度測試工具")
    parser.add_argument("--server", "-s", help="測試指定伺服器 (使用 --list 查看可用伺服器)")
    parser.add_argument("--servers", nargs="+", help="測試多個指定伺服器")
    parser.add_argument("--default", action="store_true", help="測試預設伺服器組合")
    parser.add_argument("--all", action="store_true", help="測試所有伺服器")
    parser.add_argument("--list", action="store_true", help="列出所有可用伺服器")
    parser.add_argument("--size", default="100MB", choices=["100MB", "1GB"],
                       help="測試檔案大小 (預設: 100MB)")
    parser.add_argument("--cooldown", type=float, default=2.0,
                       help="測試間隔秒數 (預設: 2.0)")
    parser.add_argument("--output", help="將結果儲存為 JSON 檔案")
    parser.add_argument("--timeout", type=int, default=30,
                       help="單次測試超時秒數 (預設: 30)")
    parser.add_argument("--no-progress", action="store_true",
                       help="不顯示進度條")
    parser.add_argument("--quick", action="store_true",
                       help="快速測試模式 (部分下載，預設為完整下載)")

    args = parser.parse_args()

    if args.list:
        list_all_servers()
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
        # 加入 Vultr 伺服器
        for region, servers in VULTR_SERVERS.items():
            server_keys.extend(servers.keys())
    else:
        print("請指定要測試的伺服器，使用 --help 查看使用說明")
        return

    # 驗證伺服器鍵值
    invalid_keys = [key for key in server_keys if get_server_by_key(key) is None]
    if invalid_keys:
        print(f"無效的伺服器鍵值: {invalid_keys}")
        print("使用 --list 查看所有可用伺服器")
        return

    print(f"開始測試 {len(server_keys)} 個伺服器...")
    print("=" * 50)

    # 執行測試
    SpeedTest.timeout = args.timeout
    show_progress = not args.no_progress
    quick_test = args.quick
    results = test_multiple_servers(server_keys, args.size, args.cooldown, show_progress, quick_test)

    # 儲存結果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n[INFO] 結果已儲存至 {args.output}")

    # 顯示摘要
    successful_tests = [r for r in results if "download_mbps" in r]
    if successful_tests:
        print(f"\n成功測試 {len(successful_tests)}/{len(results)} 個伺服器")
        avg_speed = sum(r["download_mbps"] for r in successful_tests) / len(successful_tests)
        print(f"平均下載速度: {avg_speed:.1f} Mbps")

if __name__ == "__main__":
    main()