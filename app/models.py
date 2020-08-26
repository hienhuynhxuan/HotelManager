from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)           # tên loại phòng
    unit_price = Column(Integer, nullable=False)        # đơn giá
    note = Column(String(50), nullable=True)            # ghi chú
    rooms = relationship('Room', backref="KindOfRoom", lazy=True)

    def __str__(self):
        return self.name


class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)                                       #tên phòng
    kind_of_room_id = Column(Integer, ForeignKey(KindOfRoom.id), nullable=False)    #loại phòng
    status = Column(Boolean, nullable=False)                                        #tình trạng phòng
    rent_slips = relationship('RentSlip', backref="Room", lazy=True)
    bill_details = relationship('BillDetail', backref="Room", lazy=True)

    def __str__(self):
        return self.name


class RentSlip(db.Model):             # phieu thue
    id = Column(Integer, primary_key=True, autoincrement=True)
    hire_start_date = Column(Date, nullable=False)                                              # ngay bat dau thue
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)              # ma phong
    rent_slip_details = relationship('RentSlipDetail', backref="RentSlip", lazy=True)

    def __str__(self):
        return self.hire_start_date.__str__()


class CustomerType(db.Model):           # loai kh
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_type_name = Column(String(50), nullable=False)
    rent_slip_details = relationship('RentSlipDetail', backref="CustomerType", lazy=True)

    def __str__(self):
        return self.customer_type_name


class RentSlipDetail(db.Model):       # chi tiet phieu thue
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(50), nullable=False)
    customer_type_id = Column(Integer, ForeignKey(CustomerType.id), nullable=False)      # ma loai kh
    identity_card = Column(String(50), nullable=False)      #chứng minh nhân dân
    address = Column(String(50), nullable=False)  # địa chỉ
    rent_slip_id = Column(Integer, ForeignKey(RentSlip.id), nullable=False)

    def __str__(self):
        return self.customer_name


class Bill(db.Model):           #hóa đơn thanh toán
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)                                # địa chỉ
    date_of_payment = Column(Date, nullable=False)                              # ngày thanh toan
    value = Column(Integer, nullable=False)                                     # trị giá
    bill_details = relationship('BillDetail', backref="Bill", lazy=True)

    def __str__(self):
        return self.customer_name


class BillDetail(db.Model):           # chi tiet hóa đơn thanh toán
    id = Column(Integer, primary_key=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey(Bill.id), nullable=False)              # ma hoa don
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)              # ma phong
    address = Column(String(50), nullable=False)                                # địa chỉ
    number_of_rental_days = Column(Date, nullable=False)                        # số ngày thuê
    unit_price = Column(Integer, nullable=False)                                # đơn giá
    into_money = Column(Integer, nullable=False)                                # thành tiền


class AdditionalParameters(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    maximum_of_guests = Column(Integer, nullable=False)     # so luong khach toi da
    coefficient = Column(Integer, nullable=False)           # he so khach nuoc ngoai
    surcharge = Column(Integer, nullable=False)             # phu thu


if __name__ == "__main__":
    db.create_all()




# class Customer(db.Model):
#     _tablename__ = "customer"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)               #tên kh
#     address = Column(String(50), nullable=False)            #địa chỉ
#     identity_card = Column(String(50), nullable=False)      #chứng minh nhân dân
#     customer_type = Column(String(50), nullable=False)      #loại kh
#     #date       #ngày sinh
#     #phone      #số điện thoại
#     #passport   #Số hộ chiếu
#     #node       #ghi chú

