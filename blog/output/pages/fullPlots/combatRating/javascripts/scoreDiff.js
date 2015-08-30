

        data_scoreDiff=[{"values": [{"y": 0.141564561734213, "x": "(0,1416.67)"}, {"y": 0.15683317624882187, "x": "[1416.67, 2833.33)"}, {"y": 0.15193213949104617, "x": "[2833.33, 4250.00)"}, {"y": 0.13638077285579642, "x": "[4250.00, 5666.67)"}, {"y": 0.11611687087653158, "x": "[5666.67, 7083.33)"}, {"y": 0.098114985862393964, "x": "[7083.33, 8500.00)"}, {"y": 0.073044297832233748, "x": "[8500.00, 9916.67)"}, {"y": 0.0471253534401508, "x": "[9916.67, 11333.33)"}, {"y": 0.034967012252591897, "x": "[11333.33, 12750.00)"}, {"y": 0.021394910461828464, "x": "[12750.00, 14166.67)"}, {"y": 0.013100848256361923, "x": "[14166.67, 15583.33)"}, {"y": 0.0094250706880301596, "x": "[15583.33, Inf)"}], "key": "Distribution", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_scoreDiff;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-15)                .axisLabel('Score Difference');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#scoreDiff svg')
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



