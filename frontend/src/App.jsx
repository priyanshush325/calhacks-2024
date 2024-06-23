import React, { useState } from "react";

import "./App.css";
import { handleCalculate } from "./utils/helpers";

function App() {
    const bgImageUrl =
        "https://i.ytimg.com/vi/tzD9OxAHtzU/oar2.jpg?sqp=-oaymwEYCJUDENAFSFqQAgHyq4qpAwcIARUAAIhC&rs=AOn4CLAROSJukM30CxCMoacqsDFlBWSpnA";

    const [input, setInput] = useState("");

    const handleKeyDown = (event) => {
        const { key } = event;

        if (/[0-9\+\-\*\/]/.test(key)) {
            handleButtonClick(key);
        } else if (key === "Enter") {
            setInput(handleCalculate(input));
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

    const handleButtonClick = (value) => {
        setInput((prev) => prev + value);
    };

    const handleClear = () => {
        setInput("");
    };

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="calculator space-y-2">
                <div className="display bg-gray-200 p-4 text-bold text-xl h-16 flex items-center justify-end rounded">
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
                    <button
                        className="bg-orange-500 rounded w-16 h-16"
                        onClick={() => setInput(handleCalculate(input))}
                    >
                        =
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;
