Mix and Match
===============================================
:date: 2015-07-12
:modified: 2015-07-12
:tags: Crucible, weapon 
:authors: Giovanni Briggs
:summary: Examining how people pair primaries and secondaries.
:category: Stat Porn Sunday

See the `original post on reddit <https://www.reddit.com/r/DestinyTheGame/comments/3d1hy0/stat_sunday_weapon_pairings/>`_.

Welcome
---------------
Hey everyone it's Sunday again which means a new Crucible statistic for your viewing pleasure (woo! excitement!).
Last week's post was about `Kills per Minute <https://www.reddit.com/r/DestinyTheGame/comments/3c88p0/stat_sunday_kills_per_minute/>`_.

I Need a Weapon
-----------------
Before we begin, it is important to note that all of this data was taken from Control matches around the release of House of Wolves, but I think the general trends remain true.

This week, I looked at how frequently Primary and Secondary weapons are paired together. 
The first plot shows how frequently players use particular primary/secondary weapon combos. 
A player's weapon combo is determined by their most used weapon class during a game. For example, if a player has 5 kills with Hand Cannons, 3 kills with Pulse Rifles and 5 kills with Shotguns, then their primary/secondary weapon combo is Hand Cannon/Shotgun.

.. html::
    <div class="plotContainer">
        <h4 class="text-center"><a href="/DestinyProject/blog/output/fullPlots/weaponPairings.html">Frequency of Primary/Secondary Weapon Pairings</a></h4>
        <div id="weaponPairings">
            <svg></svg>
            <script src='../fullPlots/javascripts/weaponPairings.js'></script>
        </div>
    </div>


There are several takeaways from this graph. First, hand cannons are the most used primary weapon (surprise!) with shotguns being the most used secondary weapon (double surprise!) and the hand cannon/shotgun combo is the most used primary/secondary weapon combo (triple surprise!). 

What is actually surprising is what the second most used primary weapon is: *None*.

*None* occurs when a player has no primary weapon kills at the end of the match, and this accounts for about 15% of all players. One discrepancy here is that Universal Remote and No Land Beyond will still appear as secondary weapons even though they fit in the primary weapon slot. But even so, 15% is huge.
But now lets compare how secondaries are used with each primary weapon respectively. The next plot will show the distribution of secondary weapons across each primary weapon.

.. html::
    <div class="plotContainer">
        <h4 class="text-center"><a href="/DestinyProject/blog/output/fullPlots/primarySecondary.html">Frequency of Secondary Weapons with each Primary Weapons</a></h4>
        <div id="primarySecondary">
            <svg></svg>
            <script src='../fullPlots/javascripts/primarySecondary.js'></script>
        </div>
    </div>

What we see here is that the use of each secondary weapon is pretty static across all primary weapons. 
So, when a player switches between their Thorn and their Red Death, they probably aren't switching out their secondary weapon. 
Auto Rifle users don't appear to follow the same trend as everyone else though. Auto-rifle users are the most likely to use only their auto-rifle during a game.

TL;DR
---------
Players use the Hand Cannon/Shotgun weapon combo the most, but about 15% of players complete a Crucible match without ever using a primary weapon. 
Furthermore, user's don't seem to switch out their secondary when choosing a different primary. Across the board, if a player has any primary weapon, you have a 40% chance that they are using a shotgun with it.
If there is any other trends you'd like to see, post them in the comments and I'll see what I can do!