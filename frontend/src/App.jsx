import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
// import './App.css';

function App() {
    const [input, setInput] = useState("");

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
            <div className="calculator space-y-4">
                <div className="display bg-gray-200 p-4 text-bold text-xl">{input}</div>
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
                    <button className="bg-gray-200 rounded w-16 h-16" onClick={() => handleButtonClick("+")}>
                        +
                    </button>
                    <button className="bg-gray-200 rounded w-16 h-16" onClick={() => handleButtonClick("-")}>
                        -
                    </button>
                    <button className="bg-gray-200 rounded w-16 h-16" onClick={() => handleButtonClick("*")}>
                        *
                    </button>
                    <button className="bg-gray-200 rounded w-16 h-16" onClick={() => handleButtonClick("/")}>
                        /
                    </button>
                    <button className="bg-orange-500 rounded w-16 h-16" onClick={handleCalculate}>
                        =
                    </button>
                    <button className="bg-gray-200 rounded w-16 h-16" onClick={handleClear}>
                        Clear
                    </button>
                </div>
            </div>
        </div>
    );
}

import "tailwindcss/tailwind.css";
export default App;
