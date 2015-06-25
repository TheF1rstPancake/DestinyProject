URL_BASE = "http://localhost:8888/";

function getCharacters() {
    var gamertag = $("#gamertag");
    var gt = gamertag.val()

    var gt = $('#gamertag').val()
    var url = URL_BASE + "get_characters/?gamertag=" + gt

    var characters = $.getJSON(url, function (data) {
        var charactersDiv = $('#characters');
        //remove all current options from the HOP bar
        if (charactersDiv.find('tr').length > 1) {

            charactersDiv
                    .find('tr')
                    .slice(1)       //skip the first row with <tr> which is the head
                    .remove()
            ;

            charactersDiv.dataTable().fnClearTable();
        }

        /*if the table as already been initialized with certain options, just call the default constructor*/
        if ($.fn.dataTable.isDataTable('#characters')) {
            table = charactersDiv.dataTable();
        }
        else {
            charactersDiv.dataTable();
        }
        //add the key value pairs to the drop down menu.
        $.each(data.characters, function (i, item) {
            var emblem = "EMBLEM";
            var level = data.levels[i];
            var check = "<div class='checkbox'><input type='radio' required name='characterId' value=" + i + "></div>";
            var emblem = "<img src ='"+data.emblems[i]+"'/>"
            charactersDiv.append("<tr><td>"
                            + check + "</td>" //checkbox
                            + "<td>" + emblem + "</td>"             //emblem
                            + "<td>" + level + "</td>"     //level
                            + "<td>" + item + "</td>"               //class
                            + "</tr>");
            //add data to the table
            charactersDiv.dataTable().fnAddData([check, emblem, data.levels[i], item, i]);
        });

    });

}

function generateQuery() {
    var query = "/postgamestats/";
    var necessaryFields = ["gamertag","characterId"]
    for (var i = 0; i < necessaryFields.length; i++) {
        var delim = "&";
        if (i == 0) {
            delim = "?";
        }
        var v;
        if (necessaryFields[i] == 'characterId') {
            v = $("input[name='characterId']:checked", "#pgcrForm").val();
        }
        else if (necessaryFields[i] == 'gamertag') {
            v = $("#gamertag").val();
        }
        query += delim + necessaryFields[i] + "=" + v;
    }
    var dest = window.location.protocol + "//" + window.location.host + query;
    window.open(dest, '_blank');
    console.log(query);
}