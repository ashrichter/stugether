$(document).ready(function() {
    const tabs = document.querySelectorAll(".search-tabs .search-tabs-items li");
    const sections = document.querySelectorAll(".search-tabs .tab-content");

    tabs.forEach(tab => {
      tab.addEventListener("click", e => {
        e.preventDefault();
        removeActiveTab();
        addActiveTab(tab);
      });
    })

    const removeActiveTab = () => {
      tabs.forEach(tab => {
        tab.classList.remove("is-active");
      });
      sections.forEach(section => {
        section.classList.remove("is-active");
      });
    }

    const addActiveTab = tab => {
      tab.classList.add("is-active");
      const href = tab.querySelector("a").getAttribute("href");
      const matchingSection = document.querySelector(href);
      matchingSection.classList.add("is-active");
    }
})