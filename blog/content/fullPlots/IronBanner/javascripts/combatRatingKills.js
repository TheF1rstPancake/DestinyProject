

                data_combatRatingKills=[{"values": [{"y": 0.0047225120885638523, "x": "[0, 20)"}, {"y": 0.014775531778932831, "x": "[20, 40)"}, {"y": 0.04757999173622425, "x": "[40, 60)"}, {"y": 0.11446073899993424, "x": "[60, 80)"}, {"y": 0.18583568983295012, "x": "[80, 100)"}, {"y": 0.20271935299350935, "x": "[100, 120)"}, {"y": 0.1730107069250689, "x": "[120, 140)"}, {"y": 0.11625866858909058, "x": "[140, 160)"}, {"y": 0.068404458468322812, "x": "[160, 180)"}, {"y": 0.036574032139387314, "x": "[180, 200)"}, {"y": 0.016984168541319501, "x": "[200, 220)"}, {"y": 0.018674147906696265, "x": "[220, inf)"}], "key": "%Kills", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_combatRatingKills;



                //var width = $('#combatRatingKills').width() - 60 - 60;
                var width = $('#combatRatingKills').width()
                chart.width(width);
                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Combat Rating');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#combatRatingKills svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', $('#combatRatingKills').width())
            .attr('height', 450)
            .call(chart);

    
        });


