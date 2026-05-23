import inventory

food: int = 100
population: int = 20
metal: int = 0
plank: int = 0
science: int = 0

def store_resource():
	global food, population, metal, plank, science
	for i, slot in enumerate(inventory.slots):
		if slot == None:
			continue
		if slot["item"] == "metal":
			metal += slot["count"]
		elif slot["item"] == "plank":
			plank += slot["count"]
		elif slot["item"] == "bone":
			science += slot["count"]
		elif slot["item"] == "mango":
			food += 5 * slot["count"]
		elif slot["item"] == "can":
			food += 8 * slot["count"]
		elif slot["item"] == "cake":
			food += 3 * slot["count"]
			population += slot["count"]
		inventory.slots[i] = None
	return
