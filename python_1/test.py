import random
#this is the list of all the countrys.
countries = [
  {"name":"France","continent": "Europe"},
  {"name":"United States of America","continent": "North America"},
  {"name":"England","continent": "Europe"},
  {"name":"Germany","continent": "Europe"},
  {"name":"Guatemala","continent": "Central America"},
  {"name":"Mexico","continent": "North America"},
  {"name":"Ecuador","continent": "South America"},
  {"name":"Switzerland","continent": "Europe"},
  {"name":"Japan","continent": "Asia"},
  {"name":"Colombia","continent": "South America"},
  {"name":"Brazil","continent": "South America"},
  {"name":"India","continent": "Asia"},
  {"name":"Canada","continent": "North America"}
]

secret = random.choice(countries)

print("I'm thinking of a country. Try and guess which one!")
print(f"Hint: It's in {secret['continent']}")
print(f"Hint: It starts with the letter '{secret['name'][0]}'")
# this shows how much tries the player takes
guess = ""
tries = 0

while guess != secret["name"]:
    guess = input("Your guess: ").strip().title()
    tries += 1
#Below this message is my custom message. What this does is reuse the lines of code by a singular sentence of code.
    def secret_guesser():

        if guess == secret["name"]:
            print(f" Nice job, you got it! It was {secret['name']}. You got it in {tries} tries.")
        else:
            print(" Not quite, try again tho.")
    secret_guesser()