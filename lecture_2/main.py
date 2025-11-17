def generate_profile(age: int):
    if age < 0: return "-"
    if age <= 12: return "Child"
    if age <= 19: return "Teenager" 
    return "Adult"
         
def profile_summary(dictionary: dict):
    print("-"*3)
    print("Profile Summary:")
    for key,value in dictionary.items():
        if key == "Hobbies":
            if value:
                print(f"Favorite Hobbies({len(value)}):")
                for i in value:
                    print(f"- {i}")  
            else:
                print("You didn't mention any hobbies")
        else:    
            print(f"{key}: {value}")
    print("-"*3)        

def main():
    user_name = input("Enter your full name: ")  
    birth_year_str = input("Enter your birth year: ")
    birth_year = int(birth_year_str)
    current_age = 2025 - birth_year
    hobbies = []
    while (hobby := input("Enter a favorite hobby or type 'stop' to finish: ")).lower() != "stop":
        hobbies.append(hobby)
    life_stage = generate_profile(current_age) 
    user_profile={"Name": user_name, 
                  "Age": current_age,
                  "Life Stage": life_stage,
                  "Hobbies": hobbies }
    profile_summary(user_profile)

main()