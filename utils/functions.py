import subprocess
from utils.bcolors import Bcolors


# print colored text
def print_c(text, style, newLine=False):
    if newLine:
        print(style + text + Bcolors.ENDC, end='')
    else:
        print(style + text + Bcolors.ENDC)


def send_message(text):
    subprocess.Popen(['notify-send', text])


# get ping of server
def ping(server='example.com', count=1, wait_sec=1):
    cmd = "ping -c {} -W {} {}".format(count, wait_sec, server).split(' ')
    try:
        output = subprocess.check_output(cmd).decode().strip()
        lines = output.split("\n")
        total = lines[-2].split(',')[3].split()[1]
        loss = lines[-2].split(',')[2].split()[0]
        timing = lines[-1].split()[3].split('/')
        return {
            'type': 'rtt',
            'min': timing[0],
            'avg': timing[1],
            'max': timing[2],
            'mdev': timing[3],
            'total': total,
            'loss': loss,
        }
    except Exception as e:
        # print(e)
        return False