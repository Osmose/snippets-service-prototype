;(function($, nunjucks) {
    'use strict';

    var VARIABLE_URL = '/admin/base/snippettemplate/{{id}}/variables/';

    var env = new nunjucks.Environment();
    env.addFilter('format', function(str) {
        var replacements = Array.prototype.slice.call(arguments, 1);
        for (var k = 0; k < replacements.length; k++) {
            str = str.replace('%s', replacements[k]);
        }
        return str;
    });

    var tmplGlobals = {
        '_': function(str) {
            return str;
        }
    };

    function TemplateDataWidget(templateSelect, dataWidget) {
        var self = this;
        this.$template = $(templateSelect);
        this.$dataWidget = $(dataWidget);
        this.$data = this.$dataWidget.find('input');
        this.$dataFields = this.$dataWidget.find('.fields');
        this.snippetPreview = this.$dataWidget.find('.snippet-preview')[0];

        this.data = JSON.parse(this.$data.val());
        this.template = null;

        var tmpl = new nunjucks.Template(this.$dataWidget.find('.editor-tmpl').text());

        // Whenever the selected template changes, refresh the list of template
        // data to include new variables.
        this.$template.change(function(e) {
            var templateId = self.$template.val();
            $.get(VARIABLE_URL.replace('{{id}}', templateId))
             .success(function(template) {
                self.template = template;

                for (var k = 0; k < template.fields.length; k++) {
                    var field = template.fields[k];

                    // TODO: Handle case where new variable has the same name as an
                    // existing one, but a different type.
                    if (!(field.name in self.data)) {
                        self.data[field.name] = {
                            value: '',
                            type: field.type
                        };
                    } else {
                        self.data[field.name].type = field.type;
                    }
                }

                self.$dataFields.html(tmpl.render({
                    data: self.data
                }));
                self.writeData();
            });
        });

        this.$dataFields.on('change input', '.text', function(e) {
            self.writeData();
            self.updatePreview();
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
                self.updatePreview();
            };
            reader.readAsDataURL(file);
        });

        $(this.snippetPreview).on('load', function() {
            self.updatePreview();
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
        },

        updatePreview: function() {
            this.snippetPreview.contentWindow.postMessage(this.renderSnippet(),
                                                         '*');
        },

        renderSnippet: function() {
            var renderData = Object.create(tmplGlobals);
            for (var name in this.data) {
                renderData[name] = this.data[name].value;
            }

            if (this.template._tmpl === undefined) {
                this.template._tmpl = new nunjucks.Template(this.template.code,
                                                            env);
            }

            return this.template._tmpl.render(renderData);
        }
    };

    $(function() {
        var widget = new TemplateDataWidget('#id_template',
                                            '.template-data-widget');
    });
})(jQuery, nunjucks);
