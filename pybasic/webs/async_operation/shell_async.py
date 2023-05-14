import asyncio
import time

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
    return 'finished'

async def main():
    return await asyncio.gather(
        run('sleep 2; echo "world"'),
        run('sleep 1; echo "hello"'),
        run('ls /zzz'))


async def fun_a():
    print(f'hello start: {time.time()}')
    await asyncio.sleep(3)
    print(f'------hello end : {time.time()} ----')

async def fun_b():
    print(f"world start: {time.time()}")
    await asyncio.sleep(2)
    print(f'------world end : {time.time()} ----')

# 通过创建 task 方法
async def main_create_task():
    print('start main:')
    task1 = asyncio.create_task(fun_a())
    task2 = asyncio.create_task(fun_b())
    await task1
    await task2
    print('-----------end start----------')


# r = asyncio.run(main())
r = asyncio.run(main_create_task())

print('r', r)
