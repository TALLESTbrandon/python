extends Node2D
func _ready():
	$ButtonLeft.pressed.connect(on_button_left_pressed)
	$ButtonMiddle.pressed.connect(on_button_middle_pressed)
	$ButtonRight.pressed.connect(on_button_middle_pressed) 
