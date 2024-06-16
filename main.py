# main.py
from fastapi import FastAPI, Depends, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
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
    themes = crud.get_themes(db)
    return templates.TemplateResponse("dashboard/sites.html", {"request": request, "sites": sites, "themes": themes})


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
    return templates.TemplateResponse("dashboard/theme.html", {"request": request, "themes": themes})


@app.post("/sites", response_model=schemas.Site)
async def create_site(domain: str = Form(...),
                      login: str = Form(...),
                      password: str = Form(...),
                      theme_id: int = Form(...),
                      db: Session = Depends(get_db)):
    site_create = schemas.SiteCreate(domain=domain, login=login, password=password, theme_id=theme_id)
    crud.create_site(db, site_create)
    return RedirectResponse(url="/", status_code=303)


@app.post("/posts", response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, site_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.create_post(db, post, site_id)


@app.post("/themes", response_model=schemas.Theme)
async def create_theme(name: str = Form(...),
                       name_file_to_key: str = Form(...),
                       folder_to_pict: str = Form(...),
                       db: Session = Depends(get_db)):
    theme_create = schemas.ThemeCreate(name=name, name_file_to_key=name_file_to_key, folder_to_pict=folder_to_pict)
    crud.create_theme(db, theme_create)
    return RedirectResponse(url='/themes', status_code=303)


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
    crud.delete_site(db, site_id)
    return RedirectResponse(url='/', status_code=303)


@app.post("/posts/{post_id}/delete", response_model=schemas.Post)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, post_id)


@app.post("/themes/{theme_id}/delete", response_model=schemas.Theme)
async def delete_theme(theme_id: int, db: Session = Depends(get_db)):
    crud.delete_theme(db, theme_id)
    return RedirectResponse(url='/themes', status_code=303)
