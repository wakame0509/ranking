import eval7
import random

def evaluate_hand(cards):
    return eval7.evaluate(cards)

def generate_deck():
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    return [card for card in deck if card not in known_cards]

def run_nextcard_winrate_shift(p1_card1, p1_card2, board, stage='turn', selected_range=None,
                                extra_excluded=None, num_simulations=1000):
    """
    Flop or Turn に1枚カードを追加した時の勝率変化を記録
    stage='turn' → Flopに対してTurnカードを1枚ずつ追加
    stage='river'→ Turnに対してRiverカードを1枚ずつ追加
    """

    assert stage in ['turn', 'river']
    known = [p1_card1, p1_card2] + board
    full_deck = generate_deck()
    deck = remove_known_cards(full_deck, known)
    if extra_excluded:
        deck = remove_known_cards(deck, extra_excluded)

    shifts = {}

    for next_card in deck:
        total_win = 0
        total_tie = 0

        for _ in range(num_simulations):
            sim_deck = deck.copy()
            sim_deck.remove(next_card)
            random.shuffle(sim_deck)

            if selected_range:
                raw = random.choice(selected_range)
                if len(raw) == 2:
                    r1, r2 = raw
                    c1, c2 = r1 + 'c', r2 + 'd'
                else:
                    r1, r2, suited = raw
                    if suited == "s":
                        suit = random.choice(['c', 'd', 'h', 's'])
                        c1 = r1 + suit
                        c2 = r2 + suit
                    else:
                        suits_combo = random.sample(['c', 'd', 'h', 's'], 2)
                        c1 = r1 + suits_combo[0]
                        c2 = r2 + suits_combo[1]
                opp_hand = [c1, c2]
            else:
                opp_hand = [sim_deck.pop(), sim_deck.pop()]

            if stage == 'turn':
                full_board = board + [next_card] + [sim_deck.pop()]
            else:
                full_board = board + [next_card]

            p1_hand = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in full_board]
            p2_hand = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in full_board]

            s1 = evaluate_hand(p1_hand)
            s2 = evaluate_hand(p2_hand)

            total_win += s1 > s2
            total_tie += s1 == s2

        winrate = (total_win + total_tie / 2) / num_simulations * 100
        shifts[next_card] = winrate

    return shifts
