import aioconsole
import json


from whirlpool.dryer import Dryer


async def show_dryer_menu(d: Dryer, manager: "ApplicationsManager"):
    def print_menu():
        print("\n")
        print(30 * "-", "MENU", 30 * "-")
        print("u. Update status from server")
        print("p. Print status")
        print("v. Print raw status")
        print("m. Print modeled status")
        print("c. Custom command")
        print("q. Exit")
        print(67 * "-")

    def print_status(d: Dryer):
        print(f"online: {d.get_online()}")
        print(f"state: {d.get_machine_state_value()}")
        print(f"door open: " + str(d.get_op_status_dooropen()))
        print(f"est time remaining: " + str(d.get_time_status_est_time_remaining()))
        print(f"extra power changeable: " + str(d.get_change_status_extrapowerchangeable()))
        print(f"steam changeable: " + str(d.get_change_status_steamchangeable()))
        print(f"cycle select: " + str(d.get_change_status_cycleselect()))
        print(f"dryness: " + str(d.get_change_status_dryness()))
        print(f"manual dry time: " + str(d.get_change_status_manualdrytime()))
        print(f"static guard: " + str(d.get_change_status_staticguard()))
        print(f"temperature: " + str(d.get_change_status_temperature()))
        print(f"wrinkle shield: " + str(d.get_change_status_wrinkleshield()))
        print(f"airflow status: " + str(d.get_cycle_status_airflow_status()))
        print(f"cool down: " + str(d.get_cycle_status_cool_down()))
        print(f"damp: " + str(d.get_cycle_status_damp()))
        print(f"drying: " + str(d.get_cycle_status_drying()))
        print(f"limited cycle: " + str(d.get_cycle_status_limited_cycle()))
        print(f"sensing: " + str(d.get_cycle_status_sensing()))
        print(f"static reduce: " + str(d.get_cycle_status_static_reduce()))
        print(f"steaming: " + str(d.get_cycle_status_steaming()))
        print(f"wet: " + str(d.get_cycle_status_wet()))
        print(f"cycle count: " + str(d.get_odometer_status_cycle_count()))
        print(f"running hours: " + str(d.get_odometer_status_running_hours()))
        print(f"total hours: " + str(d.get_odometer_status_total_hours()))
        print(f"isp check: " + str(d.get_wifi_status_isp_check()))
        print(f"rssi antenna diversity: " + str(d.get_wifi_status_rssi_antenna_diversity()))

        print(f"set dryness: " + str(d.get_dryness()))
        print(f"set manual dry time: " + str(d.get_manual_dry_time()))
        print(f"set cycle select: "  + str(d.get_cycle_select()))

    def print_modeled_status(d: Dryer):
        print(f"state: {d.get_machine_state()}")

    def attr_upd():
        print("Attributes updated")

    d.register_attr_callback(attr_upd)

    await manager.connect()

    loop = True
    while loop:
        print_menu()
        choice = await aioconsole.ainput("Enter your choice: ")

        if choice == "p":
            print_status(d)
        elif choice == "u":
            await d.fetch_data()
            print_status(d)
        elif choice == "m":
            print_modeled_status(d)
        elif choice == "v":
            print(json.dumps(d.data, sort_keys=True, indent=4))
        elif choice == "c":
            cmd = await aioconsole.ainput("Command: ")
            val = await aioconsole.ainput("Value: ")
            await d.set_value(cmd, val)
        elif choice == "q":
            print("Bye")
            loop = False
        else:
            print("Wrong option selection. Enter any key to try again..")

    await manager.disconnect()
