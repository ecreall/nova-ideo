
var font_default_val = "white";

var background_default_val = "black";

var default_palette = [
        ["#000","#444","#666","#999","#ccc","#eee","#f3f3f3","#fff"],
        ["#f00","#f90","#ff0","#0f0","#0ff","#00f","#90f","#f0f"],
        ["#f4cccc","#fce5cd","#fff2cc","#d9ead3","#d0e0e3","#cfe2f3","#d9d2e9","#ead1dc"],
        ["#ea9999","#f9cb9c","#ffe599","#b6d7a8","#a2c4c9","#9fc5e8","#b4a7d6","#d5a6bd"],
        ["#e06666","#f6b26b","#ffd966","#93c47d","#76a5af","#6fa8dc","#8e7cc3","#c27ba0"],
        ["#c00","#e69138","#f1c232","#6aa84f","#45818e","#3d85c6","#674ea7","#a64d79"],
        ["#900","#b45f06","#bf9000","#38761d","#134f5c","#0b5394","#351c75","#741b47"],
        ["#600","#783f04","#7f6000","#274e13","#0c343d","#073763","#20124d","#4c1130"]
        ];

function initialize_color_picker(oid){
    var font_input = $("#"+oid+"-font");
    var background_input = $("#"+oid+"-background");
    var input = $("#"+oid);
    var input_val = input.val();
    var font_input_val = font_default_val;
    var background_input_val = background_default_val;
    if(input_val != ""){
        font_input_val = input_val.split(",")[0];
        background_input_val = input_val.split(",")[1];
    }
    else{
        input.val(font_input_val+","+background_input_val);
    };
    font_input.val(font_input_val);
    background_input.val(background_input_val);
    font_input.spectrum({
        color: font_input_val,
        preferredFormat: "hex",
        showInput: true,
        chooseText: "valider",
        showPalette: true,
        palette: default_palette,
        allowEmpty:true,
        clickoutFiresChange: true,
        showInitial: true,
        change: function(tinycolor) {
            var color = font_default_val;
            if(tinycolor != null){
                color = tinycolor.toHexString();
            } else{
                font_input.val(color);
            };
            input.val(color +","+background_input.val());
            input.change();
        }
        });
    background_input.spectrum({
        color: background_input_val,
        preferredFormat: "hex",
        chooseText: "valider",
        showInput: true,
        showPalette: true,
        palette: default_palette,
        allowEmpty:true,
        clickoutFiresChange: true,
        showInitial: true,
        change: function(tinycolor) {
            var color = background_default_val;
            if(tinycolor != null){
                color = tinycolor.toHexString();
            } else{
                background_input.val(color);
            };
            input.val(font_input.val()+","+ color);
            input.change();
        },
    });
    input.change();
};

