from app import admin, db
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user
from app.models import User, KindOfRoom, Room, RentSlip, CustomerType, RentSlipDetail
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


class KindOfRoomModelView(AuthenticatedView):
    column_display_pk = True
    form_columns = ('name', 'unit_price', 'note')
    column_labels = dict(name="Loại phòng", unit_price="Đơn giá", note="Ghi chú")

    # def is_accessible(self):
    #     return current_user.is_authenticated and \
    #            (current_user.roles == "tieptan" or current_user.roles == "admin")


class RoomModelView(AuthenticatedView):
    column_display_pk = True
    form_columns = ('name', 'kind_of_room_id', 'status')
    column_labels = dict(name="Số phòng", kind_of_room_id="Loại phòng", status="Trạng thái")

    def is_accessible(self):
        return current_user.is_authenticated


class RentSlipModelView(AuthenticatedView):
    column_display_pk = True
    form_columns = ('hire_start_date', 'room_id')
    column_labels = dict(hire_start_date="Ngày bắt đầu thuê", room_id="Số phòng")


class UserModelView(AuthenticatedView):
    column_display_pk = True
    column_labels = dict(name =  "Tên người dùng", active = "Kích hoạt"
                         , user_name = "Tên đăng nhập", pass_word = "Mật khẩu", roles = "Vai trò")

    def on_model_change(self, form, User, is_created=False):
        User.pass_word = hashlib.md5(User.pass_word.encode('utf-8')).hexdigest()


class CustomerTypeModelView(AuthenticatedView):
    column_display_pk = True


class RentSlipDetailModelView(AuthenticatedView):
    column_display_pk = True


admin.add_view(KindOfRoomModelView(KindOfRoom, db.session, name="Loại Phòng"))
admin.add_view(RoomModelView(Room, db.session, name="Phòng"))
admin.add_view(RentSlipModelView(RentSlip, db.session, name="Phiếu Thuê"))
admin.add_view(CustomerTypeModelView(CustomerType, db.session, name="Loại Khách Hàng"))
admin.add_view(RentSlipDetailModelView(RentSlipDetail, db.session, name="Chi Tiết Phiếu Thuê"))
admin.add_view(UserModelView(User, db.session, name="Người Dùng"))
admin.add_view(AboutUsView(name="Giới Thiệu"))
admin.add_view(LogoutView(name="Đăng Xuất"))