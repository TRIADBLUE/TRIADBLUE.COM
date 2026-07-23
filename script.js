/* TriadBlue — shared behavior (app-mode mobile experience + desktop enhancements) */
(function () {
  document.body.classList.add("js");

  var mobile = window.matchMedia("(max-width: 820px)");

  /* ==========================================================
     APP MODE — screen-based navigation (mobile only)
     Desktop keeps the classic one-page website.
     ========================================================== */

  var tabItems = document.querySelectorAll(".tab-bar .tab-item");
  var screens = document.querySelectorAll("[data-screen]");
  var isIndexPage = screens.length > 0;

  /* Map legacy anchors to app screens */
  var screenFor = {
    home: "home", platforms: "home",
    blueprint: "ecosystem", triad: "ecosystem", "bp-panel": "ecosystem",
    hosts: "ecosystem", swipes: "ecosystem",
    ecosystem: "ecosystem",
    faq: "faq"
  };

  function setAppMode() {
    document.body.classList.toggle("app-mode", mobile.matches);
    if (!mobile.matches) {
      document.body.removeAttribute("data-active");
    } else if (isIndexPage && !document.body.getAttribute("data-active")) {
      activateScreen(currentScreenFromHash() || "home", false);
    }
  }

  function currentScreenFromHash() {
    var id = location.hash.replace("#", "");
    return screenFor[id] || null;
  }

  function activateScreen(name, animate) {
    if (!isIndexPage) return;
    document.body.setAttribute("data-active", name);
    tabItems.forEach(function (t) {
      t.classList.toggle("active", t.getAttribute("data-tab") === name);
    });
    if (animate !== false) {
      screens.forEach(function (s) {
        if ((s.getAttribute("data-screen") || "").split(" ").indexOf(name) !== -1) {
          s.classList.remove("screen-in");
          void s.offsetWidth; /* restart animation */
          s.classList.add("screen-in");
        }
      });
    }
    window.scrollTo(0, 0);
  }

  /* Tab bar taps (index page: switch screens; links to other pages pass through) */
  tabItems.forEach(function (t) {
    t.addEventListener("click", function (e) {
      var href = t.getAttribute("href") || "";
      if (isIndexPage && href.charAt(0) === "#" && mobile.matches) {
        e.preventDefault();
        var name = t.getAttribute("data-tab");
        history.replaceState(null, "", "#" + name);
        activateScreen(name);
      }
    });
  });

  /* In-content anchor links (Learn More → #blueprint etc.) */
  function handleHash() {
    var id = location.hash.replace("#", "");
    if (!id) return;
    if (mobile.matches && isIndexPage && screenFor[id]) {
      activateScreen(screenFor[id]);
      if (id === "hosts" || id === "swipes" || id === "bp-panel") {
        activatePanel(id === "bp-panel" ? "bp-panel" : id);
      }
    }
  }
  window.addEventListener("hashchange", handleHash);

  if (mobile.addEventListener) { mobile.addEventListener("change", setAppMode); }
  else if (mobile.addListener) { mobile.addListener(setAppMode); }

  /* ---------- Platform tab browser (The Triad screen) ---------- */
  var tabs = document.querySelectorAll(".ptab");
  var panels = document.querySelectorAll(".platform");

  function activatePanel(id) {
    tabs.forEach(function (t) {
      t.classList.toggle("active", t.getAttribute("data-panel") === id);
    });
    panels.forEach(function (p) {
      p.classList.toggle("active", p.id === id);
    });
  }

  if (tabs.length) {
    activatePanel(tabs[0].getAttribute("data-panel"));
    tabs.forEach(function (t) {
      t.addEventListener("click", function () {
        activatePanel(t.getAttribute("data-panel"));
      });
    });
  }

  /* ---------- Products page sub-screens (Free / Suites / Coach / More) ---------- */
  var subTabs = document.querySelectorAll(".stab");
  var subScreens = document.querySelectorAll("[data-sub-screen]");

  function activateSub(name, animate) {
    document.body.setAttribute("data-sub-active", name);
    subTabs.forEach(function (t) {
      t.classList.toggle("active", t.getAttribute("data-sub") === name);
    });
    if (animate !== false) {
      subScreens.forEach(function (s) {
        if (s.getAttribute("data-sub-screen") === name) {
          s.classList.remove("screen-in");
          void s.offsetWidth;
          s.classList.add("screen-in");
        }
      });
    }
  }

  if (subTabs.length) {
    var subFor = { free: "free", suites: "suites", coach: "coach", apps: "more" };
    activateSub(subFor[location.hash.replace("#", "")] || "free", false);
    subTabs.forEach(function (t) {
      t.addEventListener("click", function () {
        activateSub(t.getAttribute("data-sub"));
      });
    });
    window.addEventListener("hashchange", function () {
      var name = subFor[location.hash.replace("#", "")];
      if (name && mobile.matches) activateSub(name);
    });
  }

  /* ---------- FAQ accordions (mobile) ---------- */
  document.querySelectorAll(".faq article").forEach(function (item, i) {
    var h = item.querySelector("h4");
    if (!h) return;
    if (i === 0) item.classList.add("open");
    h.addEventListener("click", function () {
      if (!mobile.matches) return;
      item.classList.toggle("open");
    });
  });

  /* ---------- Scroll reveal ---------- */
  var revealTargets = document.querySelectorAll(".section-head, .card, .platform, .flow, .faq article, .bundle-banner");
  revealTargets.forEach(function (el) { el.classList.add("reveal"); });

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    revealTargets.forEach(function (el) { io.observe(el); });
  } else {
    revealTargets.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Boot ---------- */
  setAppMode();
  handleHash();
})();
