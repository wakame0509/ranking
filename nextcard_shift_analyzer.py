import pandas as pd
from calculate_winrate_nextcard import run_nextcard_winrate_shift
from utils import get_group_hands
from flop_samples import representative_flops

def analyze_nextcard_shifts(group_name, stage='turn', num_simulations=1000, opponent_range=None):
    results = []
    hands = get_group_hands(group_name)

    for hand in hands:
        r1, r2 = hand[0], hand[1]
        suited = len(hand) == 3 and hand[2] == "s"
        if suited:
            card1 = r1 + "s"
            card2 = r2 + "s"
        else:
            card1 = r1 + "s"
            card2 = r2 + "h"

        for flop in representative_flops:
            board = flop[:3] if stage == 'turn' else flop[:4]

            try:
                shift_dict = run_nextcard_winrate_shift(
                    p1_card1=card1,
                    p1_card2=card2,
                    board=board,
                    stage=stage,
                    selected_range=opponent_range,
                    num_simulations=num_simulations
                )

                baseline = sum(shift_dict.values()) / len(shift_dict)

                for next_card, winrate in shift_dict.items():
                    shift = round(winrate - baseline, 2)
                    results.append({
                        "Hand": "".join(hand),
                        "Flop": "".join(board[:3]),
                        "NextCard": next_card,
                        "Stage": stage.capitalize(),
                        "Shift": shift
                    })

            except Exception as e:
                print(f"Error processing {hand} on {flop}: {e}")
                continue

    df = pd.DataFrame(results)
    return df
