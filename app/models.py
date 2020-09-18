from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db, Status


class User(db.Model, UserMixin):
    """
    Người dùng
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)               # ten nguoi dung
    active = Column(Boolean, default=True)
    user_name = Column(String(50), nullable=False)          # ten dang nhap
    pass_word = Column(String(50), nullable=False)          # mat khau
    roles = Column(String(50), nullable=False)   # phan quyen

    def __str__(self):
        return self.name


class KindOfRoom(db.Model):
    """
    Loại phòng
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)           # tên loại phòng
    unit_price = Column(Integer, nullable=False)        # đơn giá
    note = Column(String(50), nullable=True)            # ghi chú
    rooms = relationship('Room', backref="KindOfRoom", lazy=True)

    def __str__(self):
        return self.name


class Room(db.Model):
    """
    Phòng
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)                                       #tên phòng
    kind_of_room_id = Column(Integer, ForeignKey(KindOfRoom.id), nullable=False)    #loại phòng
    status = Column(Enum(Status), nullable=True)         #tình trạng phòng
    amount = Column(Integer, nullable=False)             # số lượng
    rent_slips = relationship('RentSlip', backref="Room", lazy=True)

    def __str__(self):
        return self.name


class CustomerType(db.Model):
    """
    Loại khách hàng
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_type_name = Column(String(50), nullable=False)
    coefficient = Column(Float, nullable=False)
    note = Column(String(50), nullable=False)
    rent_slip_details = relationship('RentSlip', backref="CustomerType", lazy=True)

    def __str__(self):
        return self.customer_type_name


class Surcharge(db.Model):
    """
        Phụ thu
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    surcharge = Column(Integer, nullable=False) #phụ thu
    amount = Column(Integer, nullable=False)    # số lượng
    rentSlip = relationship('RentSlip', backref="Surcharge", lazy=True)

    def __str__(self):
        return self.amount.__str__() + " người - " + self.surcharge.__str__() + " %"


class RentSlip(db.Model):
    """
    Phiếu thuê phòng
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    hire_start_date = Column(DateTime, nullable=False)                         # ngay bat dau thue
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)         # ma phong
    customer_name = Column(String(50), nullable=False)
    amount = Column(String(50), ForeignKey(Surcharge.id), nullable=False)                    #số lượng
    customer_type_id = Column(Integer, ForeignKey(CustomerType.id), nullable=False)  # ma loai kh
    identity_card = Column(String(50), nullable=False)  # chứng minh nhân dân
    address = Column(String(50), nullable=False)  # địa chỉ
    bill = relationship('Bill', backref="RentSlip", lazy=True)

    def __str__(self):
        return self.id.__str__()


class Bill(db.Model):
    """
    Hóa đơn thanh toán
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_of_payment = Column(Integer, nullable=False, default = 0)                      # ngày thanh toan
    value = Column(Integer, nullable=False, default = 0)                                 # trị giá
    price = Column(Integer, nullable=False, default = 0)                                 # Thành tiền
    rentSlip_id = Column(Integer, ForeignKey(RentSlip.id), nullable=False)

    def __str__(self):
        return self.customer_name


if __name__ == "__main__":
    db.create_all()
