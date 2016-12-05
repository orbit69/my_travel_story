function picIter(){
    var form = document.getElementById('add_place_form');
    var imagList = document.getElementById("place_images").files;
    var imagListSize = document.getElementById("place_images").files.length;


    var count;
    for(count=0;count<imagListSize;count++){
        var elemTab;
        elemTab = document.createElement("img");
        elemTab.src = window.URL.createObjectURL(imagList[count]);
        elemTab.maxHeight = "300";

        var table = document.createElement("table");

        for(var ind=0;ind<4;ind++){
            var tr = document.createElement("tr");
            for(var ind2=0;ind2<2;ind2++){
                var td = document.createElement("td");
                tr.appendChild(td);
            }
            table.appendChild(tr);
        }

        table.childNodes[0].childNodes[0].appendChild(document.createTextNode("Name: "));
        var element = document.createElement("input");
        element.type = "text";
        element.value = imagList[count].name;
        element.readOnly = "true";
        table.childNodes[0].childNodes[1].appendChild(element);

        table.childNodes[1].childNodes[0].appendChild(document.createTextNode("Description: "));
        var element = document.createElement("input");
        element.type = "text";
        element.value = "";
        table.childNodes[1].childNodes[1].appendChild(element);

        table.childNodes[2].childNodes[0].appendChild(document.createTextNode("Date: "));
        var element = document.createElement("input");
        element.type = "date";
        table.childNodes[2].childNodes[1].appendChild(element);

        table.childNodes[3].childNodes[0].appendChild(document.createTextNode("Rate: "));
        var element = document.createElement("input");
        element.type="number";
        table.childNodes[3].childNodes[1].appendChild(element);

        var root = document.createElement("div");
        root.id="image_div" + String(count);
        root.display="inline-block";
        root.appendChild(elemTab);
        root.appendChild(table);

        form.appendChild(root);
    }
}
