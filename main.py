import runpy
while True:
    try:
        file_globals = runpy.run_path("gass.py")
    except Exception as error:
        print(error)









