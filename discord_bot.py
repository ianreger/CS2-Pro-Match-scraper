import discord
from discord import app_commands
from discord.ext import commands
from subprocess import run
import os


bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

# Program path (use os.path.join for platform independence)
program_path = os.path.join(os.getcwd(), "get_matches.py")  # Replace with your actual file

async def execute_program(program):
    python_exe = "python.exe"  # Path to the Python interpreter
    # Run the program and capture output/errors
    try:
        result = run([python_exe, program], capture_output=True, text=True)
        output, error = result.stdout, result.stderr
    except Exception as e:
        error = f"Error running program: {e}"
        output = ""
    return output, error

@bot.tree.command(name="getgames")
async def get_matches(interaction: discord.Interaction):
  # Execute the program and get output/error
  output, error = await execute_program(program_path)

  # Handle errors or send output
  if error:
    await interaction.response.send_message(error, ephemeral=True)
  else:
    # Optionally format the output (e.g., using code blocks)
    formatted_output = f"`\n{output}\n`"
    await interaction.response.send_message(formatted_output, ephemeral=False)


@bot.event
async def on_ready():
	print("Bot is up and ready!")
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} command(s)")

	except Exception as e:
		print(e)

@bot.tree.command(name="hello")
async def hello(interatcion: discord.Interaction):
	await interatcion.response.send_message(f"Hey {interatcion.user.name}! Nice command you got there.", ephemeral=True)

bot.run('Add token here')
