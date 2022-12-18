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
var fb_info_page = fb_info.getElementsByClassName('xu06os2 x1ok221b')[0];
var fb_info_name, fb_info_post_time = undefined;
if (fb_info_page.length > 0) {
    fb_info_name = fb_info_page[0];
    fb_info_post_time = fb_info_page[0];
}

console.log(fb_info_post_time, fb_info_name);

// fb_contents
// fb_post_content
var fb_post_content = inside_post_info.getElementsByClassName('x1iorvi4 x1pi30zi x1l90r2v x1swvt13')[0];

// fb_post_images <= this elements fb change each load pages => find new way to get this element
var fb_post_image = inside_post_info.querySelector('#jsc_c_2c');
if (fb_post_image.length > 0) {
    ahref = fb_post_image[0].getElementsByClassName('img')[0];
    console.log('images, ', ahref);
}

// get fb comments
var fb_post_comments = inside_post_info.getElementsByClassName('x168nmei x13lgxp2 x30kzoy x9jhf4c x6ikm8r x10wlt62')[0];
var reactions_comments_summaries = fb_post_comments.getElementsByClassName('x6s0dn4 xi81zsa x78zum5 x6prxxf x13a6bvl xvq8zen xdj266r xktsk01 xat24cr x1d52u69 x889kno x4uap5 x1a8lsjc xkhd6sd xdppsyt')[0];
var total_reactions = reactions_comments_summaries.getElementsByClassName('x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62')[0];
console.log('total_reactions, ', total_reactions);
var comment_summaries = reactions_comments_summaries.getElementsByClassName('x6s0dn4 x78zum5 x2lah0s x17rw0jw')[0];
console.log('total_reactions, ', comment_summaries);