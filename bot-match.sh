# this script makes the Search Bot battle against each of the other bots


# run the loop inside a subshell with SIGINT killing so that all bot matches can be killed with ctrl-c
# (see https://stackoverflow.com/a/52033580)
(trap 'kill 0' SIGINT;

for battle_bot in safest most_damage; do

  # search bot vs. battle bot: random battles with random teams each time
  for i in {1..100}; do
    python3 bot_match.py -e env --log-record logs/record-rand-team-vs-$battle_bot.log &
    python3 bot_match.py -e env_$battle_bot &
    wait
  done

  # search bot vs. battle bot: battles with the same team
  for i in {1..100}; do
    python3 bot_match.py -e env_specificteam --log-record logs/record-same-team-vs-$battle_bot.log &
    python3 bot_match.py -e env_specificteam_$battle_bot &
    wait
  done

done
)
