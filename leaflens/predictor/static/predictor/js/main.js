document.addEventListener("DOMContentLoaded", function () {
  // =====================================
  // Upload Page
  // =====================================

  const uploadZone = document.getElementById("upload-zone");
  const imageInput = document.getElementById("image");
  const previewWrap = document.getElementById("preview-wrap");
  const previewImage = document.getElementById("preview-image");
  const filenameText = document.getElementById("filename-text");
  const removeBtn = document.getElementById("remove-btn");
  const analyzeBtn = document.getElementById("analyze-btn");
  const uploadForm = document.getElementById("upload-form");

  if (uploadZone && imageInput) {
    function handleFile(file) {
      if (!file) return;

      if (!file.type.match(/image\/(jpeg|jpg|png)/)) {
        alert("Please upload a JPG or PNG image.");
        return;
      }

      const reader = new FileReader();

      reader.onload = function (e) {
        previewImage.src = e.target.result;
        filenameText.textContent = file.name;

        previewWrap.classList.add("active");

        uploadZone.style.display = "none";

        analyzeBtn.disabled = false;
      };

      reader.readAsDataURL(file);
    }

    uploadZone.addEventListener("click", function (e) {
      if (e.target.closest("label")) return;

      imageInput.click();
    });

    imageInput.addEventListener("change", function () {
      if (imageInput.files.length) handleFile(imageInput.files[0]);
    });

    ["dragenter", "dragover"].forEach((event) => {
      uploadZone.addEventListener(event, function (e) {
        e.preventDefault();

        uploadZone.classList.add("drag-active");
      });
    });

    ["dragleave", "drop"].forEach((event) => {
      uploadZone.addEventListener(event, function (e) {
        e.preventDefault();

        uploadZone.classList.remove("drag-active");
      });
    });

    uploadZone.addEventListener("drop", function (e) {
      const file = e.dataTransfer.files[0];

      if (!file) return;

      const dt = new DataTransfer();

      dt.items.add(file);

      imageInput.files = dt.files;

      handleFile(file);
    });

    removeBtn.addEventListener("click", function () {
      imageInput.value = "";

      previewImage.src = "";

      previewWrap.classList.remove("active");

      uploadZone.style.display = "block";

      analyzeBtn.disabled = true;
    });

    uploadForm.addEventListener("submit", function () {
      analyzeBtn.classList.add("is-loading");

      analyzeBtn.disabled = true;
    });
  }

  // =====================================
  // Result Page
  // =====================================

  const progressFill = document.getElementById("confidence-progress");

  if (progressFill) {
    const confidence = parseFloat(progressFill.dataset.confidence);

    progressFill.style.width = "0%";

    setTimeout(function () {
      progressFill.style.width = confidence + "%";
    }, 200);
  }
});
