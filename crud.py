# crud.py
from sqlalchemy.orm import Session
from models import Site, Post, Theme
from schemas import SiteCreate, PostCreate, ThemeCreate


# Sites CRUD
def get_site(db: Session, site_id: int):
    return db.query(Site).filter(Site.id == site_id).first()


def get_sites(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Site).offset(skip).limit(limit).all()


def create_site(db: Session, site: SiteCreate):
    db_site = Site(**site.dict())
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site


def delete_site(db: Session, site_id: int):
    db_site = get_site(db, site_id)
    if db_site:
        db.delete(db_site)
        db.commit()
        return db_site
    return None


def update_site(db: Session, site_id: int, site: SiteCreate):
    db_site = get_site(db, site_id)
    if db_site:
        db_site.domain = site.domain
        db_site.login = site.login
        db_site.password = site.password
        db_site.theme_id = site.theme_id
        db.commit()
        db.refresh(db_site)
        return db_site
    return None


# Posts CRUD
def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate, site_id: int):
    db_post = Post(**post.dict(), site_id=site_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
        return db_post
    return None


def update_post(db: Session, post_id: int, post: PostCreate):
    db_post = get_post(db, post_id)
    if db_post:
        db_post.domain = post.domain
        db.commit()
        db.refresh(db_post)
        return db_post
    return None


# Theme CRUD
def get_theme(db: Session, theme_id: int):
    return db.query(Theme).filter(Theme.id == theme_id).first()


def get_themes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Theme).offset(skip).limit(limit).all()


def create_theme(db: Session, theme: ThemeCreate):
    db_theme = Theme(**theme.dict())
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme


def delete_theme(db: Session, theme_id: int):
    db_theme = get_theme(db, theme_id)
    if db_theme:
        db.delete(db_theme)
        db.commit()
        return db_theme
    return None


def update_theme(db: Session, theme_id: int, theme: ThemeCreate):
    db_theme = get_theme(db, theme_id)
    if db_theme:
        db_theme.name = theme.name
        db_theme.name_file_to_key = theme.name_file_to_key
        db_theme.folder_to_pict = theme.folder_to_pict
        db.commit()
        db.refresh(db_theme)
        return db_theme
    return None
