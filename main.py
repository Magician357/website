from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import os

import uvicorn
import random

app = FastAPI()

async def getelseblank(path: str):
    # Gets a file using asyncio
    try:
        contents = await asyncio.to_thread(pathlib.Path(path).read_text)
        return contents.replace('"', r'\"').replace("'", r"\'") # Just in case a string has invalid characters
    except:
        return ""

async def renderhtml(filename: str, request: Request, customarg: str=""):
    # Takes the filename, returns a string with the rendered html
    basecss=await getelseblank("html/base.css")
    css=await getelseblank("html/"+filename+".css")
    js=await getelseblank("html/"+filename+".js")
    response=templates.TemplateResponse(filename+".html", {"request": request,"css":css,"js":js,"basecss":basecss,"extra":customarg})
    return response.body.decode()

templates = Jinja2Templates(
    directory="html",
    comment_start_string='{=',
    comment_end_string='=}',
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return await renderhtml("index",request)

@app.get("/background", response_class=HTMLResponse)
async def background(request: Request):
    return await renderhtml("background",request)

@app.get("/fakecode.txt", response_class=HTMLResponse)
async def fakecode():
    with open("html/fakecode.txt","r") as f:
      text=f.read()
    return text

@app.get("/fakecode", response_class=HTMLResponse)
async def displaycode():
  # Way to view the fake code
  with open("html/fakecode.txt","r") as f:
      text=f.read()
  return "<pre>"+text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")+"</pre>"

@app.get("/about", response_class=HTMLResponse)
async def aboutme(request: Request):
    return await renderhtml("aboutme",request)

@app.get("/aboutthis", response_class=HTMLResponse)
async def aboutme(request: Request):
    return await renderhtml("aboutthis",request)

@app.get("/files")
async def getfiles():
  # Gets all files as list
  root=os.getcwd()
  current=[]
  for path, subdirs, files in os.walk(root):
      for name in files:
          if "venv" in path or ".config" in path or "__pycache__" in path or ".cache" in path or ".git" in path or name in ["replit.nix",".replit","pyproject.toml","poetry.lock","store.json"]:
            continue
          print(os.path.join(path, name))
          current.append(os.path.join(path, name).replace("/","_"))
  return current

@app.get("/source", response_class=HTMLResponse)
async def sourcedisplay(request: Request):
    return await renderhtml('source',request,await getfiles())

@app.get("/source/{absolutepath}")
async def source(absolutepath):
    # Simply shows whatever file is there
    path=os.path.relpath(absolutepath.replace("_","/"))
    return FileResponse("./"+path)

@app.get("/icon", include_in_schema=False)
async def icon():
    return FileResponse("./html/icon/favicon.ico")

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=5050,)#reload=True