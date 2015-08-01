Who needs strength when you have brains
===============================================
:date: 2015-08-02
:modified: 2010-08-02
:tags: Characters, Shaders, Class, Armor
:authors: Giovanni Briggs
:summary: Examining trends in armor usage
:category: Stat Porn Sunday
:status: draft

View project on `Github <https://github.com/Jalepeno112/DestinyProject/>`_

Welcome to Stat Porn Sunday where we all come together to drool over our keyboards while looking at Destiny stats.  Our moms should be proud.

Recap
-------
First, hope you all find the new site useable.
It's a work in progress, but this way I can present all of the plots in one page rather than forcing you to open links all over the place.
For all you mobile users out there, I am trying to resolve a lot of the mobile problems.
Most of these graphs here should work.  There may be some weirdness, and if that's the case, I recommmend requesting the desktop site.
Please feel free to leave any comments (on the reddit post cause comments aren't set up here quite yet) if you come across any problems or have any solutions!

`Last week's post was about shaders <https://www.reddit.com/r/DestinyTheGame/comments/3eol7l/stat_porn_sunday_i_am_the_prettiest_guardian/>`_ and you all seemed to like it a lot.
There was one suggestion made by `/u/BungieUserResearch/ <https://www.reddit.com/user/BungieUserResearch>`_ to look at the top 10 shaders in each class rather than overall.
Since I want to be his/her friend, I felt obligated to make that graph.

.. html::
    <div class="plotContainer">
        <h4 class="text-center">Top 10 Shaders for Each Class</h4>
        <div id="Top10ShadersInEachClass">
            <svg></svg>
            <script src='../fullPlots/characterData/javascripts/Top10ShadersInEachClass.js'></script>
        </div>
    </div>

Like the plot from last week, this one only looks at players at level 20 or above.  
Doing this removes 12% of our dataset, but still leaves us with 255,000 characters to work with.
The x-axis is the shader, the color is the class.  Not all classes have the same top 10 shaders, which is why some shaders only have 1 bar.
Clicking on *stacked* currently is, well, interesting...  The charting library looses its mind a little bit because not every class uses each of these shaders.
But you can see the general idea.  I find it very interesting that Titans so heavily prefer Thunderdevil.  
The Default Shader is still in the running, but Warlocks seem to favor it more than Hunters, and Titans aren't about that Default Shader life.

Class Armor
-------------
This week we are going to take a closer look at class armor.
There has been **a lot** of analysis done on player weapon preferences, but not very much about their armor selection.
I'm not so interested in what exact pieces of armor players are using.  I'm more interested in which slot players use for their exotic piece of armor.
It's also important to note that this isn't limited to Crucible like the other Stat Porn Sunday posts.
These characters could be playing either Curcible or PvE.  There's no way for me to differentiate in this set.

I hate choices!
~~~~~~~~~~~~~~~~
For this graph we are going to get really fancy.
Rather than just looking at the breakdown by class, we are going to go all the way down to subclass.
We also have to remove all players below level 20 since they can't equip exotic gear.
So these percentages only apply to characters at 20 or higher, not to all characters.

.. html::
    <div class="plotContainer">
        <h4 class="text-center">Exotic Armor Slot Selection Breakdown by Sub</h4>
        <div id="ExoticArmorChoicesBySub">
            <svg></svg>
            <script src='../fullPlots/characterData/javascripts/ExoticArmorChoicesBySub.js'></script>
        </div>
    </div>

Helmets are by far the prefered slot to use for exotic armor except for Sunsingers who seem to value their exotic chest pieces more.
This is probably because helmets seem to be more tailored towards each super, which means you are more likely to select pieces that boost your characters super abilities.
We can generalize this even more to say that helmets offer perks that people care about.
This can be compared to legs (the overall least used by far).
Maybe we will see a change in The Taken King towards creating exotic armors that offer a more balanced spattering of perks, rather than having one class of exotic clearly dominate the market.

If you stack the bars, you see another interesting tid-bit.  The bars don't stack up to 100%.  Most of them actually only go up to 90%, which means that 10% of players above level 20 don't equip an exotic armor piece at all.

Also, warlocks in general are interesting to look at because they don't have any exotic boots.  This means that they really only have to choose between 3 exotic slots.

Brains vs Braun
~~~~~~~~~~~~~~~~

Another interesting stat to look at is the distribution of intellect, strength and discipline across each subclass.
Since the exotics only target one of these three, I expect this distribution to follow a similar pattern to the distribution of exotics.
One stat should dominate each subclass.
However, this will show us how people prefer to utilize their other armor slots.

For this next graph, I again separated the dataset by subclass and then took the average intellect, discipline and strength ratings for each subclass.

.. html::
    <div class="plotContainer">
        <h4 class="text-center">Stat Breakdown by Subclass</h4>
        <div id="IntellectDisciplineStrengthBySub">
            <svg></svg>
            <script src='../fullPlots/characterData/javascripts/IntellectDisciplineStrengthBySub.js'></script>
        </div>
    </div>

The distribution of discipline, strength and intellect is actually more balanced than I expected it to be.
Intellect seems to be the crowd favorite except for our dear Sunsinger friends.
The prevelance of intellect isn't terribly surprising since intellect makes you get your super faster, and everyone likes a good super.

Wrapping Up
--------------
None of these stats should be terribly controversial.
People seem to prefer stats that impact their supers.
We see this both in the choice of exotic and in prevelance of high intellect.

Thanks for reading and tune in next week for more stat porn!
