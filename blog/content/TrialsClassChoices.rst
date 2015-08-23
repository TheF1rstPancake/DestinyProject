I Choose You
===============================================
:date: 2015-08-23
:modified: 2015-08-23
:tags: Trials Of Osiris, Crucible
:authors: Giovanni Briggs
:summary: A brief look at character selection trends in Trials of Osiris
:category: Stat Porn Sunday

See the `original post on reddit <http://www.reddit.com>`_.

Recap
---------
Welcome to Stat Porn Sunday where we use black magic (math) to try and become the most awesome ninja space warriros.

Last week we looked at `what people like to fly in space <https://www.reddit.com/r/DestinyTheGame/comments/3h7wqg/stat_porn_sunday_im_a_leaf_on_the_wind/>`_.
And found that players tend to stick to their Common tier ships until they find a Legendary ship and then switch over which causes them to miss out on all of the Uncommon and Rare ships out there.

New Data
------------------
Many of these Stat Porn Sundays have talked about player *choices*.  
I am no psycologist by any standards, so the analysis has been focused on looking at what factors impact certain trends and then looking at what we can logically conclude from those trends.

I am going to continue that pattern this week and start looking at **how players select characters when playing Trials of Osiris**.

Trials is the most competitive arena in the Crucible.  
It has very high stakes and the small team dynamic leads to a more calculating game play than the organized chaos that exists in Clash and Control.
Because of this, Trials has been an area that I have been wanting to look at for a while, but haven't had the time to.
This post will be the first of many to come in examining what makes certain Trials teams more successful than others.

The Trials dataset that I have isn't complete yet.  Right now, it only has about 3,000 games but within the next couple of weeks it will hopefully be as large as the other datasets that I have built (closer to 11,000 games).

Bring Your Best
-------------------
A discussion that I have often had before going into Trials is "what character should I use?" and the final decision usually revolves around what characters everyone else in my fireteam is bringing.
It often feels like establishing a sense of *balance* is important.  
One of each character seems like a logical choice because if the characters are designed in an intelligent way, then each character should be better suited to handle certain situations than others.

.. plot:: classCombos Distribution of Class Combinations in Trials
    :dir: ../pages/fullPlots/trialsOfOsiris/

As we can see, 20% of teams favor this approach, but a large portion of teams also choose to replace their Titan with either another Hunter of another Warlock.
There are very few teams that try and pull a full team of just one class.
The preference seems to be to have some sort of variation.

But preference doesn't always mean that this strategy is the most effective.
What we really want to see is if these different groups win at different rates.
If everything is nice and fair and even, each group would win 50% of their matches.
This would indicate to us that it doesn't really matter what class combos a team decides to use.

.. plot:: classCombosVictoryRate Victory Rate for different Class Combinations in Trials
    :dir: ../pages/fullPlots/trialsOfOsiris/

Fortunately (or unfortunately depending on how you view it) there is a difference in victory rates.  
The three Titan approach isn't used often at all, and they also don't win very often either.  
The one that surprised me was the *3 Warlock* approach.  Not only are they used infrequently, but they had the highest success rate.  
Actually, any combination containing at least 2 Warlocks has above 50% victory rate.

This does not mean that everyone should start rocking 3 Warlocks in Trials.

It does however mean that the 1 of every class combination isn't as good as you might think.  
Now these numbers don't take into account the fact that a team that has one of each class is likely to also play another team that has one of each class, and that explains why the victory rate is lower than others.
There is 1 loss and 1 win in those situations making the victory rate 50%.
But, since the victory rate is *below* 50% for this class combo, it means that this class combo is often losing to teams using a different class combo meaning that it is not as strong of a class combination as others.

Also interesting to note is that **all** combinations involving more than 1 Titan have a victory rate below 50%.  
So while having 1 Titan can still lead to a successful Trials run, having more than that is going to seriously impact your chances.
I think this graph makes it hard to argue for the balance approach.  Ideally, everyone would just use what characters they feel most comfortable with.  Unless of course, everyone feels like using their Titan.

TL;DR
--------
Choosing your classes carefully for a Trials run is a smart idea, but having one of each class isn't necessarily the most effective.
There are several other class combinations that have a higher rate of success.  And whatever you do - don't roll with 3 Titans.