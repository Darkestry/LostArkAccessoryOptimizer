import itertools
import random

# User input for desired engraving levels
desired_engraving_levels = {
    "Death Strike": 3,
    "Grudge": 3,
    "Hit Master": 3,
    "Cursed Doll": 3,
    "Keen Blunt Weapon": 3,
    "Adrenaline": 1
}

# Define data structures for accessories and engraving books
class Accessory:
    def __init__(self, name, accessory_type, combat_stats, engravings, reduction_effect, price):
        self.name = name
        self.accessory_type = accessory_type
        self.combat_stats = combat_stats
        self.engravings = engravings
        self.reduction_effect = reduction_effect
        self.price = price

class EngravingBook:
    def __init__(self, name, engraving, price):
        self.name = name
        self.engraving = engraving
        self.price = price

def generate_accessories(num_accessories):
    accessories = []
    engraving_options = ["Death Strike", "Grudge", "Hit Master", "Cursed Doll", "Keen Blunt Weapon", "Adrenaline"]
    reduction_effects = ["atk_power", "atk_speed", "move_speed", "defense"]
    accessory_types = ["Necklace", "Earring", "Ring"]
    
    for i in range(num_accessories):
        accessory_type = random.choice(accessory_types)
        if accessory_type == "Necklace":
            combat_stats = {"specialization": random.randint(400, 500) if random.choice([True, False]) else 0,
                            "swiftness": random.randint(400, 500) if random.choice([True, False]) else 0,
                            "crit": random.randint(400, 500) if random.choice([True, False]) else 0}
        else:
            combat_stats = {"specialization": random.randint(200, 300),
                            "swiftness": random.randint(200, 300),
                            "crit": random.randint(200, 300)}

        # Ensure only one engraving can exceed 3 points and the maximum is 6
        engraving_1, engraving_2 = random.sample(engraving_options, 2)
        engravings = {engraving_1: 3, engraving_2: random.randint(4, 6)}

        reduction_effect = (random.choice(reduction_effects), random.randint(1, 4))
        price = random.randint(3000, 150000)  # Assuming a price range

        accessories.append(Accessory(f"Accessory{i+1}", accessory_type, combat_stats, engravings, reduction_effect, price))

    return accessories

# Function to calculate total combat stats for a combination of accessories
def calculate_total_combat_stats(accessories):
    total_combat_stats = {"specialization": 0, "swiftness": 0, "crit": 0}
    for accessory in accessories:
        for stat, value in accessory.combat_stats.items():
            total_combat_stats[stat] += value
    return total_combat_stats

# Function to calculate total engraving points for a combination of items
def calculate_total_engraving_points(accessories, engraving_books, ability_stone_combo):
    total_engraving_points = {}

    # Process engravings from accessories
    for accessory in accessories:
        for engraving, points in accessory.engravings.items():
            total_engraving_points[engraving] = total_engraving_points.get(engraving, 0) + points

    # Process engravings from engraving books
    for book in engraving_books:
        total_engraving_points[book.engraving] = total_engraving_points.get(book.engraving, 0) + 12

    for engraving, strength in ability_stone_combo:
        if engraving != "Death Strike":  # Skip "Death Strike"
            total_engraving_points[engraving] = total_engraving_points.get(engraving, 0) + strength

    return total_engraving_points

# Function to calculate total reduction effects for a combination of accessories
def calculate_total_reduction_effects(accessories):
    total_reduction_effects = {"atk_power": 0, "atk_speed": 0, "move_speed": 0, "defense": 0}
    for accessory in accessories:
        effect, points = accessory.reduction_effect
        total_reduction_effects[effect] += points
    return total_reduction_effects

def generate_ability_stone_combinations(desired_engravings):
    # Define the possible pairs of engraving strengths
    engraving_strengths = [(4, 10), (5, 9), (6, 8), (7, 7)]

    # Generate all possible pairs of desired engravings
    engraving_pairs = list(itertools.combinations(desired_engravings, 2))

    # Generate combinations of engraving pairs with their strengths
    ability_stone_combinations = []
    for strength_pair in engraving_strengths:
        for engraving_pair in engraving_pairs:
            # Pair each engraving with a strength and add it to the combinations
            combination = ((engraving_pair[0], strength_pair[0]), (engraving_pair[1], strength_pair[1]))
            ability_stone_combinations.append(combination)

    return ability_stone_combinations

# Function to generate all possible combinations of accessories and engraving books
def generate_combinations(accessories, engraving_books):
    necklaces = [accessory for accessory in accessories if accessory.accessory_type == "Necklace"]
    earrings = [accessory for accessory in accessories if accessory.accessory_type == "Earring"]
    rings = [accessory for accessory in accessories if accessory.accessory_type == "Ring"]

    accessory_combinations = [(necklace, earring1, earring2, ring1, ring2)
                              for necklace in necklaces
                              for earring1, earring2 in itertools.combinations(earrings, 2)
                              for ring1, ring2 in itertools.combinations(rings, 2)]

    book_combinations = list(itertools.combinations(engraving_books, 2))
    ability_stone_combinations = generate_ability_stone_combinations(desired_engraving_levels.keys())
    all_combinations = [(accessory_combo, book_combo, ability_stone_combo) for accessory_combo in accessory_combinations for book_combo in book_combinations for ability_stone_combo in ability_stone_combinations]
    return all_combinations

# Function to calculate the total cost of a build
def calculate_total_cost(accessory_combo, book_combo):
    total_cost = sum(accessory.price for accessory in accessory_combo)
    total_cost += sum(book.price * 20 for book in book_combo)
    return total_cost

# Main function
def main():
    # User input for primary and secondary combat stats
    primary_combat_stat = "crit"
    secondary_combat_stat = "swiftness"

    # Retrieve item data (accessories, engraving books) from a data source (e.g., database, file)
    accessories = [
        Accessory("Necklace1", "Necklace", {"specialization": 0, "swiftness": 493, "crit": 500}, {"Hit Master": 6, "Grudge": 3}, ("defense", 2), 50000),
        Accessory("Earring5", "Earring", {"specialization": 0, "swiftness": 0, "crit": 293}, {"Death Strike": 3, "Adrenaline": 6}, ("atk_speed", 3), 69999),
        Accessory("Earring4", "Earring", {"specialization": 0, "swiftness": 0, "crit": 296}, {"Grudge": 6, "Cursed Doll": 3}, ("move_speed", 3), 17000),
        Accessory("Ring5", "Ring", {"specialization": 0, "swiftness": 0, "crit": 200}, {"Cursed Doll": 6, "Keen Blunt Weapon": 3}, ("move_speed", 1), 39999),
        Accessory("Ring5", "Ring", {"specialization": 0, "swiftness": 0, "crit": 193}, {"Cursed Doll": 6, "Grudge": 3}, ("defense", 2), 10000)
    ] # generate_accessories(20)

    engraving_books = [
        EngravingBook("Book1", "Death Strike", 0),
        EngravingBook("Book2", "Grudge", 3400),
        EngravingBook("Book3", "Hit Master", 850),
        EngravingBook("Book4", "Cursed Doll", 1100),
        EngravingBook("Book5", "Keen Blunt Weapon", 2300),
        EngravingBook("Book6", "Adrenaline", 1950)
    ]

    # Generate all possible combinations of accessories and engraving books
    all_combinations = generate_combinations(accessories, engraving_books)

    # Evaluate each combination and find the optimal builds
    optimal_builds = []
    processed_combinations = 0
    for accessory_combo, book_combo, ability_stone_combo in all_combinations:
        # Calculate total combat stats, engraving points, and reduction effects for the current combination
        total_combat_stats = calculate_total_combat_stats(accessory_combo)
        total_engraving_points = calculate_total_engraving_points(accessory_combo, book_combo, ability_stone_combo)
        total_reduction_effects = calculate_total_reduction_effects(accessory_combo)

        # Check if the current combination meets the desired engraving levels
        if all(total_engraving_points.get(engraving, 0) >= level * 5 for engraving, level in desired_engraving_levels.items()) and all(effect <= 4 for effect in total_reduction_effects.values()):
            # Calculate the remaining engraving points needed from the ability stone

            # Determine the required ability stone stats
            ability_stone_stats = ability_stone_combo

            # Determine the required reduction effect for the ability stone
            ability_stone_reduction_effect = None
            for effect, points in total_reduction_effects.items():
                if points == 0:
                    ability_stone_reduction_effect = effect
                    break

            # Calculate the total cost of the build
            total_cost = calculate_total_cost(accessory_combo, book_combo)

            # Add the build to the list of optimal builds
            optimal_builds.append((accessory_combo, book_combo, ability_stone_stats, ability_stone_reduction_effect, total_cost, total_combat_stats))
            processed_combinations += 1
            if processed_combinations % 1000 == 0:  # Update progress every 1000 combinations
                    progress_percentage = (processed_combinations / all_combinations) * 100
                    print(f"Processed {processed_combinations}/{all_combinations} combinations ({progress_percentage:.2f}%)")

    # Sort the optimal builds based on primary and secondary combat stats
    optimal_builds.sort(key=lambda x: (-x[5][primary_combat_stat], -x[5][secondary_combat_stat], x[4]))

    # Display the best few combinations to the user
    num_combinations_to_display = min(5, len(optimal_builds))
    if optimal_builds:
        print(f"Best {num_combinations_to_display} combinations:")
        for i, build in enumerate(optimal_builds[:num_combinations_to_display], 1):
            accessory_combo, book_combo, ability_stone_stats, ability_stone_reduction_effect, total_cost, total_combat_stats = build
            print(f"Combination {i}:")
            print("Accessories:")
            for accessory in accessory_combo:
                print(f"  - {accessory.name} ({accessory.accessory_type}): {', '.join([f'{engraving} +{points}' for engraving, points in accessory.engravings.items()])} with reduction effect on {accessory.reduction_effect[0]} by {accessory.reduction_effect[1]}")
            print("Engraving Books:")
            for book in book_combo:
                print(f"  - {book.name} for {book.engraving} (+12 points)")
            print("Required Ability Stone Stats:")
            if ability_stone_stats:
                for engraving, points in ability_stone_stats:
                    print(f"  - {engraving}: +{points} points")
            else:
                print("  - No ability stone required.")
            print(f"Required Ability Stone Reduction Effect: {ability_stone_reduction_effect if ability_stone_reduction_effect else 'None'}")
            
            # Enhanced display of total combat stats
            print("Total Combat Stats:")
            for stat, value in total_combat_stats.items():
                print(f"  - {stat.capitalize()}: {value}")
            
            print(f"Total Cost: {total_cost} Gold")
            print("-" * 40)  # Separator for readability
    else:
        print("No combination found that meets the desired engraving levels.")

if __name__ == "__main__":
    main()