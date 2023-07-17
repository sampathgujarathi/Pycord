import io

import pydub  # pip install pydub==0.25.1

import discordtool
from discordtool.sinks import MP3Sink

bot = discordtool.Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


async def finished_callback(sink: MP3Sink, channel: discordtool.TextChannel):
    mention_strs = []
    audio_segs: list[pydub.AudioSegment] = []
    files: list[discordtool.File] = []

    longest = pydub.AudioSegment.empty()

    for user_id, audio in sink.audio_data.items():
        mention_strs.append(f"<@{user_id}>")

        seg = pydub.AudioSegment.from_file(audio.file, format="mp3")

        # Determine the longest audio segment
        if len(seg) > len(longest):
            audio_segs.append(longest)
            longest = seg
        else:
            audio_segs.append(seg)

        audio.file.seek(0)
        files.append(discordtool.File(audio.file, filename=f"{user_id}.mp3"))

    for seg in audio_segs:
        longest = longest.overlay(seg)

    with io.BytesIO() as f:
        longest.export(f, format="mp3")
        await channel.send(
            f"Finished! Recorded audio for {', '.join(mention_strs)}.",
            files=files + [discordtool.File(f, filename="recording.mp3")],
        )


@bot.command()
async def join(ctx: discordtool.ApplicationContext):
    """Join the voice channel!"""
    voice = ctx.author.voice

    if not voice:
        return await ctx.respond("You're not in a vc right now")

    await voice.channel.connect()

    await ctx.respond("Joined!")


@bot.command()
async def start(ctx: discordtool.ApplicationContext):
    """Record the voice channel!"""
    voice = ctx.author.voice

    if not voice:
        return await ctx.respond("You're not in a vc right now")

    vc: discordtool.VoiceClient = ctx.voice_client

    if not vc:
        return await ctx.respond(
            "I'm not in a vc right now. Use `/join` to make me join!"
        )

    vc.start_recording(
        MP3Sink(),
        finished_callback,
        ctx.channel,
        sync_start=True,  # WARNING: This feature is very unstable and may break at any time.
    )

    await ctx.respond("The recording has started!")


@bot.command()
async def stop(ctx: discordtool.ApplicationContext):
    """Stop the recording"""
    vc: discordtool.VoiceClient = ctx.voice_client

    if not vc:
        return await ctx.respond("There's no recording going on right now")

    vc.stop_recording()

    await ctx.respond("The recording has stopped!")


@bot.command()
async def leave(ctx: discordtool.ApplicationContext):
    """Leave the voice channel!"""
    vc: discordtool.VoiceClient = ctx.voice_client

    if not vc:
        return await ctx.respond("I'm not in a vc right now")

    await vc.disconnect()

    await ctx.respond("Left!")


bot.run("TOKEN")
