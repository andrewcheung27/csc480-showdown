# this script makes the SearchBot battle against the MostDamageBot where each team has a Gyarados.
# the goal is to show our bot's abilities in a basic and consistent way,
# as well as integration with the local Pokemon Showdown server, for a live demo.
# our bot should set up while the other bot attacks, and win.


# run the loop inside a subshell with SIGINT killing so that all bot matches can be killed with ctrl-c
# (see https://stackoverflow.com/a/52033580)
(trap 'kill 0' SIGINT;
  battle_bot=most_damage
  # search bot vs. battle bot: battles with the same team
  for i in {1..1}; do
    python3 bot_match.py -e env_specificteam -t gen5/gyara-1v1 --log-record logs/record-gyara-1v1-vs-$battle_bot.log &
    python3 bot_match.py -e env_specificteam_$battle_bot -t gen5/gyara-1v1 &
    wait
  done
)
