import main

color = main.Color()

print(color.ORANGE+"""░▒█▀▀█░▄▀▀▄░▄▀▀▄░█▀▀▀░█░░█▀▀░░░▒█▀▄▀█░█▀▀░█▀▀░█▀▀░█▀▀▄░█▀▀▀░█▀▀░█▀▀░░░▒█▀▀▄░▒█░░░░▀█▀
░▒█░▄▄░█░░█░█░░█░█░▀▄░█░░█▀▀░░░▒█▒█▒█░█▀▀░▀▀▄░▀▀▄░█▄▄█░█░▀▄░█▀▀░▀▀▄░░░▒█░░░░▒█░░░░▒█░
░▒█▄▄▀░░▀▀░░░▀▀░░▀▀▀▀░▀▀░▀▀▀░░░▒█░░▒█░▀▀▀░▀▀▀░▀▀▀░▀░░▀░▀▀▀▀░▀▀▀░▀▀▀░░░▒█▄▄▀░▒█▄▄█░▄█▄""" + color.RESET)


if __name__ == "__main__":
    main.initialize()
    while True:
        option = int(input((f"{color.CYAN}\nSelect an option:\n1.Send a SMS\n2.Read SMS from a specific contact\n3.List of Recent Messages\n4.Exit{color.RESET}{color.YELLOW}\n\n[+]Enter the following number to select an option: {color.RESET}")))
        if option == 1:
            number = input(f"{color.CYAN}\n[+]Enter the phone number [i.e. +91987654321]: {color.RESET}")
            message = input(f"{color.CYAN}\n[+]Enter the message: {color.RESET}")
            main.findContact(number)
            main.sendMessage(message)
            print(f"{color.GREEN}\n[+]Message sent successfully!{color.RESET}")

        elif option == 2:
            number = input(f"{color.CYAN}\n[+]Enter the phone number [i.e. +91987654321]: {color.RESET}")
            main.findContact(number)
            for io in main.readMessage():
                main.print_message(io)
            print(f"{color.GREEN}\n[+]Message read successfully!{color.RESET}")

        elif option == 3:
            main.getConvosList()
            print(f"{color.GREEN}\n[+]List of recent messages fetched successfully!{color.RESET}")

        elif option == 4:
            print(f"{color.RED}\n[+]Exiting...{color.RESET}")
            main.close()
            exit()

        else:
            print(f"{color.RED}\n[+]Invalid option!{color.RESET}")
        print("-"*60)
