import function as md

def main():
    while True:   
        try:
            print('----- Welcome to JB Garage Used Car System -----')
            Choice = input('''    1.Add Car
    2.Update Car
    3.Delete Car
    4.View Car
    5.Exit
    Enter : ''')
            print('------------------------------------------------')

            if Choice not in ['1','2','3','4','5']:
                print(' Error: ValueError!!')
                continue  

        except ValueError:
            print(' Error ValueError!!')
            continue

        match Choice:
            case '1':
                md.Add()
            case '2':
                md.Update()
            case '3':
                md.Delete()
            case '4':
                while True:
                    try:
                        view_choice = input('''    
    1.Single Car
    2.All Cars
    3.Filter
    4.Car not sale + Summary
    5.Sold Car (with customer + Summary)
    6.Exit
    Enter : ''')
                        print('------------------------------------------------')
                        if view_choice in ['1','2','3','4','5']:
                            md.View(int(view_choice))
                        elif view_choice == '6': 
                            break
                        else:
                            print(' Error: ValueError!!')
                            print('------------------------------------------------')
                    except ValueError:
                        print(' Error: ValueError!!')
            case '5': 
                print(' Thank you for using JB Garage Used Car System')
                break

if __name__ == '__main__':
    main()
