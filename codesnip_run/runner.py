import copy
import logging
import os
import time
import shlex
import signal
import subprocess
import threading

import TexSoup
import TexSoup.utils
import yaml

from . import screenshot

LOGGER = logging.getLogger(__name__)

def find_codesnips(soup):
    return [c for c in soup.find_all('codesnip')]

def pop_comments(node):
    comments = []
    for e in node.contents:
        if (isinstance(e, TexSoup.utils.TokenWithPosition)
            and e.startswith('%')):
            comments.append(e.lstrip('%'))
            node.expr.remove_content(e)
    return comments
    #return yaml.load('\n'.join(comments))

def compile_codesnip(codesnip):
    comments = pop_comments(codesnip)
    variable_dict = yaml.load('\n'.join(comments))

    output = []
    for t in codesnip.contents:
        if (isinstance(t, TexSoup.data.TexNode)
            and t.name == 'variable'):
            output.append(str(variable_dict.get(t.string)))
        else:
            output.append(str(t))
    return '\n'.join(output)

def get_command(codesnip):
    comments = pop_comments(codesnip)
    v_dict = yaml.load('\n'.join(comments))
    if v_dict is not None:
        for e in codesnip.children:
            if e.name == 'variable':
                try:
                    e.replace(v_dict[e.string])
                except KeyError:
                    pass

    #cmd = [str(c).strip() for c in codesnip.contents]
    cmd = ' '.join([str(c).strip() for c in codesnip.contents])
    LOGGER.debug('command tokens = %s', shlex.split(cmd))
    return cmd

def runner_thread(cmd, stop_event, out_queue=None):
    #https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        preexec_fn=os.setpgrp
    )
    LOGGER.debug('process=%s', vars(process))
    LOGGER.debug('pgid=%s', os.getpgid(process.pid))

    stdout_lines = []
    while process.poll() == None:
        try:
            stdout, stderr = process.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            pass
        else:
            stdout_lines.append(stdout)
            LOGGER.debug(stdout.decode('utf-8'))

        if stop_event.is_set():
            active_win = screenshot.active_window_info()
            LOGGER.debug('process=%s, active_win=%s', process.args, active_win)
            screenshot.grab(
                win['geometry']['Y'], win['geometry']['X'],
                win['geometry']['Width'], win['geometry']['Height'],
                1,
                '{}.png'.format(process.pid))
            LOGGER.debug('killing process=%s', process.args)
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)

    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    LOGGER.debug('process=%s return=%s', process.args, return_code)
    #if out_queue:
    #    out_queue.append(stdout_lines)

def run_command(command):
    screenshot_name = "{}_{:03d}.png"
    runner_stop_event = threading.Event()
    runner = threading.Thread(name='runner_thread',
                              target=runner_thread,
                              args=(command, runner_stop_event))
    runner.start()
    i = 0
    cmd0 = shlex.split(command)[0]
    while runner.is_alive():
        i += 1
        active_win = screenshot.active_window_info()
        LOGGER.debug("(%d)", i)
        #LOGGER.debug("(%d) %s %s", i, active_win['app'], active_win['title'])
        time.sleep(1.0)
        if i > 1:
            runner_stop_event.set()

def main():
    import argparse
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument(dest='tex_file', type=argparse.FileType('r'))
    parser.add_argument('-v', '--verbose', dest='verbosity', action='count')
    args = parser.parse_args()

    soup = TexSoup.TexSoup(args.tex_file)
    for codesnip in find_codesnips(soup):
        command = get_command(codesnip)
        run_command(command)


if __name__ == "__main__":
    main()
