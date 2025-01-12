plant_json_schema = {
	"type": "object",
	"properties": {
		"display": {"type": "string"},
		"latin": {"type": "string"},
		"seed_to_harvest_days": {"type": "integer"},
		"pre_grow_days": {"type": "integer"},
		"seed_ranges": {"type": "array", "items": {"type": "object", "properties": {"max": {"type": "integer"}, "min": {"type": "integer"}}}},
		"categories": {"type": "array", "items": {"type": "string"}},
		"icon": {"type": "string"},
		"literature": {"type": "array", "items": {"type": "string"}},
		"detail": {"type": "string"},
	},
	"required": ["display", "seed_to_harvest_days"],
}
