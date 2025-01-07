import aioconsole
import json


from whirlpool.washer import Washer


async def show_washer_menu(w: Washer, manager: "ApplicationsManager"):
    def print_menu():
        print("\n")
        print(30 * "-", "MENU", 30 * "-")
        print("u. Update status from server")
        print("p. Print status")
        print("v. Print raw status")
        print("c. Custom command")
        print("q. Exit")
        print(67 * "-")

    def print_status(w: Washer):
        print("online: " + str(w.get_online()))
        print("state: " + str(w.get_machine_state()))
        print("sensing: " + str(w.get_cycle_status_sensing()))
        print("filling: " + str(w.get_cycle_status_filling()))
        print("soaking: " + str(w.get_cycle_status_soaking()))
        print("washing: " + str(w.get_cycle_status_washing()))
        print("rinsing: " + str(w.get_cycle_status_rinsing()))
        print("spinning: " + str(w.get_cycle_status_spinning()))

    def attr_upd():
        print("Attributes updated")

    w.register_attr_callback(attr_upd)

    await manager.connect()

    loop = True
    while loop:
        print_menu()
        choice = await aioconsole.ainput("Enter your choice: ")

        if choice == "p":
            print_status(w)
        elif choice == "u":
            await w.fetch_data()
            print_status(w)
        elif choice == "v":
            print(json.dumps(w.data, indent=4, sort_keys=True, default=str))
        elif choice == "c":
            cmd = aioconsole.ainput("Command: ")
            val = aioconsole.ainput("Value: ")
            await w.set_value(cmd, val)
        elif choice == "q":
            print("Bye")
            loop = False
        else:
            print("Wrong option selection. Enter any key to try again..")

    await manager.disconnect()
