from datetime import datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


# Main Game Table (e.g., X01, Cricket)
class Game(db.Model):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    modes: Mapped[List["GameMode"]] = relationship("GameMode", back_populates="game")


# Game Mode Table (X01 has different modes: Standard, Parchessi, Hit and Run)
class GameMode(db.Model):
    __tablename__ = "game_mode"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    game_id: Mapped[int] = mapped_column(db.ForeignKey("game.id"), nullable=False)

    game: Mapped["Game"] = relationship("Game", back_populates="modes")
    rules: Mapped[List["GameRule"]] = relationship(
        "GameRule", back_populates="game_mode"
    )


# Game Rules Table (Defines start score, out rules, etc.)
class GameRule(db.Model):
    __tablename__ = "game_rule"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_mode_id: Mapped[int] = mapped_column(
        db.ForeignKey("game_mode.id"), nullable=False
    )
    rule_name: Mapped[str] = mapped_column(
        nullable=False
    )  # e.g., "start_score", "out_rule"
    rule_value: Mapped[str] = mapped_column(nullable=False)  # e.g., "501", "double_out"

    game_mode: Mapped["GameMode"] = relationship("GameMode", back_populates="rules")


# Game Session Table (Tracks active games)
class GameSession(db.Model):
    __tablename__ = "game_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_mode_id: Mapped[int] = mapped_column(
        db.ForeignKey("game_mode.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[str] = mapped_column(default="active")  # "active", "completed"

    game_mode: Mapped["GameMode"] = relationship("GameMode")


# Players Table
class Player(db.Model):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    sessions: Mapped[List["SessionPlayer"]] = relationship(
        "SessionPlayer", back_populates="player"
    )


# Session Player Table (Tracks players and scores per session)
class SessionPlayer(db.Model):
    __tablename__ = "session_player"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        db.ForeignKey("game_session.id"), nullable=False
    )
    player_id: Mapped[int] = mapped_column(db.ForeignKey("player.id"), nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    turn_order: Mapped[int] = mapped_column(nullable=False)

    player: Mapped["Player"] = relationship("Player", back_populates="sessions")
    session: Mapped["GameSession"] = relationship("GameSession")


# Turn Table (Tracks each player's turn)
class Turn(db.Model):
    __tablename__ = "turn"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        db.ForeignKey("game_session.id"), nullable=False
    )
    player_id: Mapped[int] = mapped_column(db.ForeignKey("player.id"), nullable=False)
    score_before: Mapped[int] = mapped_column(nullable=False)
    score_after: Mapped[int] = mapped_column(nullable=False)
    darts_hit: Mapped[List[dict]] = mapped_column(
        db.JSON, nullable=False
    )  # [{"score": 20, "multiplier": 2}]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
