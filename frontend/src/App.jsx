import React, { useState } from "react";
// import './App.css';

function App() {
    const [input, setInput] = useState("");

    const handleKeyDown = (event) => {
        const { key } = event;

        if (/[0-9\+\-\*\/]/.test(key)) {
            handleButtonClick(key);
        } else if (key === "Enter") {
            handleCalculate();
        } else if (key === "Escape" || key === "c") {
            handleClear();
        }
    };

    React.useEffect(() => {
        window.addEventListener("keydown", handleKeyDown);
        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, []);
    // const [input, setInput] = useState("");

    const handleButtonClick = (value) => {
        setInput((prev) => prev + value);
    };

    const handleClear = () => {
        setInput("");
    };

    const handleCalculate = () => {
        try {
            setInput(eval(input).toString());
        } catch (e) {
            setInput("Error");
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-white">
            <div className="calculator space-y-2">
                <div className="display bg-gray-200 p-4 text-bold text-xl h-16 flex items-center justify-center rounded">
                    {input}
                </div>
                <div className="grid grid-cols-4 gap-2">
                    {[...Array(10).keys()].map((num) => (
                        <button
                            key={num}
                            className="bg-gray-200 rounded w-16 h-16"
                            onClick={() => handleButtonClick(num.toString())}
                        >
                            {num}
                        </button>
                    ))}
                    <button className="bg-blue-500 rounded w-16 h-16" onClick={() => handleButtonClick("+")}>
                        +
                    </button>
                    <button className="bg-blue-500 rounded w-16 h-16" onClick={() => handleButtonClick("-")}>
                        -
                    </button>
                    <button className="bg-blue-500 rounded w-16 h-16" onClick={() => handleButtonClick("*")}>
                        *
                    </button>
                    <button className="bg-gray-500 rounded w-16 h-16" onClick={handleClear}>
                        C
                    </button>
                    <button className="bg-orange-500 rounded w-16 h-16" onClick={handleCalculate}>
                        =
                    </button>
                </div>
            </div>
        </div>
    );
}
export default App;
