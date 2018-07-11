import copy
import time
import shlex
import subprocess
import threading

import TexSoup
import TexSoup.utils
import yaml


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
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)
    #while process.poll() == None or not event.is_set():
    while process.poll() == None:
        out, err = process.communicate()
        print(out.decode('utf-8'))
        if event.is_set():
            process.kill()

def active_window_geometry():
    pass

def main():
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

        #cmd = [str(c).strip() for c in codesnip.contents]
        cmd = ' '.join([str(c).strip() for c in codesnip.contents])
        print(shlex.split(cmd))

        screenshot_name = "{}_{:03d}.png"
        runner_stop_event = threading.Event()
        runner = threading.Thread(target=runner_thread,
                                  args=(cmd, runner_stop_event))
        runner.start()
        i = 0
        cmd0 = shlex.split(cmd)[0]
        while runner.is_alive():
            i += 1
            print(i)
            time.sleep(2.0)
            if i > 1:
                runner_stop_event.set()

if __name__ == "__main__":
    main()
