;(function($, nunjucks) {
    'use strict';

    var VARIABLE_URL = '/admin/base/snippettemplate/{{id}}/variables/';

    function TemplateDataWidget(templateSelect, data, dataFields,
                                dataEditorTemplate) {
        var self = this;
        this.$template = $(templateSelect);
        this.$data = $(data);
        this.$dataFields = $(dataFields);

        this.data = JSON.parse(this.$data.val());

        var tmpl = new nunjucks.Template($(dataEditorTemplate).text());

        // Whenever the selected template changes, refresh the list of template
        // data to include new variables.
        this.$template.change(function(e) {
            var templateId = self.$template.val();
            $.get(VARIABLE_URL.replace('{{id}}', templateId))
             .success(function(variables) {
                for (var k = 0; k < variables.length; k++) {
                    var variable = variables[k];

                    // TODO: Handle case where new variable has the same name as an
                    // existing one, but a different type.
                    if (!(variable.name in self.data)) {
                        self.data[variable.name] = {
                            value: '',
                            type: variable.type
                        };
                    }
                }

                self.$dataFields.html(tmpl.render({
                    data: self.data
                }));
            });
        });

        this.$dataFields.on('change keydown', '.text', function(e) {
            self.writeData();
        });

        this.$dataFields.on('change', '.image-upload', function(e) {
            if (this.files.length < 1) return;
            var file = this.files[0];

            // Check to see if this is an image
            if (!file.type.match(/image.*/)) return;

            // Load file.
            var $upload = $(this);
            var preview = $upload.next('.preview')[0];
            var $hidden_input = $upload.next('.value');

            var reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                $hidden_input.val(e.target.result);
                self.writeData();
            };
            reader.readAsDataURL(file);
        });

        this.$template.change();
    }

    TemplateDataWidget.prototype = {
        writeData: function() {
            var self = this;
            this.$dataFields.find('.template-data').each(function() {
                var $row = $(this);
                var name = $row.find('.name').text();
                var value = $row.find('.value').val();
                self.data[name].value = value;
            });

            this.$data.val(JSON.stringify(this.data));
        }
    };

    $(function() {
        var widget = new TemplateDataWidget('#id_template', '#id_data',
                                            '.template-data-fields',
                                            '#template-data-editor');
    });
})(jQuery, nunjucks);
