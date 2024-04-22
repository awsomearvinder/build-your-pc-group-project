

const myName = "WHAT A BOGUS FEATURE HAHAHA";
const h1 = document.querySelector(".heading-primary");

console.log(myName);
console.log(h1);

h1.addEventListener("click", function() {
    h1.textContent = myName;
    h1.style.backgroundColor = "red";
    h1.style.padding = "5rem";
})

//////////////////////////////////////////////////////////////////
// Smooth scrolling animation

const allLinks = document.querySelectorAll("a:link");
console.log(allLinks);

allLinks.forEach(function(link) {
    link.addEventListener("click", function(e) {
        e.preventDefault(); 
        const href = link.getAttribute("href");
        console.log(href);

        if(href == "#") window.scrollTo({
        // if(href !== "#" && href.startwith("#"))({ console.log(href)
            // 
            top: 0,
            behavior: "smooth",
        });

        // Scroll to other links
        if(href !== "#" && href.startsWith("#")) {
            const sectionEl = document.querySelector(href);
            sectionEl.scrollIntoView({behavior: "smooth"}); 
        }

        if(link.classList.contains("main-nav-link")) {
        }
    });
});

////////////////////////////////////////////////////////////////////
// STICKY NAVIGATION

const sectionHeroEl = document.querySelector(".section-hero");

const obs = new IntersectionObserver(
    function(entries) {
        const ent = entries[0];
        console.log(ent);
}, 
{
    // In the viewport
    root: null,
    threshold: 0,
});
obs.observe(sectionHeroEl);
