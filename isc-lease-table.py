#!/usr/bin/env python

import re
from datetime import datetime as dt

with open("w/dhcpd/dhcpd2.leases", "r") as file:
  file_content = file.read()

file_content = re.sub(r"#.*\n(\n)?|server-duid.+;\n", r'', file_content) # Remove comment and 'server-duid'
lease_logs   = [ fc for fc in re.split(r"\n}\n*", file_content) ]        # Split entries by lease-IP section

logs = []
for lease_log in lease_logs:
  log_entries = re.split(";\n| {\n", lease_log) # Split entry by line
  log_entries = [ re.sub(r"^(\n)?\s+|;$", r'', log_entry) for log_entry in log_entries ] # Format value (Remove ';' and space)

  tmp = {}
  for log_entry in log_entries:
    if log_entry == '':
      continue

    key = log_entry.split(" ")[0]
    val = ' '.join(log_entry.split(" ")[1:])
    tmp[key] = val

  logs.append(tmp)

def format_text(target, length):
  text_len = len(target)
  if text_len > length:
    return target[0:text_len]
  else:
    return target + " "*(length - text_len)

label_text_len = {
  "lease": 15,
  "starts": 25,
  "ends": 25,
  "tstp": 25,
  "clct": 25,
  "binding": 13,
  "hardware": 30,
  "uid": 30,
  "client-hostname": 30,
}

ENABLE_LABELS = ["lease", "starts", "ends", "hardware", "client-hostname"]

# Print LABEL
for label in ENABLE_LABELS:
  print(format_text(target=label, length=label_text_len[label]), end='')
print()

# Print VALUE
for log in logs:
  tmp = ''
  for label in ENABLE_LABELS:

    # TODO: 日付の比較をして現在、リリース中か判定する。
    if label == 'ends':
      try:
        log_date = dt.strptime(log[label], '%w %Y/%m/%d %H:%M:%S')
      except:
        break
      if log_date < dt.now():
        tmp = ''
        break

    try:
      tmp += format_text(target=log[label], length=label_text_len[label])
    except KeyError:
      continue

  if tmp != '':
    print(tmp)

