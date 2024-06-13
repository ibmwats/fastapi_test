# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True)  # без https, только домен domain.com
    login = Column(String, index=True)
    password = Column(String, index=True)
    theme_id = Column(Integer, ForeignKey('themes.id'), nullable=False)

    posts = relationship("Post", back_populates="site")
    theme = relationship("Theme", back_populates="sites")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('sites.id'))
    domain = Column(String, index=True)
    date_post = Column(DateTime(timezone=True), server_default=func.now())

    site = relationship("Site", back_populates="posts")


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    name_file_to_key = Column(String, index=True)  # В каком файле у нас будут ключи для постинга
    folder_to_pict = Column(String, index=True)  # Название папки с картинками под посты (картинки рандомные)

    sites = relationship("Site", back_populates="theme")
