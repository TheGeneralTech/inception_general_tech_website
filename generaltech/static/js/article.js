var fetch_more = true;

document.addEventListener("scroll", fetchMoreContent);

function fetchMoreContent() {
  if (fetch_more) {
    if (window.scrollY + 3 * window.innerHeight > document.body.scrollHeight) {
      fetch_more = false;

      var request = new XMLHttpRequest();

      request.open(
        "GET",
        window.location.href + "/related",
        true
      );

      request.onload = function() {
        if (request.status == 200) {
          result = JSON.parse(request.responseText);

          articles = result["articles"];
          Object.keys(articles).map(function(article_key){
              console.log(article_key);
              article_element = document.createElement("article");
              document.body.appendChild(article_element);
              article_element.outerHTML = articles[article_key];
          })

        } else fetch_more = true;
      };

      request.send();
    }
  }
}
function showFullArticle(article_id){
    article = document.getElementById("article-"+article_id);
    article.style.height = "auto";
    article.style.overflow = "unset";
    article.lastElementChild.style.display = "none";
}