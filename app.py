import streamlit as st
from datetime import datetime
import io

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Trà Sữa - Tính Hóa Đơn",
    page_icon="🧋",
    layout="centered"
)

# ==============================
# DỮ LIỆU MENU
# Có thể thay đổi giá tại đây
# ==============================
MENU_TRA_SUA = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa trân châu đường đen": 40000,
    "Trà sữa dâu": 35000,
    "Trà sữa ô long": 38000,
}

MENU_TOPPING = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 6000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
}

MUC_DUONG = ["100%", "70%", "0%"]
MUC_DA = ["100%", "70%", "0%"]


# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# ==============================
# KHỞI TẠO GIỎ HÀNG
# ==============================
if "gio_hang" not in st.session_state:
    st.session_state.gio_hang = []


# ==============================
# TIÊU ĐỀ
# ==============================
st.title("🧋 TRÀ SỮA - TÍNH HÓA ĐƠN")
st.caption("Ứng dụng quản lý đơn hàng và xuất hóa đơn")


# ==============================
# THÔNG TIN KHÁCH HÀNG
# ==============================
st.subheader("👤 Thông tin khách hàng")

ten_khach_hang = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)


# ==============================
# CHỌN TRÀ SỮA
# ==============================
st.subheader("🧋 Chọn trà sữa")

col1, col2 = st.columns(2)

with col1:
    loai_tra_sua = st.selectbox(
        "Loại trà sữa",
        list(MENU_TRA_SUA.keys())
    )

with col2:
    so_luong = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )

gia_tra_sua = MENU_TRA_SUA[loai_tra_sua]

st.info(
    f"Giá: **{dinh_dang_tien(gia_tra_sua)} / ly**"
)


# ==============================
# ĐƯỜNG VÀ ĐÁ
# ==============================
st.subheader("🥤 Tùy chọn đồ uống")

col1, col2 = st.columns(2)

with col1:
    muc_duong = st.selectbox(
        "Mức đường",
        MUC_DUONG,
        index=0
    )

with col2:
    muc_da = st.selectbox(
        "Mức đá",
        MUC_DA,
        index=0
    )


# ==============================
# TOPPING
# ==============================
st.subheader("🍮 Topping")

chon_topping = st.multiselect(
    "Chọn topping",
    list(MENU_TOPPING.keys())
)

# Lưu số lượng topping
topping_so_luong = {}

if chon_topping:
    st.write("**Số lượng từng topping:**")

    for topping in chon_topping:
        topping_so_luong[topping] = st.number_input(
            f"{topping} - {dinh_dang_tien(MENU_TOPPING[topping])}/phần",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
            key=f"topping_{topping}"
        )


# ==============================
# THÊM VÀO ĐƠN HÀNG
# ==============================
if st.button("➕ Thêm vào hóa đơn", use_container_width=True):

    if not ten_khach_hang.strip():
        st.warning("Vui lòng nhập tên khách hàng.")
    else:

        item = {
            "loai_tra_sua": loai_tra_sua,
            "gia_tra_sua": gia_tra_sua,
            "so_luong": so_luong,
            "muc_duong": muc_duong,
            "muc_da": muc_da,
            "topping": topping_so_luong.copy()
        }

        st.session_state.gio_hang.append(item)

        st.success("Đã thêm sản phẩm vào hóa đơn!")


# ==============================
# HIỂN THỊ HÓA ĐƠN
# ==============================
st.divider()

st.subheader("🧾 HÓA ĐƠN")

if len(st.session_state.gio_hang) == 0:

    st.info("Chưa có sản phẩm nào trong hóa đơn.")

else:

    tong_tien = 0

    for index, item in enumerate(st.session_state.gio_hang, start=1):

        tien_tra_sua = (
            item["gia_tra_sua"] *
            item["so_luong"]
        )

        tien_topping = 0

        for topping, sl in item["topping"].items():
            tien_topping += MENU_TOPPING[topping] * sl

        thanh_tien = tien_tra_sua + tien_topping

        tong_tien += thanh_tien

        # Hiển thị sản phẩm
        with st.container():

            st.markdown(
                f"### {index}. {item['loai_tra_sua']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"**Số lượng:** {item['so_luong']}"
                )

                st.write(
                    f"**Đường:** {item['muc_duong']}"
                )

                st.write(
                    f"**Đá:** {item['muc_da']}"
                )

            with col2:
                st.write(
                    f"**Đơn giá:** "
                    f"{dinh_dang_tien(item['gia_tra_sua'])}"
                )

                st.write(
                    f"**Tiền trà sữa:** "
                    f"{dinh_dang_tien(tien_tra_sua)}"
                )

            if item["topping"]:

                st.write("**Topping:**")

                for topping, sl in item["topping"].items():

                    thanh_tien_topping = (
                        MENU_TOPPING[topping] * sl
                    )

                    st.write(
                        f"- {topping}: {sl} phần "
                        f"→ {dinh_dang_tien(thanh_tien_topping)}"
                    )

            st.write(
                f"**Thành tiền: "
                f"{dinh_dang_tien(thanh_tien)}**"
            )

            st.divider()

    # ==============================
    # TỔNG TIỀN
    # ==============================
    st.subheader("💰 TỔNG THANH TOÁN")

    st.markdown(
        f"""
        <div style="
            background-color:#fff3cd;
            padding:20px;
            border-radius:10px;
            text-align:center;
            border:1px solid #ffeeba;
        ">
            <h2>TỔNG TIỀN</h2>
            <h1 style="color:#d63384;">
                {dinh_dang_tien(tong_tien)}
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # ==============================
    # TẠO NỘI DUNG HÓA ĐƠN
    # ==============================
    thoi_gian = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    noi_dung_hoa_don = ""

    noi_dung_hoa_don += "=" * 45 + "\n"
    noi_dung_hoa_don += "        HÓA ĐƠN TRÀ SỮA\n"
    noi_dung_hoa_don += "=" * 45 + "\n"
    noi_dung_hoa_don += f"Khách hàng: {ten_khach_hang}\n"
    noi_dung_hoa_don += f"Thời gian: {thoi_gian}\n"
    noi_dung_hoa_don += "-" * 45 + "\n"

    for index, item in enumerate(
        st.session_state.gio_hang,
        start=1
    ):

        tien_tra_sua = (
            item["gia_tra_sua"] *
            item["so_luong"]
        )

        tien_topping = 0

        noi_dung_hoa_don += (
            f"{index}. {item['loai_tra_sua']}\n"
        )

        noi_dung_hoa_don += (
            f"   Số lượng: {item['so_luong']}\n"
        )

        noi_dung_hoa_don += (
            f"   Đường: {item['muc_duong']}\n"
        )

        noi_dung_hoa_don += (
            f"   Đá: {item['muc_da']}\n"
        )

        noi_dung_hoa_don += (
            f"   Tiền trà sữa: "
            f"{dinh_dang_tien(tien_tra_sua)}\n"
        )

        if item["topping"]:

            noi_dung_hoa_don += "   Topping:\n"

            for topping, sl in item["topping"].items():

                tien_tp = MENU_TOPPING[topping] * sl

                tien_topping += tien_tp

                noi_dung_hoa_don += (
                    f"      - {topping}: "
                    f"{sl} phần = "
                    f"{dinh_dang_tien(tien_tp)}\n"
                )

        thanh_tien = tien_tra_sua + tien_topping

        noi_dung_hoa_don += (
            f"   Thành tiền: "
            f"{dinh_dang_tien(thanh_tien)}\n"
        )

        noi_dung_hoa_don += "-" * 45 + "\n"

    noi_dung_hoa_don += (
        f"TỔNG THANH TOÁN: "
        f"{dinh_dang_tien(tong_tien)}\n"
    )

    noi_dung_hoa_don += "=" * 45 + "\n"
    noi_dung_hoa_don += "       CẢM ƠN QUÝ KHÁCH!\n"
    noi_dung_hoa_don += "=" * 45 + "\n"


    # ==============================
    # NÚT THANH TOÁN
    # ==============================
    if st.button(
        "💳 THANH TOÁN & XUẤT HÓA ĐƠN",
        type="primary",
        use_container_width=True
    ):

        st.success(
            f"Thanh toán thành công! "
            f"Tổng tiền: {dinh_dang_tien(tong_tien)}"
        )

        # Cho phép tải hóa đơn
        file_hoa_don = io.BytesIO(
            noi_dung_hoa_don.encode("utf-8")
        )

        ten_file = (
            f"hoa_don_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        st.download_button(
            label="📥 Tải hóa đơn",
            data=file_hoa_don,
            file_name=ten_file,
            mime="text/plain",
            use_container_width=True
        )


    # ==============================
    # XÓA HÓA ĐƠN
    # ==============================
    if st.button(
        "🗑️ Xóa toàn bộ hóa đơn",
        use_container_width=True
    ):

        st.session_state.gio_hang = []

        st.rerun()

