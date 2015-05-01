/*
The MIT License (MIT)
Copyright (c) 2014 NTHUOJ team
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
$(document).ready(function() {
    add_attribute('id_coowner', 'class', 'searchable');
    add_attribute('id_problem', 'class', 'searchable');
    hide('id_owner');
    enable_search();
    modify_label();
    widen_multiselect();
});

function enable_search() {
    $('.searchable').multiSelect({
        selectableHeader: 
        "<input type='text' class='search-input form-control' autocomplete='off' placeholder='Search and Add...'>",
        selectionHeader: 
        "<input type='text' class='search-input form-control' autocomplete='off' placeholder='Search and Delete...'>",
        selectableFooter: "<div class='all-header' style='text-align:center;'>All</div>",
        selectionFooter: "<div class='selected-header' style='text-align:center;'>Selected</div>",
        afterInit: function(ms) {
            var that = this,
                $selectableSearch = that.$selectableUl.prev(),
                $selectionSearch = that.$selectionUl.prev(),
                selectableSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selectable:not(.ms-selected)',
                selectionSearchString = '#' + that.$container.attr('id') + ' .ms-elem-selection.ms-selected';

            that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
                .on('keydown', function(e) {
                    if (e.which === 40) {
                        that.$selectableUl.focus();
                        return false;
                    }
                });

            that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
                .on('keydown', function(e) {
                    if (e.which == 40) {
                        that.$selectionUl.focus();
                        return false;
                    }
                });
        },
        afterSelect: function() {
            this.qs1.cache();
            this.qs2.cache();
        },
        afterDeselect: function() {
            this.qs1.cache();
            this.qs2.cache();
        }
    });
}

function widen_multiselect(){
    add_attribute('ms-id_coowner','style','width:100%;');
    add_attribute('ms-id_problem','style','width:100%;');
}

function modify_label(){
    modify_html('[for=id_cname]','Contest name');
    modify_html('[for=id_freeze_time]','Freeze Time(mins):');
    modify_html('[for=id_start_time]','Start Time(YYYY-MM-DD hh:mm:ss):');
    modify_html('[for=id_end_time]','End Time(YYYY-MM-DD hh:mm:ss):');
    modify_html('.help-block','');
}
