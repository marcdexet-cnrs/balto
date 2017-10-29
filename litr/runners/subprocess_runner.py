import json
import shlex
import asyncio

from litr.runners.base import BaseRunner

async def _read_stream(stream, cb):
    while True:
        line = await stream.readline()
        if line:
            await cb(line)
        elif stream.at_eof():
            break


class SubprocessRunnerSession(BaseRunner):

    async def run(self):
        cmd, args = self.command

        final_cmd = "%s %s" % (cmd, shlex.quote(args))

        await self.launch_cmd(final_cmd)

    async def read_line(self, line):
        # Remove \n and/or whitespace only lines
        line = line.strip()

        if not line:
            return

        decodedline = line.decode('utf-8')
        try:
            data = json.loads(decodedline)
        except json.JSONDecodeError:
            print("Invalid line", repr(decodedline))
            return

        await self.event_emitter.emit(data)

    async def launch_cmd(self, cmd):
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.working_directory,
            loop=self.loop
        )

        await asyncio.gather(
            _read_stream(process.stdout, self.read_line),
            _read_stream(process.stderr, self.read_line)
        )

        return await process.wait()
