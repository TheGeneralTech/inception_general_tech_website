var fetch_more = true;
var page_num = 1;

document.addEventListener("scroll", fetchMoreContent);

function fetchMoreContent() {
  if (fetch_more) {
    if (window.scrollY + 2 * window.innerHeight > document.body.scrollHeight) {
      fetch_more = false;

      var request = new XMLHttpRequest();

      request.open(
        "GET",
        window.location.href + "/feed/page/" +
          page_num,
        true
      );

      request.onload = function() {
        if (request.status == 200) {
          result = JSON.parse(request.responseText);

          posts = result["posts"];
          art_conts = document.getElementsByClassName('norm_articles');
          last_cont = art_conts[art_conts.length - 1];
          new_art_cont = last_cont.cloneNode();
          new_art_cont.innerHTML = posts;

          document.getElementById("main")
          .insertBefore(new_art_cont, last_cont)

          if (result["hasMore"] == true) fetch_more = true;
          else fetch_more = false;
          page_num++;
        }
      };

      request.send();
    }
  }
}