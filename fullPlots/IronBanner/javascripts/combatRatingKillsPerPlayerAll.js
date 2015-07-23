

                data_combatRatingKillsPerPlayerAll=[{"values": [{"y": 0.86559017511939962, "x": "[0, 20)"}, {"y": 2.1424973011874777, "x": "[20, 40)"}, {"y": 3.6502617801047119, "x": "[40, 60)"}, {"y": 5.4804538973384034, "x": "[60, 80)"}, {"y": 7.3964146377598894, "x": "[80, 100)"}, {"y": 9.2319037124936436, "x": "[100, 120)"}, {"y": 11.032043674341324, "x": "[120, 140)"}, {"y": 12.641122504047491, "x": "[140, 160)"}, {"y": 13.893397177419354, "x": "[160, 180)"}, {"y": 14.917004048582996, "x": "[180, 200)"}, {"y": 16.122497055359247, "x": "[200, 220)"}, {"y": 16.77814938684504, "x": "[220, inf)"}], "key": "%Kills", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_combatRatingKillsPerPlayerAll;



                var width = $('#combatRatingKillsPerPlayerAll').width() - 60 - 60;
                chart.width(width);
                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Combat Rating');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2f'));

    
    
            nv.utils.windowResize(function(){ chart.update(); });

        



            d3.select('#combatRatingKillsPerPlayerAll svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', $('#combatRatingKillsPerPlayerAll').width())
            .attr('height', 450)
            .call(chart);

    
        });


