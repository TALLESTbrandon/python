import random
countries =[
  {"name":"France","continent": "Europe"},
  {"name":"United States of America","continent": "North America"},
  {"name":"England","continent": "Europe"},
  {"name":"Germany","continent": "Europe"},
  {"name":"Guatemala","continent": "Central America"},
  {"name":"Mexico","continent": "North America"},
  {"name":"Ecuador","continent": "South America"},
  {"name":"Switerland","continent": "Europe"},
  {"name":"Japan","continent": "Asia"},
  {"name":"Columbia","continent": "South America"},
  {"name":"Brazil","continent": "South America"},
  {"name":"India","continent": "Asia"},
  {"name":"Canada","continent": "North America",}
  ]
secret =  random.choice(countries)
print("I'm thinking of a country. Try and guess which one!")
print(f"Hint: It's in {secret['continent']}")
print(f"Hint: It starts with the letter '{secret['name'][0]}'")
guess = ""
tries = 0
while guess != secret:
    guess = input("Your guess: ").strip().title()
    tries += 1
    print("Not quite, try again tho.")    
if guess == secret:
    print(f" Nice job you got it! It was {secret}. You got it in {tries} tries.")
   