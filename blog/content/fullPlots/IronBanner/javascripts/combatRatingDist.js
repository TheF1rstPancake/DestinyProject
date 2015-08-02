

        data_combatRatingDist=[{"values": [{"y": 0.042698025811087698, "x": "[0.00, 20.00)"}, {"y": 0.053972169083016927, "x": "[20.00, 40.00)"}, {"y": 0.10201108963963526, "x": "[40.00, 60.00)"}, {"y": 0.16345080064867595, "x": "[60.00, 80.00)"}, {"y": 0.19663232309499995, "x": "[80.00, 100.00)"}, {"y": 0.17185057147573776, "x": "[100.00, 120.00)"}, {"y": 0.12273376125229415, "x": "[120.00, 140.00)"}, {"y": 0.071975839734314762, "x": "[140.00, 160.00)"}, {"y": 0.038532127909573798, "x": "[160.00, 180.00)"}, {"y": 0.019188378213033725, "x": "[180.00, 200.00)"}, {"y": 0.0082443993435554822, "x": "[200.00, 220.00)"}, {"y": 0.0087105137940745193, "x": "[220.00, Inf)"}], "key": "Distribution", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_combatRatingDist;



                //var width = $('#combatRatingDist').width() - 60 - 60;
                var width = $('#combatRatingDist').width()
                chart.width(width);
                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-25)                .axisLabel('Combat Rating');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#combatRatingDist svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', $('#combatRatingDist').width())
            .attr('height', 450)
            .call(chart);


    chart.dispatch.on('stateChange', function(e) {
            nv.log('New State:', JSON.stringify(e));
     });
        chart.state.dispatch.on('change', function(state){
            nv.log('state', JSON.stringify(state));
    });

    });



