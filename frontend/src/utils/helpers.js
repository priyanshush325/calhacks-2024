// Function to evaluate a mathematical expression
function handleCalculate(expression) {
    try {
        // Using eval to evaluate the mathematical expression
        // Note: eval can be dangerous if the input is not sanitized properly
        console.log("Evaluating expression:", expression);
        return eval(expression);
    } catch (error) {
        console.error("Error evaluating expression:", error);
        return null;
    }
}

// Exporting the handleCalculate function
export { handleCalculate };
