from enum import Enum

import discordtool

bot = discordtool.Bot(debug_guilds=[...])
connections = {}


class Sinks(Enum):
    mp3 = discordtool.sinks.MP3Sink()
    wav = discordtool.sinks.WaveSink()
    pcm = discordtool.sinks.PCMSink()
    ogg = discordtool.sinks.OGGSink()
    mka = discordtool.sinks.MKASink()
    mkv = discordtool.sinks.MKVSink()
    mp4 = discordtool.sinks.MP4Sink()
    m4a = discordtool.sinks.M4ASink()


async def finished_callback(sink, channel: discordtool.TextChannel, *args):
    recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
    await sink.vc.disconnect()
    files = [
        discordtool.File(audio.file, f"{user_id}.{sink.encoding}")
        for user_id, audio in sink.audio_data.items()
    ]
    await channel.send(
        f"Finished! Recorded audio for {', '.join(recorded_users)}.", files=files
    )


@bot.command()
async def start(ctx: discordtool.ApplicationContext, sink: Sinks):
    """Record your voice!"""
    voice = ctx.author.voice

    if not voice:
        return await ctx.respond("You're not in a vc right now")

    vc = await voice.channel.connect()
    connections.update({ctx.guild.id: vc})

    vc.start_recording(
        sink.value,
        finished_callback,
        ctx.channel,
    )

    await ctx.respond("The recording has started!")


@bot.command()
async def stop(ctx: discordtool.ApplicationContext):
    """Stop recording."""
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        del connections[ctx.guild.id]
        await ctx.delete()
    else:
        await ctx.respond("Not recording in this guild.")


bot.run("TOKEN")
