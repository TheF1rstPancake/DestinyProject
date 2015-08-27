

        data_combatRatingDistTeamBased=[{"values": [{"y": 0.00022179834094840972, "x": "(0,12.53)"}, {"y": 0.0027502994277602802, "x": "[12.53, 25.07)"}, {"y": 0.0074967839240562481, "x": "[25.07, 37.60)"}, {"y": 0.020050570021736238, "x": "[37.60, 50.13)"}, {"y": 0.046400212926407308, "x": "[50.13, 62.67)"}, {"y": 0.10460009759127002, "x": "[62.67, 75.20)"}, {"y": 0.17761611143148648, "x": "[75.20, 87.73)"}, {"y": 0.22046755090271924, "x": "[87.73, 100.27)"}, {"y": 0.20374395599520917, "x": "[100.27, 112.80)"}, {"y": 0.12558222064498958, "x": "[112.80, 125.33)"}, {"y": 0.05828860400124207, "x": "[125.33, 137.87)"}, {"y": 0.022978308122255247, "x": "[137.87, 150.40)"}, {"y": 0.0074524242558665658, "x": "[150.40, 162.93)"}, {"y": 0.0019074657321563235, "x": "[162.93, 175.47)"}, {"y": 0.00044359668189681943, "x": "[175.47, Inf)"}], "key": "Distribution", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_combatRatingDistTeamBased;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-25)                .axisLabel('Combat Rating');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#combatRatingDistTeamBased svg')
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



