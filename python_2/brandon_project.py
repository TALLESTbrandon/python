
import tkinter as tk
import random

NAVY = "#071426"
PANEL = "#EAF4FF"
BLUE = "#1677D2"
LIGHT_BLUE = "#000000"
WHITE = "#000000"
BUTTON_TEXT = "#FFFFFF"
GREEN = "#168A50"
RED = "#D93030"

STARTING_LIVES = 5
COINS_PER_CORRECT_ANSWER = 5
SECOND_HINT_COST = 5
THIRD_HINT_COST = 10
RESULTS_FILE = "game_results.txt"

countries_by_level = {
    "easy": [
        "Canada", "Japan", "Brazil", "Argentina", "Spain",
        "Portugal", "England", "France", "India", "Colombia",
        "United States"
    ],
    "medium": [
        "Albania", "Chad", "Croatia", "Chile", "Guatemala",
        "New Zealand", "Switzerland", "Bosnia and Herzegovina",
        "Bolivia", "Haiti"
    ],
    "hard": [
        "Tanzania", "Senegal", "Mauritius", "Azerbaijan",
        "Democratic Republic of the Congo", "Montenegro",
        "Kazakhstan", "Armenia", "Algeria", "Denmark"
    ]
}

country_hints = {
    "Canada": ["It is in North America.", "Its capital is Ottawa.", "It starts with C."],
    "Japan": ["It is in Asia.", "Its capital is Tokyo.", "It starts with J."],
    "Brazil": ["It is in South America.", "Its capital is Brasília.", "It starts with B."],
    "Argentina": ["It is in South America.", "Its capital is Buenos Aires.", "It starts with A."],
    "Spain": ["It is in Europe.", "Its capital is Madrid.", "It starts with S."],
    "Portugal": ["It is in Europe.", "Its capital is Lisbon.", "It starts with P."],
    "England": ["It is part of the United Kingdom.", "Its capital is London.", "It starts with E."],
    "France": ["It is in Europe.", "Its capital is Paris.", "It starts with F."],
    "India": ["It is in Asia.", "Its capital is New Delhi.", "It starts with I."],
    "Colombia": ["It is in South America.", "Its capital is Bogotá.", "It starts with C."],
    "United States": ["It is in North America.", "Its capital is Washington, D.C.", "It starts with U."],
    "Albania": ["It is in Europe.", "Its capital is Tirana.", "It starts with A."],
    "Chad": ["It is in Africa.", "Its capital is N'Djamena.", "It starts with C."],
    "Croatia": ["It is in Europe.", "Its capital is Zagreb.", "It starts with C."],
    "Chile": ["It is in South America.", "Its capital is Santiago.", "It starts with C."],
    "Guatemala": ["It is in Central America.", "Its capital has the same name as the country.", "It starts with G."],
    "New Zealand": ["It is in Oceania.", "Its capital is Wellington.", "It starts with N."],
    "Switzerland": ["It is in Europe.", "Its capital is Bern.", "It starts with S."],
    "Bosnia and Herzegovina": ["It is in Europe.", "Its capital is Sarajevo.", "It starts with B."],
    "Bolivia": ["It is in South America.", "It has two capital cities.", "It starts with B."],
    "Haiti": ["It is in the Caribbean.", "Its capital is Port-au-Prince.", "It starts with H."],
    "Tanzania": ["It is in Africa.", "Its capital is Dodoma.", "It starts with T."],
    "Senegal": ["It is in Africa.", "Its capital is Dakar.", "It starts with S."],
    "Mauritius": ["It is an island country in the Indian Ocean.", "Its capital is Port Louis.", "It starts with M."],
    "Azerbaijan": ["It is in the Caucasus region.", "Its capital is Baku.", "It starts with A."],
    "Democratic Republic of the Congo": ["It is in Central Africa.", "Its capital is Kinshasa.", "It starts with D."],
    "Montenegro": ["It is in Europe.", "Its capital is Podgorica.", "It starts with M."],
    "Kazakhstan": ["It is in Central Asia.", "Its capital is Astana.", "It starts with K."],
    "Armenia": ["It is in the Caucasus region.", "Its capital is Yerevan.", "It starts with A."],
    "Algeria": ["It is in North Africa.", "Its capital is Algiers.", "It starts with A."],
    "Denmark": ["It is in Europe.", "Its capital is Copenhagen.", "It starts with D."]
}


def calculate_accuracy(correct, total):
    if total == 0:
        return 0
    return round((correct / total) * 100)


def load_previous_results():
    results = []

    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as results_file:
            while True:
                line = results_file.readline()

                if line == "":
                    break

                results.append(line.strip())

    except FileNotFoundError:
        print("No previous game results found.")

    except OSError as error:
        print(f"Could not read game results: {error}")

    else:
        print("Previous game results loaded successfully.")

    finally:
        print("Finished loading game results.")

    return results


previous_results = load_previous_results()


class EarthBackground:

    def __init__(self, window, filename):
        self.window = window
        self.frames = []
        self.delays = []
        self.frame_index = 0

        self.background_label = tk.Label(
            window,
            bg=NAVY,
            bd=0
        )

        self.background_label.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        try:
            from PIL import Image, ImageTk, ImageSequence

            gif = Image.open(filename)

            for frame in ImageSequence.Iterator(gif):
                resized = frame.convert("RGB").resize(
                    (600, 550),
                    Image.Resampling.LANCZOS
                )

                self.frames.append(ImageTk.PhotoImage(resized))

                delay = frame.info.get("duration", 100)
                self.delays.append(max(delay, 40))

            if self.frames:
                self.animate()

        except Exception as error:
            print(f"Earth background unavailable: {error}")

    def animate(self):
        if not self.frames:
            return

        self.background_label.config(
            image=self.frames[self.frame_index]
        )

        delay = self.delays[self.frame_index]

        self.frame_index = (
            self.frame_index + 1
        ) % len(self.frames)

        self.window.after(delay, self.animate)


selected_difficulty = ""
current_country = ""
remaining_countries = []

score = 0
coins = 0
total_coins_earned = 0
lives = STARTING_LIVES
hints_used = 0
wrong_answers = 0

answer_locked = False
result_saved = False


def show_modes():
    welcome_frame.place_forget()

    mode_frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )


def return_home():
    game_over_frame.place_forget()
    mode_frame.place_forget()
    game_frame.place_forget()

    welcome_frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )


def choose_difficulty(level):
    global selected_difficulty
    global remaining_countries
    global score, coins, total_coins_earned, lives
    global wrong_answers, result_saved

    selected_difficulty = level

    remaining_countries = countries_by_level[level].copy()

    score = 0
    coins = 0
    total_coins_earned = 0
    lives = STARTING_LIVES
    wrong_answers = 0
    result_saved = False

    mode_frame.place_forget()

    game_frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    difficulty_label.config(
        text=f"{level.capitalize()} Mode"
    )

    feedback_label.config(text="")

    update_stats()
    new_country()


def update_stats():
    score_label.config(text=f"⭐ Score: {score}")
    coins_label.config(text=f"🪙 Coins: {coins}")
    lives_label.config(text=f"❤️ Lives: {lives}")


def new_country():
    global current_country, hints_used, answer_locked

    if lives <= 0:
        end_game("You ran out of lives!")
        return

    if len(remaining_countries) == 0:
        end_game("You completed the entire round!")
        return

    current_country = random.choice(remaining_countries)
    remaining_countries.remove(current_country)

    hints_used = 0
    answer_locked = False

    hint_label.config(text="")
    hint_button.config(text="USE HINT", state="normal")

    question_label.config(text="Guess the country!")

    answer_entry.config(state="normal")
    answer_entry.delete(0, tk.END)

    submit_button.config(state="normal")
    next_button.config(state="disabled")

    feedback_label.config(text="")

    progress_label.config(
        text=f"Countries remaining: {len(remaining_countries) + 1}"
    )


def check_answer():
    global score, coins, total_coins_earned, lives
    global wrong_answers, answer_locked

    if answer_locked:
        return

    guess = answer_entry.get().strip()

    if guess == "":
        feedback_label.config(
            text="Please enter a country!",
            fg=RED
        )
        return

    if guess.lower() == current_country.lower():
        score += 1
        coins += COINS_PER_CORRECT_ANSWER
        total_coins_earned += COINS_PER_CORRECT_ANSWER

        feedback_label.config(
            text="Correct! You earned 5 coins!",
            fg=GREEN
        )

    else:
        lives -= 1
        wrong_answers += 1

        feedback_label.config(
            text=f"Incorrect! The answer was {current_country}.",
            fg=RED
        )

    answer_locked = True

    answer_entry.config(state="disabled")
    submit_button.config(state="disabled")
    hint_button.config(state="disabled")
    next_button.config(state="normal")

    update_stats()


def next_country():
    if answer_locked:
        new_country()


def use_hint():
    global hints_used, coins

    if answer_locked:
        return

    if hints_used >= 3:
        hint_label.config(text="You have used all 3 hints!")
        return

    if hints_used == 1:
        if coins < SECOND_HINT_COST:
            hint_label.config(text="You need 5 coins for this hint!")
            return

        coins -= SECOND_HINT_COST

    elif hints_used == 2:
        if coins < THIRD_HINT_COST:
            hint_label.config(text="You need 10 coins for this hint!")
            return

        coins -= THIRD_HINT_COST

    hint_label.config(
        text=country_hints[current_country][hints_used]
    )

    hints_used += 1

    hint_button.config(
        text=f"USE HINT ({hints_used}/3)"
    )

    update_stats()


def save_game_result():
    accuracy = calculate_accuracy(score, score + wrong_answers)

    result = (
        f"Difficulty: {selected_difficulty.capitalize()} | "
        f"Score: {score} | "
        f"Accuracy: {accuracy}% | "
        f"Coins remaining: {coins} | "
        f"Total coins earned: {total_coins_earned}"
    )

    try:
        with open(RESULTS_FILE, "a", encoding="utf-8") as results_file:
            results_file.write(result + "\n")

    except OSError as error:
        save_status_label.config(
            text="Could not save your results.",
            fg=RED
        )
        print(f"File error: {error}")

    else:
        save_status_label.config(
            text="Your results were saved!",
            fg=GREEN
        )
        print("Game results saved successfully.")

    finally:
        print("Finished saving game results.")


def end_game(message):
    global result_saved

    game_frame.place_forget()

    game_over_message.config(text=message)

    accuracy = calculate_accuracy(score, score + wrong_answers)

    final_score_label.config(
        text=f"Final Score: {score}"
    )

    final_coins_label.config(
        text=f"Coins Remaining: {coins}"
    )

    total_earned_label.config(
        text=f"Total Coins Earned: {total_coins_earned}"
    )

    accuracy_label.config(
        text=f"Accuracy: {accuracy}%"
    )

    if not result_saved:
        save_game_result()
        result_saved = True

    game_over_frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )


def make_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 13, "bold"),
        bg=BLUE,
        fg=BUTTON_TEXT,
        activebackground="#3195ED",
        activeforeground=BUTTON_TEXT,
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=9
    )


window = tk.Tk()

window.title("Country Guesser")
window.geometry("600x550")
window.resizable(False, False)
window.configure(bg=NAVY)

earth_background = EarthBackground(window, "earth.gif")


welcome_frame = tk.Frame(
    window,
    bg=PANEL,
    padx=35,
    pady=25
)

title_label = tk.Label(
    welcome_frame,
    text="🌎 COUNTRY GUESSER",
    font=("Arial", 25, "bold"),
    bg=PANEL,
    fg=WHITE
)
title_label.pack(pady=20)

welcome_message = tk.Label(
    welcome_frame,
    text="A WORLD OF COUNTRIES AWAITS",
    font=("Arial", 11, "bold"),
    bg=PANEL,
    fg=LIGHT_BLUE
)
welcome_message.pack(pady=10)

if previous_results:
    previous_message = f"Previous result: {previous_results[-1]}"
else:
    previous_message = "No previous games saved yet."

previous_results_label = tk.Label(
    welcome_frame,
    text=previous_message,
    font=("Arial", 9),
    bg=PANEL,
    fg=LIGHT_BLUE,
    wraplength=400
)
previous_results_label.pack(pady=8)

play_button = make_button(
    welcome_frame,
    "PLAY",
    show_modes
)
play_button.pack(pady=25)

welcome_frame.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


mode_frame = tk.Frame(
    window,
    bg=PANEL,
    padx=45,
    pady=25
)

mode_title = tk.Label(
    mode_frame,
    text="CHOOSE YOUR MODE",
    font=("Arial", 22, "bold"),
    bg=PANEL,
    fg=WHITE
)
mode_title.pack(pady=20)

easy_button = make_button(
    mode_frame,
    "EASY",
    lambda: choose_difficulty("easy")
)
easy_button.pack(pady=8, fill="x")

medium_button = make_button(
    mode_frame,
    "MEDIUM",
    lambda: choose_difficulty("medium")
)
medium_button.pack(pady=8, fill="x")

hard_button = make_button(
    mode_frame,
    "HARD",
    lambda: choose_difficulty("hard")
)
hard_button.pack(pady=8, fill="x")


game_frame = tk.Frame(
    window,
    bg=PANEL,
    padx=25,
    pady=15
)

difficulty_label = tk.Label(
    game_frame,
    text="",
    font=("Arial", 21, "bold"),
    bg=PANEL,
    fg=WHITE
)
difficulty_label.pack(pady=8)

stats_frame = tk.Frame(
    game_frame,
    bg=PANEL
)
stats_frame.pack(pady=8)

score_label = tk.Label(
    stats_frame,
    text="⭐ Score: 0",
    font=("Arial", 11, "bold"),
    bg=PANEL,
    fg=WHITE
)
score_label.pack(side="left", padx=8)

coins_label = tk.Label(
    stats_frame,
    text="🪙 Coins: 0",
    font=("Arial", 11, "bold"),
    bg=PANEL,
    fg=LIGHT_BLUE
)
coins_label.pack(side="left", padx=8)

lives_label = tk.Label(
    stats_frame,
    text="❤️ Lives: 5",
    font=("Arial", 11, "bold"),
    bg=PANEL,
    fg=WHITE
)
lives_label.pack(side="left", padx=8)

progress_label = tk.Label(
    game_frame,
    text="",
    font=("Arial", 10),
    bg=PANEL,
    fg=LIGHT_BLUE
)
progress_label.pack(pady=5)

question_label = tk.Label(
    game_frame,
    text="Guess the country!",
    font=("Arial", 16, "bold"),
    bg=PANEL,
    fg=WHITE
)
question_label.pack(pady=12)

answer_entry = tk.Entry(
    game_frame,
    font=("Arial", 14),
    justify="center",
    bg="#FFFFFF",
    fg=NAVY,
    relief="flat"
)
answer_entry.pack(pady=10, ipady=7)

submit_button = make_button(
    game_frame,
    "SUBMIT ANSWER",
    check_answer
)
submit_button.pack(pady=7)

hint_button = make_button(
    game_frame,
    "USE HINT",
    use_hint
)
hint_button.pack(pady=7)

hint_label = tk.Label(
    game_frame,
    text="",
    font=("Arial", 11),
    bg=PANEL,
    fg=LIGHT_BLUE,
    wraplength=420
)
hint_label.pack(pady=8)

feedback_label = tk.Label(
    game_frame,
    text="",
    font=("Arial", 11, "bold"),
    bg=PANEL,
    fg=WHITE,
    wraplength=420
)
feedback_label.pack(pady=5)

next_button = make_button(
    game_frame,
    "NEXT COUNTRY",
    next_country
)
next_button.pack(pady=7)

next_button.config(state="disabled")


game_over_frame = tk.Frame(
    window,
    bg=PANEL,
    padx=40,
    pady=30
)

game_over_title = tk.Label(
    game_over_frame,
    text="GAME OVER",
    font=("Arial", 28, "bold"),
    bg=PANEL,
    fg=WHITE
)
game_over_title.pack(pady=15)

game_over_message = tk.Label(
    game_over_frame,
    text="",
    font=("Arial", 13),
    bg=PANEL,
    fg=LIGHT_BLUE
)
game_over_message.pack(pady=10)

final_score_label = tk.Label(
    game_over_frame,
    text="",
    font=("Arial", 14, "bold"),
    bg=PANEL,
    fg=WHITE
)
final_score_label.pack(pady=8)

final_coins_label = tk.Label(
    game_over_frame,
    text="",
    font=("Arial", 13),
    bg=PANEL,
    fg=LIGHT_BLUE
)
final_coins_label.pack(pady=5)

total_earned_label = tk.Label(
    game_over_frame,
    text="",
    font=("Arial", 13),
    bg=PANEL,
    fg=GREEN
)
total_earned_label.pack(pady=5)

accuracy_label = tk.Label(
    game_over_frame,
    text="",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=WHITE
)
accuracy_label.pack(pady=5)

save_status_label = tk.Label(
    game_over_frame,
    text="",
    font=("Arial", 10),
    bg=PANEL,
    fg=GREEN
)
save_status_label.pack(pady=5)

home_button = make_button(
    game_over_frame,
    "RETURN HOME",
    return_home
)
home_button.pack(pady=20)


window.bind("<Return>", lambda event: check_answer())

window.mainloop()
