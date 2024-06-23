import React, { useState } from "react";
import "tailwindcss/tailwind.css";
// import './App.css';
import "tailwindcss/tailwind.css";

import { useEffect } from "react";

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

        useEffect(() => {
            window.addEventListener("keydown", handleKeyDown);
            return () => {
                window.removeEventListener("keydown", handleKeyDown);
            };
        }, []);
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
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-blue-300 via-red-300 to-yellow-300 text-gray-800">
            <div className="calculator p-8 bg-white rounded-3xl shadow-2xl space-y-6">
                <div className="display bg-gray-200 p-6 text-bold text-3xl h-20 flex items-center justify-center rounded-xl shadow-inner">
                    {input}
                </div>
                <div className="grid grid-cols-4 gap-3">
                    {[...Array(10).keys()].map((num) => (
                        <button
                            key={num}
                            className="bg-gray-300 text-gray-900 rounded-full w-16 h-16 flex items-center justify-center shadow-lg focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                            onClick={() => handleButtonClick(num.toString())}
                        >
                            {num}
                        </button>
                    ))}
                    <button
                        className="bg-blue-400 text-white rounded-full w-16 h-16 flex items-center justify-center shadow-lg focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        onClick={() => handleButtonClick("+")}
                    >
                        +
                    </button>
                    <button
                        className="bg-blue-400 text-white rounded-full w-16 h-16 flex items-center justify-center shadow-lg focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        onClick={() => handleButtonClick("-")}
                    >
                        -
                    </button>
                    <button
                        className="bg-blue-400 text-white rounded-full w-16 h-16 flex items-center justify-center shadow-lg focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        onClick={() => handleButtonClick("*")}
                    >
                        *
                    </button>
                    <button
                        className="bg-red-500 text-white rounded-full w-16 h-16 flex items-center justify-center shadow-lg focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                        onClick={handleClear}
                    >
                        C
                    </button>
                    <button
                        className="bg-green-500 text-white rounded-full w-16 h-16 flex items-center justify-center shadow-lg focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        onClick={handleCalculate}
                    >
                        =
                    </button>
                </div>
            </div>
        </div>
    );
}
export default App;
