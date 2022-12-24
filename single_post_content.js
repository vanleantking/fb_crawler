var feed = document.getElementsByClassName('x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z');
var single_post = undefined;

console.log(feed.length);
if (feed.length > 0) {
    single_post = feed[0];
}
if (single_post === undefined) {
    //return;
}
var feed_content = single_post.querySelectorAll('#jsc_c_2b');
console.log('feed content by id, ', feed_content.length);
if (feed_content.length > 0) {
    console.log(feed_content);
}

// inside_post_info include [fb_info, fb_contents(fb_post_content, fb_post_images), fb_comments]
var inside_post_info = single_post.getElementsByClassName('x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld')[0];


// get facebook name && facebook post time
var fb_info = inside_post_info.getElementsByClassName('x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a')[0];
var fb_info_name = fb_info.getElementsByClassName('xu06os2 x1ok221b')[0];
var fb_info_post_time = fb_info.getElementsByClassName('xu06os2 x1ok221b')[1];

console.log('fb_info_post_time, fb_info_post_time.textContent, ', fb_info_post_time, fb_info_post_time.textContent);
console.log('fb_info_name, fb_info_name.textContent, ', fb_info_name, fb_info_name.textContent);

// fb_contents
// fb_post_content
var fb_post_content = inside_post_info.getElementsByClassName('x1iorvi4 x1pi30zi x1l90r2v x1swvt13')[0];
console.log('fb_post_content, ', fb_post_content);

// fb_post_images <= this elements fb change each load pages => find new way to get this element
// var fb_post_image = inside_post_info.querySelector('#jsc_c_2c');
// if (fb_post_image.length > 0) {
//     ahref = fb_post_image[0].getElementsByClassName('img')[0];
//     console.log('images, ', ahref);
// }

// get fb comments
var fb_post_comments = inside_post_info.getElementsByClassName('x168nmei x13lgxp2 x30kzoy x9jhf4c x6ikm8r x10wlt62')[0];
var reactions_comments_summaries = fb_post_comments.getElementsByClassName('x6s0dn4 xi81zsa x78zum5 x6prxxf x13a6bvl xvq8zen xdj266r xktsk01 xat24cr x1d52u69 x889kno x4uap5 x1a8lsjc xkhd6sd xdppsyt')[0];
var total_reactions = reactions_comments_summaries.getElementsByClassName('x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62')[0];
console.log('total_reactions, ', total_reactions);
var comment_summaries = reactions_comments_summaries.getElementsByClassName('x6s0dn4 x78zum5 x2lah0s x17rw0jw')[0];
console.log('total_reactions, ', comment_summaries);


var post_comments_only = fb_post_comments.getElementsByClassName('x1jx94hy x12nagc')[0];
console.log('post_comments_only, ', post_comments_only);


// click to choice comment [the most relevant comment (comment from friends, the most action comments on fb), newest comment on fb, all of comment]
var click_option_view_cmt = post_comments_only.getElementsByClassName('x78zum5 x13a6bvl xexx8yu x1pi30zi x18d9i69 x1swvt13 x1n2onr6')[0];
var span_click_option_view_cmt = click_option_view_cmt.getElementsByClassName('x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa')[0];
 console.log(span_click_option_view_cmt.click());

 console.log(span_click_option_view_cmt);


var menu_opt_choice_all = document.getElementsByClassName('x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h');
console.log('menu_opt_choice_all, ', menu_opt_choice_all);

// there are 3 index: [0: the most relevant comment, 1: newest comment, 2: all comments]

//var menu_opts_cmt_choice = document.getElementsByClassName('x1n2onr6 xcxhlts')[0];
//console.log('menu_opts_cmt_choice, ', menu_opts_cmt_choice);
 //var opts = menu_opts_cmt_choice.getElementsByClassName('x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')
 //console.log(opts[2].click())


// click for see all of the comment
var click_able = post_comments_only.getElementsByClassName('x78zum5 x13a6bvl xexx8yu x1pi30zi x18d9i69 x1swvt13 x1n2onr6')[1];
var span_click = click_able.getElementsByClassName('x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa')[0];
 console.log(span_click.click());

 console.log(click_able);

var fb_comment_detail = post_comments_only.getElementsByTagName('li');
console.log('fb_comment_detail, ', fb_comment_detail.length);
for(var idx = 0; idx < fb_comment_detail.length; idx++ ){
    var elm = fb_comment_detail[idx];
    console.log(elm.innerHTML);
    console.log('comment tezt, ', elm.textContent);
}