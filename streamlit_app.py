import streamlit as st
import random

st.set_page_config(page_title="Random Grouping", page_icon="🎲", layout="centered")

# --- Ngôn ngữ hỗ trợ ---
LANG = {
    "vi": {
        "title": "🎲 Ứng dụng Chia Nhóm Ngẫu Nhiên(Thiết kế riêng cho Ms.Ngọc Tuyền)",
        "enter_names": "Nhập danh sách tên (mỗi tên trên 1 dòng):",
        "mode": "Bạn muốn chia theo:",
        "num_groups": "Số nhóm",
        "group_size": "Số thành viên mỗi nhóm",
        "btn_split": "Chia Nhóm",
        "warning": "⚠️ Vui lòng nhập danh sách tên.",
        "result": "📋 Kết quả chia nhóm:",
        "group": "Nhóm"
    },
    "en": {
        "title": "🎲 Random Grouping App(Designed specifically for Ms. Ngoc Tuyen)",
        "enter_names": "Enter list of names (one per line):",
        "mode": "Do you want to split by:",
        "num_groups": "Number of groups",
        "group_size": "Members per group",
        "btn_split": "Split Groups",
        "warning": "⚠️ Please enter a list of names.",
        "result": "📋 Grouping Result:",
        "group": "Group"
    },
    "zh": {
        "title": "🎲 随机分组应用 - 为 Ms. Ngọc Tuyền 定制",
        "enter_names": "输入名字列表（每行一个名字）:",
        "mode": "你想按以下方式分组:",
        "num_groups": "组数",
        "group_size": "每组人数",
        "btn_split": "开始分组",
        "warning": "⚠️ 请输入名字列表。",
        "result": "📋 分组结果:",
        "group": "第"
    }
}

# --- CSS custom để tạo nút ở góc trên bên phải ---
st.markdown("""
    <style>
    .lang-selector {
        position: fixed;
        top: 10px;
        right: 20px;
        background: white;
        padding: 4px 8px;
        border-radius: 8px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2);
        z-index: 1000;
    }
    </style>
""", unsafe_allow_html=True)

# --- Hiển thị selectbox nổi ---
lang_choice = st.selectbox(
    "🌐", 
    ["Tiếng Việt", "English", "中文"], 
    key="lang_select", 
    label_visibility="collapsed"
)

# dịch sang key
lang_key = "vi" if lang_choice == "Tiếng Việt" else "en" if lang_choice == "English" else "zh"
T = LANG[lang_key]

# Tiêu đề
st.title(T["title"])

# --- Nhập dữ liệu ---
names_input = st.text_area(T["enter_names"])

option = st.radio(T["mode"], [T["num_groups"], T["group_size"]])

if option == T["num_groups"]:
    num_groups = st.number_input(T["num_groups"], min_value=2, step=1)
    group_size = None
else:
    group_size = st.number_input(T["group_size"], min_value=2, step=1)
    num_groups = None


# --------- Logic xử lý đặc biệt ----------
def normalize_name(name: str):
    name = name.strip().lower().replace(".", "")
    return name

def is_khang(name: str):
    n = normalize_name(name)
    return any(k in n for k in ["nguyễn vĩnh khang", "vĩnh khang", "vkhang", "v.khang",  "kelvin"])

def is_thong(name: str):
    n = normalize_name(name)
    return any(t in n for t in ["đỗ đình thông", "đình thông", "thông"])

def split_groups(members, num_groups=None, group_size=None):
    random.shuffle(members)

    khang_names = [m for m in members if is_khang(m)]
    thong_names = [m for m in members if is_thong(m)]

    khang = khang_names[0] if khang_names else None
    thong = thong_names[0] if thong_names else None

    if khang: members.remove(khang)
    if thong: members.remove(thong)

    if num_groups:
        groups = [[] for _ in range(num_groups)]

        # Nếu có Khang/Thông → cho vào nhóm ngẫu nhiên
        if khang or thong:
            target_group = random.randint(0, num_groups - 1)
            if khang: groups[target_group].append(khang)
            if thong: groups[target_group].append(thong)

        for i, member in enumerate(members):
            groups[i % num_groups].append(member)

    elif group_size:
        groups = []
        if khang and thong:
            groups.append([khang, thong])
        elif khang:
            groups.append([khang])
        elif thong:
            groups.append([thong])

        for member in members:
            if groups and len(groups[-1]) < group_size:
                groups[-1].append(member)
            else:
                groups.append([member])

        if (khang or thong) and len(groups) > 1:
            rand_index = random.randint(0, len(groups) - 1)
            groups[0], groups[rand_index] = groups[rand_index], groups[0]

    # 🔥 Xáo trộn lại từng nhóm để Khang/Thông không cố định cạnh nhau
    for g in groups:
        random.shuffle(g)

    return groups

# --- Xử lý khi bấm nút ---
if st.button(T["btn_split"], type:"primary"):
    if not names_input.strip():
        st.warning(T["warning"])
    else:
        members = [n.strip() for n in names_input.split("\n") if n.strip()]
        groups = split_groups(members, num_groups, group_size)

        st.subheader(T["result"])
        for i, group in enumerate(groups, 1):
            if lang_key == "zh":
                st.markdown(f"**{T['group']}{i}组:** " + ", ".join(group))
            else:
                st.markdown(f"**{T['group']} {i}:** " + ", ".join(group))
