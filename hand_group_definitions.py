def get_group_name(hand: str) -> str:
    """ハンドを12分類のどれに属するか判定する"""

    high_pairs = {"AA", "KK", "QQ"}
    middle_pairs = {"JJ", "TT", "99"}
    low_pairs = {"88", "77", "66", "55", "44", "33", "22"}

    suited_aces = {f"A{r}s" for r in "KQJT98765432"}
    offsuit_aces = {f"A{r}o" for r in "KQJT98765432"}

    suited_broadway = {"AKs", "KQs", "KJs", "QJs", "JTs", "AQs", "AJs", "ATs"}
    offsuit_broadway = {"AKo", "AQo", "AJo", "KQo", "QJo"}

    suited_connectors = {"JTs", "T9s", "98s", "87s", "76s", "65s", "54s"}
    offsuit_connectors = {"T9o", "98o", "87o", "76o", "65o", "54o"}

    suited_one_gappers = {"J9s", "T8s", "97s", "86s", "75s", "64s", "53s"}
    offsuit_one_gappers = {"J9o", "T8o", "97o", "86o", "75o", "64o", "53o"}

    if hand in high_pairs:
        return "High Pair"
    elif hand in middle_pairs:
        return "Middle Pair"
    elif hand in low_pairs:
        return "Low Pair"
    elif hand in suited_aces:
        return "Suited Ace"
    elif hand in offsuit_aces:
        return "Offsuit Ace"
    elif hand in suited_broadway:
        return "Suited Broadway"
    elif hand in offsuit_broadway:
        return "Offsuit Broadway"
    elif hand in suited_connectors:
        return "Suited Connector"
    elif hand in offsuit_connectors:
        return "Offsuit Connector"
    elif hand in suited_one_gappers:
        return "Suited One-Gapper"
    elif hand in offsuit_one_gappers:
        return "Offsuit One-Gapper"
    else:
        return "Other"
