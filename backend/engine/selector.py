import math
from typing import List, Dict, Set
from .probability import ProbabilityEngine
from .constraints import is_valid_attribute

class QuestionSelector:
    def __init__(self, engine: ProbabilityEngine, all_attributes: List[str]):
        self.engine = engine
        self.all_attributes = all_attributes
        self.asked_attributes: Set[str] = set()
        self.answered_attributes: Dict[str, bool] = {}
        
        import random
        # Stage 1: Shuffled dynamic filter sequence to ensure completely different starting questions every game
        self.hard_filter_sequence = [
            "is_overseas",
            "is_batsman",
            "is_bowler",
            "is_wicket_keeper",
            "is_currently_active",
            "played_for_csk",
            "played_for_mi",
            "played_for_rcb",
            "played_for_kkr"
        ]
        random.shuffle(self.hard_filter_sequence)
        
    def get_best_attribute(self, use_heuristic: bool = False) -> str:
        """
        Stage 1: Deterministic filtering if candidates >= 50
        Stage 2: Expected Entropy (or heuristic) if candidates < 50
        """
        active_count = self.engine.get_active_candidate_count()
        
        if active_count >= 50:
            for attr in self.hard_filter_sequence:
                if attr not in self.asked_attributes:
                    if is_valid_attribute(attr, self.answered_attributes):
                        return attr
                    
        if use_heuristic:
            return self._get_best_attribute_heuristic()
        return self._get_best_attribute_entropy()

    def _get_best_attribute_heuristic(self) -> str:
        best_attr = None
        best_score = float('inf') # Minimize difference from 0.5
        
        current_probs = {p["name"]: p["probability"] for p in self.engine.get_probabilities()}
        
        for attr in self.all_attributes:
            if attr in self.asked_attributes:
                continue
                
            if not is_valid_attribute(attr, self.answered_attributes):
                continue
                
            mass_true = 0.0
            for player in self.engine.players:
                if player["attributes"].get(attr, False):
                    mass_true += current_probs[player["name"]]
                    
            score = abs(mass_true - 0.5)
            
            if score < best_score:
                best_score = score
                best_attr = attr
                
        return best_attr

    def _get_best_attribute_entropy(self) -> str:
        best_attr = None
        min_score = float('inf')
        
        all_probs = self.engine.get_probabilities()
        active_count = self.engine.get_active_candidate_count()
        
        # 3. Top-2 disambiguation preparation
        top1 = None
        top2 = None
        if active_count < 10 and len(all_probs) >= 2:
            top1_name = all_probs[0]["name"]
            top2_name = all_probs[1]["name"]
            top1 = next((p for p in self.engine.players if p["name"] == top1_name), None)
            top2 = next((p for p in self.engine.players if p["name"] == top2_name), None)
            
        current_probs = {p["name"]: p["probability"] for p in all_probs}
        
        for attr in self.all_attributes:
            if attr in self.asked_attributes:
                continue
                
            if not is_valid_attribute(attr, self.answered_attributes):
                continue
                
            p_true_mass = 0.0
            
            for player in self.engine.players:
                if player["attributes"].get(attr, False):
                    p_true_mass += current_probs[player["name"]]
                    
            p_false_mass = 1.0 - p_true_mass
            
            if p_true_mass <= 1e-9 or p_false_mass <= 1e-9:
                continue
                
            h_true = 0.0
            h_false = 0.0
            
            for player in self.engine.players:
                prob = current_probs[player["name"]]
                if prob <= 1e-9:
                    continue
                    
                if player["attributes"].get(attr, False):
                    p_given_t = prob / p_true_mass
                    if p_given_t > 0:
                        h_true -= p_given_t * math.log2(p_given_t)
                else:
                    p_given_f = prob / p_false_mass
                    if p_given_f > 0:
                        h_false -= p_given_f * math.log2(p_given_f)
                        
            expected_entropy = p_true_mass * h_true + p_false_mass * h_false
            
            # Phase-aware scoring
            isolation_score = min(p_true_mass, p_false_mass)
            
            if active_count >= 20:
                score = expected_entropy
            elif active_count >= 10:
                score = 0.6 * expected_entropy + 0.4 * isolation_score
            else:
                score = isolation_score
                
            # Top-2 disambiguation tie-breaker
            if active_count < 10 and top1 and top2:
                val1 = top1["attributes"].get(attr, False)
                val2 = top2["attributes"].get(attr, False)
                if val1 != val2:
                    score -= 0.0001
            
            if score < min_score:
                min_score = score
                best_attr = attr
                
        if best_attr is None:
            for attr in self.all_attributes:
                if attr not in self.asked_attributes:
                    if is_valid_attribute(attr, self.answered_attributes):
                        return attr
                    
        return best_attr

    def mark_asked(self, attribute: str):
        """Marks an attribute as asked so it isn't selected again."""
        self.asked_attributes.add(attribute)
