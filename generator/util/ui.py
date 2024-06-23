import os
import subprocess


def startUI(uiPort, projectPort):

    # save the current directory
    with open("./generator/ui/.env", "w") as f:
        f.write(f"VITE_PROJECT_URL=http://localhost:{projectPort}\n")
        f.write(f"VITE_SERVER_URL=http://localhost:5000")

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


def startProjectServer(webServerAbsolute, sourceDirectory, projectPort):

    if not os.path.exists("./generator-logs"):
        os.mkdir("./generator-logs")
    if not os.path.exists(webServerAbsolute):
        with open(webServerAbsolute, 'w') as f:
            f.write("")
    originalDirectory = os.getcwd()
    os.chdir(args.directory)
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
