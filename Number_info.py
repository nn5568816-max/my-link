#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
============================================
NARESH DEVELOPER - NUMBER INFORMATION
Python Flask Server for Termux & PC
============================================
"""

from flask import Flask, render_template_string, request, jsonify
import requests
import re
import os
import json

app = Flask(__name__)

# ============================================
# API CONFIGURATION
# ============================================
API_URL = "https://markplace.site/api.php"
API_KEY = "hackerkris_23a69529d622873f"  # <-- Aapki API Key yahan configured hai

# ============================================
# HTML TEMPLATE (Complete Hacker Theme UI)
# ============================================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NARESH DEVELOPER - TERMINAL ACCESS</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --term-green: #00ff41;
            --term-dark: #0d0208;
            --term-black: #000000;
            --term-glow: 0 0 10px rgba(0, 255, 65, 0.5);
            --term-red: #ff003c;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }

        input, textarea {
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
        }

        body {
            font-family: 'Share Tech Mono', monospace;
            background-color: var(--term-black);
            color: var(--term-green);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-x: hidden;
            text-transform: uppercase;
        }

        body::after {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 2;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }

        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--term-black); border-left: 1px solid var(--term-green); }
        ::-webkit-scrollbar-thumb { background: var(--term-green); }

        .disclaimer-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .disclaimer-overlay.hidden { opacity: 0; visibility: hidden; transition: all 0.5s; }
        .disclaimer-overlay.hide-permanent { display: none !important; }

        .disclaimer-box {
            background: var(--term-black);
            border: 2px solid var(--term-red);
            padding: 40px;
            max-width: 500px;
            width: 90%;
            text-align: center;
            box-shadow: 0 0 30px rgba(255, 0, 60, 0.3);
            position: relative;
        }

        .disclaimer-box h2 {
            color: var(--term-red);
            font-size: 24px;
            margin-bottom: 20px;
            text-shadow: 0 0 10px var(--term-red);
            animation: blink 1s infinite;
        }

        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

        .disclaimer-box .content {
            color: #fff;
            font-size: 14px;
            line-height: 1.8;
            margin-bottom: 30px;
        }

        .disclaimer-box .btn-accept {
            background: transparent;
            border: 2px solid var(--term-red);
            color: var(--term-red);
            padding: 12px 30px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
            text-transform: uppercase;
        }

        .disclaimer-box .btn-accept:hover {
            background: var(--term-red);
            color: var(--term-black);
            box-shadow: 0 0 15px var(--term-red);
        }

        .top-header {
            width: 100%;
            background: #001100;
            border-bottom: 1px solid var(--term-green);
            padding: 8px 0;
            position: sticky;
            top: 0;
            z-index: 999;
        }

        .top-header .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            letter-spacing: 2px;
        }

        .main-header {
            width: 100%;
            padding: 30px 0 10px;
            text-align: center;
        }

        .main-header .title-section h1 {
            font-size: 40px;
            font-weight: normal;
            letter-spacing: 4px;
            text-shadow: var(--term-glow);
            margin-bottom: 5px;
        }

        .main-header .sub-title {
            color: #888;
            font-size: 14px;
            letter-spacing: 5px;
        }

        .main-container {
            max-width: 650px;
            width: 100%;
            padding: 20px;
            margin: 20px 0;
        }

        .card {
            background: rgba(0, 15, 0, 0.8);
            border: 1px solid var(--term-green);
            box-shadow: var(--term-glow);
            position: relative;
        }

        .card::before {
            content: "[ ROOT_TERMINAL ] - /usr/bin/intel_gather";
            display: block;
            background: var(--term-green);
            color: var(--term-black);
            padding: 5px 15px;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .card-body { padding: 30px; }
        .form-group { margin-bottom: 25px; }

        .form-label {
            display: block;
            font-size: 14px;
            margin-bottom: 10px;
        }

        .input-group {
            display: flex;
            align-items: center;
            background: var(--term-black);
            border: 1px solid var(--term-green);
            position: relative;
        }

        .input-group::before {
            content: ">";
            color: var(--term-green);
            padding-left: 15px;
            font-size: 18px;
            animation: blink 1s infinite;
        }

        .input-group input {
            flex: 1;
            padding: 15px;
            background: transparent;
            border: none;
            color: var(--term-green);
            font-size: 18px;
            font-family: 'Share Tech Mono', monospace;
            outline: none;
            letter-spacing: 3px;
        }

        .input-group input::placeholder {
            color: rgba(0, 255, 65, 0.3);
        }

        .status-bar {
            font-size: 12px;
            margin-bottom: 15px;
            color: #888;
        }
        .status-bar span { color: var(--term-green); }

        .btn-search {
            width: 100%;
            padding: 15px;
            background: transparent;
            border: 1px solid var(--term-green);
            color: var(--term-green);
            font-size: 18px;
            font-family: 'Share Tech Mono', monospace;
            cursor: pointer;
            letter-spacing: 3px;
            transition: 0.2s;
            text-transform: uppercase;
        }

        .btn-search:hover:not(:disabled) {
            background: var(--term-green);
            color: var(--term-black);
            box-shadow: var(--term-glow);
        }

        .btn-search:disabled {
            border-color: #555;
            color: #555;
            cursor: not-allowed;
        }

        .result-box {
            margin-top: 30px;
            border: 1px dashed var(--term-green);
            background: #000;
            display: none;
            padding: 1px;
        }

        .result-box.show { display: block; }

        .result-header {
            background: rgba(0, 255, 65, 0.1);
            padding: 10px;
            border-bottom: 1px dashed var(--term-green);
            display: flex;
            justify-content: space-between;
            font-size: 12px;
        }

        .result-item {
            display: flex;
            padding: 12px 15px;
            border-bottom: 1px solid rgba(0, 255, 65, 0.2);
            word-break: break-all;
        }
        
        .result-item:last-child { border-bottom: none; }

        .result-item .label {
            color: #888;
            width: 35%;
        }

        .result-item .label::before { content: "[+] "; color: var(--term-green); }

        .result-item .value {
            color: #fff;
            width: 65%;
            text-shadow: 0 0 5px rgba(255,255,255,0.5);
        }

        .social-section {
            margin-top: 30px;
            text-align: center;
            border: 1px solid rgba(0, 255, 65, 0.3);
            padding: 15px;
        }

        .social-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 10px;
        }

        .social-btn {
            color: var(--term-green);
            text-decoration: none;
            font-size: 12px;
            border: 1px solid var(--term-green);
            padding: 5px 15px;
            transition: 0.3s;
        }

        .social-btn:hover {
            background: var(--term-green);
            color: var(--term-black);
        }

        .footer-section {
            margin-top: auto;
            width: 100%;
            text-align: center;
            padding: 20px;
            border-top: 1px solid var(--term-green);
            font-size: 12px;
            color: #555;
            background: #000;
        }

        .error-text { color: var(--term-red); font-size: 12px; display: none; padding-bottom: 10px; text-shadow: 0 0 5px var(--term-red); }
        .error-text.show { display: block; }

        .json-toggle {
            margin-top: 20px;
            padding: 10px;
            background: transparent;
            border: 1px dashed #555;
            color: #888;
            width: 100%;
            cursor: pointer;
            font-family: 'Share Tech Mono', monospace;
        }
        .json-toggle:hover { border-color: var(--term-green); color: var(--term-green); }

        .json-box {
            margin-top: 10px;
            background: #000;
            padding: 15px;
            font-size: 11px;
            color: #00ff41;
            display: none;
            border: 1px solid var(--term-green);
            max-height: 250px;
            overflow: auto;
        }
        .json-box.show { display: block; }
    </style>
</head>

<body>

    <div class="disclaimer-overlay" id="disclaimerOverlay">
        <div class="disclaimer-box">
            <h2>WELCOME</h2>
            <div class="content">
                UNAUTHORIZED ACCESS DETECTED.<br>
                THIS TOOL IS CONFIGURED FOR <strong>EDUCATIONAL & OSINT</strong> PURPOSES ONLY.<br><br>
                DEVELOPED BY NARESH
            </div>
            <button class="btn-accept" onclick="acceptDisclaimer()">[ INITIATE CONNECTION ]</button>
        </div>
    </div>

    <div class="top-header">
        <div class="container">
            <div><i class="fas fa-terminal"></i> NARESH_DEVELOPER // SECURE_NODE</div>
            <div>STATUS: <span style="color:#00ff41;">CONNECTED</span></div>
        </div>
    </div>

    <div class="main-header">
        <div class="title-section">
            <h1>NARESH<span style="color:#fff;">_DEV</span></h1>
            <div class="sub-title">== INTEL GATHERING SUBSYSTEM ==</div>
        </div>
    </div>

    <div class="main-container">
        <div class="card">
            <div class="card-body">
                <form id="trackForm">
                    <div class="form-group">
                        <label class="form-label">ENTER TARGET NUMBER [10 DIGITS]:</label>
                        <div class="input-group">
                            <input type="tel" id="phoneInput" placeholder="TARGET_NUMBER" maxlength="10" inputmode="numeric">
                        </div>
                    </div>

                    <div class="status-bar">
                        SYS_MSG: <span id="statusText">AWAITING INPUT...</span>
                    </div>

                    <div class="error-text" id="errorText">ERR: FATAL EXCEPTION</div>

                    <button type="submit" class="btn-search" id="trackBtn">
                        <i class="fas fa-satellite-dish"></i> EXECUTE TRACE
                    </button>
                </form>

                <div class="result-box" id="resultBox">
                    <div class="result-header">
                        <div><i class="fas fa-database"></i> DUMP_SUCCESS</div>
                        <div>RECORDS: <span id="recordCount">0</span></div>
                    </div>
                    <div id="resultContent"></div>
                </div>

                <div class="social-section">
                    <div style="font-size:12px; color:#888; margin-bottom:10px;">// SECURE COMMS CHANNELS //</div>
                    <div class="social-buttons">
                        <a href="https://youtube.com/shorts/_uR_pBqeEt4?si=YF0mMI45kgmabFTt" target="_blank" class="social-btn"><i class="fab fa-youtube"></i> YT_LINK</a>
                        <a href="https://instagram.com/krish_ah_420" target="_blank" class="social-btn"><i class="fab fa-instagram"></i> INSTA_NODE</a>
                        <a href="https://t.me/krish_ah_420" target="_blank" class="social-btn"><i class="fab fa-telegram-plane"></i> TELE_NET</a>
                    </div>
                </div>

                <button class="json-toggle" onclick="toggleJson()">[ VIEW_RAW_JSON_DUMP ]</button>
                <div class="json-box" id="jsonBox"></div>
            </div>
        </div>
    </div>

    <div class="footer-section">
        (C) 2026 NARESH DEVELOPER - END OF TRANSMISSION
    </div>

    <script>
        (function () {
            if (sessionStorage.getItem('disclaimerShown') === 'true') {
                document.getElementById('disclaimerOverlay').classList.add('hide-permanent');
            }
        })();

        function acceptDisclaimer() {
            sessionStorage.setItem('disclaimerShown', 'true');
            document.getElementById('disclaimerOverlay').classList.add('hidden');
            setTimeout(function () {
                document.getElementById('disclaimerOverlay').classList.add('hide-permanent');
            }, 500);
        }

        function toggleJson() {
            const box = document.getElementById('jsonBox');
            box.classList.toggle('show');
        }

        async function callAPI(number) {
            try {
                const response = await fetch('/api/lookup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ number: number })
                });
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return await response.json();
            } catch (error) {
                return { status: 'error', message: error.message };
            }
        }

        function displayResults(number, responseData) {
            const resultBox = document.getElementById('resultBox');
            const resultContent = document.getElementById('resultContent');
            const recordCount = document.getElementById('recordCount');
            const errorText = document.getElementById('errorText');

            document.getElementById('jsonBox').textContent = JSON.stringify(responseData, null, 2);

            if (responseData.status === 'error') {
                resultBox.classList.remove('show');
                errorText.textContent = 'ERR: ' + (responseData.message || 'TARGET NOT FOUND IN DATABASE.');
                errorText.classList.add('show');
                return;
            }

            let rawData = responseData.data;

            // Handle nested formats dynamically
            let itemData = null;
            if (Array.isArray(rawData) && rawData.length > 0) {
                itemData = rawData[0];
                recordCount.textContent = rawData.length;
            } else if (rawData && typeof rawData === 'object') {
                if (Array.isArray(rawData.result) && rawData.result.length > 0) {
                    itemData = rawData.result[0];
                    recordCount.textContent = rawData.result.length;
                } else {
                    itemData = rawData;
                    recordCount.textContent = '1';
                }
            }

            if (!itemData) {
                resultBox.classList.remove('show');
                errorText.textContent = 'ERR_404: NO RECORD DATA FOUND.';
                errorText.classList.add('show');
                return;
            }

            let html = '';
            for (const [key, val] of Object.entries(itemData)) {
                if (typeof val !== 'object' && val !== null && key !== 'status') {
                    html += `
                        <div class="result-item">
                            <span class="label">${key.toUpperCase()}</span>
                            <span class="value">${val}</span>
                        </div>
                    `;
                }
            }

            resultContent.innerHTML = html || '<div class="result-item"><span class="label">INFO</span><span class="value">NO FIELD DATA</span></div>';
            resultBox.classList.add('show');
            errorText.classList.remove('show');
        }

        async function searchNumber() {
            const input = document.getElementById('phoneInput');
            const number = input.value.trim();
            const trackBtn = document.getElementById('trackBtn');
            const errorText = document.getElementById('errorText');
            const statusText = document.getElementById('statusText');

            if (!/^[0-9]{10}$/.test(number)) {
                errorText.textContent = 'SYS_WARN: INVALID 10-DIGIT NUMBER FORMAT.';
                errorText.classList.add('show');
                return;
            }
            errorText.classList.remove('show');
            trackBtn.disabled = true;
            trackBtn.innerHTML = 'ESTABLISHING CONNECTION...';
            statusText.textContent = 'FETCHING DATA FROM SERVER...';

            const data = await callAPI(number);
            displayResults(number, data);
            trackBtn.disabled = false;
            trackBtn.innerHTML = '<i class="fas fa-satellite-dish"></i> EXECUTE TRACE';
            statusText.textContent = 'TRACE COMPLETED.';
        }

        document.getElementById('trackForm').addEventListener('submit', e => { e.preventDefault(); searchNumber(); });
        document.getElementById('phoneInput').addEventListener('input', function () { this.value = this.value.replace(/[^0-9]/g, ''); });
    </script>
</body>
</html>
'''

# ============================================
# FLASK ROUTE: HOME PAGE
# ============================================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# ============================================
# FLASK ROUTE: API LOOKUP (PROXY)
# ============================================
@app.route('/api/lookup', methods=['POST'])
def lookup():
    try:
        data = request.get_json()
        number = data.get('number', '').strip()
        
        if not number:
            return jsonify({"status": "error", "message": "Phone number required"})
        
        clean_number = re.sub(r'[\+\s\-]', '', number)
        
        # Build API Parameters
        params = {
            'key': API_KEY,
            'type': 'number',
            'num': clean_number
        }
        
        # Custom Browser User-Agent Header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }
        
        # Call External API
        response = requests.get(API_URL, params=params, headers=headers, timeout=25, verify=False)
        
        if response.status_code != 200:
            return jsonify({"status": "error", "message": f"Server Status Error Code: {response.status_code}"})
        
        try:
            api_data = response.json()
        except Exception:
            # Fallback if API returns string response
            return jsonify({"status": "success", "data": {"raw_response": response.text}})
        
        return jsonify({
            "status": "success",
            "data": api_data
        })
        
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "API Connection Timeout"})
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"API Request Error: {str(e)}"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"})

# ============================================
# MAIN SERVER LAUNCHER
# ============================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*50)
    print("🛡️   NARESH DEVELOPER - NUMBER INFORMATION")
    print("="*50)
    print(f"✅ Server running on: http://127.0.0.1:{port}")
    print(f"📱 Open in browser: http://127.0.0.1:{port}")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
