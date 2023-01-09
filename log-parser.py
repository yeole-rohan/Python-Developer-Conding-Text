import sys

# Parse the input file and return a list of tuples (time, username, action)
def parse_input(input_path):
  with open(input_path, 'r') as f:
    lines = f.readlines()
  records = []
  for line in lines:
    parts = line.strip().split(" ")
    if len(parts) == 3 and parts[1].isalnum() and (parts[2].lower()=='end' or parts[2].lower()=='start'):
      records.append((parts[0], parts[1], parts[2]))
  return records

# Calculate the duration of the sessions in seconds
def calculate_durations(records, users, result, user_session):
  
  # Loop through User list
  for user in users:
    time_list = []
    session_counter = 0
    # Loop through filtered records 
    for record in records:
      # check current user
      if record[1] == user:
        # Check action
        if record[2].lower() == "start":
          # User session starts, so add this time to list and keep doing so untill we find end for same user
          time_list.append(record[0])
          # Increment session by one, every time start found
          session_counter +=1
        elif record[2].lower() == "end":
          # for same user id found end, assign it to end_time, start time becomes first record in file, considering no start time provided.
          end_time = record[0]
          start_time = records[0][0]
          # If we already found start record for this user
          if len(time_list) > 0:
            # if start time exists, pop out as we already have session end time
            start_time = time_list.pop()
          else:
            # increase the counter by 1
            session_counter +=1
          # calculate session time with start and end time in sec

          session_time = time_to_seconds(end_time) - time_to_seconds(start_time)
          # assign back time to result dict
          result[user] = result[user]+ session_time
    # update session counter value to session dict  
    user_session[user] = session_counter
  # Return result dict
  return result

  # Convert a time string in the format HH:MM:SS to a number of seconds
def time_to_seconds(time_str):
    if time_str:
        parts = time_str.split(':')
        # retrun time in seconds
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

def get_users(records, result):
  userlist = []
  for r in records:
    if r[1] not in userlist:
      userlist.append(r[1])
      result[r[1]] = 0
  return userlist


def main():
  input_path = sys.argv[1]
  result = {}
  user_session = {}
  # parse the input file
  records = parse_input(input_path)
  # User dict
  users = get_users(records, result)
  # Calculate duration of session according to data
  calculate_durations(records, users, result,user_session)
  # Printing data in rwquired format
  for username in result:
    print(f"{username} {user_session[username]} {int(result[username])}")
    
if __name__ == '__main__':
    main()