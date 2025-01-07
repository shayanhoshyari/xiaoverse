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
            if not processed:
                raise ValueError("Invalid path, you want to paretn of root")
            processed.pop(-1)
            continue
        processed.append(part)

    if processed == [""]:
        return "/"

    return "/".join(processed)



def test_simplify_path() -> None:
    simplify_path("/") == "/" 
    simplify_path("/////") == "/" 
    simplify_path("/a") == "/a" 
    simplify_path("//a") == "/a" 
    simplify_path("//a/") == "/a" 
    simplify_path("//a/..") == "/" 
    simplify_path("//a/b/..") == "/a" 
    simplify_path("//a/../b") == "/b" 
    simplify_path("//a/../b/c/d/.") == "/b/c/d" 
    simplify_path("//a/../b//./././///c/d/.") == "/b/c/d" 
    simplify_path("/.....") == "/....." 

if __name__ == "__main__":
    sys.exit(pytest.main(["-vv", __file__]))
