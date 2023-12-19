odoo.define('ks_odoo11_web_listview_sticky_header.stick_header', function (require) {
'use strict';
    var ListView = require('web.ListRenderer');
    ListView.include({

    _freezeColumnWidths: function () {
        if(this.state.model== 'maintenance.equipment'){
            if(this.getParent() && this.getParent().$el && (this.getParent().$el.hasClass("o_field_one2many") !== false || this.getParent().$el.hasClass("o_field_many2many") !== false)) {
                this._super.apply(this,arguments);
            }
            else{
                var self = this;
                const table = this.el.getElementsByTagName('table')[0];

                var o_content_area = $(".o_content")[0];

                function sticky(){
                    self.$el.find(".table.o_list_table").each(function () {
                        $(this).stickyTableHeaders({scrollableArea: o_content_area, fixedOffset: 0.1});
                    });
                  }

                function fix_body(position){
                     $("body").css({
                       'position': position,
                    });
                }


                if(this.$el.parents('.o_field_one2many').length === 0){
                        sticky();
                        fix_body("fixed");
                        $(window).unbind('resize', sticky).bind('resize', sticky);
                        this.$el.css("overflow-x","visible");
                        this.$el.css("overflow-y","visible");
                }
                else{
                    fix_body("relative");
                }
                $("div[class='o_sub_menu']").css("z-index",4);
            }
        }
        else{
            if (!this.columnWidths && this.el.offsetParent === null) {
                // there is no record nor widths to restore or the list is not visible
                // -> don't force column's widths w.r.t. their label
                return;
            }
            const thElements = [...this.el.querySelectorAll('table thead th')];
            if (!thElements.length) {
                return;
            }
            const table = this.el.getElementsByClassName('o_list_table')[0];
            let columnWidths = this.columnWidths;
    
            if (!columnWidths || !columnWidths.length) { // no column widths to restore
                // Set table layout auto and remove inline style to make sure that css
                // rules apply (e.g. fixed width of record selector)
                table.style.tableLayout = 'auto';
                thElements.forEach(th => {
                    th.style.width = null;
                    th.style.maxWidth = null;
                });
    
                // Resets the default widths computation now that the table is visible.
                this._computeDefaultWidths();
    
                // Squeeze the table by applying a max-width on largest columns to
                // ensure that it doesn't overflow
                columnWidths = this._squeezeTable();
            }
    
            thElements.forEach((th, index) => {
                // Width already set by default relative width computation
                if (!th.style.width) {
                    th.style.width = `${columnWidths[index]}px`;
                }
            });
    
            // Set the table layout to fixed
            table.style.tableLayout = 'fixed';
        }
        },

    _onCellClick: function (event) {
        // The special_click property explicitely allow events to bubble all
        // the way up to bootstrap's level rather than being stopped earlier.
        var $td = $(event.currentTarget);
        var $tr = $td.parent();
        var rowIndex = $tr.index();
        if (!this._isRecordEditable($tr.data('id')) || $(event.target).prop('special_click')) {
            return;
        }
        var fieldIndex = Math.max($tr.find('.o_field_cell').index($td), 0);
        this._selectCell(rowIndex, fieldIndex, {event: event});
    },
    setRowMode: function (recordID, mode) {
        var self = this;
        return this._super.apply(this, arguments).then(function (){
            var editMode = (mode === 'edit');
            var $row = self._getRow(recordID);
            self.currentRow = editMode ? $row.index() : null;
        });
    },
    on_attach_callback: function () {
        var self = this;
        $("div.modal-footer a").bind('click', function() {
                if($(this).prop("href").split("/.")[1] && $(this).prop("href").split("/.")[1] === "o_onboarding_container") {
                    setTimeout(function(){
                        if($(".o_content").length && (($(".o_content").offset().top+1) != $(".tableFloatingHeaderOriginal").css("top"))) {
                            $(".tableFloatingHeaderOriginal").css("top",$(".o_content").offset().top+0.50);
                        }
                    },400);
                }
        });
     },

    });
});
