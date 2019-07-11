var fetch_more = true;
var offset = 20;
var step = 20;

document.addEventListener("scroll", fetchMoreContent);

function fetchMoreContent() {
  if (fetch_more) {
    if (window.scrollY + 2 * window.innerHeight > document.body.scrollHeight) {
      fetch_more = false;

      var request = new XMLHttpRequest();

      request.open(
        "GET",
        "https://api.pinkadda.com/v1/posts/published" +
          "?project=pinkadda&limit=20&offset=" +
          offset,
        true
      );

      request.onload = function() {
        if (request.status == 200) {
          result = JSON.parse(request.responseText);
          posts = result["posts"];

          posts.forEach(post => {
            var parent = document.getElementById("norm_articles");

            parent.appendChild(document.createElement("hr"));

            var newPost = document.createElement("a");
            newPost.className = "norm_article_cont";
            newPost.setAttribute("href", "/article/" + post["url"]);

            var postImage = document.createElement("img");
            postImage.className = "norm_article_img";
            postImage.setAttribute("src", post["titleImage"]);
            postImage.setAttribute("alt", "fix_me");
            newPost.appendChild(postImage);

            var postSummary = document.createElement("summary");

            var postHeading = document.createElement("h3");
            postHeading.className = "article_heading";
            postHeading.appendChild(document.createTextNode(post["title"]));
            postSummary.appendChild(postHeading);
            postSummary.appendChild(document.createElement("br"));

            var postDescription = document.createElement("div");
            postDescription.className = "article_description";
            var postDescriptionPara = document.createElement("p");
            postDescriptionPara.appendChild(document.createTextNode("fix_me"));
            postDescription.appendChild(postDescriptionPara);
            postSummary.appendChild(postDescription);

            var postWriter = document.createElement("span");
            postWriter.className = "article_writer";
            postWriter.appendChild(document.createTextNode(post["author"]));
            postSummary.appendChild(postWriter);

            var interpunct = document.createElement("span");
            interpunct.className = "interpunct";
            interpunct.appendChild(document.createTextNode(" · "));
            postSummary.appendChild(interpunct);

            var postCreatedOn = document.createElement("span");
            postCreatedOn.className = "article_publish_date";
            postCreatedOn.appendChild(
              document.createTextNode(post["created_on"])
            );
            postSummary.appendChild(postCreatedOn);

            newPost.appendChild(postSummary);

            parent.appendChild(newPost);
          });

          offset += step;
          if (result["hasMore"] == true) fetch_more = true;
          else fetch_more = false;
        }
      };

      request.send();
    }
  }
}
