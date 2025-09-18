# Global Network Speed Test Tools

A collection of Python-based network connectivity and speed testing tools for global servers and data centers.

## 🚀 Features

- **No External Dependencies**: Uses Python standard library only
- **Global Coverage**: Tests connections to worldwide servers and data centers
- **Multiple Testing Modes**: Command-line and interactive interfaces
- **Comprehensive Metrics**: DNS resolution, TCP connection, HTTP response times
- **Real-time Progress**: Live download progress and speed monitoring
- **Flexible Configuration**: Customizable test parameters and server selection
- **Export Results**: Save test results in JSON format

## 📦 Tools Included

### 1. simple_netcheck.py
A lightweight network connectivity tester that measures connection performance to global websites and Vultr data centers.

**Key Features:**
- Tests DNS resolution, TCP connection, and HTTP response times
- Includes 11 major global websites and 32 Vultr data centers
- Intelligent scoring system (0-100 based on latency)
- Regional filtering and statistics
- No external dependencies required

### 2. vultr_speedtest.py
A comprehensive speed testing tool for Vultr global data centers and Taiwan HiNet servers.

**Key Features:**
- Download speed testing with real-time progress
- Support for 100MB and 1GB test files
- Ping latency measurements
- Both quick test and full download modes
- Taiwan HiNet speed test integration

### 3. interactive_vultr_test.py
An interactive menu-driven interface for the Vultr speed testing tool.

**Key Features:**
- User-friendly text-based menu system
- Multiple test modes (quick, regional, specific servers)
- Configurable test settings
- Automatic result saving and statistics
- Progress visualization

## 🌍 Supported Test Locations

### Global Websites
- Taiwan, Japan, South Korea, Singapore, Hong Kong, Malaysia
- Australia, United Kingdom, Germany, United States

### Vultr Data Centers (32 locations)
- **Asia**: Tokyo, Osaka, Seoul, Singapore, Mumbai, Delhi, Bangalore, Tel Aviv
- **Europe**: London, Manchester, Frankfurt, Paris, Amsterdam, Warsaw, Stockholm, Madrid
- **North America**: Atlanta, Chicago, Dallas, Honolulu, Los Angeles, Miami, New York, Seattle, Silicon Valley, Toronto, Mexico City
- **South America**: São Paulo, Santiago
- **Africa**: Johannesburg
- **Oceania**: Melbourne, Sydney

### Taiwan HiNet
- 250MB and 2GB test files from official HiNet speed test servers

## 🛠️ Installation

No installation required! These tools use only Python standard library.

### Prerequisites
- Python 3.6 or higher
- Internet connection
- `ping` command available (for latency testing)

### Quick Start
```bash
git clone <repository-url>
cd global-netcheck
```

## 📖 Usage

### Simple Network Check
```bash
# Test all sites (default)
python3 simple_netcheck.py

# Test only global websites
python3 simple_netcheck.py --sites global

# Test only Vultr data centers
python3 simple_netcheck.py --sites vultr

# Filter by region
python3 simple_netcheck.py --region Asia

# Save results to JSON
python3 simple_netcheck.py --output results.json

# List all available test sites
python3 simple_netcheck.py --list
```

### Vultr Speed Test (Command Line)
```bash
# Test default server set
python3 vultr_speedtest.py --default

# Test specific server
python3 vultr_speedtest.py --server tokyo

# Test multiple servers
python3 vultr_speedtest.py --servers tokyo singapore new_york

# Test all servers
python3 vultr_speedtest.py --all

# Use 1GB test file with quick mode
python3 vultr_speedtest.py --server tokyo --size 1GB --quick

# List all available servers
python3 vultr_speedtest.py --list
```

### Interactive Vultr Test
```bash
# Launch interactive interface
python3 interactive_vultr_test.py
```

Then follow the menu prompts to:
1. Choose test mode (quick test, regional test, etc.)
2. Configure test settings (file size, download mode)
3. Execute tests and view results
4. Optionally save results to JSON

## 📊 Understanding Results

### Simple Network Check Output
```
🌐 Simple Network Connection Test
📍 Testing global website connectivity performance
============================================================
[ 1/11] Testing Taipei, Taiwan      ✅   45.2ms (Score: 100)
[ 2/11] Testing Tokyo, Japan        ✅   67.8ms (Score:  90)

============================================================
🏆 Test Results Ranking (sorted by total latency):
Rank  Location             Total     DNS      TCP      HTTP     Score
----------------------------------------------------------------------
1     Taipei, Taiwan       45.2ms    12.3ms   15.6ms   17.3ms   100
2     Tokyo, Japan         67.8ms    18.7ms   23.1ms   26.0ms    90

🥇 Best Connection: Taipei, Taiwan (45.2ms)

📊 Regional Statistics:
  Asia           : Average latency   89.4ms (8 servers)
  Europe         : Average latency  156.7ms (2 servers)
```

### Vultr Speed Test Output
```
Testing Tokyo-Japan (hnd-jp-ping.vultr.com)...
    Testing latency...
    Testing download speed...
    File size: 100.0 MB
    [████████████████████] 100.0% | 100.0MB | 89.5 Mbps
Tokyo-Japan: ↓ 89.5 Mbps | ping 35.2 ms

📊 Test Summary:
Successful tests: 5/6 servers
Average download speed: 78.3 Mbps
Fastest server: Tokyo-Japan (89.5 Mbps)
```

## 🎯 Scoring System (simple_netcheck.py)

- **100 points**: < 50ms (Excellent)
- **90 points**: 50-100ms (Very Good)
- **80 points**: 100-200ms (Good)
- **60 points**: 200-500ms (Fair)
- **40 points**: 500-1000ms (Poor)
- **20 points**: 1000-2000ms (Very Poor)
- **10 points**: > 2000ms (Unacceptable)

## 🔧 Configuration Options

### Command Line Arguments

#### simple_netcheck.py
| Option | Description | Default |
|--------|-------------|---------|
| `--region` | Filter by region | All regions |
| `--timeout` | Connection timeout (seconds) | 10.0 |
| `--output` | Save results to JSON file | None |
| `--sites` | Site type: global/vultr/all | all |
| `--list` | List all test sites | False |

#### vultr_speedtest.py
| Option | Description | Default |
|--------|-------------|---------|
| `--server` | Test specific server | None |
| `--servers` | Test multiple servers | None |
| `--default` | Test default server set | False |
| `--all` | Test all servers | False |
| `--size` | Test file size: 100MB/1GB | 100MB |
| `--cooldown` | Delay between tests (seconds) | 2.0 |
| `--timeout` | Test timeout (seconds) | 30 |
| `--quick` | Quick test mode | False |
| `--no-progress` | Hide progress bar | False |

## 📁 Output Files

### JSON Export Format
```json
{
  "server_key": "tokyo",
  "server_name": "Japan-Tokyo",
  "server_host": "hnd-jp-ping.vultr.com",
  "ping_ms": 35.2,
  "download_mbps": 89.5,
  "downloaded_bytes": 104857600,
  "test_duration": 9.3,
  "timestamp": "2024-03-15T10:30:45.123456+00:00"
}
```

## 🚨 Important Notes

1. **Network Impact**: Speed tests consume bandwidth, especially with 1GB files
2. **Firewall Restrictions**: Some networks may block connections to certain servers
3. **Test Frequency**: Avoid excessive testing to prevent rate limiting
4. **Results Interpretation**: Results reflect current network conditions and may vary
5. **Keyboard Interruption**: All tools support Ctrl+C for safe cancellation

## 🎯 Use Cases

- **Network Diagnostics**: Quickly assess network connectivity quality
- **Server Selection**: Compare performance of different data center locations
- **Network Monitoring**: Regular network performance checks
- **Educational**: Understanding network connection phases
- **VPS Hosting**: Choose optimal server locations for your applications

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve these tools.

## 📄 License

This project is open source. Please check the license file for details.

## 📚 Additional Documentation

- [simple_netcheck.py Documentation](simple_netcheck.md)
- [interactive_vultr_test.py Documentation](interactive_vultr_test.md)
- [Traditional Chinese README](README.zh-TW.md)
- [Japanese README](README.ja.md)