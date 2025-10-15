from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class TransactionDetail(Base):
    """取引明細"""
    __tablename__ = 'transaction_details'
    __table_args__ = {'comment': '取引明細'}

    TRD_ID = Column(
        Integer,
        ForeignKey('transactions.TRD_ID', ondelete='NO ACTION', onupdate='NO ACTION'),
        primary_key=True,
        comment='取引一意キー'
    )
    DTL_ID = Column(
        Integer,
        primary_key=True,
        comment='取引明細一意キー'
    )
    PRD_ID = Column(
        Integer,
        ForeignKey('product_master.PRD_ID', ondelete='NO ACTION', onupdate='NO ACTION'),
        nullable=False,
        index=True,
        comment='商品一意キー'
    )
    PRD_CODE = Column(
        String(13),
        nullable=False,
        comment='商品コード'
    )
    PRD_NAME = Column(
        String(50),
        nullable=False,
        comment='商品名称'
    )
    PRD_PRICE = Column(
        Integer,
        nullable=False,
        comment='商品単価'
    )
    TAX_CD = Column(
        String(2),
        nullable=True,
        comment='消費税区分'
    )

    def __repr__(self):
        return f"<TransactionDetail(TRD_ID={self.TRD_ID}, DTL_ID={self.DTL_ID}, PRD_NAME={self.PRD_NAME})>"

