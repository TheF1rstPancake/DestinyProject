

                data_Top20WeaponsCR=[{"values": [{"y": 119.5663612737157, "x": "Radegast's Fury"}, {"y": 117.42378414279538, "x": "Jolder's Hammer"}, {"y": 114.93559539042451, "x": "The Messenger (Adept)"}, {"y": 113.93470797459406, "x": "BTRD-345"}, {"y": 111.0713835823443, "x": "Felwinter's Lie"}, {"y": 107.02076547589017, "x": "Judgment VI"}, {"y": 106.49767979323452, "x": "Matador 64"}, {"y": 105.9073672589917, "x": "Party Crasher +1"}, {"y": 105.37986870446747, "x": "The Last Word"}, {"y": 104.80136852839968, "x": "Thorn"}, {"y": 103.54092299966402, "x": "Praedyth's Revenge"}, {"y": 102.61274085355583, "x": "Found Verdict"}, {"y": 101.52935417673817, "x": "Bad Juju"}, {"y": 100.64518285688281, "x": "Red Death"}, {"y": 99.805674308294286, "x": "Her Courtesy"}, {"y": 98.954198205057452, "x": "Invective"}, {"y": 98.697023588961969, "x": "MIDA Multi-Tool"}, {"y": 97.863588122945785, "x": "Vex Mythoclast"}, {"y": 92.307581654389068, "x": "SUROS Regime"}, {"y": 91.753760408100433, "x": "Ice Breaker"}], "key": "Weapons", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_Top20WeaponsCR;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Weapon Name');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2f'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#Top20WeaponsCR svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


