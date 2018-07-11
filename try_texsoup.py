import copy
import time
import shlex
import subprocess
import threading

#import pyautogui
import TexSoup
import TexSoup.utils
import yaml


#pyautogui.PAUSE = 2.5
#pyautogui.FAILSAFE = True

soup = TexSoup.TexSoup(r"""
\begin{document}

\section{Hello \textit{world}.}

\subsection{Watermelon}

(n.) A sacred fruit. Also known as:

\begin{itemize}
\item red lemon
\item life
\end{itemize}

Here is the prevalence of each synonym.

\begin{tabular}{c c}
red lemon & uncommon \\
life & common
\end{tabular}

\begin{codesnip}
    % i: 3
    python -c 'print(\variable{i} * \variable{i} + 1)'
\end{codesnip}

\begin{codesnip}
    echo \variable{y} = \variable{x}^2
\end{codesnip}

\begin{codesnip}
    % file: try_texsoup.py
    git diff \variable{file}
\end{codesnip}

\begin{codesnip}
    mpl_qt
\end{codesnip}

\end{document}
""")


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
    #comments = [e.lstrip('%') for e in c0
    #            if (isinstance(e, TexSoup.utils.TokenWithPosition)
    #                and e.startswith('%'))]
    #variable_dict = yaml.load('\n'.join(comments))
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


def runner_thread(cmd, event):
#def runner_thread(cmd):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)
    #while process.poll() == None or not event.is_set():
    while process.poll() == None:
        out, err = process.communicate()
        print('out=', out.decode('utf-8'))

#compiled = [compile_codesnip(c) for c in find_codesnips(soup)]

cs = find_codesnips(soup)
cs0 = cs[0]
print([type(c) for c in cs0])
print([c for c in cs0])

for codesnip in find_codesnips(soup):
    comments = pop_comments(codesnip)
    v_dict = yaml.load('\n'.join(comments))
    if v_dict is not None:
        for e in codesnip.children:
            if e.name == 'variable':
                try:
                    e.replace(v_dict[e.string])
                except KeyError:
                    pass
    #print(' '.join([str(c).strip() for c in codesnip.contents]))
    #cmd = [str(c).strip() for c in codesnip.contents]
    cmd = ' '.join([str(c).strip() for c in codesnip.contents])
    print(shlex.split(cmd))

    # run in one thread:
    #try:
    #    p = subprocess.Popen(cmd,
    #                         stdout=subprocess.PIPE,
    #                         stderr=subprocess.PIPE,
    #                         shell=True)
    #    out, err = p.communicate()
    #    print(out.decode('utf-8'))
    #except Exception as e:
    #    print(e)

    screenshot_name = "{}_{:03d}.png"
    runner_stop_event = threading.Event()
    runner = threading.Thread(target=runner_thread,
                              args=(cmd, runner_stop_event))
    #runner = threading.Thread(target=runner_thread,
    #                          args=(cmd, ))
    runner.start()
    i = 0
    cmd0 = shlex.split(cmd)[0]
    while runner.is_alive():
        #print(pyautogui.size())
        #pyautogui.screenshot(screenshot_name.format(cmd0, i))
        i += 1
        time.sleep(2.0)
        if i > 1:
            break

    #pyautogui.hotkey('command', 't')

    # in another thread (main thread):
    #while True:
    #    out, err = p.communicate()
    #
    # to communicate with screen use
    # * out
    # * Xlib.disblay.Display (or even pyautogui)

