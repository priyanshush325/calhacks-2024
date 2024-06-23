import os
import subprocess

UI_STARTED = False
PROJECT_SERVER_STARTED = False


def startUI(uiPort, projectPort):
    global UI_STARTED

    if UI_STARTED:
        print("UI already started")
        return

    print(f"Starting UI on port {uiPort}")

    # save the current directory
    with open("./generator/ui/.env", "w") as f:
        f.write(f"VITE_PROJECT_URL=http://localhost:{projectPort}\n")
        f.write(f"VITE_SERVER_URL=http://127.0.0.1:5000")

    # start the UI
    cwd = os.getcwd()
    os.chdir("./generator/ui")

    command = f"npm run dev -- --port {uiPort}"
    command += f" 2>/dev/null"
    command += f" 1>/dev/null"
    command += f" < /dev/null &"
    process = subprocess.Popen(
        command,
        shell=True,
        text=True
    )

    os.chdir(cwd)

    UI_STARTED = True


def startProjectServer(webServerAbsolute, sourceDirectory, projectPort):
    global PROJECT_SERVER_STARTED

    if PROJECT_SERVER_STARTED:
        print("Project server already started")
        return

    print(f"Starting project server on port {projectPort}")

    if not os.path.exists("./generator-logs"):
        os.mkdir("./generator-logs")
    if not os.path.exists(webServerAbsolute):
        with open(webServerAbsolute, 'w') as f:
            f.write("")
    originalDirectory = os.getcwd()
    os.chdir(sourceDirectory)
    command = f"npm run dev -- --port {projectPort}"
    command += f" 2>{webServerAbsolute}"
    command += f" 1>{webServerAbsolute}"
    command += f" < /dev/null &"
    process = subprocess.Popen(
        command,
        shell=True,
        text=True
    )
    os.chdir(originalDirectory)
    PROJECT_SERVER_STARTED = True
