"""数据库模块"""
import time

from sqlalchemy import(
    Boolean,
    Column,
    Float,
    Integer,
    orm,
    create_engine,
)

from sqlalchemy.orm import sessionmaker

DATA_PATH = "data/game"

engine = create_engine(f"sqlite:///{DATA_PATH}/game.db")
session = sessionmaker(engine)
Base = orm.declarative_base()

class UserData(Base):

    """用户数据表
        id: 排行
        userid: 用户qid
        integral: 积分数
        *_frequency: 当日使用频率
        sign_time: 签到时间
    """

    __tablename__: str = "userdata"

    id = Column(Integer,primary_key=True)
    userid = Column(Integer, nullable=False, index=True)
    integral = Column(Integer, nullable=False, default=0)
    fish_frequency = Column(Integer, nullable=False)
    sign_time = Column(Float, nullable=False)

class GroupData(Base):

    """群数据表
        groupid: 群id
        *_state: 是否允许
    """

    __tablename__:str = "groupdata"

    groupid = Column(Integer, primary_key=True, index=True)
    game_state = Column(Boolean, nullable=False, default=True)
    sign_state = Column(Boolean, nullable=False, default=True)
    

class backpack(Base):

    """背包
        userid: 用户qid
        crucian: 鲫鱼
        squid: 鱿鱼
        dolphin:海豚
        shark: 鲨鱼
        mantis: 皮皮虾
        crab: 螃蟹
        puffer: 河豚
        shell: 贝壳
        pearl: 珍珠
        box: 箱子
    """

    __tablename__:str = "backpack"

    userid = Column(Integer, primary_key=True, index=True)
    crucian = Column(Integer, nullable=False)
    squid = Column(Integer, nullable=False)
    dolphin = Column(Integer, nullable=False)
    shark = Column(Integer, nullable=False)
    mantis = Column(Integer, nullable=False)
    crab = Column(Integer, nullable=False)
    puffer = Column(Integer, nullable=False)
    shell = Column(Integer, nullable=False)
    pearl = Column(Integer, nullable=False)
    box = Column(Integer, nullable=False)
    
Base.metadata.create_all(engine)


def check_group_allow(groupid: int) -> bool:
    """检查群签到是否允许, 传入群号, 类型是int"""
    with session() as s:
        if s.query(GroupData).filter(GroupData.groupid == groupid).first():
            return s.query(GroupData).filter(GroupData.groupid == groupid).first().sign_state  # type: ignore
        else:
            return False

def is_in_table(userid: int) -> bool:
    """传入一个userid，判断是否在表中"""
    with session() as s:
        return bool(s.query(UserData).filter(UserData.userid == userid).first())

def get_today() -> str:
    """获取当前年月日格式: 1970-01-01"""
    return time.strftime("%Y-%m-%d", time.localtime())

def insert_sign():
    """插入签到积分"""