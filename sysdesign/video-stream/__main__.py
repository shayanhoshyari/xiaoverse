import contextlib
from pathlib import Path

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

SAMPLE_VIDEO = Path.cwd() / "video.mp4"


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    if not SAMPLE_VIDEO.exists():
        response = requests.get("https://download.samplelib.com/mp4/sample-5s.mp4")
        assert response.ok
        SAMPLE_VIDEO.write_bytes(response.content)
    yield


app = FastAPI(lifespan=lifespan)


def get_byte_range(range_header: str, file_size: int) -> tuple[int, int]:
    units, _, range_spec = range_header.partition("=")
    if units != "bytes":
        raise HTTPException(status_code=416, detail="Invalid range unit")

    start_str, _, end_str = range_spec.partition("-")
    start = int(start_str) if start_str else 0
    end = int(end_str) if end_str else file_size - 1
    end = min(end, file_size - 1)

    if start > end or start >= file_size:
        raise HTTPException(status_code=416, detail="Range not satisfiable")

    return start, end


@app.get("/video")
async def stream_video(request: Request):
    file_size = SAMPLE_VIDEO.stat().st_size
    range_header = request.headers.get("range")
    print(f"Range is {range_header}")

    start, end = 0, file_size - 1
    if range_header:
        start, end = get_byte_range(range_header, file_size)

    chunk_size = end - start + 1

    def iter_file():
        with SAMPLE_VIDEO.open("rb") as f:
            f.seek(start)
            remaining = chunk_size
            while remaining > 0:
                chunk = f.read(min(4096, remaining))
                if not chunk:
                    break
                yield chunk
                remaining -= len(chunk)

    headers = {
        "Content-Type": "video/mp4",
        "Accept-Ranges": "bytes",
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Content-Length": str(chunk_size),
    }

    status_code = 206 if range_header else 200
    return StreamingResponse(iter_file(), status_code=status_code, headers=headers)


static_files = Path(__file__).with_name("static")

app.mount("/", StaticFiles(directory=static_files, html=True, follow_symlink=True))


if __name__ == "__main__":
    uvicorn.run(app)
