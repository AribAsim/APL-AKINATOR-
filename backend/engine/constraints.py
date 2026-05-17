from typing import Dict, List

# Logical dependencies: Attribute A requires Attribute B to be True.
# e.g., We only ask if they are a spin bowler if they are a bowler.
ATTRIBUTE_DEPENDENCIES = {
    "is_left_handed_batsman": ["is_batsman"],
    "is_right_handed_batsman": ["is_batsman"],
    "has_scored_century": ["is_batsman"],
    "is_spin_bowler": ["is_bowler"],
    "is_fast_bowler": ["is_bowler"],
    "has_taken_5_wicket_haul": ["is_bowler"],
    "has_taken_hat_trick": ["is_bowler"],
    "is_australian": ["is_overseas"],
    "is_english": ["is_overseas"],
    "is_south_african": ["is_overseas"],
    "is_west_indian": ["is_overseas"],
}

# Mutually exclusive: If A is True, B must be False.
MUTUALLY_EXCLUSIVE_IF_TRUE = {
    "is_indian": ["is_overseas"],
    "is_overseas": ["is_indian"],
    "is_left_handed_batsman": ["is_right_handed_batsman"],
    "is_right_handed_batsman": ["is_left_handed_batsman"],
}

def is_valid_attribute(attr: str, answered: Dict[str, bool]) -> bool:
    """
    Checks if an attribute is logically valid to ask based on previous answers.
    Ensures 'Question Intelligence' by avoiding redundant or contradictory questions.
    """
    # 1. Check Dependencies
    if attr in ATTRIBUTE_DEPENDENCIES:
        for dependency in ATTRIBUTE_DEPENDENCIES[attr]:
            if dependency in answered and answered[dependency] is False:
                return False

    # 2. Check Mutually Exclusive (if the exclusive counterpart was answered 'Yes')
    if attr in MUTUALLY_EXCLUSIVE_IF_TRUE:
        for exclusive in MUTUALLY_EXCLUSIVE_IF_TRUE[attr]:
            if exclusive in answered and answered[exclusive] is True:
                return False

    return True
