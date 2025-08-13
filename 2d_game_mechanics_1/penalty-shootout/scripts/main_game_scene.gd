extends Node2D

var current_level = 1
var total_shots = 0
var goals_scored = 0
var misses = 0
var tries_per_level = 3

var ball_start_position
var goalie_start_x

var goalie_positions = {
	1: 200,
	2: 400,
	3: 600
}

const CROSSBAR_Y := 50
const BOUNCE_OFFSET := Vector2(-60, 140)
const CROSSBAR_HIT_TIME := 0.20
const BOUNCE_TIME := 0.35
const CROSSBAR_HIT_CHANCE := 0.25

func get_required_goals(level):
	return level

func get_max_shots(level):
	return level + 2

func _ready():
	goalie_start_x = $Goalkeeper.position.x
	$UI/Layout/ButtonLeft.pressed.connect(on_button_left_pressed)
	$UI/Layout/ButtonMiddle.pressed.connect(on_button_middle_pressed)
	$UI/Layout/ButtonRight.pressed.connect(on_button_right_pressed)

	# Initialize labels
	$UI/Layout/ScoreLabel.text = "Score: " + str(goals_scored)
	$UI/Layout/MissesLabel.text = "Misses: " + str(misses)
	$UI/Layout/TriesLabel.text = "Tries: 0 / " + str(tries_per_level)

func on_button_left_pressed():
	shoot(1)

func on_button_middle_pressed():
	shoot(2)

func on_button_right_pressed():
	shoot(3)

func shoot(player_choice):
	var goalie_choice = randi() % 3 + 1
	total_shots += 1

	var goalie_target_x = goalie_positions[goalie_choice]
	var tween_goalie = get_tree().create_tween()
	tween_goalie.tween_property($Goalkeeper, "position:x", goalie_target_x, 0.3)

	var target_x = $Ball.position.x
	if player_choice == 1:
		target_x = 200
	elif player_choice == 2:
		target_x = 400
	elif player_choice == 3:
		target_x = 600

	var target_y = 0
	var hit_crossbar = randf() < CROSSBAR_HIT_CHANCE

	if player_choice == goalie_choice:
		$UI/Layout/MessageLabel.text = "SAVED!"
		target_y = 150
		misses += 1
	elif hit_crossbar:
		$UI/Layout/MessageLabel.text = "HIT THE CROSSBAR!"
		target_y = CROSSBAR_Y
		misses += 1
	else:
		$UI/Layout/MessageLabel.text = "GOAL!"
		goals_scored += 1
		target_y = 80

	var tween = get_tree().create_tween()
	tween.tween_property($Ball, "position", Vector2(target_x, target_y), 0.3)

	await get_tree().create_timer(0.6).timeout
	$Ball.position = Vector2(499, 310)  

	#
	$UI/Layout/ScoreLabel.text = "Score: " + str(goals_scored)
	$UI/Layout/MissesLabel.text = "Misses: " + str(misses)
	$UI/Layout/TriesLabel.text = "Tries: " + str(total_shots) + " / " + str(tries_per_level)

	
	var required_goals = get_required_goals(current_level)
	var max_shots = get_max_shots(current_level)
	
	if goals_scored >= required_goals:
		$UI/Layout/MessageLabel.text = "Level " + str(current_level) + " Complete!"
		current_level += 1
		goals_scored = 0
		misses = 0
		total_shots = 0
		tries_per_level += 2  
	elif total_shots >= max_shots:
		$UI/Layout/MessageLabel.text = "Try Again! Level " + str(current_level)
		goals_scored = 0
		misses = 0
		total_shots = 0
