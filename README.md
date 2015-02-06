# Genetic_Expression

## Usage
Currently we have not made ease of use a priority however if you decide you want to play with it. You will have to edit re_ga.py directly. The file will run as is, provided you point the generate dataset function at a file that can be obtained here http://www.ssa.gov/OACT/babynames/limits.html . It has currently only been tested for python version 2.7.2 . If you're up to it you can modify the strategy function in the my pool class.


## Inspiration
This is a pet project a coworker and I developed after reading this article http://thedailywtf.com/articles/genderize

Initially we were perplexed as to the reason someone would do try to guess a users gender based upon their name.
What started to concern us more was how accurate the "algorithm" was at determining gender based upon name. So we found a dataset of names and occurence and ran the algorithm against it. These are
the results

|Parameters       | Numbers   |
|-----------------|:---------:|
|Correct Guesses  | 258522673 |
|Incorrect Guesses| 74895097  |
|Total Occurences | 333417770 |
|% Accuracy       | ~0.775    |

It evaluated in ~11.352 seconds with an ~77% accuracy.

Naturally we wanted to out do him. We start by assuming the name is male and if we find a match our pseudo-randomly with
the psuedo-randomly generated regular expression we assume its female. Here are the results of the most recent run.
```regex
RE : (nah|rah|jo|ys|ifer|uz|ndy|beth|mn|igh|yn|mmer|ber|cy|tal|ril|say|zy|nn|vy|sy|nay|udy|any|i|ko|e|a|ty|iny|idy|men|lah|ly|gy|yah|eah|mah|tay|fy|gen|ail|eny|kah|bil|nn|ren|ten|wny|dah|tny)$
```
|Parameters       | Numbers   |
|-----------------|:---------:|
|Correct Guesses  | 2955175   |
|Incorrect Guesses| 488278    |
|Total Guesses    | 3443453   |
|% Accuracy       | 0.858201055743|

The data thats been tested against is yob1980.txt file found at the above url.

We'll be making updates in the future even though this project is certainly pointless.
