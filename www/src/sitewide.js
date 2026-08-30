/* © 2026 1F2L. All rights reserved. */

// animations
/** List of elements with .animated class */ let animElements = new Map();

/**
 * Loads a cookie as a boolean rather than a string
 * @param {string} name - Name of the cookie to retrieve
 * @returns {(boolean|null)}
 */
export function loadcookieBoolean(name) {
    const bool = parseBoolean(loadCookieString(name))

    if (bool !== null && bool !== "") {
        return bool
    } else {
        console.error(`Cookie ${name} does not exist`)
        return null
    }
}

/**
 * Gets a cookie from user cookies with some extra features
 * @param {string} name - name of the cookie to retreive
 * @returns {string}
 */
export function loadCookieString(name) {
    // make list of cookies by splitting
    let ca = document.cookie.split(";");

    // iterate over each cookie
    for (let i = 0; i < ca.length; i++) {
        let cookie = ca[i].trim() // trim extra stuff

        // if it matches the cookie we're looking for
        if (cookie.startsWith(name + "=")) {
            // get the value
            const value = cookie.substring(name.length + 1);
            // return as string
            if (value != null && value != "") {
                return value.toString();
            } else {
                console.warn("Non-existing cookie: " + name)
                return null
            }
        }
    }
    return null;
}

/**
 * @param {string} name - name of the cookie to save
 * @param {string} value - the value to save to the cookie
 * @param {number} days - number of days to save the cookies (can also use 'forever')
 * @param {string} location - the path where the cookie should be accessible
 * @returns {null} nothing is returned
 */
export function writeCookie(name, value, days, location = '/') {
    const date = new Date();
    // current time + time to expire (in milliseconds)
    if (days !== 'forever') {
        date.setTime(date.getTime() + ((((days * 24) * 60) * 60) * 1000));
    } else {
        date.setFullYear(date.getFullYear() + 10);
    }
    // put together expire time string
    const expires = date.toUTCString();
    // write the cookie
    document.cookie = `${name}=${value};expires=${expires};path=${location};`;
}

/**
 * Turns a string into a boolean
 * @param {string} str - the string to transform 
 * @returns {boolean} the boolean version
 */
export function parseBoolean(str) {
    if (str == null) return null;
    str = str.toLowerCase()
    if (str === "true" || str === "1") {
        return true;
    } else if (str === "false" || str === "0") {
        return false;
    } else {
        console.log('Failed to parse string ' + str + ' to boolean null');
        return null;
    }
}


/**
 * Waits using a promise
 *
 * AWAIT THIS FUNCTION
 * @param {number} timeSec time in seconds to wait
 * @returns {boolean} True
 */
export async function wait(timeSec) {
    await new Promise(resolve => setTimeout(resolve, Math.floor(timeSec * 1000)));
    return true;
}

/**
 * Waits using a promise
 *
 * AWAIT THIS FUNCTION
 * @param {number} timeMS time in ms to wait
 * @returns {boolean} True
 */
export async function waitms(timeMS) {
    await new Promise(resolve => setTimeout(resolve, Math.floor(timeMS)));
    return true;
}


/**
 * Checks if an element is (at least 20%) on the screen
 * @param {element} el - the element to check
 * @returns {boolean} Boolean, on screen or not
 */
export function isElementInViewport(el) {
    const percentageVisible = 10; //? Percentage that has to be on screen

    const rect = el.getBoundingClientRect();
    const elementHeight = rect.height;
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;

    // calculate how much of the element's height is on screen
    const visibleHeight = Math.min(rect.bottom, viewportHeight) - Math.max(rect.top, 0);

    // return if its atleast percentageVisible percent on screen
    return visibleHeight >= elementHeight * (percentageVisible / 100);
}

/**
 * Check if an element has a certain percentage amount on the screen
 * @param {element} el - the element to check
 * @param {number} percentage - The percentage that has to be on screen
 * @returns {boolean} Boolean, on screen or not
 */
export function isElementInViewportP(el, percentage) {
    if (percentage > 100) {
        throw new Error("[isElementInViewportP] Percentage cannot be greater than 100%?");
    }
    else if (percentage < 0) {
        percentage = 0;
    }

    const rect = el.getBoundingClientRect(); //? Element information relative to the viewport
    const elementHeight = rect.height;
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;

    // calculate how much of the element's height is on screen
    const visibleHeight = Math.min(rect.bottom, viewportHeight) - Math.max(rect.top, 0);

    // return if its atleast percentageVisible percent on screen
    return visibleHeight >= elementHeight * (percentage / 100);
}



//* Animate .animated elements when they come on screen
/** This is set to true if the user scrolls or resizes the page */ let updateAnimations = false;

// Listeners that check if we need to check .animated elements
document.body.addEventListener('scroll', () => {
    updateAnimations = true;
});
document.querySelector('main')?.addEventListener('scroll', () => {
    updateAnimations = true;
});
window.addEventListener('resize', () => {
    updateAnimations = true;
});

/**
 * A function that checks if an update is required on this frame
 * 
 * Makes use of requestAnimationFrame() to render efficiently
 */
export function animationLoop() {
    if (updateAnimations) {
        applyAnimations(); // Function that checks and applys animations

        // reset
        updateAnimations = false;
    }

    // Recall this function right before the next frame is drawn
    requestAnimationFrame(animationLoop);
}

/**
 * Apply animations to all .animated elements that are on the screen
 *
 * Uses percentage value from isElementInViewport()
 */
export async function applyAnimations() {
    findAnimatedElements() // Update animElements Map

    // Loop over all .animated elements
    for (const [el, isAnimatedAlready] of animElements) {

        // Skip already animated elements
        if (isAnimatedAlready === true) continue;

        // Check if its in view
        if (isElementInViewport(el)) {
            const anim = el.getAttribute('anim') // The animation to apply

            if (anim) {
                // Apply animation and make visible again
                el.style.animation = anim;
                el.style.visibility = "visible";

                // Set element as played
                animElements.set(el, true);
            }
        }
    }
}

/**
 * Updates the animElements Map with all the elements with the .animated class
 */
export function findAnimatedElements() {
    // Get all .animated elements
    const elements = document.querySelectorAll(".animated");

    // Loop over them
    for (const el of elements) {

        // Check if it is not already in the map
        if (!animElements.has(el)) {

            // Add it
            animElements.set(el, false);

            // Animations begin without being visible to look nice
            el.style.visibility = "hidden";
        }
    }
}


/**
 * Toggle between light and dark mode on pages
 */
export function toggleTheme() {
    // Read current theme from cookie
    const currentTheme = loadcookieBoolean("darkMode");

    // Toggle theme
    const isNowDark = !currentTheme;

    console.log(`Toggling theme to ${isNowDark ? "dark ⚫️" : "light ⚪️"}`);

    // Write new theme to cookie
    writeCookie("darkMode", isNowDark, 365);

    applyTheme();
}

/**
 * Checks if the dark theme is set
 * @returns {boolean} True if dark, false if light
 */
export function isDarkTheme() {
    // Read current theme from cookie
    const currentTheme = loadcookieBoolean("darkMode");

    // Default to dark mode
    if (currentTheme === null) {
        // Set the cookie
        writeCookie("darkMode", true, 365);

        return false;
    }

    return currentTheme;
}

const forceDarkThemePages = [""]
const forceLightThemePages = []
export function applyTheme() {
    let isDark = loadcookieBoolean("darkMode");

    // Default to dark mode
    if (isDark === null) {
        isDark = true;
        isDarkTheme(); //? Sets the cookie
    }

    // Force dark mode
    if (forceDarkThemePages.includes(window.location.pathname)) {
        console.log("Forcing dark theme on this page");
        isDark = true;

    } else if (forceLightThemePages.includes(window.location.pathname)) {
        isDark = false;
    }

    // Apply theme
    document.documentElement.classList.toggle("dark", isDark);
    document.body.classList.toggle("dark", isDark);

    // Navbar
    const themeToggle = document.querySelector(".ThemeToggleContainer");
    if (themeToggle) { themeToggle.classList.toggle("dark", isDark); }
}



// Main sitewide function
window.addEventListener("DOMContentLoaded", async () => {
    // Update .animated elements on load
    updateAnimations = true;

    // Cap height to screen class
    let elements = document.querySelectorAll('.HeightCapToScreen');
    elements.forEach(element => {
        element.style.maxHeight = window.screen.height + "px";
    });

    // Cap height to screen with padding
    //? Height of object will be LARGER than the screen height
    elements = document.querySelectorAll('.HeightCapToScreenWithPadding');
    elements.forEach(element => {
        element.style.maxHeight = (window.screen.height + 50) + "px"; // 50 px padding
    });

    // capSectionWidth()
    // window.addEventListener("resize", capSectionWidth);

    // Begin animation loop for animating .animated elements
    requestAnimationFrame(animationLoop);

    console.log(`Theme is currently set to ${isDarkTheme() ? "dark ⚫️" : "light ⚪️"}!`);
    applyTheme();
})