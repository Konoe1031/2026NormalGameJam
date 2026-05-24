
seed = 9
tile_size = 48
home_position = (0, -1)
shop_position = (4, 3)
player_state = {
	"unstable": 20,
	"movability": 30,
	"elmo": 65,
	"void": 40,
	"upsidedown": 75
}
good_price = {
	"distance": [{"metal": 5, "plank": 5}, {"metal": 10, "plank": 10}, {"metal": 10, "plank": 10}, None],
	"speed": [{"science": 5, "food": 5}, {"science": 15, "food": 10}, None],
	"restaurant": [{"plank": 5, "food": 5}, {"metal": 5, "food": 10}, {"science": 5, "food": 20}, {"science": 10, "food": 40}, None],
	"lab": [{"science": 5}, {"science": 10, "metal": 3}, {"science": 15, "food": 15}, None],
	"house": [{"plank": 10}, {"plank": 15, "metal": 5}, {"plank": 15, "science": 10}, None],
	"resistance": [{"population": 30}, None]
}