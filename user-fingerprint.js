
/*
 Detect user without cookies, based on browser fingerprint technique
 
 Usage:
 Save javascript file content into user-fingerprint.js
 Create test html page:
 

      <html>
      <head>
       <script src="user-fingerprint.js"></script> 
      </head>
      <body>
      <div id='fp'></div>

      <script>
        document.getElementById("fp").innerHTML = fingerprint;
      </script>

      </body>
      </html>
 
*/

var fingerprint = (function(window, screen, navigator) {

    function murmurhash3_32_gc(key, seed) {
      var remainder, bytes, h1, h1b, c1, c2, k1, i;

      remainder = key.length & 3; // key.length % 4
      bytes = key.length - remainder;
      h1 = seed;
      c1 = 0xcc9e2d51;
      c2 = 0x1b873593;
      i = 0;

      while (i < bytes) {
          k1 =
            ((key.charCodeAt(i) & 0xff)) |
            ((key.charCodeAt(++i) & 0xff) << 8) |
            ((key.charCodeAt(++i) & 0xff) << 16) |
            ((key.charCodeAt(++i) & 0xff) << 24);
        ++i;

        k1 = ((((k1 & 0xffff) * c1) + ((((k1 >>> 16) * c1) & 0xffff) << 16))) & 0xffffffff;
        k1 = (k1 << 15) | (k1 >>> 17);
        k1 = ((((k1 & 0xffff) * c2) + ((((k1 >>> 16) * c2) & 0xffff) << 16))) & 0xffffffff;

        h1 ^= k1;
            h1 = (h1 << 13) | (h1 >>> 19);
        h1b = ((((h1 & 0xffff) * 5) + ((((h1 >>> 16) * 5) & 0xffff) << 16))) & 0xffffffff;
        h1 = (((h1b & 0xffff) + 0x6b64) + ((((h1b >>> 16) + 0xe654) & 0xffff) << 16));
      }

      k1 = 0;

      switch (remainder) {
        case 3: k1 ^= (key.charCodeAt(i + 2) & 0xff) << 16;
        case 2: k1 ^= (key.charCodeAt(i + 1) & 0xff) << 8;
        case 1: k1 ^= (key.charCodeAt(i) & 0xff);

        k1 = (((k1 & 0xffff) * c1) + ((((k1 >>> 16) * c1) & 0xffff) << 16)) & 0xffffffff;
        k1 = (k1 << 15) | (k1 >>> 17);
        k1 = (((k1 & 0xffff) * c2) + ((((k1 >>> 16) * c2) & 0xffff) << 16)) & 0xffffffff;
        h1 ^= k1;
      }

      h1 ^= key.length;

      h1 ^= h1 >>> 16;
      h1 = (((h1 & 0xffff) * 0x85ebca6b) + ((((h1 >>> 16) * 0x85ebca6b) & 0xffff) << 16)) & 0xffffffff;
      h1 ^= h1 >>> 13;
      h1 = ((((h1 & 0xffff) * 0xc2b2ae35) + ((((h1 >>> 16) * 0xc2b2ae35) & 0xffff) << 16))) & 0xffffffff;
      h1 ^= h1 >>> 16;

      return h1 >>> 0;
    }
        
    // https://github.com/darkskyapp/string-hash
    function checksum(str) {
        var hash = 5381,
            i = str.length;    
        while (i--) hash = (hash * 33) ^ str.charCodeAt(i);
        return hash >>> 0;
    }

    function map(arr, fn){
        var i = 0, len = arr.length, ret = [];
        while(i < len){
            ret[i] = fn(arr[i++]);
        }
        return ret;
    }
    
    function getScreenResolution() {
      var resolution;
       if(this.screen_orientation){
         resolution = (screen.height > screen.width) ? [screen.height, screen.width] : [screen.width, screen.height];
       }else{
         resolution = [screen.height, screen.width];
       }
       return resolution;
    }
    
    
    function hasLocalStorage() {
      try{
        return !!window.localStorage;
      } catch(e) {
        return true; // SecurityError when referencing it means it exists
      }
    }

    function hasSessionStorage() {
      try{
        return !!window.sessionStorage;
      } catch(e) {
        return true; // SecurityError when referencing it means it exists
      }
    }

    function hasIndexDb() {
      try{
        return !!window.indexedDB;
      } catch(e) {
        return true; // SecurityError when referencing it means it exists
      }
    }

    function isCanvasSupported() {
      var elem = document.createElement('canvas');
      return !!(elem.getContext && elem.getContext('2d'));
    }

    function isIE() {
      if(navigator.appName === 'Microsoft Internet Explorer') {
        return true;
      } else if(navigator.appName === 'Netscape' && /Trident/.test(navigator.userAgent)){// IE 11
        return true;
      }
      return false;
    }

    function getPluginsString() {
      if(isIE() && ie_activex){
        return getIEPluginsString();
      } else {
        return getRegularPluginsString();
      }
    }
    

    function getIEPluginsString() {
      if(window.ActiveXObject){
        var names = ['ShockwaveFlash.ShockwaveFlash',//flash plugin
          'AcroPDF.PDF', // Adobe PDF reader 7+
          'PDF.PdfCtrl', // Adobe PDF reader 6 and earlier, brrr
          'QuickTime.QuickTime', // QuickTime
          // 5 versions of real players
          'rmocx.RealPlayer G2 Control',
          'rmocx.RealPlayer G2 Control.1',
          'RealPlayer.RealPlayer(tm) ActiveX Control (32-bit)',
          'RealVideo.RealVideo(tm) ActiveX Control (32-bit)',
          'RealPlayer',
          'SWCtl.SWCtl', // ShockWave player
          'WMPlayer.OCX', // Windows media player
          'AgControl.AgControl', // Silverlight
          'Skype.Detection'];

        // starting to detect plugins in IE
        return this.map(names, function(name){
          try{
            new ActiveXObject(name);
            return name;
          } catch(e){
            return null;
          }
        }).join(';');
      } else {
        return ""; // behavior prior version 0.5.0, not breaking backwards compat.
      }
    }

    function getRegularPluginsString() {
      return map(navigator.plugins, function (p) {
        var mimeTypes = map(p, function(mt){
          return [mt.type, mt.suffixes].join('~');
        }).join(',');
        return [p.name, p.description, mimeTypes].join('::');
      }, this).join(';');
    }

    function getCanvasFingerprint() {
      var canvas = document.createElement('canvas');
      var ctx = canvas.getContext('2d');
      var txt = 'http://ipinfo.io';
      ctx.textBaseline = "top";
      ctx.font = "14px 'Arial'";
      ctx.textBaseline = "alphabetic";
      ctx.fillStyle = "#f60";
      ctx.fillRect(125,1,62,20);
      ctx.fillStyle = "#069";
      ctx.fillText(txt, 2, 15);
      ctx.fillStyle = "rgba(102, 204, 0, 0.7)";
      ctx.fillText(txt, 4, 17);
      return canvas.toDataURL();
    }
    
    function fp() {
          var keys = [];
          keys.push(navigator.userAgent);
          keys.push(navigator.language);
          keys.push(screen.colorDepth);
          if (this.screen_resolution) {
            var resolution = getScreenResolution();
            if (typeof resolution !== 'undefined'){ // headless browsers, such as phantomjs
              keys.push(resolution.join('x'));
            }
          }
          keys.push(new Date().getTimezoneOffset());
          keys.push(hasSessionStorage());
          keys.push(hasLocalStorage());
          keys.push(hasIndexDb());
          //body might not be defined at this point or removed programmatically
          if(document.body){
            keys.push(typeof(document.body.addBehavior));
          } else {
            keys.push(typeof undefined);
          }
          keys.push(typeof(window.openDatabase));
          keys.push(navigator.cpuClass);
          keys.push(navigator.platform);
          keys.push(navigator.doNotTrack);
          keys.push(getPluginsString());
          if(isCanvasSupported()){
            keys.push(getCanvasFingerprint());
          }
          s = murmurhash3_32_gc(keys.join('###'), 31);
          return s;
    }
    
    return fp();

}(this, screen, navigator));

