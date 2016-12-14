function init_iconpicker(oid){
    $('#'+oid).iconpicker().on('change', function(e) {
        $('#'+$(this).data('oid')).val(e.icon_class +','+ $($(this).find('input').first()).val())
    });
}

$(document).on('iconpicker-loaded', function(){
    $.fn.iconpicker.Constructor.prototype.select = function (icon) {
        var op = this.options;
        var el = this.$element;
        op.selected = $.inArray(icon.replace(op.iconClassFix, ''), op.icons);
        if (op.selected === -1) {
            op.selected = 0;
            icon = op.iconClassFix + op.icons[op.selected];
        }
        if (icon !== '' && op.selected >= 0) {
            op.icon = icon;
            if(op.inline === false){
                el.find('input').val(icon);
                el.find('i').attr('class', '').addClass(op.iconClass).addClass(icon);
            }
            if(icon === op.iconClassFix){
                el.trigger({ type: "change", icon: 'empty' });
            }
            else {
                //edited by Amen: add icon class to the tiggered event
                el.trigger({ type: "change", icon: icon, icon_class: op.iconClass });
            }
            op.table.find('button.' + op.selectedClass).removeClass(op.selectedClass);
        }
    };

});