const maxImageHeight = 500;


document.addEventListener("DOMContentLoaded", function() {

  const imgInPost = document.querySelectorAll('#article_content img');
  imgInPost.forEach(tempImage => {
    if (tempImage.attributes["data-aspect-ratio"] && tempImage.attributes["data-aspect-ratio"].value) {
      let imageWidth = tempImage.offsetWidth;
      let imageHeight = (tempImage.offsetWidth / tempImage.attributes["data-aspect-ratio"].value);
      if (imageHeight > maxImageHeight) {
        const resizeFactor = maxImageHeight / imageHeight;
        imageHeight = maxImageHeight;
        imageWidth *= resizeFactor;
      }
      tempImage.style.width = imageWidth + 'px';
      tempImage.style.height = imageHeight + 'px';
    }
  })

  if ("IntersectionObserver" in window) {
    lazyLoadingWithIntersectionObserver();
  } else {
    lazyLoadingWihtoutIntersectionObserver();
  }
});


function lazyLoadingWithIntersectionObserver() {
  var lazyImages = [].slice.call(document.querySelectorAll("img.lazy"));
  let lazyImageObserver = new IntersectionObserver(function(entries, observer) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        let lazyImage = entry.target;
        
        lazyImage.src = `${lazyImage.dataset.src}?w=${lazyImage.offsetWidth}&h=${lazyImage.offsetHeight}`;
        lazyImage.classList.remove("lazy");
        lazyImageObserver.unobserve(lazyImage);
      }
    });
  });

  lazyImages.forEach(function(lazyImage) {
    lazyImageObserver.observe(lazyImage);
  });
}


function lazyLoadingWihtoutIntersectionObserver() {
  let lazyImages = [].slice.call(document.querySelectorAll("img.lazy"));
  let active = false;

  const lazyLoad = function() {
    if (active === false) {
      active = true;

      setTimeout(function() {
        lazyImages.forEach(function(lazyImage) {
          if ((lazyImage.getBoundingClientRect().top <= window.innerHeight && lazyImage.getBoundingClientRect().bottom >= 0) && getComputedStyle(lazyImage).display !== "none") {
            lazyImage.src = `${lazyImage.dataset.src}?w=${lazyImage.offsetWidth}&h=${lazyImage.offsetHeight}`;
            lazyImage.classList.remove("lazy");

            lazyImages = lazyImages.filter(function(image) {
              return image !== lazyImage;
            });

            if (lazyImages.length === 0) {
              document.removeEventListener("scroll", lazyLoad);
              window.removeEventListener("resize", lazyLoad);
              window.removeEventListener("orientationchange", lazyLoad);
            }
          }
        });

        active = false;
      }, 200);
    }
  };

  document.addEventListener("scroll", lazyLoad);
  window.addEventListener("resize", lazyLoad);
  window.addEventListener("orientationchange", lazyLoad);

  lazyLoad();
}