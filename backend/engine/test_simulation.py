import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.probability import ProbabilityEngine
from engine.selector import QuestionSelector

def load_dataset():
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'players.json')
    with open(data_path, 'r') as f:
        return json.load(f)

def run_simulation(target_player_name: str, players: list, use_heuristic: bool, max_questions: int = 8):
    target_player = next((p for p in players if p["name"] == target_player_name), None)
    if not target_player:
        return False, 0
        
    all_attributes = list(players[0]["attributes"].keys())
    
    prob_engine = ProbabilityEngine(players)
    selector = QuestionSelector(prob_engine, all_attributes)
    
    question_count = 0
    print(f"\n--- Simulating for: {target_player_name} ---")
    while question_count < max_questions:
        active_count = prob_engine.get_active_candidate_count()
        is_hard_mode = active_count >= 50
        
        best_attr = selector.get_best_attribute(use_heuristic=use_heuristic)
        if not best_attr:
            break
            
        selector.mark_asked(best_attr)
        question_count += 1
        
        has_attr = target_player["attributes"].get(best_attr, False)
        response = "yes" if has_attr else "no"
        
        prob_engine.update(best_attr, response, hard_mode=is_hard_mode)
        
        new_active = prob_engine.get_active_candidate_count()
        all_probs = prob_engine.get_probabilities()
        top1 = all_probs[0]
        top2 = all_probs[1] if len(all_probs) > 1 else {"probability": 0}
        
        top1_prob = top1['probability']
        top2_prob = top2['probability']
        confidence = top1_prob / (top1_prob + top2_prob + 1e-9)
        
        mode_str = "HARD " if is_hard_mode else "SOFT "
        print(f"  Q{question_count} [{mode_str}] | {best_attr}? {response.upper()} | Candidates: {new_active:3} | Top: {top1['name']} (Conf: {confidence*100:.1f}%)")
        
        # 4. Confidence rule
        if confidence >= 0.80 and question_count >= 5:
            success = (top1['name'] == target_player_name)
            if success:
                print(f"  [SUCCESS] Reached >=80% confidence in {question_count} questions.")
            return success, question_count
            
    all_probs = prob_engine.get_probabilities()
    top1 = all_probs[0]
    top2 = all_probs[1] if len(all_probs) > 1 else {"probability": 0}
    
    top1_prob = top1['probability']
    top2_prob = top2['probability']
    confidence = top1_prob / (top1_prob + top2_prob + 1e-9)
    
    success = (top1['name'] == target_player_name) and (confidence >= 0.80) and (question_count >= 5)
    if not success:
        print(f"  [FAILED] Best guess: {top1['name']} (Conf: {confidence*100:.1f}%)")
    return success, question_count

def main():
    players = load_dataset()
    targets = ["Virat Kohli", "MS Dhoni", "Lasith Malinga", "AB de Villiers", "Player_150", "Player_10", "Player_220", "Player_18", "Rohit Sharma", "Player_45"]
    
    print("--- Running Convergence Test ---")
    print(f"Dataset Size: {len(players)} players")
    print(f"Target Pool: {len(targets)} players\n")
    
    max_q = 8
    print(f"== Test Limit: {max_q} Questions ==")
    
    successes = 0
    total_q = 0
    stage_distribution = {"Early (1-4)": 0, "Mid (5-6)": 0, "End (7-8)": 0}
    
    for target in targets:
        reached_confidence, qs = run_simulation(target, players, use_heuristic=False, max_questions=max_q)
        total_q += qs
        if reached_confidence:
            successes += 1
            if qs <= 4:
                stage_distribution["Early (1-4)"] += 1
            elif qs <= 6:
                stage_distribution["Mid (5-6)"] += 1
            else:
                stage_distribution["End (7-8)"] += 1
                
    avg_q = total_q / len(targets)
    acc_80 = (successes / len(targets)) * 100
    
    print(f"\n[RESULTS]")
    print(f"  Reached >=80% Confidence Accuracy: {acc_80:.1f}%")
    print(f"  Average Questions Asked: {avg_q:.1f}")
    print(f"  Distribution of Successes: {stage_distribution}")

if __name__ == "__main__":
    main()
