# detailed_shift_analyzer.py

import pandas as pd
from calculate_winrate_detailed_v2 import run_winrate_evolution
from utils import get_group_hands
from flop_samples import representative_flops

def analyze_detailed_features(group_name, num_simulations=10000):
    results = []

    hands = get_group_hands(group_name)
    for hand in hands:
        card1 = hand[0] + "s"
        card2 = hand[1] + "h"
        suited = len(hand) == 3 and hand[2] == "s"
        if suited:
            card1 = hand[0] + "s"
            card2 = hand[1] + "s"

        for flop in representative_flops:
            # 入力としてフロップを指定
            board = flop

            # 勝率と特徴量の取得
            try:
                result, features = run_winrate_evolution(
                    p1_card1=card1,
                    p1_card2=card2,
                    board=board,
                    selected_range=None,
                    extra_excluded=None,
                    num_simulations=num_simulations,
                    six_player_mode=False,
                    return_features=True
                )

                # 勝率変動情報に特徴量の情報をマージ
                for feat in features:
                    results.append({
                        "Hand": "".join(hand),
                        "Board": "".join(flop),
                        "ShiftFlop": round(result["ShiftFlop"], 2),
                        "ShiftTurn": round(result["ShiftTurn"], 2),
                        "ShiftRiver": round(result["ShiftRiver"], 2),
                        "Feature": feat["Feature"],
                        "Shift": feat["Shift"]
                    })

            except Exception as e:
                print(f"Error processing {hand} on {flop}: {e}")
                continue

    df = pd.DataFrame(results)
    return df
