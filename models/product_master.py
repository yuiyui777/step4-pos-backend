from sqlalchemy import Column, Integer, String
from database import Base


class ProductMaster(Base):
    """商品マスタ"""
    __tablename__ = 'product_master'
    __table_args__ = {'comment': '商品マスタ'}

    PRD_ID = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment='商品一意キー'
    )
    CODE = Column(
        String(25),
        nullable=False,
        unique=True,
        index=True,
        comment='商品コード(バーコード)'
    )
    NAME = Column(
        String(50),
        nullable=False,
        comment='商品名称'
    )
    PRICE = Column(
        Integer,
        nullable=False,
        comment='商品単価'
    )

    def __repr__(self):
        return f"<ProductMaster(PRD_ID={self.PRD_ID}, CODE={self.CODE}, NAME={self.NAME}, PRICE={self.PRICE})>"

