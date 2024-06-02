Each of the folders corresponds to a different match specified in the folder name. For example, "random team search vs safest/" was a 100-game match between our SearchBot and Pmariglia's SafestBot, with randomly generated teams for every battle. 



Each folder has a record log (named something like "record-same-team-vs-safest.log"), which has "W" characters representing a win for SearchBot and "L" characters representing a loss. For the data analysis, count the W's and L's to find our bot's winrates in the matches. Visualize the winrate for each match (with a pie chart or something).



To extract additional data, look at the individual log files for each battle in a match:

A) To figure out how many times our bot ran out of time, search for the string "|-message|SearchBot lost due to inactivity.". This is important for the report because one of our main issues was the search taking too long.

B) To determine the score (the number of Pokemon on the winning team that were knocked out by the loser):
    1. Look for "|player|p1|SearchBot" or "|player|p2|SearchBot" to determine whether our bot was p1 or p2. 
    2. Look for "W: 1	L: 0" or "W: 0	L: 1" to determine whether our bot won or lost the battle. 
    3. Look for "|faint|p1" or "|faint|p2" to determine how many Pokemon fainted on each side. The loser should have 6 Pokemon fainted, and the winner should have between 0 and 5 fainted.
    4. Record the scores for each battle. For example, if SearchBot won a battle with 4 Pokemon fainted, then you could write "4, 6" to a scores file to represent SearchBot losing 4 Pokemon and the opponent losing 6.
    5. Visualize the scores for each of the folders (histogram of scores, average score in a win, average score in a loss, etc.).

