import discord
from discord.ext import commands
import os
from moviepy.editor import *
from dotenv import load_dotenv

from google_drive_upload import GoogleDriveUploader

load_dotenv()

intents = discord.Intents.default()

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

uploader = GoogleDriveUploader()


@client.event
async def on_ready():
    print("The bot is now ready for use!")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, I'm a bot")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == "hi":
        await message.channel.send('👋🏻 Hello!')

    if message.attachments and message.content == "!montage":
        video_clips = []
        video_clips_name = []
        await message.channel.send('🎥 Processing')
        for attachment in message.attachments:
            if attachment.filename.endswith((".mp4", ".avi", ".mov")):
                # Get the current working directory
                current_directory = os.getcwd()

                # Create the "downloads" directory if it doesn't exist
                downloads_directory = os.path.join(
                    current_directory, "downloads")
                os.makedirs(downloads_directory, exist_ok=True)

                # Specify the full path for saving downloaded files
                filename = os.path.join(
                    downloads_directory, attachment.filename)
                await attachment.save(filename)
                video_clips.append(VideoFileClip(filename))
                video_clips_name.append(filename)

        if video_clips:
            # Create a montage using MoviePy
            final_montage = concatenate_videoclips(video_clips)
            file_name = "{}-{}.mp4".format(message.author, message.id)

            # Export the montage
            final_montage.write_videofile(file_name)

            # Send the montage back to the Discord channel
            # await message.channel.send(file=discord.File("montage.mp4"))

            # Upload a photo using the uploader object
            web_view_link = uploader.upload_photo(
                file_name, file_name)
            await message.channel.send('🧑‍🎓 Done! Get your montage here: https://drive.google.com/drive/folders/1mrMHlVH70fR6tl6zHajOpYstKNPc_l0b')

            # Clean up downloaded files
            for clip in video_clips:
                clip.close()

            for file in video_clips_name:
                os.remove(file)

            os.remove(file_name)

client.run(os.getenv('TOKEN'))
