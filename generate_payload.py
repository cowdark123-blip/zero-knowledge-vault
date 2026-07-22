import http.server
import socketserver
import threading
import subprocess
import json
import time
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

PORT = 8889
base_dir = r"C:\Users\xuanhoang\.gemini\antigravity\scratch\zero-knowledge-vault"
os.chdir(base_dir)

saved_payload = None

class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        global saved_payload
        if self.path == '/save-encrypted-payload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            saved_payload = json.loads(post_data.decode('utf-8'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))

httpd = socketserver.TCPServer(("127.0.0.1", PORT), TestHandler)
server_thread = threading.Thread(target=httpd.serve_forever)
server_thread.daemon = True
server_thread.start()

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [edge_path, "--headless=new", "--disable-gpu", f"http://127.0.0.1:8889/encrypt_browser.html"]
subprocess.Popen(cmd)

print("Running Web Crypto API encryption in Edge headless...")
for i in range(15):
    if saved_payload:
        out_file = os.path.join(base_dir, "zk_vault_encrypted_42_accounts.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(saved_payload, f, ensure_ascii=False, indent=2)
        print(f"SUCCESS! Pre-encrypted ZK Backup file saved to {out_file}")
        httpd.shutdown()
        sys.exit(0)
    time.sleep(1)

print("FAILED to encrypt in time.")
httpd.shutdown()
sys.exit(1)
