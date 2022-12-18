# fb_crawler
python web driver


## crawler facebook page info: [fb fanpage infor](crawl.py)
* get all facebook fanpage info: includes [group name, group id, total member, description, ]
## crawler feed facebook page: [feed fb fanpage](feed_fb_page.py)
- **facebook hierachy**:
    * facebook page === `feed` -> include multiple `posts` => a list of elements class: [`x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z`]
    * *fb_post*(single class == `x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z`[idx==i++]) -> include [*post_info*, *post_content*, *post_comments*]
      * *post_info*(single class == `x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a`) -> include [*fb_name*, *post time*]
      * *post_content*: 
- **crawler detail steps**:
  * **step 1**: single class for element post:
     `x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z`
      `var feed = document.getElementsByClassName('x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z');`
      `console.log(feed.length);`
      `for(var idx = 0; idx < feed.length; idx ++){`
          `var elm = feed[idx];`
          `console.log(elm);`
      `}`
     
     *example*: get all posts in facebook page:
     - loop scroll page until can not scroll anymore
     - get all elements with document get `xpath == 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z'` from the class above
     - get *single post* with the index increments `start == 0` to get all post facebook

  * **step2**: `single post`: (for each class *single post* from previous step): include [*post_info*, *post_content*, *post_comments*]
    - *post_info*: include [*facebook name*, *post time*]
    `x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a`
      => include 2 class element index:
      + [`xu06os2 x1ok221b`][0]: facebook fanpage info
      + [`xu06os2 x1ok221b`][1]: facebook post time info
      - *facebook name* => element id:
      `jsc_c_29`
      => get a.href to parse facebook fanpage link
      - *facebook post time* => element id:
      `jsc_c_2a`
    - *post_content*: include two elements: [*post_content*, *post_image*]
        + *post_content*: `x1iorvi4 x1pi30zi x1l90r2v x1swvt13`
        + *post_images*: `#jsc_c_2c`
    - *facebook post comments*: (in foreach *element post* from step 1): `x168nmei x13lgxp2 x30kzoy x9jhf4c x6ikm8r x10wlt62`  include two div elements:
        + *comments summary*: `x6s0dn4 xi81zsa x78zum5 x6prxxf x13a6bvl xvq8zen xdj266r xktsk01 xat24cr x1d52u69 x889kno x4uap5 x1a8lsjc xkhd6sd xdppsyt`: include 2 elements:
            + for get *total reactions*: `x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62`
            + for get *total comments*, *total shares*: `x6s0dn4 x78zum5 x2lah0s x17rw0jw`
        + *detail comments*: get all content comments for facebook single post (include `preview contents`, and if want to load more content, press on `xem thêm bình luận` element): include 2 elements:
            + *the first element*: only some commment previews:
            `ul li`
            + *the second element*: to load more comments:
            `x78zum5 x13a6bvl xexx8yu x1pi30zi x18d9i69 x1swvt13 x1n2onr6`
                + the first index child: `x78zum5 x1iyjqo2 x21xpn4 x1n2onr6`
                **so if want to get all element comments in facebook**:
                    + check if exist element `x78zum5 x13a6bvl xexx8yu x1pi30zi x18d9i69 x1swvt13 x1n2onr6`, click on the element
                    + loop over the class comments to get the content: `ul li`
        + **every single** *detail comment* (**after click on load more comment** action): (inside single *comment* in the previous step): [`ul li`]:
            + each single comment include 2 elements:
              + `div class=x1n2onr6` (single element class: ) == li.index[0]: includes 2 elements [`icon profile comment author`, `detail comment` (include `author name(link to profile detail)`, ``)]*detail comment*
                + *icon profile comment author*: `xqcrz7y x14yjl9h xudhj91 x18nykt9 xww2gxu x1lliihq x1w0mnb x1n2onr6 xr9ek0c` => get a.href to parse `profile page comment author`
                + *detail content*: `x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi`: include 2 elements:
                  + the first element *comment for the post*: *comments content* && *author name*: `x1rg5ohu xv55zj0 x1vvkbs xxymvpz` > `x3nfvp2 x1n2onr6 xxymvpz xh8yej3`
                    + > `x1y1aw1k xn6708d xwib8y2 x1ye3gou`
                      + *author name*: `x1y1aw1k xn6708d xwib8y2 x1ye3gou`: get a.href
                      + *comment content*: `x1lliihq xjkvuk6 x1iorvi4`
                  + the second element: `x1ve5b48 x177n6bx x10l6tqk x1ja2u2z xlshs6z` *report*, hide comment*
              + **not required** reply for the comment: == li.index[1]:
                + *total reply*: `x1n2onr6 x46jau6`: click on the element to show all *reply*
                + after click on the element: `xdj266r xexx8yu x4uap5 x18d9i69 xkhd6sd` > `ul` > `li`: get all *comments reply*
    


### example get all posts:
`var feed = document.getElementsByClassName('x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z');`
`console.log(feed.length);`
`for(var idx = 0; idx < feed.length; idx ++){`
    `console.log('------------------------------------------------------------');`
    `var elm = feed[idx];`
    `var feed_content = elm.querySelectorAll('#jsc_c_2b');`
    `console.log('feed content by id, ', feed_content.length);`
    `if (feed_content.length > 0) {`
    `    console.log(feed_content);`
    `}`
    `var clss_feed_content = elm.getElementsByClassName('x1iorvi4 x1pi30zi x1l90r2v x1swvt13');`
    `console.log('feed content by class name, ', clss_feed_content.length);`
    `if (clss_feed_content.length > 0) {`
    `    console.log(clss_feed_content[0]);`
    `}`
    `console.log(clss_feed_content);`
`}`


### example get all comments for single post:
var feed = document.getElementsByClassName('x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z');
var single_post = undefined;

console.log(feed.length);
if (feed.length > 0) {
    single_post = feed[0]
}
if (single_post === undefined) {
    return
}
var feed_content = single_post.querySelectorAll('#jsc_c_2b');
console.log('feed content by id, ', feed_content.length);
if (feed_content.length > 0) {
    console.log(feed_content);
}
var clss_feed_content = single_post.getElementsByClassName('x1iorvi4 x1pi30zi x1l90r2v x1swvt13');
console.log('feed content by class name, ', clss_feed_content.length);
var post_info = clss_feed_content.getElementByClassName('x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z');
