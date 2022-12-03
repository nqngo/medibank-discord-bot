import interactions
import os
import subprocess
import time


rg_bin = "rg"
rg_init_param = "-iINz"
rg_init_threads = "8"
rg_glob1 = "!confluence-exports/**"
rg_glob2 = "!*.7z"
rg_dir = "/mnt/data/"

rg_param = "-i"
wc_ps = ["wc", "-l"]

def _ripgrep(term, process=None):
  """Run ripgrep against the process pipe"""
  if process is None:
      cmd = [rg_bin, rg_init_param, "--glob", rg_glob1, "--glob", rg_glob2,
             "-j", rg_init_threads, term, rg_dir]
      print(' '.join(cmd))
      ps = subprocess.run(cmd, capture_output=True)
      return ps.stdout
  cmd = [rg_bin, rg_param, term]
  ps = subprocess.run(cmd, input=process, capture_output=True)
  return ps.stdout


def _wc(process):
  """Return the count on how many times it appear."""
  ps = subprocess.run(wc_ps, input=process, capture_output=True)
  return ps.stdout.decode("UTF-8").strip()


async def search(term1, term2=None, term3=None, term4=None, term5=None):
  """Search the right info."""
  start = time.time()
  print("----------------------------")
  print(f"Query: {term1} {term2} {term3} {term4} {term5}")
  n = _ripgrep(term1)
  if term2:
    n = _ripgrep(term2, n)
  if term3:
    n = _ripgrep(term3, n)
  if term4:
    n = _ripgrep(term4, n)
  if term5:
    n = _ripgrep(term5, n)
  result = _wc(n)
  finished = time.time() - start
  print(f"Found {result} results.")
  print("Query takes {:.2f} seconds.".format(finished)) 
  print("----------------------------")
  return result


bot = interactions.Client(os.environ.get['DISCORD_TOKEN'])

@bot.event
async def on_ready():
  """Check the bot status."""
  print(f"We're online! We've logged in as {bot.me.name}.")
  print(f"Our latency is {round(bot.latency)} ms.")


@bot.command(
  name="amipwned",
  description="Search Medibank leaked csvs. Use email, name, DoB...",
  scope=os.environ.get['DISCORD_GUILDS'].split(', '),
  options = [
    interactions.Option(
      name="term",
      description="The term to search.",
      type=interactions.OptionType.STRING,
      required=True,
    ),
    interactions.Option(
      name="term2",
      description="Another term in to search.(AND join)",
      type=interactions.OptionType.STRING,
      required=False,
    ),
    interactions.Option(
      name="term3",
      description="Another term in to search.(AND join)",
      type=interactions.OptionType.STRING,
      required=False,
    ),
    interactions.Option(
      name="term4",
      description="Another term in to search.(AND join)",
      type=interactions.OptionType.STRING,
      required=False,
    ),
    interactions.Option(
      name="term5",
      description="Another term in to search.(AND join)",
      type=interactions.OptionType.STRING,
      required=False,
    ),
  ],
)
async def amipwned(ctx: interactions.CommandContext,
  term: str, term2=None, term3=None, term4=None, term5=None):
  """Search the Medibank data for your info."""
  await ctx.defer()
  msg = await ctx.send("Searching the database dump...")
  result = await(search(term, term2, term3, term4, term5))
  await ctx.send(f"<@{ctx.author.user.id}> Your terms appear {result} times in the Medibank leak!")


bot.start()

