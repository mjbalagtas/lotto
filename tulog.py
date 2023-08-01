from entry import Entry
from entry import Entries
import time 
import os

timestr = time.strftime("%m_%d_%Y")

basedir = "C:/Users/mjmba/Documents/lotto-v3/"
senders = ["agustin", "bryan", "agustin_palaban", "bryan_palaban"]
all_entries = []
all_tulog = []
for sender in senders:
  try:
    filename = os.path.abspath(f"{basedir}input/{timestr}_{sender}.txt")
  except FileNotFoundError:
    print("file not found...")
    no_file = input("Press enter to exit...")
    break
  writefile_tulog = os.path.abspath(f"{basedir}tulog/{timestr}__tulog_{sender}.txt")
  entries = Entries(filename, 49)
  entries.process_file()
  entries.set_prev_tulog()
  entries.set_tulog()
  entries.write_tulog(writefile_tulog, sender)
  # tulog = entries.get_tulog()
  # print(f"{filename} tulog: {tulog}")

# for entries in all_entries:
#   tulog = entries.get_tulog()
#   all_tulog.append(tulog)
