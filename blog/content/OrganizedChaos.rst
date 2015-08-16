Organized Chaos
===============================================
:date: 2015-07-05
:modified: 2015-07-05
:tags: Crucible, maps 
:authors: Giovanni Briggs
:summary: Examining map dynamics.
:category: Stat Porn Sunday

See the `original post on reddit <https://www.reddit.com/r/DestinyTheGame/comments/3c88p0/stat_sunday_kills_per_minute/>`_

Welcome
------------
Welcome to Stat Sunday! 
My plan is to throw up some stats with a little analysis each week. If there is a stat you'd like to see, post it in the comments or send me a message!

Kills per Minute
-------------------
I've seen a couple of posts over the past week about bringing Bastion and First Light back into matchmaking, so this week's topic focuses on comparing gameplay on each map.
First off, all of this data is pulled from Control. The trends in here probably still apply to other gametypes, but I can't prove it (yet).
One way to compare gameplay on different maps is to look at their Kills Per Minute. We should expect smaller maps to have a larger Kill Per Minute value versus larger maps. And if you look at the link below, you can see that this is the case:

.. html::
    <div class="plotContainer">
        <h4 class="text-center"><a href="/DestinyProject/blog/output/fullPlots/KillsPerMinute.html">Kills Per Minute on Each Map</a></h4>
        <div id="KillsPerMinute">
            <svg></svg>
            <script src='../fullPlots/javascripts/KillsPerMinute.js'></script>
        </div>
    </div>


This plot on its own (while pretty to look at) doesn't tell us much. 
It confirms the fact that battles are more spread out on larger maps and so there is less action happening all at once.

We can then take this plot and look at quit rate versus kills per minute.

.. html::
    <div class="plotContainer">
        <h4 class="text-center"><a href="/DestinyProject/blog/output/fullPlots/quitRateByKillsPerMinute.html">Kills Per Minute on Each Map</a></h4>
        <div id="quitRateByKillsPerMinute">
            <svg></svg>
            <script src='../fullPlots/javascripts/quitRateByKillsPerMinute.js'></script>
        </div>
    </div>

The general trend in that graph is that as the kills per minute increases, the quit rate decreases. This (to me at least) indicates that players vastly prefer the chaos that smaller maps offer versus the more sporadic battles that larger maps like First Light and Bastion offer.

TL;DR
----------
Kills per minute increases as map sizes decreases, and y'all are some blood thirsty players who quit less on maps when the Kills per Minute is higher.