from fabric.api import *

env.user = 'fds'
env.password='1470319289'
env.hosts = ['192.168.15.129']


def deploy():
    workspace_dir = "~/workspace/StreamRecorder"
    code_dir = "~/workspace/StreamRecorder/src"
    with settings(warn_only=True):
        if run("test -d {}".format(workspace_dir)).failed:
            run("mkdir -p {}".format(workspace_dir))

    with settings(warn_only=True):
        with cd(workspace_dir):
            if run("test -d {}".format(code_dir)).failed:
                run("git clone --branch dev https://github.com/FortuneDayssss/StreamRecorder.git {}".format(code_dir))
                run("mkdir -p video log")
    with cd(code_dir):
        run("git pull origin dev")
    with cd(code_dir + "/docker"):
        run("docker-compose up")


