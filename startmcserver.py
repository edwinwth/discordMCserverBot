import subprocess
from subprocess import PIPE
import os
import time

class MCServer():
    process = None
    executable = ''
    minecraft_dir = ""
    def __init__(self):
        self.process = None
        self.executable = 'java -Xms2G -Xmx4G -jar craftbukkit-1.15.1-R0.1-SNAPSHOT.jar java nogui' #Arguments for java to initiate server,CHANGE minRam,maxRam,name of server.jar to your own preference
        self.minecraft_dir = "D:\Minecraft Server\craftbukkit"  #Minecraft server directory,CHANGE TO WHERE YOUR SERVER.JAR IS LOCATED

    def server_command(cmd):   ##Passes cmd argument into server's input stream
        cmd = cmd + '\n'
        cmd = cmd.encode("utf-8")
        print(cmd)
        self.process.stdin.write(cmd)
        self.process.stdin.flush()

    def server_stop(self):  #Stops server instance
        if(self.process is not None):
            self.process.communicate("stop".encode("utf-8"))
            self.process.kill()
            self.process = None
        else:
            print("No Server Running.")

    def server_start(self): #Starts the server instance
        if(self.process is None):
            os.chdir(self.minecraft_dir)
            self.process = subprocess.Popen(self.executable,stdin=PIPE)
            print("Server started.")
        else:
            print("Server already running.")