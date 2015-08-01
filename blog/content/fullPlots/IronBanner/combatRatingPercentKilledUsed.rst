Percent Killed divded by Percent Used within each Combat Rating Bin
======================================================================
:date: 2015-06-12
:modified: 2010-07-23
:tags: Crucible, Iron Banner, combat rating, balance
:authors: Giovanni Briggs
:summary: A different look at the effectiveness of each weapon (based on Iron Banner data).
:category: Iron Banner

`View project on Github <https://github.com/Jalepeno112/DestinyProject/>`_

.. html::
    <div id="combatRatingPercentKilledUsed">
        	<svg></svg>
        	<script src='\fullPlots\IronBanner\javascripts\combatRatingPercentKilledUsed.js'></script>
    </div>

This graph shows the effectiveness of each weapon in each combat rating group. 
Each bar is the percentage of kills with a particular weapon divided by the percentage of players using that weapon. 
What this does is show us the impact that certain weapons have on each group.  
Values greater than 1 mean that the percentage of kills is higher than the percentage of users.  
In other words, these users are generating more kills than other users in their combat rating group. 
For example, if a 15 percent of *Group-A* use *Weapon-Z* and *Weapon-Z* accounts for 30 percent of kills in that group, Then *Weapon-Z's* effectiveness in that group is 2.  
This could then be compared to *Weapon-Y* which is used by 20 percent of players but only accounts for 10 percent of all kills. 
While *Weapon-Y* is used more, it accounts for less kills thus making it less effective. Be careful when comparing across groups though. 
Just because *Weapon-Z* has an effectiveness of 2 in *Group-A* and only an effectiveness of 1 in *Group-B* does not mean that *Group-A8 is more effective with the weapon than *Group-B*.
