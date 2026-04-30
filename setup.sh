#!/bin/bash
# Setup script for IPTV Bangladesh Filter
# Makes it easy to configure proxy and run merge.py

set -e

echo "=========================================="
echo "🇧🇩 IPTV Bangladesh Filter - Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q requests
echo "✅ Dependencies installed"
echo ""

# Check if proxy is already set
if [ ! -z "$HTTP_PROXY" ]; then
    echo "Found existing HTTP_PROXY: $HTTP_PROXY"
    read -p "Use this proxy? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        export HTTPS_PROXY="$HTTP_PROXY"
        USE_PROXY=1
    else
        USE_PROXY=0
    fi
else
    USE_PROXY=0
fi

# Prompt for proxy if needed
if [ $USE_PROXY -eq 0 ]; then
    echo "=========================================="
    echo "⚙️  Configure Bangladeshi Proxy"
    echo "=========================================="
    echo ""
    echo "You need a Bangladesh proxy to use this script."
    echo ""
    echo "Options:"
    echo "1) Test popular Bangladesh proxies"
    echo "2) Enter custom proxy"
    echo "3) Find proxies online"
    echo ""
    
    read -p "Choose option (1-3) [1]: " OPTION
    OPTION=${OPTION:-1}
    
    case $OPTION in
        1)
            echo ""
            echo "Testing popular Bangladesh proxies..."
            python3 proxy_test.py --list
            echo ""
            read -p "Enter proxy from list above (or leave blank to skip): " PROXY
            ;;
        2)
            echo ""
            read -p "Enter proxy URL (e.g., http://ip:port): " PROXY
            ;;
        3)
            echo ""
            echo "Free proxy sites:"
            echo "  • https://free-proxy-list.net"
            echo "  • https://proxy-list.download"
            echo "  • Search: 'Bangladesh proxy list'"
            echo ""
            read -p "Enter proxy URL (e.g., http://ip:port): " PROXY
            ;;
        *)
            echo "❌ Invalid option"
            exit 1
            ;;
    esac
    
    if [ ! -z "$PROXY" ]; then
        export HTTP_PROXY="$PROXY"
        export HTTPS_PROXY="$PROXY"
        USE_PROXY=1
    fi
fi

# Test proxy if set
if [ $USE_PROXY -eq 1 ]; then
    echo ""
    echo "=========================================="
    echo "🔍 Testing Proxy"
    echo "=========================================="
    echo ""
    python3 proxy_test.py
    
    if [ $? -ne 0 ]; then
        echo ""
        read -p "Proxy test failed. Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    echo "⚠️  WARNING: No proxy configured!"
    echo "   The script requires a Bangladesh proxy to work."
fi

# Ask about sources.txt
echo ""
echo "=========================================="
echo "📋 Configure Playlist Sources"
echo "=========================================="
echo ""

if [ -f "sources.txt" ] && [ -s "sources.txt" ]; then
    echo "sources.txt exists with content."
    echo ""
    echo "Current sources:"
    head -3 sources.txt
    [ $(wc -l < sources.txt) -gt 3 ] && echo "... and more"
    echo ""
    read -p "Edit sources.txt? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v nano &> /dev/null; then
            nano sources.txt
        elif command -v vi &> /dev/null; then
            vi sources.txt
        else
            echo "⚠️  Cannot open editor. Please edit sources.txt manually."
        fi
    fi
else
    echo "sources.txt is empty or doesn't exist."
    echo ""
    read -p "Add playlist sources? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v nano &> /dev/null; then
            nano sources.txt
        elif command -v vi &> /dev/null; then
            vi sources.txt
        else
            echo "⚠️  Cannot open editor. Please edit sources.txt and add M3U8 URLs (one per line)."
        fi
    fi
fi

# Ready to run
echo ""
echo "=========================================="
echo "🚀 Ready to Run"
echo "=========================================="
echo ""

if [ $USE_PROXY -eq 1 ]; then
    echo "✅ Proxy configured"
    echo "✅ Python installed"
    if [ -f "sources.txt" ] && [ -s "sources.txt" ]; then
        echo "✅ Sources configured"
        echo ""
        read -p "Run merge.py now? (y/n) " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo ""
            echo "Running merge.py..."
            echo "=========================================="
            echo ""
            
            python3 merge.py
            
            if [ $? -eq 0 ]; then
                echo ""
                echo "=========================================="
                echo "✅ Success!"
                echo ""
                echo "Output file: merged.m3u"
                echo "Channels found: $(( $(wc -l < merged.m3u) / 2 - 1 ))"
                echo "=========================================="
            else
                echo ""
                echo "❌ merge.py failed"
                exit 1
            fi
        fi
    else
        echo "⚠️  No playlist sources configured"
        echo "   Please add URLs to sources.txt"
    fi
else
    echo "⚠️  No proxy configured"
    echo "   Please set HTTP_PROXY before running merge.py"
    echo ""
    echo "Example:"
    echo "  export HTTP_PROXY='http://proxy-ip:port'"
    echo "  python3 merge.py"
fi

echo ""
echo "=========================================="
echo "📚 For more info:"
echo "   • cat README.md"
echo "   • cat SETUP_GUIDE.md"
echo "   • python3 proxy_test.py --help"
echo "=========================================="
echo ""
