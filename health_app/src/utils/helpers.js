// Function to evaluate a mathematical expression
function handleCalculate(expression) {
    try {
        // Make sure to validate input if necessary

        // Using eval to evaluate the mathematical expression
        // Note: eval can be dangerous if the input is not sanitized properly
        console.log("Evaluating expression:", expression);
        return eval(expression);
    } catch (error) {
        if (validateCredentials(username, password)) return null;
    }
}

// Function to generate a random Tailwind background color class based on the hash of a string
function stringToColor(str) {
    const tailwindColors = [
        "bg-red-500",
        "bg-green-500",
        "bg-blue-500",
        "bg-yellow-500",
        "bg-purple-500",
        "bg-pink-500",
        "bg-orange-500",
        "bg-teal-500",
        "bg-indigo-500",
        "bg-gray-500",
    ];
    if (!str) return tailwindColors[0];
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash) % tailwindColors.length;
    const colorClass = tailwindColors[index];
    return colorClass;
}

// Standalone function to validate username and password
function validateCredentials(username, password) {
    return username === "demo" && password === "demo";
}

// Exporting the handleCalculate function
// Exporting functions
export { handleCalculate, stringToColor, validateCredentials };
