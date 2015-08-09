

        data_ExoticArmorChoicesBySub=[{"values": [{"y": 0.23226393431969325, "x": "Bladedancer"}, {"y": 0.13733519539848985, "x": "Defender"}, {"y": 0.12956030413653591, "x": "Gunslinger"}, {"y": 0.26862630224916578, "x": "Striker"}, {"y": 0.41322358900144718, "x": "Sunsinger"}, {"y": 0.22157335415747123, "x": "Voidwalker"}], "key": "Chest Armor", "yAxis": "1"}, {"values": [{"y": 0.18961072720577085, "x": "Bladedancer"}, {"y": 0.19113783227211401, "x": "Defender"}, {"y": 0.15527704792243124, "x": "Gunslinger"}, {"y": 0.17109452609592704, "x": "Striker"}, {"y": 0.10316570188133141, "x": "Sunsinger"}, {"y": 0.18049095168573659, "x": "Voidwalker"}], "key": "Gauntlets", "yAxis": "1"}, {"values": [{"y": 0.39039923748456556, "x": "Bladedancer"}, {"y": 0.54392027836296064, "x": "Defender"}, {"y": 0.55637454367893602, "x": "Gunslinger"}, {"y": 0.35469573855676406, "x": "Striker"}, {"y": 0.37771345875542695, "x": "Sunsinger"}, {"y": 0.47760839303296776, "x": "Voidwalker"}], "key": "Helmet", "yAxis": "1"}, {"values": [{"y": 0.053592704113684123, "x": "Bladedancer"}, {"y": 0.029848273250171611, "x": "Defender"}, {"y": 0.04303950519682842, "x": "Gunslinger"}, {"y": 0.066226852441478384, "x": "Striker"}, {"y": 0.0, "x": "Sunsinger"}, {"y": 0.0, "x": "Voidwalker"}], "key": "Leg Armor", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_ExoticArmorChoicesBySub;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-25)                .axisLabel('Class');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#ExoticArmorChoicesBySub svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);


    chart.dispatch.on('stateChange', function(e) {
            nv.log('New State:', JSON.stringify(e));
     });
        chart.state.dispatch.on('change', function(state){
            nv.log('state', JSON.stringify(state));
    });

    });



