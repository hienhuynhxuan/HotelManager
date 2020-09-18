from urllib import request

from wtforms import validators
from app import admin, db, dao
from flask import redirect, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user
from app.models import *
from datetime import datetime
import hashlib


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class AboutUsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


class UserModelView(AuthenticatedView):
    column_display_pk = True
    column_labels = dict(name="Tên người dùng", active="Kích hoạt"
                         , user_name="Tên đăng nhập", pass_word="Mật khẩu", roles="Vai trò")

    def on_model_change(self, form, User, is_created=False):
        User.pass_word = hashlib.md5(User.pass_word.encode('utf-8')).hexdigest()

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.roles == "admin")


class KindOfRoomModelView(AuthenticatedView):
    column_display_pk = True
    form_columns = ('name', 'unit_price', 'note')
    column_labels = {"id": "Mã LP", "name": "Loại phòng", "unit_price": "Đơn giá", "note": "Ghi chú"}

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.roles == "admin")

    # (current_user.roles == "abc" or current_user.roles == "ad"


class CustomerTypeModelView(AuthenticatedView):
    column_display_pk = True
    form_columns = ('customer_type_name', 'coefficient', 'note')
    column_labels = {"id": "Mã LK", "customer_type_name": "Loại khách", "coefficient": "Hệ số", "note": "Ghi chú"}

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.roles == "admin")


class RoomModelView(AuthenticatedView):
    column_display_pk = True
    form_columns = ('name', 'KindOfRoom', 'status', 'amount')
    column_labels = {"id": "Mã phòng", "name": "Phòng", "KindOfRoom": "Loại phòng", "status": "Trạng thái", "amount": "Số lượng"}

    def _status_formatter(view, context, model, name):
        if model.status:
            status = model.status.value
            return status
        else:
            return None

    column_formatters = {
        'status': _status_formatter
    }


class SurchargeModelView(AuthenticatedView):
    column_display_pk = True
    column_list = ["amount", "surcharge"]
    column_labels = {"amount": "Số lượng", "surcharge": "Phụ thu (%)"}
    form_excluded_columns = ['rentSlip']

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.roles == "admin")


class RentSlipModelView(AuthenticatedView):
    column_display_pk = True
    column_labels = {"id": "Mã PT", "Room": "Phòng", "hire_start_date": "Ngày bắt đầu thuê",
                     "customer_name": "Khách hàng", "Surcharge": "Số lượng và phụ thu", "CustomerType": "Loại khách",
                     "identity_card": "CMND", "address": "Địa chỉ"}
    form_excluded_columns = ['bill']

    def on_model_change(self, form, RentSlip, is_created):
        room = Room.query.get(form.Room.data.id)
        if form.Room.data.status == Status.OutOfRoom:
            raise validators.ValidationError("Phòng đã có người đặt")
        else:
            room.status = Status.OutOfRoom
            db.session.add(room)
            db.session.commit()


class BillModelView(AuthenticatedView):
    column_display_pk = True
    column_labels = {"id": "Mã hóa đơn", "date_of_payment": "Số ngày thuê", "value": "Trị giá", "price": "Thành tiền",
                     "RentSlip": "Mã phiếu thuê"}
    form_excluded_columns = ['date_of_payment', 'value', 'price']

    def on_model_change(self, form, Bill, is_created):
        room = Room.query.get(form.RentSlip.data.room_id)
        if form.RentSlip.data.Room.status == Status.OutOfRoom:
            room.status = Status.ThereIsRoom
            db.session.add(room)
            db.session.commit()

        if (datetime.now() - form.RentSlip.data.hire_start_date).days == 0:
            billOfPay = (datetime.now().hour - form.RentSlip.data.hire_start_date.hour)
        else:
            billOfPay = (datetime.now() - form.RentSlip.data.hire_start_date).days * 24
            hourOfPri = billOfPay * form.RentSlip.data.Room.KindOfRoom.unit_price

        Bill.date_of_payment = billOfPay / 24  # so ngay
        Bill.value = hourOfPri

        if form.RentSlip.data.Surcharge.surcharge == 0 and form.RentSlip.data.CustomerType.coefficient == 0:
            Bill.price = hourOfPri
        else:
            if form.RentSlip.data.Surcharge.surcharge != 0 and form.data.RentSlip.data.CustomerType.coefficient == 0:
                Bill.price = hourOfPri + (hourOfPri * (form.RentSlip.data.Surcharge.surcharge / 100))
            else:
                if form.RentSlip.data.Surcharge.surcharge == 0 and form.RentSlip.data.CustomerType.coefficient != 0:
                    Bill.price = hourOfPri * form.RentSlip.data.CustomerType.coefficient
                else:
                    if form.RentSlip.data.Surcharge.surcharge != 0 and form.RentSlip.data.CustomerType.coefficient != 0:
                        Bill.price = hourOfPri * form.RentSlip.data.CustomerType.coefficient + (
                                hourOfPri + (hourOfPri * (form.RentSlip.data.Surcharge.surcharge / 100)))


class RoomListView(BaseView):
    @expose("/")
    def index(self):
        name = request.args.get("name")
        kind_of_room_id = request.args.get("kind")
        status = request.args.get("status")
        amount = request.args.get("amount")

        return self.render("admin/roomlist.html",
                           rooms=dao.read_room_infos(name=name, kind_of_room_id=kind_of_room_id, status=status,
                                                     amount=amount), status=Status)


admin.add_view(RoomListView(name="Danh sách phòng"))
admin.add_view(AboutUsView(name="Giới Thiệu"))
admin.add_view(KindOfRoomModelView(KindOfRoom, db.session, name="Loại Phòng"))
admin.add_view(SurchargeModelView(Surcharge, db.session, name="Phụ thu"))
admin.add_view(CustomerTypeModelView(CustomerType, db.session, name="Loại Khách Hàng"))
admin.add_view(RoomModelView(Room, db.session, name="Phòng"))
admin.add_view(RentSlipModelView(RentSlip, db.session, name="Lập phiếu Thuê"))
admin.add_view(BillModelView(Bill, db.session, name="Lập hóa đơn"))
admin.add_view(UserModelView(User, db.session, name="Người Dùng"))
admin.add_view(LogoutView(name="Đăng Xuất"))
