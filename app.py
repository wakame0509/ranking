import streamlit as st
import pandas as pd
from utils import get_all_group_names, get_group_hands, get_hand_range_25, get_hand_range_30, get_static_preflop_winrates
from detailed_shift_analyzer import analyze_detailed_features
from flop_samples import representative_flops

# タイトル
st.title("♠️ テキサスホールデム 勝率変動ランキング＋特徴量分析")

st.markdown("""
このアプリでは、任意のハンドグループに対し、代表フロップ100通りにおける
**勝率の変動（フロップ→ターン→リバー）** を計算し、その変動要因となる
**特徴量（ペア、ストレートドロー、オーバーカードなど）** を自動的に抽出します。
""")

# --- ハンドグループ選択 ---
group_names = get_all_group_names()
selected_group = st.selectbox("🃏 ハンドグループを選択してください", group_names)
hands = get_group_hands(selected_group)

# --- 相手のレンジ選択 ---
range_option = st.radio("🎯 相手のハンドレンジ", ["ランダム", "上位25%", "上位30%"])
if range_option == "ランダム":
    opponent_range = None
elif range_option == "上位25%":
    opponent_range = get_hand_range_25()
else:
    opponent_range = get_hand_range_30()

# --- シミュレーション回数選択 ---
num_simulations = st.selectbox("🎲 シミュレーション試行回数", [1000, 5000, 10000], index=2)

# --- 計算実行 ---
if st.button("✅ 勝率変動と特徴量を計算"):
    with st.spinner("計算中...しばらくお待ちください。"):
        df = analyze_detailed_features(
            hands=hands,
            flop_list=representative_flops,
            opponent_range=opponent_range,
            num_simulations=num_simulations,
            return_dataframe=True
        )

    st.success("✅ 計算完了！")
    
    # --- ランキング表示 ---
    def show_shift_ranking(stage):
        st.markdown(f"### 💡 {stage} 勝率変動ランキング")

        top10 = df.sort_values(by=f"Shift{stage}", ascending=False).head(10)
        bottom10 = df.sort_values(by=f"Shift{stage}", ascending=True).head(10)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🔼 上昇幅 Top10")
            st.dataframe(top10[["Hand", f"Shift{stage}", "Feature"]].reset_index(drop=True))

        with col2:
            st.markdown("#### 🔽 下降幅 Top10")
            st.dataframe(bottom10[["Hand", f"Shift{stage}", "Feature"]].reset_index(drop=True))

    show_shift_ranking("Flop")
    show_shift_ranking("Turn")
    show_shift_ranking("River")

    # --- 結果保存 ---
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 CSVとしてダウンロード", data=csv, file_name="shift_results.csv", mime="text/csv")

# --- プリフロップ勝率表の表示 ---
st.markdown("### 🎯 代表的なハンドのプリフロップ勝率（vs ランダム）")

preflop_df = pd.DataFrame(get_static_preflop_winrates().items(), columns=["Hand", "Winrate"])
preflop_df = preflop_df.sort_values(by="Winrate", ascending=False).reset_index(drop=True)
st.dataframe(preflop_df)
