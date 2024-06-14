import runpy
import datetime
print("starting file...")
while True:
    try:
        file_globals = runpy.run_path("gass.py")
    except Exception as error:
        print()
        with open("error_logs.txt", "a") as e:
            now = datetime.datetime.now()
            error_message = f"{error} - {now.strftime('%I:%M %p, %d/%m/%Y, %A.')}\n"
            e.write(error_message)
