from jupyter_server import serverapp
# import sys
# from pathlib import Path

if __name__ == "__main__":
    # This is dirtying the output, which might have some unwanted side-effect
    # but is needed for vscode intellisense to work
    # python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    # lib =  Path(sys.executable).parents[1] / f"lib/{python_version}"
    # pylance_cue = lib / "site-packages/pylance-cue.txt"

    # site = lib / "site.py"
    # content = site.read_text()
    # site.unlink()
    # site.write_text(content)

    # sys_path = [path for path in sys.path if path] # remove ""
    # pylance_cue.write_text("\n".join(sys_path))

    # print("Python is", sys.executable)
    # print("Wrote pylance cue to", pylance_cue)

    serverapp.main(open_browser=False, token="", disable_check_xsrf=True)
