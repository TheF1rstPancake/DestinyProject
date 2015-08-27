

        data_scoreDiff=[{"values": [{"y": 0.16234918381831087, "x": "(0,2230.56)"}, {"y": 0.23163591199432221, "x": "[2230.56, 4461.11)"}, {"y": 0.20892476933995741, "x": "[4461.11, 6691.67)"}, {"y": 0.16758339247693399, "x": "[6691.67, 8922.22)"}, {"y": 0.11559616749467708, "x": "[8922.22, 11152.78)"}, {"y": 0.062278211497515966, "x": "[11152.78, 13383.33)"}, {"y": 0.033534421575585519, "x": "[13383.33, 15613.89)"}, {"y": 0.013839602555003548, "x": "[15613.89, 17844.44)"}, {"y": 0.0041696238466997874, "x": "[17844.44, 20075.00)"}, {"y": 8.8715400993612495e-05, "x": "[20075.00, Inf)"}], "key": "Distribution", "yAxis": "1"}];


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



