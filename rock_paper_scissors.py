import random 
done=False
wins,loses,ties=0,0,0
names={"R":"Rock","P":"paper","S":"scissors"}
while not done:
    choice=input('Provide your next move(R,P,S)&(Q to Quit):\t')
    cpu_choice=random.choice(["R",'P',"S"])
    if choice =="R":
        if cpu_choice=='P':
            print(f"CPU wins! You chose{names[choice]},the CPU chose {names[cpu_choice]}.")
            loses=+1
        else:
            print(f'You win! You chose {names[choice]},the CPU chose {names[cpu_choice]}.')   
            wins=+1
        pass 
    elif choice=='P':
        if cpu_choice=="S":
            print(f"CPU wins! You chose{names[choice]},the CPU chose {names[cpu_choice]}.")   
            loses=+1
        else:
            print(f'You win! You chose {names[choice]},the CPU chose {names[cpu_choice]}.')   
            wins=+1
    elif choice=='S':
        if cpu_choice=="R":
           print(f"CPU wins! You chose{names[choice]},the CPU chose {names[cpu_choice]}.")   
           loses=+1
        else:
            print(f'You win! You chose {names[choice]},the CPU chose {names[cpu_choice]}.')   
            wins=+1
    elif choice==cpu_choice:
        print(f'Its a tie! You both choice {names[choice]}')
        ties=+1
    elif choice=='Q':
        print("Scared is it!")
        done=True
    else:
        print("invalid command")
print("Current stats are Wins:",wins,"Loses:",loses,"tied:",ties,"\t")
    
