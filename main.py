# main.py
from fastapi import FastAPI, Depends, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_sites(request: Request, db: Session = Depends(get_db)):
    sites = crud.get_sites(db)
    return templates.TemplateResponse("index.html", {"request": request, "sites": sites})


@app.get("/add-sites", response_class=HTMLResponse)
async def add_sites(request: Request, db: Session = Depends(get_db)):
    themes = crud.get_themes(db)
    return templates.TemplateResponse("add_site_custom.html", {"request": request, "themes": themes})


@app.get("/sites/{site_id}", response_class=HTMLResponse)
async def read_site(request: Request, site_id: int, db: Session = Depends(get_db)):
    site = crud.get_site(db, site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return templates.TemplateResponse("site_detail.html", {"request": request, "site": site})


@app.get("/posts/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post_detail.html", {"request": request, "post": post})


@app.get("/themes", response_class=HTMLResponse)
async def read_themes(request: Request, db: Session = Depends(get_db)):
    themes = crud.get_themes(db)
    return templates.TemplateResponse("theme_list.html", {"request": request, "themes": themes})


@app.get("/add-themes", response_class=HTMLResponse)
async def add_themes(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("add_themes.html", {"request": request})


@app.post("/sites", response_model=schemas.Site)
async def create_site(site: schemas.SiteCreate, db: Session = Depends(get_db)):
    return crud.create_site(db, site)


@app.post("/posts", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, site_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.create_post(db, post, site_id)


@app.post("/themes", response_model=schemas.Theme)
async def create_theme(theme: schemas.ThemeCreate, db: Session = Depends(get_db)):
    return crud.create_theme(db, theme)


@app.post("/sites/{site_id}", response_model=schemas.Site)
async def update_site(site_id: int, site: schemas.SiteCreate, db: Session = Depends(get_db)):
    return crud.update_site(db, site_id, site)


@app.post("/posts/{post_id}", response_model=schemas.Post)
async def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.update_post(db, post_id, post)


@app.post("/themes/{theme_id}", response_model=schemas.Theme)
async def update_theme(theme_id: int, theme: schemas.ThemeCreate, db: Session = Depends(get_db)):
    return crud.update_theme(db, theme_id, theme)


@app.post("/sites/{site_id}/delete", response_model=schemas.Site)
async def delete_site(site_id: int, db: Session = Depends(get_db)):
    return crud.delete_site(db, site_id)


@app.post("/posts/{post_id}/delete", response_model=schemas.Post)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, post_id)


@app.post("/themes/{theme_id}/delete", response_model=schemas.Theme)
async def delete_theme(theme_id: int, db: Session = Depends(get_db)):
    return crud.delete_theme(db, theme_id)
