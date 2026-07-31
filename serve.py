#!/usr/bin/env python3
"""本地启动脚本：在 http://localhost:5173 提供售票大屏网页版。

用法:
    python3 serve.py            # 默认端口 5173
    python3 serve.py 8080      # 指定端口
"""
import sys, http.server, socketserver, os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5173
root = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=root, **k)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"售票大屏已启动 →  http://localhost:{PORT}")
        print("按 Ctrl+C 停止")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")
