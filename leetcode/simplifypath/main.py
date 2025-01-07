# https://leetcode.com/problems/simplify-path

import pytest
import sys

SELF = "."

def simplify_path(path: str) -> str:
    assert path.startswith("/")
    parts = path.split("/")

    processed = [""]
    for part in parts[1:]:
        if part == "":
            # consecutive slash
            continue
        if part == ".":
            # this folder
            continue
        if part == "..":
            if len(processed) > 1:
                processed.pop(-1)
            continue
        processed.append(part)

    if processed == [""]:
        return "/"

    return "/".join(processed)



def test_simplify_path() -> None:
    assert simplify_path("/") == "/" 
    assert simplify_path("/////") == "/" 
    assert simplify_path("/a") == "/a" 
    assert simplify_path("//a") == "/a" 
    assert simplify_path("//a/") == "/a" 
    assert simplify_path("//a/..") == "/" 
    assert simplify_path("//a/b/..") == "/a" 
    assert simplify_path("//a/../b") == "/b" 
    assert simplify_path("//a/../b/c/d/.") == "/b/c/d" 
    assert simplify_path("//a/../b//./././///c/d/.") == "/b/c/d" 
    assert simplify_path("/.....") == "/....."
    assert simplify_path("/./././././") == "/"
    assert simplify_path("/../") == "/"

if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
