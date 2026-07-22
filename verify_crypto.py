import http.server
import socketserver
import subprocess
import threading
import sys
import json
import time
import os

# Set UTF-8 encoding for stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

PORT = 8888
TEST_RESULTS = None

class TestResultHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        global TEST_RESULTS
        if self.path == '/test-result':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            TEST_RESULTS = json.loads(post_data.decode('utf-8'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        return

def run_server(httpd):
    httpd.serve_forever()

def main():
    global TEST_RESULTS
    os.chdir(r"C:\Users\xuanhoang\.gemini\antigravity\scratch\zero-knowledge-vault")
    
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), TestResultHandler)
    server_thread = threading.Thread(target=run_server, args=(httpd,))
    server_thread.daemon = True
    server_thread.start()
    
    print(f"Server started on http://127.0.0.1:{PORT}")
    
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    url = f"http://127.0.0.1:{PORT}/test_crypto.html"
    
    edge_cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        url
    ]
    
    print("Launching Edge headless browser to run Crypto Engine test suite...")
    proc = subprocess.Popen(edge_cmd)
    
    start_time = time.time()
    while TEST_RESULTS is None:
        if time.time() - start_time > 15:
            print("ERROR: Test timed out after 15 seconds!")
            proc.kill()
            httpd.shutdown()
            sys.exit(1)
        time.sleep(0.2)
    
    proc.kill()
    httpd.shutdown()
    
    print("\n==================================================")
    print("      ZERO-KNOWLEDGE CRYPTO TEST REPORT           ")
    print("==================================================\n")
    
    all_passed = TEST_RESULTS.get("allPassed", False)
    for test in TEST_RESULTS.get("tests", []):
        status = "[PASS]" if test["pass"] else "[FAIL]"
        print(f"{status} {test['name']}")
        print(f"Details:\n{test['details']}\n")
        print("-" * 50)
    
    if all_passed:
        print("\nALL CRYPTO ENGINE VERIFICATION TESTS PASSED SUCCESSFULLY! [OK]")
        sys.exit(0)
    else:
        print("\nSOME TESTS FAILED! [ERROR]")
        sys.exit(1)

if __name__ == "__main__":
    main()
