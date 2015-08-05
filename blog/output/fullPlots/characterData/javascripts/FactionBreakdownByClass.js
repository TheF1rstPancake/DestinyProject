

        data_FactionBreakdownByClass=[{"values": [{"y": 0.13336323875742964, "x": "Dead Orbit"}, {"y": 0.11252663451833576, "x": "Future War Cult"}, {"y": 0.0416395648760794, "x": "New Monarchy"}, {"y": 0.71247056184815527, "x": "Other"}], "key": "Hunter", "yAxis": "1"}, {"values": [{"y": 0.20856133290800677, "x": "Dead Orbit"}, {"y": 0.055676882683483427, "x": "Future War Cult"}, {"y": 0.11591784653890511, "x": "New Monarchy"}, {"y": 0.61984393786960468, "x": "Other"}], "key": "Titan", "yAxis": "1"}, {"values": [{"y": 0.22444620159796067, "x": "Dead Orbit"}, {"y": 0.08307271075023899, "x": "Future War Cult"}, {"y": 0.11435922249890834, "x": "New Monarchy"}, {"y": 0.57812186515289199, "x": "Other"}], "key": "Warlock", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_FactionBreakdownByClass;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-25)                .axisLabel('Class');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#FactionBreakdownByClass svg')
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



