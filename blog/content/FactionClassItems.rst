I Pledge Allegiance
===============================================
:date: 2015-07-24
:modified: 2010-07-24
:tags: Character, Ships, Factions
:authors: Giovanni Briggs
:summary: Examining weapon balance in PvP.
:category: Stat Porn Sunday
:status: draft

A look at the distribution of Factions among the Destiny population.

View project on `Github <https://github.com/Jalepeno112/DestinyProject/>`_

Recap
-------
Last week we talked about how players pick `intellect, discipline, and strength <https://www.reddit.com/r/DestinyTheGame/comments/3fiuwn/stat_porn_sunday_who_needs_strength_when_you_have/>`_ when building their characters.

I've also been noticing that there's been a significant rate of downvotes on these posts so if there is something that you think I can be doing better, please leave a comment.
The feedback is appreciated!

I pledge allegiance
---------------------
This week we are going to look at factions.
I took my large player dataset and took only the characters who were level 20 and higher which gave me 255,000 players to work with.  
The reason for picking players at level 20 and above is because you can't pledge a faction until you are level 20.
I then broke it down by the class items people have equipped and then built a map that paired factions to their respective class items.
With this map, I searched the dataset for players that had one of these faction items equipped.

First, let's look at the overall distribution of factions.

.. html::
    <div class="plotContainer">
        <h4 class="text-center">Faction Distribution</h4>
        <div id="FactionBreakdown">
            <svg></svg>
            <script src='../fullPlots/characterData/javascripts/FactionBreakdown.js'></script>
        </div>
    </div>

Dead Orbit is the clear winner.  **18.76%** of all Gaurdians at 20 or higher wear a Dead Orbit class item.
It is little over twice the number of Gaurdians in either the Future War Cult or New Monarchy.
An observant Gaurdian will also note that these percentages do not add up to 100%, so that means there are **63.83%** of Gaurdians who choose not to wear a faction item.
This does *not* mean that 2/3 of Gaurdians *do not* pledge a faction.
I couldn't find where Bungie keeps your respective faction ranks.  This only means that 63.83% of Gaurdians do not wear one of the faction class items (they could be wearing emblems or shaders though or no faction items at all).

But do certain classes have different preferences for different factions?
Well, we can make a graph for that.

.. html::
    <div class="plotContainer">
        <h4 class="text-center">Faction Distribution by Class</h4>
        <div id="FactionBreakdownByClass">
            <svg></svg>
            <script src='../fullPlots/characterData/javascripts/FactionBreakdownByClass.js'></script>
        </div>
    </div>

Each class seems to have slightly different faction preferences.
The *Other* bar is in there just so you can verify that these numbers make sense (all x-tick marks add up to 100), but you can remove it by clicking on it in the legend.
Hunters like everyone else, prefer Dead Orbit over all others, but they prefer FWC over New Monarchy.
Not only that, but they have the lowest rate on faction attendance overall.  Only about 30% of all Hunters above level 20 equip a faction class item.
My theory is that because the Hunter class item makes such a large difference in their appearance, they are more likely to pick class items for their style.
This is in contrast to Warlocks whose class items really don't make a terrible impact on their appearance, so they are more likely to pick class items for the functionality.

I believe being in a Faction is the only way to go (and I play as a Hunter), because by wearing a Faction class item you are pooling both your Vanguard and Crucible rep into one pool.
Doing the Nightfall and Weekly Strikes give you a lot of rep, but if you're like me and that's all you do in the story mode anymore, it can be a few weeks before you see those efforts turn into a Vanguard package.
By wearing a class item, I can turn out packages quicker, and while the loot isn't always great, I'm still holding out for a FWC ship.
But the FWC cloak doesn't always jive with the shader or armor that I have equipped, so I often feel like I look like a clown.  
For me though, the functionality outweighs the looks, but I could see how for many other Hunters that may not be the case.

As everyone also knows, reward packages are often a bust (2 motes of light woot!) so maybe players start to become bitter and abandon factions as they play more.

.. html::
    <div class="plotContainer">
        <h4 class="text-center">Faction Distribution by Level</h4>
        <div id="FactionBreakdownByLevel">
            <svg></svg>
            <script src='../fullPlots/characterData/javascripts/FactionBreakdownByLevel.js'></script>
        </div>
    </div>

This graph is a little confusing at first.
The x-axis is character level, the y-axis is the percentage of players who are that level that wear a faction class item.
For example, 10.41 percent of level 22 players wear a Dead Orbit class item.

What this shows us is that faction items actually become more prevelant as your level goes up.  21% of all players who are level 34 wear a Dead Orbit class item.
1 out of every 5 level 34s that you meet today are going to be wearing a Dead Orbit class item.
Dead Orbit shows the greatest increase overall, but all of the factions increase as level increases.

Concluding Thoughs
---------------------
Factions are an interesting game mechanic that don't really offer much, yet there is a clear preference in which factions people like.
Overall, the majority of player's choose not to wear a faction item, but for the player's who do, they are most likely running with Dead Orbit.

If a war were to ever break out between the factions, Dead Orbit would win because the other two factions would be seriously out gunned.