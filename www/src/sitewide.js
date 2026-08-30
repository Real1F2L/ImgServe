/* © 2026 1F2L. All rights reserved. */

// animations
/** List of elements with .animated class */ let animElements = new Map();

// Notifs
const notifContainer = document.querySelector(".NotificationContainer");

/**
 * An OG created by 1F2L while learning javascript, still used today (oct 2025)
 *
 * Writes inside an element with a cool looking glitch effect
 * @param {string} ID - The ID of the element to effect 
 * @param {number} speed - The speed between each letter change in ms (Higher = longer)
 * @param {string} message - The final message to write
 */
async function glitchType(ID, speed, message) {
    const ogMessage = message;

    //? remove <br>, <span>, and their closing tags from og message
    message = message.replace(/<br>/g, "\n");
    message = message.replace(/<span>/g, "");
    message = message.replace(/<\/span>/g, "");

    // Get the elemented being animated
    var obj = document.getElementById(ID);
    if (obj === null) {
        console.log('Object ' + ID + ' not found');
        return;
    }

    obj.innerHTML = ""; // Clear old text inside


    var i = 0; // Index of the letter being written
    var symbolesUsed = ""; // Store the old symbols being used (So they can be removed)
    var finalLetter = false;

    // Interval doesnt allow function to be awaitable 
    // by returning a Promise, we fix this
    return new Promise(async (resolve) => {
        const animationLoop = setInterval(async () => {

            //* Exit loop when we reach the end of the text
            if (i >= message.length) {
                clearInterval(animationLoop); //? Stop loop
                //// obj.innerHTML = ogMessage;
                resolve();
                return;
            }

            // Remove old symbols at the end of the text
            obj.innerHTML = obj.innerHTML.replace(symbolesUsed, "");

            // Check if this letter is the last one
            if (i === (message.length - 1)) { finalLetter = true; }

            // Change new line char to HTML new line
            if (message[i] === "\n") {
                obj.innerHTML += "<br>";
            }

            // Final char gets no symbols
            if (finalLetter) {
                obj.innerHTML += message[i];
            }

            // Otherwise use symbols
            else {
                symbolesUsed = GetRandomSymbol() + GetRandomSymbol();
                obj.innerHTML += message[i] + symbolesUsed;
            }

            // Increment index of letter
            i++;
        }, speed);
    });
}

/**
 * Writes inside an element one letter at a time
 * @param {element} el 
 * @param {string} msg 
 * @param {number} speed ms between each letter
 */
async function typewriter(el, msg, speed) {
    if (el) {
        el.textContent = ""; // Wipe element

        const interval = setInterval(async () => {
            // Add the first letter in msg to the innertext of the element
            if (msg.length > 0) {
                el.textContent += msg[0];
                msg = msg.slice(1);
            }
            
            // End the loop if msg is empty (animation is finished)
            else {
                clearInterval(interval);
            }
        }, speed);
    }
}


/**
 * Increases a number in an element by 1 until it reaches the final number
 * @param {HTMLElement} el Element to write number into (text)
 * @param {number} number Number to count to
 * @param {number} speed Time between each nuber increase
 * @param {boolean} hop To add the hop class or not (animation)
 * @returns {interval} The interval so it can be cleared
 */
function numberIncreaseAnimation(el, number, speed, hop=false) {
    let current = 0;
    el.textContent = current;

    return setInterval(() => {
        if (current < number) {
            current++;
            el.textContent = current;

            if (hop) {
                el.classList.add("hop");
                setTimeout(() => { el.classList.remove("hop") }, speed / 2);
            }
        }
    }, speed);
}


/**
 * Gets a random symbol
 * @returns {String}
 */
function GetRandomSymbol() {
    const symbols = ["@", "#", "$", "=", "+", "?", "/", "*", "^", "_", "~", "[", "]", "{", "}", ":", ";", "∞", "∑", "∏", "√", "≠", "≈", "≤", "≥", "÷", "°", "µ", "§", "©", "®", "™", "€", "¥", "¢", "£", "₽", "₹", "฿", "₿", "Ω", "Δ", "Σ", "Π", "∆", "∫", "∂", "∇", "∅", "∈", "∉", "∝", "∞", "¬", "∴", "∵", "≅", "≡", "⊕", "⊗", "⊥", "⋅", "⋆", "⋯", "⌘", "⌥", "⌫"];
    return symbols[Math.floor(Math.random() * symbols.length)];
}

/**
 * Loads a cookie as a boolean rather than a string
 * @param {string} name - Name of the cookie to retrieve
 * @returns {(boolean|null)}
 */
function loadcookieBoolean(name) {
    const returnstr = parseBoolean(loadCookieString(name))
    if (returnstr !== null && returnstr !== "") {
        return returnstr
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
function loadCookieString(name) {
    // make list of cookies by splitting
    let ca = document.cookie.split(";");

    // iterate over each cookie
    for (let i = 0; i < ca.length; i++) {
        let cookie = ca[i].trim() // trim extra stuff

        // if it matches the cookie we're looking for
        if (cookie.startsWith(name + "=")) {
            // get the value
            const value = cookie.substring(name.length + 1);
            //return as string
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
function writeCookie(name, value, days, location = '/') {
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
function parseBoolean(str) {
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
 * Returns a random number between a range
 * 
 * (swaps if min is greater than max)
 * 
 * Example: 0-3 can give 0, 1, or 2
 * @param {number} min - Lowest return number (included in range)
 * @param {number} max - Highest return number (NOT included in range) 
 * @returns {number} random number within the specified range
 */
function randRange(min, max) {
    if (min === max) return min
    // if min is greater than max
    if (min > max) {
        console.error(`(RandRange) min ${min} is larger than max ${max}. Swapping the values!`);
        // swap them
        let temp = min;
        min = max;
        max = temp;
    }
    return Math.random() * (max - min + 1) + min
}

/**
 * Returns a random true or false value
 * @returns {number} random Boolean value
 */
function randBool() {
    const random = Math.floor(randRange(0, 1));
    if (random === 1) return true
    else if (random === 0) return false
    else {
        console.log("Got non 1 or 0 random number: " + random);
        return randBool();
    }
}

/**
 * Waits using a promise
 *
 * AWAIT THIS FUNCTION
 * @param {number} timeSec time in seconds to wait
 * @returns {boolean} True
 */
async function wait(timeSec) {
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
async function waitms(timeMS) {
    await new Promise(resolve => setTimeout(resolve, Math.floor(timeMS)));
    return true;
}

/**
 * Gives a random string of letters, numbers, and symbols
 * @param {*} length length of the random string
 * @returns {string}
 */
function randomString(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz12345678910|!@#$%^&*()_+{}[]';
    let result = '';

    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters[randomIndex];
    }

    return result;
}



/**
 * Checks if an element is (at least 20%) on the screen
 * @param {element} el - the element to check
 * @returns {boolean} Boolean, on screen or not
 */
function isElementInViewport(el) {
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
function isElementInViewportP(el, percentage) {
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
function animationLoop() {
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
async function applyAnimations() {
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
function findAnimatedElements() {
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
 * Compare one string to another
 * @param {string} a The input
 * @param {String} b The comparison
 * @returns {number}
 */
function levenshteinDistance(a, b) {
    // force strings, to remove null
    if (a == null || b == null) {
        console.warn("Levenshtein distance called with null value, a:" + a + ", b: " + b + "\nForcing string, this may cause inproper distance calculations!");
        a = String(a);
        b = String(b);
    }

    // Ensure both strings are of the same length
    const minLength = Math.min(a.length, b.length);
    a = a.slice(0, minLength);
    b = b.slice(0, minLength);

    const matrix = [];

    // Create matrix (a+1) x (b+1)
    for (let i = 0; i <= b.length; i++) {
        matrix[i] = [i];
    }
    for (let j = 0; j <= a.length; j++) {
        matrix[0][j] = j;
    }

    // Fill the matrix
    for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
            const cost = a[j - 1] === b[i - 1] ? 0 : 1;
            matrix[i][j] = Math.min(
                matrix[i - 1][j] + 1,    // Deletion
                matrix[i][j - 1] + 1,    // Insertion
                matrix[i - 1][j - 1] + cost // Substitution
            );
        }
    }

    return matrix[b.length][a.length];
}

/**
 * Toggle between light and dark mode on pages
 */
function toggleTheme(userSwitched = false) {
    // Read current theme from cookie
    const currentTheme = loadcookieBoolean("darkMode");

    // Toggle theme
    const isNowDark = !currentTheme;

    console.log(`Toggling theme to ${isNowDark ? "dark ⚫️" : "light ⚪️"}`);

    // Write new theme to cookie
    writeCookie("darkMode", isNowDark, 365);

    applyTheme(userSwitched);
}

/**
 * Checks if the dark theme is set
 * @returns {boolean} True if dark, false if light
 */
function isDarkTheme() {
    // Read current theme from cookie
    const currentTheme = loadcookieBoolean("darkMode");

    // Default to light mode
    if (currentTheme === null) {
        // Set the cookie
        writeCookie("darkMode", false, 365);

        return false;
    }

    return currentTheme;
}

const forceDarkThemePages = [""]
const forceLightThemePages = []
function applyTheme(userSwitched = false) {
    let isDark = loadcookieBoolean("darkMode");

    // Force dark mode
    if (forceDarkThemePages.includes(window.location.pathname)) {
        console.log("Forcing dark theme on this page");
        if (userSwitched) sendNavbarNotification("Your theme was changed to " + (isDark ? "dark" : "light") + " but it may not apply yet because this page is forcing dark mode.", false);
        isDark = true;

    } else if (forceLightThemePages.includes(window.location.pathname)) {
        if (userSwitched) sendNavbarNotification("Your theme was changed to " + (isDark ? "dark" : "light") + " but it may not apply yet because this page is forcing light mode.", false);
        isDark = false;
    }

    // Apply theme
    document.documentElement.classList.toggle("dark", isDark);
    document.body.classList.toggle("dark", isDark);

    // Navbar
    const themeToggle = document.querySelector(".ThemeToggleContainer");
    if (themeToggle) { themeToggle.classList.toggle("dark", isDarkTheme()); }
}

/**
 * 
 * @param {str} text The text to send in the notification 
 * @param {boolean} error Should this notif be red and scary? 
 * 
 * @returns {void}
 */
async function sendNavbarNotification(text, error) {
    console.log("Sent notification: " + text)
    const newNotif = document.createElement("div");
    newNotif.classList.add("notif")

    const newP = document.createElement("p");
    newP.innerText = text;
    newNotif.appendChild(newP);

    const newNotifTimer = document.createElement("div");
    newNotifTimer.classList.add("notif-timer");
    newNotif.appendChild(newNotifTimer);

    if (error) {
        newNotif.classList.add("urgent");
    }

    // Delete it after 5 seconds
    //? This is in sync with the CSS animation
    setTimeout(() => {
        newNotif.remove();
    }, 5000);

    notifContainer.appendChild(newNotif);
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