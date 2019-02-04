/*
 run from project folder command:
 npm install --save request-promise
 See more: https://github.com/request/request-promise
*/
const request = require('request-promise')

/*
  URL for checking
*/
let URL = "http://www.onet.pl/";

/*
 Generate long  long lived access token
 https://sujipthapa.co/blog/generating-never-expiring-facebook-page-access-token
*/
let ACCESS_TOKEN = "EAANITTvh38gBAF4TtxZCSmrhkVkHeZCIm6ZAP2QZBiwy4SCuhFpYTmsrvy7FYAmHc4GVZC4yMdpjWc4ZCswojBa6EnKoRPD8GzUOzCFPuGuuTJYMS0s9w1UOF9pzS0JfZCIKi9g8B86PNZAZB7tn3USxVwNXpZBLdecPeBclZA3DUL7WIpiwBWYrAqB"

const options = {
    method: 'GET',
    uri: "https://graph.facebook.com/",
    qs: {
      fields: "id,engagement,og_object",
      access_token: ACCESS_TOKEN,
      id: URL
    }
  }

/*
 let't make request to FB API
*/
request(options)
  .then(function (response) {
      console.log(response);
      /*
          Result:

          {
            "id": "http:\/\/www.onet.pl\/",
            "engagement": {
              "reaction_count": 184181,
              "comment_count": 50074,
              "share_count": 170655,
              "comment_plugin_count": 8
            },
            "og_object": {
              "id": "10150246927100496",
              "description": "Onet: codzienne \u017ar\u00f3d\u0142o informacji milion\u00f3w Polak\u00f3w - wiadomo\u015bci z kraju i ze \u015bwiata 24\/7, pogoda, sport, biznes, moto, rozrywka. B\u0105d\u017a na bie\u017c\u0105co z Onet!",
              "title": "Onet \u2013 Jeste\u015b na bie\u017c\u0105co",
              "type": "website",
              "updated_time": "2019-02-04T14:44:27+0000"
            }
          }

      */
  })
  .catch(function (err) {
      console.error(err);
});  

