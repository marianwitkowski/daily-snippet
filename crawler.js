const jsdom = require("jsdom");
const { JSDOM } = jsdom;

var Crawler = require("crawler");

var c = new Crawler({
    maxConnections : 20,
    rateLimit: 2000,
    retries: 10,
    retryTimeout: 10000,
    userAgent: "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    callback : function (error, res, done) {
        if(error){
            console.log(error);
        }else{
            var $ = res.$;
            var title = $('meta[property="og:title"]').attr('content');
            var keywords = $('meta[name="keywords"]').attr('content');
            console.log(title+"|"+keywords+"|"res.body);
        }
        done();
    }
});

c.queue(
    [
        'http://onet.pl/',
        'http://wp.pl/',
        'http://gazeta.pl/',
        'https://onet.pl/',
    ]);
    
