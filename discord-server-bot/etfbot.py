import subprocess
import discord
import asyncio

TIMEOUT_SECONDS = 5
POLL_INTERVAL = 10
PLAYER_COUNT = 0
TOKEN = "insert_token_here"
CHANNEL_ID = 253602720634634240
client = discord.Client()

async def poll():
    #print("poll!")
    try:
        res = subprocess.run(['/usr/bin/quakestat', '-P', '-q3s', 'etf.tunk.org:27960'], timeout=TIMEOUT_SECONDS, stdout=subprocess.PIPE)
        if res.returncode == 0:
            notifyChange = False
            tmp = res.stdout.decode('utf-8').splitlines()
            server = tmp[1].split()
            curPlayers = 0
            try:
                curPlayers = int(server[1].split('/')[0])
            except Exception as e:
                print("Exception: ", str(e))
                await asyncio.sleep(POLL_INTERVAL)
                asyncio.ensure_future(poll())
            mapname = server[3]
            players = ""

            global PLAYER_COUNT
            if PLAYER_COUNT == curPlayers:
                #print("no change in player count")
                await asyncio.sleep(POLL_INTERVAL)
                asyncio.ensure_future(poll())
                return

            PLAYER_COUNT = curPlayers
            
            for i in range(0, int(curPlayers)):
                #print("test: " + tmp[2 + i].split())
                players += " ".join(tmp[2 + i].split()[3:])
                if i != curPlayers - 1:
                    players += ", "

            status = ""
            if curPlayers > 0:
                status = "etf.tunk.org, map " + mapname + ", player count " + str(curPlayers) + ": " + players
            else:
                status = "etf.tunk.org, map " + mapname + ", server empty"
            print(status)
            await client.get_channel(CHANNEL_ID).send(status)
        else:
            print("error: ", res.returncode)
        await asyncio.sleep(POLL_INTERVAL)
        asyncio.ensure_future(poll())
        return
    except Exception as e:
        print('Poll func exception: ', str(e))
        await asyncio.sleep(POLL_INTERVAL)
        asyncio.ensure_future(poll())
        return

@client.event
async def on_ready():
    print("on_ready")
    try:
        await poll()
    except Exception as e:
        print("Exception: ", str(e))


client.run(TOKEN)
