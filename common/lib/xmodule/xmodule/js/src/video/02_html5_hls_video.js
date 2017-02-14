/**
 * HTML5 video player module to support HLS video playback.
 *
 */

(function(requirejs, require, define) {
    'use strict';
    define('video/02_html5_hls_video.js', ['video/02_html5_video.js', 'hls'], function(HTML5Video, HLS) {
        var HLSVideo = {};

        HLSVideo.Player = (function() {
            function PlayerHLS(el, config) {
                this.video = document.createElement('video');
                this.videoEl = $(this.video);

                this.hls = new HLS();
                this.hls.loadSource('http://www.streambox.fr/playlists/test_001/stream.m3u8');
                this.hls.attachMedia(this.video);
                this.hls.on(HLS.Events.MANIFEST_PARSED, function(data) {
                    console.log(data);
                });

                this.init(el, config);
            }

            PlayerHLS.prototype = Object.create(HTML5Video.Player.prototype);
            PlayerHLS.prototype.constructor = PlayerHLS;

            return PlayerHLS;
        }());

        return HLSVideo;
    });
}(RequireJS.requirejs, RequireJS.require, RequireJS.define));
