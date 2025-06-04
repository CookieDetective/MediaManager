from manager.CommandRouter import CommandRouter
from manager.media_manager import MediaManager  # Your main manager class

def main():
    print("This is the media manager CLI")
    print("Type 'exit' to quit.\n")

    manager = MediaManager()  # Handles Gmail, Calendar, Contacts, etc.
    router = CommandRouter(manager)

    while True:
        try:
            user_input = input("What do you want to do? > ").strip()
            if user_input.lower() in ('exit', 'quit'):
                print("👋 Goodbye!")
                break

            if user_input:
                router.route(user_input)

        except KeyboardInterrupt:
            print("\n👋 Exiting on keyboard interrupt.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()