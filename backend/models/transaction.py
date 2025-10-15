from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Transaction(Base):
    """取引ヘッダ"""
    __tablename__ = 'transactions'
    __table_args__ = {'comment': '取引ヘッダ'}

    TRD_ID = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment='取引一意キー'
    )
    DATETIME = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        comment='取引日時'
    )
    EMP_CD = Column(
        String(10),
        nullable=True,
        comment='レジ担当者コード'
    )
    STORE_CD = Column(
        String(5),
        nullable=True,
        comment='店舗コード'
    )
    POS_NO = Column(
        String(3),
        nullable=True,
        comment='POS機ID'
    )
    TOTAL_AMT = Column(
        Integer,
        nullable=True,
        comment='合計金額'
    )
    TTL_AMT_EX_TAX = Column(
        Integer,
        nullable=True,
        comment='合計金額（税抜）'
    )

    def __repr__(self):
        return f"<Transaction(TRD_ID={self.TRD_ID}, DATETIME={self.DATETIME}, TOTAL_AMT={self.TOTAL_AMT})>"

