import streamlit as st
import requests
import json
import os
import logging

# 配置日志
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s"
)

HISTORY_FILE = "history.json"

def load_history(): 
    if not os.path.exists(HISTORY_FILE): 
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: 
            return json.load(f)
    except Exception as e:
        logging.error(f"加载历史失败：{e}")
        return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:  
            json.dump(history, f, ensure_ascii=False, indent=2)  
    except Exception as e:
        logging.error(f"保存历史失败：{e}")
        st.error(f"保存失败：{e}")

@st.cache_data(ttl=600)
def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    temp = data["current_condition"][0]["temp_C"]
    weather_desc = data["current_condition"][0]["weatherDesc"][0]["value"]
    return temp, weather_desc

st.title("天气查询")

# 初始化历史记录
if "history" not in st.session_state:
    st.session_state.history = load_history()

# 侧边栏
with st.sidebar:
    st.header("使用说明")
    st.write("可以选择预设城市，或手动输入。")
    if st.button("清空历史"):
        st.session_state.history = []
        save_history([])
        st.success("已清空历史记录")

# 下拉选择 + 手动输入
option = st.selectbox("选择查询方式", ["手动输入", "北京", "伦敦", "东京"])

if option == "手动输入":
    city = st.text_input("请输入城市名（英文）")
else:
    city_map = {"北京": "Beijing", "伦敦": "London", "东京": "Tokyo"}
    city = city_map[option]
    st.write(f"当前选择：{option}")

if st.button("查询"):
    if not city:
        st.warning("请输入或选择城市")
    else:
        with st.spinner("正在查询天气..."):
            try:
                temp, weather_desc = get_weather(city)

                # 保存到历史记录并写入文件
                st.session_state.history.append({
                    "city": city,
                    "temp": temp,
                    "desc": weather_desc
                })
                save_history(st.session_state.history)

                # 两列显示当前结果
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("当前温度", f"{temp}°C")
                with col2:
                    st.write("**天气状况**")
                    st.write(weather_desc)

            except requests.RequestException as e:
                logging.error(f"请求失败：{e}")
                st.error(f"请求失败：{e}")
            except (KeyError, IndexError) as e:
                logging.error(f"数据格式异常：{e}")
                st.error("返回数据格式异常")

# 统计信息
if st.session_state.history:
    st.subheader("统计信息")

    total = len(st.session_state.history)

    # 统计城市次数
    city_count = {}
    temps = []
    for item in st.session_state.history:
        city = item["city"]
        city_count[city] = city_count.get(city, 0) + 1
        try:
            temps.append(float(item["temp"]))
        except:
            pass

    most_city = max(city_count, key=city_count.get) if city_count else "无"
    avg_temp = round(sum(temps) / len(temps), 1) if temps else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总查询次数", total)
    with col2:
        st.metric("查询最多城市", most_city)
    with col3:
        st.metric("平均温度", f"{avg_temp}°C")

# 显示历史记录
if st.session_state.history:
    st.subheader("查询历史（最近5条）")
    for item in reversed(st.session_state.history[-5:]):
        st.write(f"{item['city']}: {item['temp']}°C, {item['desc']}")