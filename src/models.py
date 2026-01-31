from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


follower_table = Table(
    "follower",
    db.Model.metadata,
    Column("follower_id", ForeignKey("user.id"), primary_key=True),
    Column("followed_id", ForeignKey("user.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")

    following: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin=id == follower_table.c.follower_id,
        secondaryjoin=id == follower_table.c.followed_id,
        back_populates="followers"
    )

    followers: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin=id == follower_table.c.followed_id,
        secondaryjoin=id == follower_table.c.follower_id,
        back_populates="following"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    caption: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    media: Mapped[list["Media"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "caption": self.caption,
            "image": self.image,
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    comment_text: Mapped[str] = mapped_column(nullable=False)
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "post_id": self.post_id,
            "comment_text": self.comment_text,
        }

class MediaType(db.Model):
    __tablename__ = "mediatype"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    media: Mapped[list["Media"]] = relationship(back_populates="media_type")

class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    media_type_id: Mapped[int] = mapped_column(ForeignKey("mediatype.id"))
    url: Mapped[str] = mapped_column(nullable=False)
    post: Mapped["Post"] = relationship(back_populates="media")
    media_type: Mapped["MediaType"] = relationship(back_populates="media")