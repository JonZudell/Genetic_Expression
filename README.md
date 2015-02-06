# Genetic_Expression
This is a pet project a coworker and I developed after reading this article http://thedailywtf.com/articles/genderize

Initially we were perplexed as to the reason someone would do try to guess a users gender based upon their name.
What started to concern us more was how accurate the "algorithm" was at determining gender based upon name. So we found a
dataset(http://www.ssa.gov/OACT/babynames/limits.html) of names and occurence and ran the algorithm against it. These are
the results

Correct Guesses: 258522673
Incorrect Guesses: 74895097
Total Guesses 333417770

It evaluated in ~11.352 seconds with an ~77% accuracy.

Naturally we wanted to out do him. We start by assuming the name is male and if we find a match our pseudo-randomly with
the psuedo-randomly generated regular expression we assume its female. Here are the results of the most recent run.

RE : (nah|rah|jo|ys|ifer|uz|ndy|beth|mn|igh|yn|mmer|ber|cy|tal|ril|say|zy|nn|vy|sy|nay|udy|any|i|ko|e|a|ty|iny|idy|men|lah|ly|gy|yah|eah|mah|tay|fy|gen|ail|eny|kah|bil|nn|ren|ten|wny|dah|tny)$
Correct Guesses : 2955175
Incorrect Guesses : 488278
Total Occurences : 3443453
Fitness Score : 1.70744686895
% Accuracy : 0.858201055743

The data thats been tested against is yob1980.txt file found at the above url.

We'll be making updates in the future even though this project is certainly pointless.
