const filterButtons = document.querySelectorAll("[data-sticker-filter]");
const stickerRows = document.querySelectorAll("[data-sticker-row]");
const emptyState = document.querySelector("[data-filter-empty]");

function rowMatchesFilter(row, filter) {
  if (filter === "with-album") {
    return row.dataset.hasAlbum === "true";
  }

  if (filter === "without-album") {
    return row.dataset.hasAlbum === "false";
  }

  if (filter === "favorites") {
    return row.dataset.isFavorite === "true";
  }

  return true;
}

function applyStickerFilter(filter) {
  let visibleRows = 0;

  stickerRows.forEach((row) => {
    const isVisible = rowMatchesFilter(row, filter);
    row.hidden = !isVisible;
    if (isVisible) {
      visibleRows += 1;
    }
  });

  if (emptyState) {
    emptyState.hidden = stickerRows.length === 0 || visibleRows > 0;
  }
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    filterButtons.forEach((currentButton) => {
      currentButton.classList.remove("status-chip--active");
    });

    button.classList.add("status-chip--active");
    applyStickerFilter(button.dataset.stickerFilter);
  });
});
