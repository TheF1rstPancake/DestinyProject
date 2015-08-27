

        data_combatRatingDiff=[{"values": [{"y": 0.18213271823988644, "x": "(0,20.04)"}, {"y": 0.33516678495386798, "x": "[20.04, 40.08)"}, {"y": 0.23465223562810503, "x": "[40.08, 60.13)"}, {"y": 0.13023420865862315, "x": "[60.13, 80.17)"}, {"y": 0.06493967352732434, "x": "[80.17, 100.21)"}, {"y": 0.032647267565649396, "x": "[100.21, 120.25)"}, {"y": 0.013662171753016324, "x": "[120.25, 140.29)"}, {"y": 0.0053229240596167496, "x": "[140.29, 160.33)"}, {"y": 0.0011533002129169624, "x": "[160.33, 180.38)"}, {"y": 8.8715400993612495e-05, "x": "[180.38, Inf)"}], "key": "Distribution", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_combatRatingDiff;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-25)                .axisLabel('Combat Rating Difference');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#combatRatingDiff svg')
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



