Fair and Square
===============================================
:date: 2015-08-05
:modified: 2015-08-05
:tags: Crucible, combat rating
:authors: Giovanni Briggs
:summary: Examining how combat rating is calculated and how to exploit it.
:category: Stat Porn Sunday
:status: draft

Recap
------
Welcome to Stat Porn Sunday.  What do we do here?  We stare with open mouths at graphs and numbers and go full nerd.

Last week we looked at `Trials team class combinations <https://www.reddit.com/r/DestinyTheGame/comments/3i3pnl/stat_porn_sunday_trials_of_osiris_character/>`_.

Fairness
---------
Last week I said I would be looking more at Trials data.  That was the plan, but for the past couple of weeks I have been working on how combat rating is calculated.
While looking into what makes combat rating work, how it's used and how it is calculated I found **a few interesting trends related to the "fairness" of games**.
I thought that these trends were more interesting than what I was pulling out of the Trials dataset, so that is what we are going to talk about this week.

There are a couple different ways to evaluate the fairness of matches.
One way is too look at the difference in score between teams at the end of a match.

.. plot:: scoreDiff Distribution of Difference in Score between Teams
    :dir: ../pages/fullPlots/combatRating/

This shows us that **19.1%** of games end with a score difference of less than 1,416.
To me, this is a pretty close point margin.  I would even say that a difference of 5,000 is still a fair match.
At 3000 I would say those are decisive victories, but I wouldn't say that they are unfair.
A turn in momentum for the other team could have changed the game.
I think that between 5000 and 80000 points, one team was clearly running the show and I would say that these matches border into the unfair territory but didn't ruin the fun for everyone.  
I will call these the "could be fairer" matches.
At 8000 the game is unfair.
One team clearly was much better than the other and dominated the match.

These are *my* standards for a fair match and are not the only way to define what is and isn't far.
Under my standards, about 60% of matches are fair, 27% of matches could have been fairer, and 13% of matches are unfair.

All in all, I would argue that Bungie's matchmaking system does a very good job at creating far and balanced games.  
Yes, 1 in 10 games you are likely going to get dominated (or dominate), but for the most part, games end with a close enough score difference to keep things interesting.
Of course, if you reduce the range for fair and could be fairer matches, your conclusion might differ.

Another trend to look at is what the score difference distribution on each map is.
This could tell us if certains map are unbalanced one way or the other.

.. plot:: scoreDiffMap Distribution of Difference in Score between Teams on each Map
    :dir: ../pages/fullPlots/combatRating/

What we get out of this graph is that there are two types of maps.
1 type has a very high percentage of very close games, and then steadily decreases.
Blind Watch is a good example of this type.
The other type has a steady rate of what I call fair matches, and then a sudden drop off.
Pantheon falls into this second category.  Games aren't as close on Pantheon, but more than 50% of games still end with a score difference of less than 5000.
Overall, that particularly stands out.
In the ideal game, I would think that all maps would behave like Blind Watch, with a very high percentage of games ending with a difference of less than 1500.

TL;DR:
--------
Bungie's matchmaking system does a fantastic job at creating well balanced and interesting games.
About 60% of matches end with a score difference less than 5000, 27% of matches end between 5000 and 8000, and only 13% of matches end with a score difference greater than 8000.
