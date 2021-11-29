from auth_server import *

from KDC import *

def determine_choice(choice):
    if choice == 'A':
        data = input("Enter client Name: ")
        msgA, msgB = init(data)
        print(f'Authentication Server Reply: {msgA}:{msgB}')
    if choice == "SR":
        data = input("Enter message C and D seperated by space: ").split()
        msgC = data[0]
        msgD = data[1]
        msgE, msgF = handle_serviceRequest(msgC, msgD)

        print(f'TGT Server Reply: {msgE}:{msgF}')
        

if __name__ == '__main__':
    while True:
        print('##################\n\
Server Running\n\
##################')
        print("Choose an option:\n\
        A : for authentication\n\
        SR: For Service Request\n\
        exit to exit")
        choice = input()
        if choice == "exit":
            break
        else:
            determine_choice(choice)
