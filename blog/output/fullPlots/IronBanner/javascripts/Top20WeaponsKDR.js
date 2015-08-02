

                data_Top20WeaponsKDR=[{"values": [{"y": 1.5903157556232113, "x": "The Messenger (Adept)"}, {"y": 1.5694436803122895, "x": "Radegast's Fury"}, {"y": 1.5686055243438213, "x": "Jolder's Hammer"}, {"y": 1.5279823032787021, "x": "BTRD-345"}, {"y": 1.4579402065999998, "x": "Praedyth's Revenge"}, {"y": 1.3605636257868299, "x": "Ice Breaker"}, {"y": 1.3488985078655391, "x": "Felwinter's Lie"}, {"y": 1.2949236766923342, "x": "The Last Word"}, {"y": 1.2677783689312505, "x": "Thorn"}, {"y": 1.2468871339337546, "x": "Matador 64"}, {"y": 1.2428986542633698, "x": "Judgment VI"}, {"y": 1.2310844001235697, "x": "Party Crasher +1"}, {"y": 1.2130486479205711, "x": "Bad Juju"}, {"y": 1.1935587696016154, "x": "Red Death"}, {"y": 1.1844770429153186, "x": "MIDA Multi-Tool"}, {"y": 1.1708821551068678, "x": "Found Verdict"}, {"y": 1.1281465059601816, "x": "Invective"}, {"y": 1.0888626330832045, "x": "Her Courtesy"}, {"y": 1.0774567052744035, "x": "Vex Mythoclast"}, {"y": 1.0155142671559187, "x": "SUROS Regime"}], "key": "Weapons", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_Top20WeaponsKDR;



                //var width = $('#Top20WeaponsKDR').width() - 60 - 60;
                var width = $('#Top20WeaponsKDR').width()
                chart.width(width);
                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Weapon Name');
            chart.yAxis
                .axisLabel('KDR')                .tickFormat(d3.format(',.2f'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#Top20WeaponsKDR svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', $('#Top20WeaponsKDR').width())
            .attr('height', 450)
            .call(chart);

    
        });


