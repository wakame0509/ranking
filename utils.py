def get_all_group_names():
    return [
        "High Pair", "Middle Pair", "Low Pair",
        "Suited Ace", "Offsuit Ace",
        "Suited Broadway", "Offsuit Broadway",
        "Suited Connector", "Offsuit Connector",
        "Suited One-Gapper", "Offsuit One-Gapper", "Other"
    ]

def get_group_hands(group_name):
    from hand_group_definitions import get_group_name
    ranks = "AKQJT98765432"
    suited_hands = [r1 + r2 + "s" for r1 in ranks for r2 in ranks if r1 != r2]
    offsuit_hands = [r1 + r2 + "o" for r1 in ranks for r2 in ranks if r1 != r2]
    pairs = [r + r for r in ranks]

    all_hands = pairs + suited_hands + offsuit_hands
    return [h for h in all_hands if get_group_name(h) == group_name]

def get_hand_range_25():
    return [
        ("A", "A"), ("K", "K"), ("Q", "Q"), ("J", "J"), ("T", "T"),
        ("A", "K", "s"), ("A", "Q", "s"), ("A", "J", "s"), ("K", "Q", "s"),
        ("A", "T", "s"), ("K", "J", "s"), ("Q", "J", "s"),
        ("A", "K", "o"), ("A", "Q", "o"), ("A", "J", "o"),
        ("K", "Q", "o"), ("Q", "J", "o")
    ]

def get_hand_range_30():
    return get_hand_range_25() + [
        ("9", "9"), ("8", "8"),
        ("J", "T", "s"), ("T", "9", "s"),
        ("K", "T", "s"), ("Q", "T", "s"),
        ("A", "T", "o"), ("K", "J", "o"),
        ("J", "T", "o")
    ]

def get_static_preflop_winrates():
    # ダミーデータ（実際は generate_static_preflop_winrates.py で生成したデータを使用）
    return {
        "AA": 85.2, "KK": 82.1, "QQ": 79.5, "AKs": 66.0, "AQs": 64.1,
        "AKo": 65.2, "KQs": 62.3, "JTs": 59.9, "T9s": 58.4, "98s": 56.8
    }
