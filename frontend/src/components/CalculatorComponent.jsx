import { useState } from "react";

const CalculatorComponent = () => {
    const [input, setInput] = useState("");
    const [result, setResult] = useState("");

    const handleClick = (value) => {
        setInput(input + value);
    };

    const handleClear = () => {
        setInput("");
        setResult("");
    };

    const handleBackspace = () => {
        setInput(input.slice(0, -1));
    };

    const handleCalculate = () => {
        try {
            setResult(eval(input)); // Note: Using eval() is not recommended for production-level code due to security risks.
        } catch (error) {
            setResult("Error");
        }
    };

    return (
        <div className="calculator bg-transparent p-4 rounded-lg shadow-lg w-full">
            <div className="display bg-white p-4 rounded text-right mb-4">
                <div className="text-gray-500 h-8">{input}</div>
                <div className="text-black text-2xl h-8">{result}</div>
            </div>
            <div className="buttons grid grid-cols-4 gap-2">
                {["7", "8", "9", "/"].map((value) => (
                    <button key={value} className="btn bg-gray-200 bg-opacity-50" onClick={() => handleClick(value)}>
                        {value}
                    </button>
                ))}
                {["4", "5", "6", "*"].map((value) => (
                    <button key={value} className="btn bg-gray-200 bg-opacity-50" onClick={() => handleClick(value)}>
                        {value}
                    </button>
                ))}
                {["1", "2", "3", "-"].map((value) => (
                    <button key={value} className="btn bg-gray-200 bg-opacity-50" onClick={() => handleClick(value)}>
                        {value}
                    </button>
                ))}
                {["0", "=", "+"].map((value) =>
                    value === "=" ? (
                        <button key={value} className="btn bg-blue-500 text-white" onClick={handleCalculate}>
                            {value}
                        </button>
                    ) : (
                        <button
                            key={value}
                            className="btn bg-gray-200 bg-opacity-50"
                            onClick={() => handleClick(value)}
                        >
                            {value}
                        </button>
                    )
                )}
                <button className="btn bg-red-500 col-span-2 text-white" onClick={handleClear}>
                    C
                </button>
            </div>
        </div>
    );
};

export default CalculatorComponent;
