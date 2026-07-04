from time import sleep

import globalvars


def attend():
    sleep(1)
    globalvars.read_for_new_connetion_lock.release()

    while not globalvars.kill_now:
        sleep(0.5)
