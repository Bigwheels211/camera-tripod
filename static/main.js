window.onload = function () {
  const button = document.getElementById("takePic");
  const preview = document.getElementById("previmg");

  button.addEventListener("click", async function () {
    // Tell server to take a picture
    await fetch("/takePic");
    // Force refresh preview image by appending timestamp
    preview.src = "/previewimg?t=" + Date.now();
  });
};
