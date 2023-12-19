odoo.define('mysm_equipment.image_field', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var FieldBinaryImage = basic_fields.FieldBinaryImage;

    FieldBinaryImage.include({
        /**
         * Only enable the zoom on image in read-only mode, and if the option is enabled.
         * Fix Review Image URL
         * 
         * @override
         * @private
         */
        _renderReadonly: function () {
            this._super.apply(this, arguments);

            var unique = this.recordData.__last_update;
            var url = this._getImageUrl(this.model, this.res_id, 'image_1920', unique);
            var $img;
            var imageField = _.find(Object.keys(this.recordData), function(o) {
                return o.startsWith('image_');
            });

            if(this.nodeOptions.background)
            {
                if('tag' in this.nodeOptions) {
                    this.tagName = this.nodeOptions.tag;
                }

                if('class' in this.attrs) {
                    this.$el.addClass(this.attrs.class);
                }

                var urlThumb = this._getImageUrl(this.model, this.res_id, this.name, unique);

                this.$el.empty();
                $img = this.$el;
                $img.css('backgroundImage', 'url(' + urlThumb + ')');
            } else {
                $img = this.$('img');
            }
            if(this.nodeOptions.zoom) {
                var zoomDelay = 0;
                var review_url = this._getImageUrl(this.model, this.res_id, this.nodeOptions.preview_image, unique);
                if (this.nodeOptions.zoom_delay) {
                    zoomDelay = this.nodeOptions.zoom_delay;
                }
                if(this.recordData[imageField]) {
                    $img.attr('data-zoom', 1);
                    $img.attr('data-zoom-image', review_url);

                    $img.zoomOdoo({
                        event: 'mouseenter',
                        timer: zoomDelay,
                        attach: '.o_content',
                        attachToTarget: true,
                        disabledOnMobile: false,
                        onShow: function () {
                            var zoomHeight = Math.ceil(this.$zoom.height());
                            var zoomWidth = Math.ceil(this.$zoom.width());
                            if( zoomHeight < 128 && zoomWidth < 128) {
                                this.hide();
                            }
                            core.bus.on('keydown', this, this.hide);
                            core.bus.on('click', this, this.hide);
                        },
                        beforeAttach: function () {
                            this.$flyout.css({ width: '512px', height: '512px' });
                        },
                        preventClicks: this.nodeOptions.preventClicks,
                    });
                }
            }
        },
    })
});