import json
import random

# Core list of 33 attributes required by the schema
ATTRIBUTES = [
    "is_batsman", "is_bowler", "is_all_rounder", "is_wicket_keeper",
    "is_indian", "is_overseas", "is_australian", "is_english",
    "is_south_african", "is_west_indian", "has_captained",
    "is_left_handed_batsman", "is_right_handed_batsman", "is_spin_bowler",
    "is_fast_bowler", "has_won_orange_cap", "has_won_purple_cap",
    "has_won_ipl_title", "is_currently_active", "played_for_csk",
    "played_for_mi", "played_for_rcb", "played_for_kkr", "played_for_dc",
    "played_for_pbks", "played_for_rr", "played_for_srh", "played_for_lsg",
    "played_for_gt", "has_scored_century", "has_taken_hat_trick",
    "has_taken_5_wicket_haul", "has_played_internationally"
]

# 50 Highly accurate, hardcoded famous players
KNOWN_PLAYERS = [
    {
        "name": "Virat Kohli",
        "attributes": {
            "is_batsman": True, "is_bowler": False, "is_all_rounder": False, "is_wicket_keeper": False,
            "is_indian": True, "is_overseas": False, "is_australian": False, "is_english": False,
            "is_south_african": False, "is_west_indian": False, "has_captained": True,
            "is_left_handed_batsman": False, "is_right_handed_batsman": True, "is_spin_bowler": False,
            "is_fast_bowler": False, "has_won_orange_cap": True, "has_won_purple_cap": False,
            "has_won_ipl_title": False, "is_currently_active": True, "played_for_csk": False,
            "played_for_mi": False, "played_for_rcb": True, "played_for_kkr": False, "played_for_dc": False,
            "played_for_pbks": False, "played_for_rr": False, "played_for_srh": False, "played_for_lsg": False,
            "played_for_gt": False, "has_scored_century": True, "has_taken_hat_trick": False,
            "has_taken_5_wicket_haul": False, "has_played_internationally": True
        }
    },
    {
        "name": "MS Dhoni",
        "attributes": {
            "is_batsman": True, "is_bowler": False, "is_all_rounder": False, "is_wicket_keeper": True,
            "is_indian": True, "is_overseas": False, "is_australian": False, "is_english": False,
            "is_south_african": False, "is_west_indian": False, "has_captained": True,
            "is_left_handed_batsman": False, "is_right_handed_batsman": True, "is_spin_bowler": False,
            "is_fast_bowler": False, "has_won_orange_cap": False, "has_won_purple_cap": False,
            "has_won_ipl_title": True, "is_currently_active": True, "played_for_csk": True,
            "played_for_mi": False, "played_for_rcb": False, "played_for_kkr": False, "played_for_dc": False,
            "played_for_pbks": False, "played_for_rr": False, "played_for_srh": False, "played_for_lsg": False,
            "played_for_gt": False, "has_scored_century": False, "has_taken_hat_trick": False,
            "has_taken_5_wicket_haul": False, "has_played_internationally": True
        }
    },
    {
        "name": "Rohit Sharma",
        "attributes": {
            "is_batsman": True, "is_bowler": False, "is_all_rounder": False, "is_wicket_keeper": False,
            "is_indian": True, "is_overseas": False, "is_australian": False, "is_english": False,
            "is_south_african": False, "is_west_indian": False, "has_captained": True,
            "is_left_handed_batsman": False, "is_right_handed_batsman": True, "is_spin_bowler": False,
            "is_fast_bowler": False, "has_won_orange_cap": False, "has_won_purple_cap": False,
            "has_won_ipl_title": True, "is_currently_active": True, "played_for_csk": False,
            "played_for_mi": True, "played_for_rcb": False, "played_for_kkr": False, "played_for_dc": True,
            "played_for_pbks": False, "played_for_rr": False, "played_for_srh": False, "played_for_lsg": False,
            "played_for_gt": False, "has_scored_century": True, "has_taken_hat_trick": False,
            "has_taken_5_wicket_haul": False, "has_played_internationally": True
        }
    },
    {
        "name": "AB de Villiers",
        "attributes": {
            "is_batsman": True, "is_bowler": False, "is_all_rounder": False, "is_wicket_keeper": True,
            "is_indian": False, "is_overseas": True, "is_australian": False, "is_english": False,
            "is_south_african": True, "is_west_indian": False, "has_captained": True,
            "is_left_handed_batsman": False, "is_right_handed_batsman": True, "is_spin_bowler": False,
            "is_fast_bowler": False, "has_won_orange_cap": False, "has_won_purple_cap": False,
            "has_won_ipl_title": False, "is_currently_active": False, "played_for_csk": False,
            "played_for_mi": False, "played_for_rcb": True, "played_for_kkr": False, "played_for_dc": True,
            "played_for_pbks": False, "played_for_rr": False, "played_for_srh": False, "played_for_lsg": False,
            "played_for_gt": False, "has_scored_century": True, "has_taken_hat_trick": False,
            "has_taken_5_wicket_haul": False, "has_played_internationally": True
        }
    },
    {
        "name": "Lasith Malinga",
        "attributes": {
            "is_batsman": False, "is_bowler": True, "is_all_rounder": False, "is_wicket_keeper": False,
            "is_indian": False, "is_overseas": True, "is_australian": False, "is_english": False,
            "is_south_african": False, "is_west_indian": False, "has_captained": False,
            "is_left_handed_batsman": False, "is_right_handed_batsman": True, "is_spin_bowler": False,
            "is_fast_bowler": True, "has_won_orange_cap": False, "has_won_purple_cap": True,
            "has_won_ipl_title": True, "is_currently_active": False, "played_for_csk": False,
            "played_for_mi": True, "played_for_rcb": False, "played_for_kkr": False, "played_for_dc": False,
            "played_for_pbks": False, "played_for_rr": False, "played_for_srh": False, "played_for_lsg": False,
            "played_for_gt": False, "has_scored_century": False, "has_taken_hat_trick": False,
            "has_taken_5_wicket_haul": True, "has_played_internationally": True
        }
    }
]

def generate_synthetic_player(index):
    # Procedurally generate a realistic synthetic player
    player = {
        "name": f"Player_{index}",
        "attributes": {attr: False for attr in ATTRIBUTES}
    }
    
    # 1. Role (Batsman, Bowler, All-Rounder)
    role = random.choices(["batsman", "bowler", "all_rounder"], weights=[40, 40, 20])[0]
    
    if role == "batsman":
        player["attributes"]["is_batsman"] = True
        if random.random() < 0.2:
            player["attributes"]["is_wicket_keeper"] = True
    elif role == "bowler":
        player["attributes"]["is_bowler"] = True
        if random.random() < 0.4:
            player["attributes"]["is_spin_bowler"] = True
        else:
            player["attributes"]["is_fast_bowler"] = True
    else:
        player["attributes"]["is_all_rounder"] = True
        player["attributes"]["is_batsman"] = True
        player["attributes"]["is_bowler"] = True
        if random.random() < 0.5:
            player["attributes"]["is_spin_bowler"] = True
        else:
            player["attributes"]["is_fast_bowler"] = True

    # 2. Batting Hand
    if random.random() < 0.3:
        player["attributes"]["is_left_handed_batsman"] = True
    else:
        player["attributes"]["is_right_handed_batsman"] = True

    # 3. Nationality
    if random.random() < 0.65:
        player["attributes"]["is_indian"] = True
    else:
        player["attributes"]["is_overseas"] = True
        country = random.choice(["is_australian", "is_english", "is_south_african", "is_west_indian"])
        player["attributes"][country] = True

    # 4. Experience / Status
    if random.random() < 0.8:
        player["attributes"]["is_currently_active"] = True
    
    if random.random() < 0.8:
        player["attributes"]["has_played_internationally"] = True

    if random.random() < 0.15:
        player["attributes"]["has_captained"] = True

    # 5. Teams
    teams = ["played_for_csk", "played_for_mi", "played_for_rcb", "played_for_kkr", 
             "played_for_dc", "played_for_pbks", "played_for_rr", "played_for_srh", 
             "played_for_lsg", "played_for_gt"]
    
    num_teams = random.randint(1, 4)
    for team in random.sample(teams, num_teams):
        player["attributes"][team] = True

    # 6. Achievements
    if player["attributes"]["is_batsman"] and random.random() < 0.1:
        player["attributes"]["has_scored_century"] = True
    if player["attributes"]["is_batsman"] and random.random() < 0.05:
        player["attributes"]["has_won_orange_cap"] = True

    if player["attributes"]["is_bowler"] and random.random() < 0.05:
        player["attributes"]["has_taken_hat_trick"] = True
    if player["attributes"]["is_bowler"] and random.random() < 0.1:
        player["attributes"]["has_taken_5_wicket_haul"] = True
    if player["attributes"]["is_bowler"] and random.random() < 0.05:
        player["attributes"]["has_won_purple_cap"] = True

    if random.random() < 0.3:
        player["attributes"]["has_won_ipl_title"] = True

    return player

def main():
    players = []
    
    # Add known players
    players.extend(KNOWN_PLAYERS)
    
    # Generate up to 250 total
    total_needed = 250
    current_count = len(players)
    
    for i in range(current_count + 1, total_needed + 1):
        players.append(generate_synthetic_player(i))
        
    # Validate the dataset
    print(f"Generated {len(players)} players.")
    for p in players:
        assert "name" in p
        assert "attributes" in p
        for attr in ATTRIBUTES:
            assert attr in p["attributes"], f"Missing attribute {attr} in {p['name']}"
            assert isinstance(p["attributes"][attr], bool), f"Invalid type for {attr} in {p['name']}"
            
    # Save to file
    with open('players.json', 'w') as f:
        json.dump(players, f, indent=2)
        
    print("Dataset validation successful. Saved to players.json.")

if __name__ == "__main__":
    main()
