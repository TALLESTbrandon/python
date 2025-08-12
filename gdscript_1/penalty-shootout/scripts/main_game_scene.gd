extends Node2D

var current_level = 1
var total_shots = 0
var goals_scored = 0 

var ball_start_position
var goalie_start_x

var goalie_positions = {
	1: 200,
	2: 400,
	3: 600
}

func get_required_goals(level):
	return level

func get_max_shots(level):
	return level + 2

func _ready():
	goalie_start_x = $Goalkeeper.position.x
	$UI/Layout/ButtonLeft.pressed.connect(on_button_left_pressed)
	$UI/Layout/ButtonMiddle.pressed.connect(on_button_middle_pressed)
	$UI/Layout/ButtonRight.pressed.connect(on_button_right_pressed)

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
	if player_choice == goalie_choice:
		$UI/Layout/MessageLabel.text = "SAVED!"
		target_y = 150
	else:
		$UI/Layout/MessageLabel.text = "GOAL!"
		goals_scored += 1
		target_y = 80

	var tween = get_tree().create_tween()
	tween.tween_property($Ball, "position", Vector2(target_x, target_y), 0.3)

	await get_tree().create_timer(0.6).timeout
	$Ball.position = Vector2(499, 310)  # Reset ball to middle position

	var required_goals = get_required_goals(current_level)
	var max_shots = get_max_shots(current_level)

	if goals_scored >= required_goals:
		$UI/Layout/MessageLabel.text = "Level " + str(current_level) + " Complete!"
		current_level += 1
		goals_scored = 0
		total_shots = 0
	elif total_shots >= max_shots:
		$UI/Layout/MessageLabel.text = "Try Again! level " + str(current_level)
		goals_scored = 0
		total_shots = 0
