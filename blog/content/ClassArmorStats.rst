Who needs strength when you have brains
===============================================
:date: 2015-08-02
:modified: 2010-08-02
:tags: Characters, Shaders, Class, Armor
:authors: Giovanni Briggs
:summary: Examining trends in armor usage
:category: Stat Porn Sunday

View project on `Github <https://github.com/Jalepeno112/DestinyProject/>`_

Welcome to Stat Porn Sunday where we all come together to drool over our keyboards while looking at Destiny stats.  Our moms should be proud.

Recap
-------
First, hope you all find the new site useable.
It's a work in progress, but this way I can present all of the plots in one page rather than forcing you to open links all over the place.
For all you mobile users out there, I am trying to resolve a lot of the mobile problems.
Most of these graphs here should work.  There may be some weirdness, and if that's the case, I recommmend requesting the desktop site.
Please feel free to leave any comments (on the reddit post cause comments aren't set up here quite yet) if you come across any problems or have any solutions!

`Last week's post was about shaders <https://www.reddit.com/r/DestinyTheGame/comments/3eol7l/stat_porn_sunday_i_am_the_prettiest_guardian/>`_ and I was glad to see that a lot of people enjoyed it.
There was one suggestion made by `/u/BungieUserResearch/ <https://www.reddit.com/user/BungieUserResearch>`_ to look at the top 10 shaders in each class rather than overall.
Since I want to be his/her friend, I feel obligated to make that graph.

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
They are the only class where one shader is so highly concentrated.  
The Default Shader still makes an appearance, with Warlocks prefering it more than Hunters and Titans saying, "Nah, we ain't about that life."

Class Armor
-------------
This week we are going to take a closer look at class armor.
There has been **a lot** of analysis done on player weapon preferences, but not very much about their armor selection.
I'm more interested in which slot players use for their exotic piece of armor rather than the exact pieces that they are using.
It's also important to note that this isn't limited to Crucible like the other Stat Porn Sunday posts.
These characters could be playing either Curcible or PvE.  There's no way for me to differentiate in this set.

I hate choices!
~~~~~~~~~~~~~~~~
For this graph we are going to get really fancy.
Rather than just looking at the breakdown by class, we are going to go all the way down to subclass.
We also have to remove all players below level 20 since they can't equip exotic gear.
So these percentages only apply to characters at 20 or higher, not to all characters.

Note that not all of the tick marks are showing us this graph.  You will have to hover over the bar to see all of the shaders (or click on them if you are on mobile).

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
This hypothesis is further backed by the fact that **all** exotic chestpieces for the Warlock have Sunsinger specific perks.
Legs are the least used overall, and its probably because there are no legs (to my knoweldge) that offer subclass specific perks.
Maybe we will see a change in The Taken King where subclass specific perks are more evenly distributed between helmets and the other slots.

If you stack the bars, you see another interesting tid-bit. 
The bars don't stack up to 100%.  
Most of them actually only go up to 90%, which means that about 10% of players above level 20 don't equip an exotic armor piece at all.

Also, warlocks in general are interesting to look at because they don't have any exotic boots.
This means that they really only have to choose between 3 exotic slots.  

Look down at the very bottom of this page to find tables detailing the frequency of specific exotic armor pieces for each class.

Brains vs Braun
~~~~~~~~~~~~~~~~

Another interesting stat to look at is the distribution of intellect, strength and discipline across each subclass.
I would expect to see one stat dominate each subclass.  
Each subclass has a different playstyle, and different perks that make intellect, strength and discipline more or less desirable.
Compare Bladedancers to Gunslingers.  Bladedancers have a powerful melee attack that (in my opinion) you want to get as often as possible.
This makes Strength the obvious choice for any Bladedancer, but since they also have Fast Twitch (which greatly reduces Blink Strike cooldown),
they really have no need for Strength.  
For Gunslingers, Golden Gun is their most powerful asset, so they want to maximize how quickly they get their super, so I would expect to see Intellect be very high for Gunslingers.

For this next graph, I again separated the dataset by subclass and then took the average intellect, discipline and strength ratings for each subclass.
Let's see if my expectations were well founded.

.. html::
    <div class="plotContainer">
        <h4 class="text-center">Stat Breakdown by Subclass</h4>
        <div id="IntellectDisciplineStrengthBySub">
            <svg></svg>
            <script src='../fullPlots/characterData/javascripts/IntellectDisciplineStrengthBySub.js'></script>
        </div>
    </div>

The distribution of intellect, discipline and strength is actually more balanced than I expected it to be.
Intellect seems to be the crowd favorite except for our dear Sunsinger friends, which actually really surprises me.
Sunsingers don't have any perks that increase the rate at which they get their super, 
yet player's feel more of a need to boost how quickly their melee comes back.  
Then again I don't play as a Sunsinger, so what do I know.

The overall prevelance of intellect isn't surprising since intellect makes you get your super faster, and everyone likes a good super.

Wrapping Up
--------------
None of these stats should be terribly controversial.
People seem to prefer stats that impact their supers.
They generally seem to chose exotics based on it, and they seem to prefer keeping their intellect as high as possible.
This makes sense because supers are a large part of what makes each character unique and using your super is generally advantegous in both PvP and PvE.

Thanks for reading and tune in next week for more safe for work (stat) porn!

Exotic Use Tables
-------------------
Each table shows the frequency of use of each exotic armor piece within a given subclass.
Each cell is the number of characters in that subclass who have that armor piece equipped divided by the total number of characters in that subclass.

Hunters
~~~~~~~~
.. html::
    <table class="table table-bordered">
        <tr><th></th><th>Bladedancer</th><th>Gunslinger</th></tr>
        <tr><td>ATS/8 ARACHNID</td><td>0.012719768</td><td>0.018125355</td></tr>
        <tr><td>Achlyophage Symbiote</td><td>0.046017383</td><td>0.238227653</td></tr>
        <tr><td>Bones of Eao</td><td>0.028872485</td><td>0.02364618</td></tr>
        <tr><td>Celestial Nighthawk</td><td>0.042882089</td><td>0.146849882</td></tr>
        <tr><td>Crest of Alpha Lupi</td><td>0.090685399</td><td>0.070979135</td></tr>
        <tr><td>Don't Touch Me</td><td>0.067448506</td><td>0.023747666</td></tr>
        <tr><td>Khepri's Sting</td><td>0.087748541</td><td>0.083685151</td></tr>
        <tr><td>Knucklehead Radar</td><td>0.045263325</td><td>0.041223512</td></tr>
        <tr><td>Lucky Raspberry</td><td>0.122078025</td><td>0.042116587</td></tr>
        <tr><td>Mask of the Third Man</td><td>0.210739374</td><td>0.041243809</td></tr>
        <tr><td>Radiant Dance Machines</td><td>0.020220661</td><td>0.013923845</td></tr>
        <tr><td>Young Ahamkara's Spine</td><td>0.018494265</td><td>0.028111553</td></tr>
    </table>

Titans
~~~~~~~
.. html::
    <table class="table table-bordered">
        <tr><th></th><th>Striker</th><th>Defender</th></tr>
         <tr><td>ACD/0 Feedback Fence</td><td>0.078426096</td><td>0.070364274</td></tr>
         <tr><td>An Insurmountable Skullfort</td><td>0.043445863</td><td>0.026984883</td></tr>
         <tr><td>Crest of Alpha Lupi</td><td>0.06004595</td><td>0.04944341</td></tr>
         <tr><td>Eternal Warrior</td><td>0.094674311</td><td>0.05386148</td></tr>
         <tr><td>Helm of Inmost Light</td><td>0.085753317</td><td>0.020899207</td></tr>
         <tr><td>Helm of Saint-14</td><td>0.050255625</td><td>0.358643392</td></tr>
         <tr><td>Mk. 44 Stand Asides</td><td>0.013350444</td><td>0.00690865</td></tr>
         <tr><td>No Backup Plans</td><td>0.011673877</td><td>0.015268333</td></tr>
         <tr><td>Peregrine Greaves</td><td>0.040465299</td><td>0.020401092</td></tr>
         <tr><td>Ruin Wings</td><td>0.04893093</td><td>0.089249361</td></tr>
         <tr><td>The Armamentarium</td><td>0.158238983</td><td>0.076211721</td></tr>
         <tr><td>The Glasshouse</td><td>0.014095585</td><td>0.037272058</td></tr>
    </table>

Warlocks
~~~~~~~~~
.. html::
    <table class="table table-bordered">
        <tr><th></th><th>Sunsinger</th><th>Voidwalker</th></tr>
        <tr><td>Apotheosis Veil</td><td>0.047215597</td><td>0.026171854</td></tr>
        <tr><td>Claws of Ahamkara</td><td>0.035841158</td><td>0.017174424</td></tr>
        <tr><td>Heart of the Praxic Fire</td><td>0.102503377</td><td>0.024913854</td></tr>
        <tr><td>Light Beyond Nemesis</td><td>0.142113778</td><td>0.052918011</td></tr>
        <tr><td>Nothing Manacles</td><td>0.028035824</td><td>0.115763277</td></tr>
        <tr><td>Obsidian Mind</td><td>0.040694475</td><td>0.128480009</td></tr>
        <tr><td>Purifier Robes</td><td>0.192681666</td><td>0.058879834</td></tr>
        <tr><td>Skull of Dire Ahamkara</td><td>0.018312514</td><td>0.034157414</td></tr>
        <tr><td>Starfire Protocol</td><td>0.04322954</td><td>0.02433955</td></tr>
        <tr><td>Sunbreakers</td><td>0.031238013</td><td>0.012443253</td></tr>
        <tr><td>The Ram</td><td>0.099901599</td><td>0.142974348</td></tr>
        <tr><td>Voidfang Vestments</td><td>0.042562418</td><td>0.070338566</td></tr>
    </table>

