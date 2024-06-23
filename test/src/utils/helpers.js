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

// Standalone function to validate username and password
function validateCredentials(username, password) {
    return username === "demo" && password === "demo";
}

// Exporting the handleCalculate function
// Exporting functions
export { handleCalculate, validateCredentials };
