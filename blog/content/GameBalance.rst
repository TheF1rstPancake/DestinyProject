Fair and Square
===============================================
:date: 2015-08-30
:modified: 2015-08-30
:tags: Crucible, matchmaking
:authors: Giovanni Briggs
:summary: Examining just how scrupulously devoted to fair play Bungie is
:category: Stat Porn Sunday

See the `original post on reddit <https://www.reddit.com/r/DestinyTheGame/comments/3izh13/stat_porn_sunday_fair_and_square/>`_.

Recap
------
Last week we looked at `fireteam class combinations in Trials <https://www.reddit.com/r/DestinyTheGame/comments/3i3pnl/stat_porn_sunday_trials_of_osiris_character/>`_
and saw that having a Warlock on your team generally increases your chances for winning a Trials match, and having 3 Titans on your team is a *really* bad idea.

Fairness
---------
Last week I said I would be looking more at Trials data in the immediate future.
That was the plan, but for the past couple of weeks I have also been working trying to figure out how combat rating is calculated and how it's used.
While looking into that, I found **a few interesting trends related to the "fairness" of matchmaking**.
I thought that these trends were more interesting than what I was pulling out of the Trials dataset.  I'll save those for another time, but this week we are going to talk about "fairness".  Be aware that I am using **Control** games for this analysis.

Fairness is in quotes because it's one of those words that can be defined in a number of different ways.
One way to examine fairness is to say that, "everyone gets what they deserve".
This isn't terribly helpful from our perspective because "everyone" isn't defined, and there are no clear guidelines for determining what they deserve.
Instead, we need a value that we can calculate that allows us to compare games and say that a given match is fairer than another.
One such calculation is to take the difference in score between teams at the end of a match.

.. plot:: scoreDiff Distribution of Difference in Score between Teams
    :dir: ../pages/fullPlots/combatRating/

This shows us that **14.16%** of games end with a score difference of less than 1,416.
To me, this is a pretty close point margin.  
I would even say that a difference of 5,000 is still a fair match.
Between 5,000 and 8,000 points, one team was clearly running the show and I would say that these matches border into the unfair territory but didn't ruin the fun for everyone.
A change in momentum could have easily brought the scores closer together, and the other team was at least able to spawn and do something.
At 8000 and above I think the game is unfair.
One team clearly was much better than the other and dominated the match.

These are *my* standards for a fair match and are not the only way to define what is and isn't fair.
Under my standards, somewhere around 58% of matches are fair, 29% of matches could have been fairer, and 13% of matches are unfair.

A potential pitfall to this metric is that it measures fairness between teams and considers teams to be representative of the players that make up that team.
If the match was fair between the teams, then the players in that match will view it as fair irregardless of their personal score.
Another metric could be to look at the variance and/or standard deviation of all player scores at the end of the game.  
A small value means that all players had similar scores, which would mean a fair match for players on an individual basis.
However (for the sake of time), I am going to make the assumption that Bungie makes fair matches by creating fair *teams*.

I would then argue that Bungie's matchmaking system does a very good job at creating fair and balanced games.  
Yes, a little over 1 in 10 games you are likely going to get dominated (or dominate), but for the most part, games end with a close enough score difference to keep things interesting.
Of course, my boundaries for fairness and unfairness were chosen based on my experience in the Crucible, but if you reduce the ranges for fair and "could be fairer" matches, your conclusion might differ from mine.

Map Balance
------------
Another fun trend to look at is what the score difference distribution on each *map* is.
This could tell us if certain map are unbalanced one way or the other.

.. plot:: scoreDiffMap Distribution of Difference in Score between Teams on each Map
    :dir: ../pages/fullPlots/combatRating/

For the most part, these maps all have a 50% fair match rate.
A lot of the smaller maps also seem to have a well defined sweet spot.
Thieves' Den  and Firebase Delphi have a spike at the second bucket.  Asylum has its in the third bucket.
Larger maps on the other hand are less predictable and have spikes all over the place.  
Bastion has one spike in the [5600, 7000) bucket, and another one at the [127500, 14000) bin and there isn't a very clean
First Light and Skyshock present similar double spikes which may be another reason why these maps are no longer in Control rotation.

Overall, there isn't any map that particularly stands out but it is interesting to see that the size of the map seems to have an influence on the fairness of the match.

TL;DR:
--------
Bungie's matchmaking system does a fantastic job at creating well balanced and interesting matches.
About 60% of matches end with a score difference less than 5000, 27% of matches end between 5000 and 8000, and only 13% of matches end with a score difference greater than 8000.