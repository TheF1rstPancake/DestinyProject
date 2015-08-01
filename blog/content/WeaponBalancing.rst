We Have a Perception Issue
===============================================
:date: 2015-07-24
:modified: 2010-07-24
:tags: Crucible, Iron Banner, weapon, balancing
:authors: Giovanni Briggs
:summary: Examining weapon balance in PvP.
:category: Stat Porn Sunday
A look at trends within Destiny's competitive multiplayer and what players can do to increase their chances for victory

View project on `Github <https://github.com/Jalepeno112/DestinyProject/>`_


Overview
--------
On Sunday 7/19/15, I made a `post on reddit <https://www.reddit.com/r/DestinyTheGame/comments/3dur9n/stat_porn_sunday_dont_hate_the_game_hate_the/>`_ about the current state of weapon balancing in Crucible and how I believe that the game is currently much more well balanced than people often make it out to be and that Bungie's upcoming weapon tunning is more about changing people's perceptions about certain weapons than actually applying weapon specific nerfs.

At least, that's what I was hoping people would take away from the discussion.  
Instead, the conversation became focused around the issue of is Thorn overpowered or not.  
Looking back at my post, I'm not surprised that this is what the conversation became.  
Thorn is an interesting case study since it is often the topic of discussion as to *why* weapon balancing needs to happen.  
I tried to show that Thorn wasn't necessarily as broken as it is made out to be, 
and hoped that would lead people to the conclusion that the game isn't as broken as it is made out to be.

I was wrong.  

The Kills-per-Player metric I created did not sit well with a lot of people.  
For this post, I want to try and re-engange the conversation except this time, I want to be as clear as possible about what I intend to show and the process I went through in gathering and analyzing the data.

The point of this post is to show that weapon balancing in PvP is not nearly as broken as it is made out to be and that weapon balancing is about changing the perspective of players on certain weapons.

In the original post players said, "Thorn is overpowered!  I'm feel like I'm dying by it all the time."  
I said the numbers don't add up.
Thorn really doesn't appear to be that unbalanced.
You say back to me, "That's because you took an *average* over the entire population!  You can't do that!"

Point taken.  

An average, while usually a good starting point for assessing data, can dilute the information. 
If, for example,  we accept `u/jamesxn/ <https://www.reddit.com/user/jamesxn>`_ assertion that "More shit players use thorn because it's good, but a weapon being good isn't enough to get kills.", 
then taking an average of Thorn's usage and power doesn't tell the whole story.

Some Perspective
-------------------
Before we go too far, I want to throw in some numbers here because there was a lot of comments like, "Everyone uses Thorn" or "I only get killed by Thorn."
Neither of these is true.  To be everyone or everytime, it would have to be 100% use.  
I would accept 50% and say the majority rounds up to everyone, but Thorn only accounts for **16.98%** of all **weapon kills**.  
And weapon kills are only **63.57%** of **kills overall**. 
That means that about 36 percent of kills come from something other than a weapon (grenades, melee, supers, exploding boxes, etc.).  
So Thorn is really only **10.79%** of all kills overall.  
If the average player dies 12 times (which they do) then in a given game you are going to die by Thorn **1.1 times**.

If I had to take a bet on whether or not you died by Thorn, I would pick no every time.  90% of the time, I would be right.
If I had to bet on the exact weapon you were killed by, I would actually pick Thorn every time because it has the highest kill (and use) frequency of any weapon.
That doesn't mean its overpowered.

I think it's important to get away from the idea of "Everyone" and "always" as these over-generalizations don't help us.
*Feeling* like Thorn kills you all the time is different than it *actually* killing you all the time.  Let's keep this in mind as we continue.


Shit Players
-------------------

But how do we detect "shit" players?  
Bungie actually does that for us.  
In every PostGameCarnageReport, player's are given a *Combat Rating*.  
From what I can tell, the higher the combat rating, the "better" the player.  
So let's use this metric to divide the player base into tiers so that we can better evaluate weapon usage.  
This first graph shows the frequency of each combat rating within my dataset.

.. html::
    <div class="plotContainer">
    <h4 class="text-center">Combat Rating Distribution Curve</h4>
    <div id="combatRatingDist">
        <svg></svg>
        <script src='http://jalepeno112.github.io/DestinyProject/output/fullPlots/IronBanner/javascripts/combatRatingDist.js'></script>
    </div>
    </div>

As we can see fom that graph, the distribution of combat ratings looks pretty normally distributed, which is what we would expect from a metric like this.  
I did remove all players who had a combat rating of -1 or 0 since these seemed to be anomalous cases and I wasn't really sure what causes them to occur (it seems to be realted to qutting, but not always).  
Removing this group took out 5% of players from the original dataset, but still left us with around 100,000 players to work with.  
One of the reasons that this graph does not perfectly fit a normal curve is that it has a very long tail to the right.  
The highest combat rating was over **600** but only one person is up that high, and very, very few people break outside of 240.  
In order to deal with this, I increased the range of the last bin from 220 onward. 
Otherwise, the last bins don't have enough people in them to make meaningful trends.
The average combat rating is a **96**.


Combat Rating Breakdown
-------------------------

With the pleasentries out of the way we can now start looking at weapon trends within each bin.  
This next plot will show how much each of the top 20 weapons contribute to the overall *weapon kills* of each bin.  

I divded the dataset into combat rating bins, and then for each of the top 20 weapons, I divided that weapon's kills in *that bin* by the total number of weapon kills in *that bin*.  
This can show us a few things.  First, it shows us how prominent each weapon is in a given tier.  
If SUROS is a higher number of kills than Thorn in the *lowest* bin, then we can say that the players who use SUROS in that bin produce a higher number of kills than those who use Thorn.
However, this could be because more players are using SUROS than Thorn.
This plot says nothing about the number of players *using* the weapon.
Second, if you stack all of the bars, you get what percentage of weapon kills in each bin is with the top 20 weapons overall.

.. html::
    <div class="plotContainer">
    <h4 class="text-center">Weapon Kills Breakdown in each Combat Rating Group</h4>
    <div id="combatRatingWeaponBreakdown" class="plot">
        <svg></svg>
        <script src='http://jalepeno112.github.io/DestinyProject/output/fullPlots/IronBanner/javascripts/combatRatingWeaponBreakdown.js'></script>
    </div>    
    </div>

We can see from the graph that overall, the top 20 weapons account for about 70% of all weapon kills in each group (some are above and some below this line).
We also get to see some weapon specific trends.
The Messenger, for example,  makes up for .6% of kills in the lowest tier and grows as the tier increases.  
Pradeyth's Revenge shows an almost opposite trend.  It makes up for less percent of kills as combat rating increases.
Thorn shows an interesting trend as well - it stays fairly constant throughout each group sitting around **16%**.

Let's further examine the Thorn trend here because it sets us up nicely for an upcomming metric.
Thorn makes up for an almost uniform percentage of kills across combat ratings, but it is very possible that certain groups use it more *effectively*.  
If we look at the number of kills a weapon has and then look at how many people used it, we can measure how effective it is.  
If a weapon has 1000 kills, but it took 1000 players to get it there, that's not terribly effective when compared to a weapon that had 1000 kills but only 200 users (1 versus 5).
Before we calculate that metric though, lets look at the percentage of *use* in each combat rating group.

.. html::
    <div class="plotContainer">
    <h4 class="text-center">Weapon Usage Breakdown in each Combat Rating Group</h4>
    <div id="combatRatingPercentUsed" class="plot">
        <svg></svg>
        <script src='http://jalepeno112.github.io/DestinyProject/output/fullPlots/IronBanner/javascripts/combatRatingPercentUsed.js'></script>
    </div>
    </div>

This graph also contains some neat trends.  
Most primary weapons show a general upward trend in use.  
As your combat rating increases, it is more likely that you will use one of these exotic primaries.  
Players still clearly favor Thorn over other weapons though hitting 35.53% at its peak.  
What's interesting about these trends though is that the percent of use increases much more rapidly than the percent of kills.
Also note that if you stack the bars, the percentages are not out of 100%.  That's because player's can be counted multiple times for each weapon that they use.
It is still accurate to say that 11.86% of players use Red Death in the [100,120) bin.
It would be wrong to say that 11.86% of players only use Red Death in the [100, 120) bin.  
Stacking the bins does show that the usage of these top 20 powerhouses increases as the combat rating increases.

Next, I'm going to divide the total number of kills with each weapon by the number of players who use that weapon.  
Those who viewed Sunday's post will recognize that I've just described my metric *Kills-per-Player*.  
It was a point of contention with many people who stated that this metric was broken and did not indicate what I said it was indicating.  
They were (mostly) right. 
I did not fully understand KPP and its impact when I first used it, so let me try again here because I do believe it is a useful metric.  

Kills Per Player may not indicate a *weapon's* effectiveness like I stated last week (although I still think that's up for debate).  
It instead indicates a *player's* effectiveness.  
This becomes more apparent when you seperate player's into combat rating bins.

.. html::
    <div class='plotContainer'>
    <h4 class="text-center">Kills Per Player in each Combat Rating Group</h4>
    <div id="combatRatingKillsPerPlayerAll" class="plot">
        <svg></svg>
        <script src='http://jalepeno112.github.io/DestinyProject/output/fullPlots/IronBanner/javascripts/combatRatingKillsPerPlayerAll.js'></script>
    </div>
    </div>

Unlike the graph from Sunday, this graph did not attempt to determine the KPP of a weapon, but instead looks at the KPP for a particular combat rating group.
KPP increases with combat rating, as it should.  Higher tier players are more *effective*.  
While their contribution to the total number of kills is small, there is a very,very smaller number of them, so their KPP is very high.  
This is in contrast to the lower tier players.
There are more lower tiered players, but the contribute much less kills to the total, so their KPP is much lower.  
What I am trying to say here is that KPP is still a useful metric, just not for what I was trying to show on Sunday.  
You can do KPP per weapon per bin but I think the trend means something different than what I originally thought.
I leave the plot here though so that you can at least see it and determine whether you buy it or not.

.. html::
    <div class="plotContainer">
    <h4 class="text-center">Kills Per Player for each Weapon by Combat Rating</h4>
    <div id="combatRatingKPP" class="plot">
        <svg></svg>
        <script src='http://jalepeno112.github.io/DestinyProject/output/fullPlots/IronBanner/javascripts/combatRatingKPP.js'></script>
    </div>
    </div>


Another Look at Effectiveness
------------------------------

One way to measure actually weapon efficiency that was suggested in the comments `another post <https://www.reddit.com/r/DestinyTheGame/comments/3e2udr/guardiangg_new_site_first_only_place_for/>`_ is to take the percent kills divided by the percent used.
By taking the percent killed by the percent used, you get a ratio that tells you how effective a weapon is.
As the percent of kills increases (and player usage stays the same), the ratio decreases.
The weapon had to be in more hands to acheive the percent of kills that it reached.
If the percent used decrases (and the kills stays the same), then the ratio increases.
The weapon needed to be in less hands to achieve the percent of kills it reached.

The post didn't mention applying this metric to speicifc combat rating bins or skill levels but I think we need to do that for the same reasons that a simple average isn't always a good measurement.

The suggestion didn't mention doing this across player skill levels, but I think that it is important to do so for the reasons that simply taking an average isn't necessarily effective.
"Shit" players could potentially be bringing down a weapon's stats.
The assumption is that "shit" players are less likely to get kills, so they inflate the player's used part of the ratio without equally contributing to the percent kills part of the ratio.

Finally, let's look at this graph.

.. html::
    <div class="plotContainer">
        <h4 class="text-center">Percent Killed divided by Percent Used for each Combat Rating </h4>
        <div id="combatRatingPercentKilledUsed" class="plot">
            <svg></svg>
            <script src='http://jalepeno112.github.io/DestinyProject/output/fullPlots/IronBanner/javascripts/combatRatingPercentKilledUsed.js'></script>
        </div>
    </div>

None of this should be a surprise.  After all, we already looked at the numerator and denominator values for this graph.
We've seen that the percentage of kills with the top 20 weapons is pretty much equal across all combat rating bins, but the percentage of use generally increases as the combat rating increases.
However, if you weren't expecting this result than this can be quite the surprise.
If we accept *Percent Kills/Percent Used* as a measurement of *effectiveness* then this graph at a glance seems to say that the lowest combat rating group is the most effective.
This would be the wrong conclusion.  We can't compare across groups in this manner.  *Percent Kills/Percent Used* is a measurement of *weapon* effectiveness.
Since I have done this calculation within each bin, it's really a measurement of how effective each weapon is in each bin.

First we need to compare between weapons in a given bin.  
Let's take the lowest bin.  
All of those weapons have an effectiveness above 1.
This means that all of the top 20 weapons have a higher percentage of kills than percentage of use.  
Again, not surprising when we remember that the top 20 account for a very small portion of use, but a very high protion of kills.
This means that the top 20 weapons make a larger impact on player perfomance in the lower skill range than the higher skill range.
Player's who have access to these weapons do better than those who don't.

The lowest tier feels the wrath of these weapons the most.
Players who aren't using these weapons in the lowest tiers are sadly outgunned, but they aren't outgunned by any weapon in particular.
All of these legendaries and exotics seem to decimate the lower tiers.
However, this weapon advantage quickly goes away.
Once we reach the average tier level, we see that the ratios become much more packed together and the curves seem to approach an asymptote.


Cool stats bro but what the hell does that mean?
---------------------------------------------------
I've thrown a lot of numbers and graphs at you all with the intent of convincing you that the current state of the Crucible is not as imbalanced as people make it out to be.
But we've gone through this entire analysis without ever defining what an "overpowered weapon" is.

One way to look at an overpowered weapon is to say that it is a weapon that people feel they have to use in order to compete.
This argument could be made for Thorn.
Players feel like Thorn is so powerful to the point where if they don't use it, they don't stand a chance.
This would explain it's high percentage of usage.
At it's peak, Thorn is used by 35.53% of all players.  That means 4 players in a given game are likely using Thorn, but that means the other 8 players felt perfectly comfortable using some other primary or no primary at all.
So it can't be that overpowered.

The other way to define an overpowered weapon is to say that the weapon is too hard to obtain and those that obtain it have an unfair advantage.
The Messenger might be such a weapon.  It's not easy for the average Destiny player to get to the lighthouse, and even if they do, there's no gaurantee that they will be awarded this weapon.
If The Messenger was truly overpowered, we would see it in its effectiveness.  Such a small population has it, but if it's some sort of monster, then these players would be raking up the kills.
It's effectiveness is actually on par with the other weapons especially in the mid to high combat rating range.

What the kill-used effectiveness ratio and KPP try and do (each in their own way) is normalize weapon statistics.
In other words, they are trying to remove the bias that comes with extreme use.  Of course we expect Thorn to have the highest number percentage of kills, because it also has the highest percentage of use.
When you strip away Thorn's high percentage of use though to try and compare these weapons on some even terms, we see that Thorn actually falls in line with all these other weapons.

I've given you two metrics, each one trying to show the effectiveness of a weapon as opposed to how people *feel* about a weapon in order to verify the statement that the Crucible is a much more well balanced machine than people give Bungie credit for.
In other terms, these metrics attempt to remove the *perception* that people have for each weapon.

Just by usage and kills, Thorn appears to be the most overpowered weapon in the game.
But finding a way to normalize the data and looking at weapon efficiency shows us that these top 20 weapons are actually fairly even.
There is a nice balance here.  The issue is that people don't see it.  Weapon tunning isn't so much about applying nerfs to create more balance as it is to change the perception that people have about certain weapons in order to force them to try new ones.
Reshifting the game like this can help make the game feel new again.  It reinvigorates the population.
It's not broken weapon balancing.  It's just good game desgin.
