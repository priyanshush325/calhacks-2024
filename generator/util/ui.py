import os
import subprocess


def startUI(uiPort, projectPort):

    # save the current directory
    with open("./generator/ui/.env", "w") as f:
        f.write(f"VITE_PROJECT_URL=http://localhost:{projectPort}")

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
