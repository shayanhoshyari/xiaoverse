from jupyter_server import serverapp

if __name__ == "__main__":
    serverapp.main(open_browser=False, token="", disable_check_xsrf=True, ip="0.0.0.0")
