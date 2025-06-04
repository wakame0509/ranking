import streamlit as st
import pandas as pd
from utils import get_all_group_names, get_group_hands, get_hand_range_25, get_hand_range_30
from nextcard_shift_analyzer import analyze_nextcard_shifts

st.title("🂡 勝率変動ランキング（NextCard別）")

st.markdown("""
このツールは、指定ハンドグループに対して、
フロップやターンから1枚カードが落ちたときに**勝率がどのように変化するか**をランキング表示します。
""")

# ハンドグループ選択
group_names = get_all_group_names()
selected_group = st.selectbox("🃏 ハンドグループを選択", group_names)

# 相手レンジ選択
range_option = st.radio("🎯 相手のレンジ", ["ランダム", "上位25%", "上位30%"])
if range_option == "ランダム":
    opponent_range = None
elif range_option == "上位25%":
    opponent_range = get_hand_range_25()
else:
    opponent_range = get_hand_range_30()

# ステージ選択（turn or river）
stage = st.radio("📍 対象ステージ", ["Flop→Turn", "Turn→River"])
stage_key = "turn" if stage == "Flop→Turn" else "river"

# シミュレーション回数
sim_count = st.selectbox("🎲 シミュレーション回数", [1000, 5000, 10000], index=0)

# 実行ボタン
if st.button("✅ 勝率変動を計算"):
    with st.spinner("計算中...しばらくお待ちください。"):
        df = analyze_nextcard_shifts(
            group_name=selected_group,
            stage=stage_key,
            num_simulations=sim_count,
            opponent_range=opponent_range
        )

    st.success("✅ 計算完了！")

    # ランキング表示
    top10 = df.sort_values(by="Shift", ascending=False).head(10)
    bottom10 = df.sort_values(by="Shift", ascending=True).head(10)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔼 勝率上昇 Top10")
        st.dataframe(top10.reset_index(drop=True))

    with col2:
        st.markdown("### 🔽 勝率下降 Top10")
        st.dataframe(bottom10.reset_index(drop=True))

    # CSVダウンロード
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 CSVとして保存", data=csv, file_name="nextcard_shift_results.csv", mime="text/csv")
