import re
class Entry:
  def __init__(self, id:int, line:str, lotto:int):
    self.__is_correct_format = True
    line = line.strip()
    parts = re.split("[^0-9]", line)
    parts=[i for i in parts if i!= ""]
    if len(parts) > 0 and len(parts) != 4:
      self.__is_correct_format = False
    if self.__is_correct_format:
      for i in range(3):
        if int(parts[i]) < 1 or int(parts[i]) > lotto:
          self.__is_correct_format = False
        if self.__is_correct_format == False:
          break
      if self.__is_correct_format:
        if int(parts[3]) % 5 != 0:
          self.__is_correct_format = False
      if self.__is_correct_format:
        if int(parts[0]) == int(parts[1]) or int(parts[0]) == int(parts[2]) or int(parts[1]) == int(parts[2]):
          self.__is_correct_format = False

    self.__combination = []
    self.__bet = 0
    if self.__is_correct_format:
      self.__combination = list(map(int, parts[:3]))
      self.__combination = sorted(self.__combination)
      self.__bet = int(parts[3])
    self.__winner = False
    self.__balik_taya = False
    self.__valid_bet = self.__bet
    self.__line = line
    self.__id = id

  def get_id(self):
    return self.__id

  def get_line(self):
    return self.__line

  def set_valid_bet(self, limit: int):
    if int(self.__bet) > limit:
      self.__valid_bet = limit
    else:
      self.__valid_bet = int(self.__bet)
  
  def get_valid_bet(self):
    return self.__valid_bet
  
  def get_combination(self):
    return self.__combination
  
  def get_orig_bet(self):
    return self.__bet
  
  def is_correct_format(self):
    return self.__is_correct_format
  
  def is_winner(self, winning_number: list):
    points = 0
    for number in winning_number:
      for entry in self.__combination:
        if int(entry) == int(number):
          points += 1

    if points >= 3:
      self.__winner = True
      return True
    else:
      self.__winner = False
      return False
    
  def is_balik_taya(self, winning_number: list):
    points = 0
    for number in winning_number:
      for entry in self.__combination:
        if int(entry) == int(number):
          points += 1

    if points == 2:
      self.__balik_taya = True
      return True
    else:
      self.__winner = False
      return False
    
  def is_same_entry(self, other_entry):
    same = 0
    for number in self.__combination:
      for other_number in other_entry.get_combination():
        if number == other_number:
          same += 1
          break
    if same == 3:
      return True
    return False

  def winner(self):
    return self.__winner
  
  def balik_taya(self):
    return self.__balik_taya
  
  def wrong_input(self):
    return f"Error @ Line {self.__id}: {self.__line} - Wrong input"
  
  def __str__(self):
    return f"Line {self.__id}:{self.__line} -- Entry:[{self.__combination} = {self.__bet}] -- is Valid entry: {self.__is_correct_format}"

class Entries:
  def __init__(self, lotto_format):
    self.__entries = []
    self.__lotto_format = lotto_format
    self.__tulog = []
    self.__prev_tulog = []

  def process_file(self, filename:str, entries:list):
    count = 0
    with open(filename, encoding="utf8") as my_file:
      for line in my_file:
        count += 1
        if line == "\n" or line == "" or line == " ":
          continue
        parts = re.split("[^0-9]", line)
        parts=[i for i in parts if i!= ""]
        if parts == []:
          continue

        entry = Entry(count, line, self.__lotto_format)

        if entry.is_correct_format():
          entries.append(entry)
        else:
          print(f"{entry.wrong_input()} in {filename}")

  def set_limit(self, limit: int):
    for entry in self.__entries:
      entry.set_valid_bet(limit)

  def set_entries(self, entries):
    self.__entries = entries

  def get_entries(self):
    return self.__entries
  
  def get_filename(self):
    return self.__filename
  
  def set_prev_tulog(self, entries):
    self.__prev_tulog = entries

  def set_tulog(self):
    for i in range(len(self.__entries) - 1):
      tulog_group = []
      tulog_group = [self.__entries[i].get_line()]
      for j in range(i+1,len(self.__entries)):
        # print(i, j)
        if self.__entries[i].is_same_entry(self.__entries[j]):
          # print(f"{self.__entries[i].get_line()} is the same as {self.__entries[j].get_line()}")
          tulog_group.append(self.__entries[j].get_line())
      if len(tulog_group) >= 2:
      
        self.__tulog.append(tulog_group)
        # print(self.__tulog)

    print(self.__tulog)

  def get_tulog(self):
    return self.__tulog

  def write_tulog(self, filename, sender):
    with open(filename, "w") as my_file:
      my_file.write(f"Latest update double entry\n")
      my_file.write(f"TULOG ENTRIES: {sender}\n\n")
      print(self.__tulog)
      print("\n\n")
      print(self.__prev_tulog)
      for i, j in zip(self.__tulog, self.__prev_tulog):
        for curr in i:
          my_file.write(curr)
          new = True
          for prev in j:
            if curr == prev:
              new = False
              break
          if new:
            my_file.write(" **")
          my_file.write(f"\n")
        my_file.write("\n")
# def main():
#   entries = ["mac balagtas","1 2 3 60", " 05 5 17 10", "14-13-12-10", "1 2 3", "1 90 11 20", "1 2 3 1"]
#   winning_number = [1, 2, 3, 4, 5, 6]

#   for i in range(len(entries)):
#     entry = Entry(i, entries[i], 49)
#     entry.set_valid_bet(10)
#     print(entry)

# main()
      