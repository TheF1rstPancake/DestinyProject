Fair and Square
===============================================
:date: 2015-08-30
:modified: 2015-08-30
:tags: Crucible, combat rating
:authors: Giovanni Briggs
:summary: Examining just how Scrupulously devoted to fair play Bungie is
:category: Stat Porn Sunday
:status: draft

Recap
------
Welcome to Stat Porn Sunday.  What do we do here?  We stare with open mouths at graphs and numbers and go full nerd because we can.

Last week we looked at `Trials team class combinations <https://www.reddit.com/r/DestinyTheGame/comments/3i3pnl/stat_porn_sunday_trials_of_osiris_character/>`_
and saw that having a Warlock on your team greatly increases your chances for winning a Trials match, and having 3 Titans on your team is a *really* bad idea.

Fairness
---------
Last week I said I would be looking more at Trials data.  
That was the plan, but for the past couple of weeks I have been working on how combat rating is calculated.
While looking into what makes combat rating work and how it is calculated I found **a few interesting trends related to the "fairness" of matchmaking**.
I thought that these trends were more interesting than what I was pulling out of the Trials dataset.  I'll save those for another time, but this week we are going to talk about "fairness".  Note that I am using **Control** games for this analysis.

Fairness is in quotes because it's one of those words that can be defined in a number of different ways.
One way to examine fairness is to say that, "everyone gets what they deserve".
This isn't terribly helpful from our perspective because everyone isn't defined, and there is no clear guidelines for determing what they deserve.
Instead, we need a figure that we can calculate that allows us to compare games and say that one is more fair than another.
One such calculation is to take the difference in score between teams at the end of a match.

.. plot:: scoreDiff Distribution of Difference in Score between Teams
    :dir: ../pages/fullPlots/combatRating/

This shows us that **19.1%** of games end with a score difference of less than 1,416.
To me, this is a pretty close point margin.  I would even say that a difference of 5,000 is still a fair match.
At 3,000 I would say those are decisive victories, but I wouldn't say that they are unfair.
A turn in momentum for the other team easily could have changed the game.
I think that between 5,000 and 8,000 points, one team was clearly running the show and I would say that these matches border into the unfair territory but didn't ruin the fun for everyone.
At 8000 I think the game is unfair.
One team clearly was much better than the other and dominated the match.

These are *my* standards for a fair match and are not the only way to define what is and isn't fair.
Under my standards, about 60% of matches are fair, 27% of matches could have been fairer, and 13% of matches are unfair.

All in all, I would argue that Bungie's matchmaking system does a very good job at creating far and balanced games.  
Yes, 1 in 10 games you are likely going to get dominated (or dominate), but for the most part, games end with a close enough score difference to keep things interesting.
Of course, my boundaries for fairness and unfairness were chosen based on my experience in the Crucible, but if you reduce the range for fair and could be fairer matches, your conclusion might differ from mine.


Map Balance
------------
Another fun trend to look at is what the score difference distribution on *each map* is.
This could tell us if certains map are unbalanced one way or the other.

.. plot:: scoreDiffMap Distribution of Difference in Score between Teams on each Map
    :dir: ../pages/fullPlots/combatRating/

What we get out of this graph is that there are two types of maps.
1 type has a very high percentage of very close games, and then steadily decreases.
Blind Watch is a good example of this type.
The other type of map  a steady rate of what I call fair matches, and then a sudden drop off.
Pantheon falls into this second category.  There aren't as many extremely close games on Pantheon, but about 50% of games still end with a score difference of less than 5000.
Overall, there isn't any map that particularly stands out but it is interesting to see that 

TL;DR:
--------
Bungie's matchmaking system does a fantastic job at creating well balanced and interesting games.
About 60% of matches end with a score difference less than 5000, 27% of matches end between 5000 and 8000, and only 13% of matches end with a score difference greater than 8000.