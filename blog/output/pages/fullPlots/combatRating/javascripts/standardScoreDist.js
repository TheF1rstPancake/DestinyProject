

        data_standardScoreDist=[{"values": [{"y": 0.0, "x": "(0,nan)"}, {"y": 0.0, "x": "[nan, nan)"}, {"y": 0.0, "x": "[nan, nan)"}, {"y": 0.0, "x": "[nan, nan)"}, {"y": 0.0, "x": "[nan, nan)"}, {"y": 0.0, "x": "[nan, nan)"}, {"y": 0.0, "x": "[nan, nan)"}, {"y": 0.0, "x": "[nan, nan)"}, {"y": 0.0, "x": "[nan, nan)"}, {"y": 0.0, "x": "[nan, Inf)"}], "key": "Distribution", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_standardScoreDist;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-15)                .axisLabel('Standardized Score');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#standardScoreDist svg')
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



