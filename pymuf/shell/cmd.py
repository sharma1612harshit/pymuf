import subprocess
import logging

logger = logging.getLogger(__name__)

class Cmd(object):
    def __init__(self, command):
        self.command = command
        self.std_out, self.std_err = ''

    def run(self, realtime=False, suppress_warning=False):
        proc = subprocess.Popen(
            self.command,
            shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if realtime:
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                logger.info(message=line.decode('utf-8'))
                self.std_out += line.decode('utf-8')

            while True:
                line = proc.stderr.readline()
                if not line:
                    break
                self.std_err += line.decode('utf-8')

        else:
            self.std_out = proc.stdout.read().decode('utf-8')
            self.std_err = proc.stderr.read().decode('utf-8')

        if (not suppress_warning) and self.std_err:
            raise Exception(self.std_err)

    def stdout(self):
        return self.std_out

    def stderr(self):
        return self.std_err
